#!/usr/bin/env python3
"""Run every testable calculation example in the skill through the FileMaker engine.

Maintainer tool — not shipped in the skill package. Needs the Claris Agentic Development
Toolkit (ADT) installed on macOS: it drives ADT's `filemaker` CLI (fm-cli), which evaluates
formulas with the real FileMaker calculation engine against a throwaway file.

    python3 maintainer/verify_examples.py                 # all reference files
    python3 maintainer/verify_examples.py references/functions-text.md
    python3 maintainer/verify_examples.py --report out.md

An example is testable when it pairs a formula with a concrete expected value, in either form:

    `Left ( "Manufacturing" ; 4 )` → `Manu`          (inline)

    Left ( "Manufacturing" ; 4 )                       (code block)
    // → Manu

Expected values that are prose ("the contents of…") are skipped, and so are formulas that need
a record, a field, a variable or Self — the CLI has no record context. Those are still
*validated* (parsed) where they contain no field references.

Exit status is 1 if any example fails, so this can gate a release.
"""

import argparse
import datetime as dt
import glob
import json
import os
import re
import subprocess
import sys
import tempfile
from decimal import Decimal, InvalidOperation

FM_CLI = os.path.expanduser("~/Library/Application Support/ADT/MCP/fm-cli/fm-cli")
SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ARROW = r"(?:→|->)"
# A formula needs no record context if it has no Table::Field, $variable or Self reference.
NEEDS_CONTEXT = re.compile(r"::|\$|\bSelf\b|\bself\b")
# Bare identifiers that are field names in Claris's examples (e.g. `IsEmpty ( OrderNum )`).
# Anything left after removing strings, numbers, function names and keywords is a field ref.
KEYWORDS = {"and", "or", "not", "xor", "true", "false", "lower", "higher", "pi"}


def fm_functions():
    with open(os.path.join(SKILL_ROOT, "references", "function-catalog.json")) as f:
        names = {fn["name"].split("(")[0].strip().lower() for fn in json.load(f)["functions"]}
    return names | {"get"}


FUNCTIONS = fm_functions()
CONSTANTS = {"jsonstring", "jsonnumber", "jsonobject", "jsonarray", "jsonboolean", "jsonnull",
             "jsonraw", "jsonstringranges", "valuenumber", "valuenumberranges", "posixpath",
             "winpath", "urlpath", "rowid", "rowmodid", "plain", "bold", "italic", "underline",
             "highlightyellow", "condense", "extend", "strikethrough", "smallcaps", "superscript",
             "subscript", "uppercase", "lowercase", "titlecase", "wordunderline",
             "doubleunderline", "allstyles"}


# Answers depend on the client, window, record, file or network rather than the formula, so
# the CLI's answer proves nothing. These are validated (parsed) instead of compared.
ENVIRONMENT = re.compile(
    r"\bGet\s*\(|\bRandom\b|LayoutObjectUUID|GetSensor|RangeBeacons|\bLocation(Values)?\b|"
    r"GetRecordIDsFromFoundSet|GetPersistentData|ListPersistentDataIDs|ExecuteSQLe?\b|"
    r"GetEmbedding\b|GetTokenCount|GetTableDDL|GetFieldsOnLayout|GetRAGSpaceInfo|ComputeModel|"
    r"GetModelAttributes|PredictFromModel|ValueListItems|WindowNames|DatabaseNames|"
    r"ConvertFromFileMakerPath|ConvertToFileMakerPath|GetAddonInfo|GetLayoutObject|"
    r"\b(Layout|Script|Table|BaseTable|Field|ValueList)(Names|IDs)\b|RelationInfo|FieldType|"
    r"FieldStyle|FieldBounds|FieldComment|FieldAnnotation|FieldDisplayNames|FieldRepetitions|"
    r"GetNextSerialValue|BaseTableComment", re.I)


def has_field_refs(formula):
    """True if the formula refers to something other than functions, constants and literals."""
    if NEEDS_CONTEXT.search(formula) or re.search(r"\b(Evaluate|GetField|GetNthRecord|GetSummary|Lookup|LookupNext)\s*\(", formula):
        return True
    if "..." in formula or "…" in formula:      # elided input, not a runnable formula
        return True
    stripped = re.sub(r'"(?:\\.|[^"\\])*"', " ", formula)          # drop string literals
    stripped = re.sub(r"/\*.*?\*/|//[^\n]*", " ", stripped, flags=re.S)
    # Get ( X ) parameter names are not field references
    stripped = re.sub(r"\bGet\s*\(\s*\w+\s*\)", " ", stripped, flags=re.I)
    let_vars = (set(re.findall(r"([A-Za-z_]\w*)\s*=(?!=)", stripped))  # Let / While variables
                if re.search(r"\b(Let|While)\s*\(", stripped, re.I) else set())
    for tok in re.findall(r"[A-Za-z_][A-Za-z0-9_.]*", stripped):
        t = tok.lower()
        if t in FUNCTIONS or t in CONSTANTS or t in KEYWORDS or tok in let_vars:
            continue
        return True
    return False


# ---------------------------------------------------------------- extraction

def clean_expected(raw):
    """Turn the text after → into an expected value, or None if it's prose."""
    s = raw.strip()
    if "![" in s or "π" in s:                 # image placeholder / symbolic answer
        return None
    m = re.match(r"^`([^`]*)`", s)            # backticked value wins
    if m:
        v = m.group(1)
        return v.replace("\\n", "\r")
    s = re.split(r"\s+\(|\s+—|\s+--|\s{2,}//", s)[0].strip()   # drop trailing commentary
    if not s or len(s) > 80:
        return None
    if re.match(r"^(the|a|an|returns?|text|number|date|time|timestamp|true|false|nothing|"
                r"empty|list|json|container|value|e\.g\.|approx|about|varies|depends|"
                r"same|all|only|1 if|0 if)\b", s, re.I) and not re.match(r"^(true|false)$", s, re.I):
        return None
    if s.startswith('"') and s.endswith('"') and len(s) >= 2:
        s = s[1:-1]
    return s


def extract(path):
    """Yield (line_no, formula, expected) from one Markdown file."""
    lines = open(path, encoding="utf-8").read().splitlines()
    in_code = False
    pending = None                                # (line_no, formula) awaiting // → line
    for i, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            pending = None
            continue
        if not in_code:
            # inline: `formula` → `expected` (formula must look like a call or expression)
            for m in re.finditer(r"`([^`]+)`\s*" + ARROW + r"\s*(.+?)(?=\s{2,}$|$|\s+`[^`]+`\s*" + ARROW + ")", line):
                formula, exp = m.group(1), clean_expected(m.group(2))
                if exp is not None and re.search(r"[(\"]|\d", formula):
                    yield i, formula, exp
            continue
        stripped = line.strip()
        same = re.match(r"^(.+?)\s*//\s*" + ARROW + r"\s*(.+)$", stripped)
        if same and not stripped.startswith("//"):
            exp = clean_expected(same.group(2))
            if exp is not None:
                yield i, same.group(1).strip(), exp
            pending = None
            continue
        nxt = re.match(r"^//\s*" + ARROW + r"\s*(.+)$", stripped)
        if nxt and pending:
            exp = clean_expected(nxt.group(1))
            if exp is not None:
                yield pending[0], pending[1], exp
            pending = None
            continue
        # a single-line formula on its own; multi-line formulas are validated, not compared
        balanced = stripped.count("(") == stripped.count(")") and stripped.count("(") > 0
        if balanced and not stripped.startswith(("//", "#")) and "[" not in stripped.split("(")[0]:
            pending = (i, stripped)
        else:
            pending = None


# ---------------------------------------------------------------- normalisation

US_DATE = re.compile(r"^(\d{1,2})/(\d{1,2})/(\d{1,4})$")
US_TIME = re.compile(r"^(\d{1,2}):(\d{2})(?::(\d{2}))?\s*([AaPp][Mm])?$")


def localise(formula):
    """Rewrite US date literals "M/D/YYYY" as Date(M;D;YYYY): the engine runs in the Mac's
    locale, and Claris's examples assume US formats."""
    def repl(m):
        mo, d, y = m.group(1), m.group(2), m.group(3)
        return f"Date ( {mo} ; {d} ; {y} )"
    return re.sub(r'"(\d{1,2})/(\d{1,2})/(\d{4})"', repl, formula)


def to_number(s):
    try:
        return Decimal(s.replace(",", "").strip())
    except (InvalidOperation, AttributeError):
        return None


def us_temporal_to_number(s):
    """Expected value in US format → FileMaker internal number (days / seconds)."""
    s = s.strip()
    parts = s.split(" ", 1)
    m = US_DATE.match(parts[0])
    if m and len(parts) == 1:
        return dt.date(int(m.group(3)), int(m.group(1)), int(m.group(2))).toordinal()
    def secs(t):
        mt = US_TIME.match(t.strip())
        if not mt:
            return None
        h, mi, se = int(mt.group(1)), int(mt.group(2)), int(mt.group(3) or 0)
        ap = (mt.group(4) or "").lower()
        if ap == "pm" and h != 12:
            h += 12
        if ap == "am" and h == 12:
            h = 0
        return h * 3600 + mi * 60 + se
    if m and len(parts) == 2:
        t = secs(parts[1])
        if t is None:
            return None
        d = dt.date(int(m.group(3)), int(m.group(1)), int(m.group(2))).toordinal()
        return (d - 1) * 86400 + t
    return secs(s)


def matches(expected, value, data_type):
    exp = expected.replace("¶", "\r").replace("\\r", "\r")
    val = value
    if exp == val or exp.rstrip("\r\n") == val.rstrip("\r\n"):
        return True
    if len(exp) >= 2 and exp[0] == exp[-1] == '"' and exp[1:-1] == val:   # "42" written quoted
        return True
    exp = exp.replace("…", "...")
    if exp.startswith("[") and val.startswith("["):  # embedding vectors: elementwise, 1e-15
        try:
            ea, va = json.loads(exp.replace("...", "")), json.loads(val)
            return len(ea) == len(va) and all(abs(float(x) - float(y)) < 1e-15 for x, y in zip(ea, va))
        except (ValueError, TypeError):
            pass
    if exp.endswith("..."):                       # truncated in docs: prefix match
        e = exp[:-3].lstrip("0")
        return val.lstrip("0").startswith(e) or val.startswith(exp[:-3])
    a, b = to_number(exp), to_number(val)
    if a is not None and b is not None:
        if a == b:
            return True
        places = len(exp.split(".")[1]) if "." in exp else 0   # docs show rounded values
        if round(b, places) == a:
            return True
        q = Decimal(1).scaleb(-places)                             # Claris sometimes truncates
        return b.quantize(q, rounding="ROUND_DOWN") == a

    return exp.strip().lower() == val.strip().lower()


# ---------------------------------------------------------------- engine

def run_ops(ops, scratch):
    path = os.path.join(scratch, "ops.ndjson")
    with open(path, "w") as f:
        for op in ops:
            f.write(json.dumps(op) + "\n")
    fm = os.path.join(scratch, "verify.fmp12")
    if os.path.exists(fm):
        os.remove(fm)
    out = subprocess.run([FM_CLI, f"--file={fm}", "--create", "--no-prompt", path],
                         capture_output=True, text=True, timeout=600).stdout
    results = [json.loads(l) for l in out.splitlines() if l.startswith('{"op"')]
    if len(results) != len(ops):
        sys.exit(f"engine returned {len(results)} results for {len(ops)} ops:\n{out[-2000:]}")
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*")
    ap.add_argument("--report", help="write a Markdown report here")
    ap.add_argument("--show-skips", action="store_true")
    args = ap.parse_args()
    if not os.path.exists(FM_CLI):
        sys.exit(f"ADT's fm-cli not found at {FM_CLI}. Install the Agentic Development Toolkit.")

    files = args.files or sorted(glob.glob(os.path.join(SKILL_ROOT, "references", "*.md")))
    cases, skipped, validate_only = [], [], []
    for f in files:
        for line, formula, expected in extract(f):
            rel = os.path.relpath(f, SKILL_ROOT)
            if has_field_refs(formula):
                skipped.append((rel, line, formula, "needs record/field/variable context"))
            elif ENVIRONMENT.search(formula):
                validate_only.append((rel, line, formula, expected))
            else:
                cases.append((rel, line, formula, expected))

    ops = []
    for _, _, formula, _ in cases:
        f = localise(formula)
        ops.append({"op": "evaluate:calculation", "calculation": f})
        # numeric form of the same value, for comparing dates/times regardless of locale
        ops.append({"op": "evaluate:calculation", "calculation": f"GetAsNumber ( {f} )"})

    for _, _, formula, _ in validate_only:
        ops.append({"op": "validate:calculation", "calculation": localise(formula)})

    with tempfile.TemporaryDirectory() as scratch:
        results = run_ops(ops, scratch) if ops else []
    vresults = results[2 * len(cases):]

    passed, failed = [], []
    for n, (rel, line, formula, expected) in enumerate(cases):
        r, rn = results[2 * n], results[2 * n + 1]
        if r["status"] != "ok":
            err = r["error"]
            failed.append((rel, line, formula, expected, f"ERROR {err.get('code')} {err.get('dbError','')}".strip()))
            continue
        val, typ = r["result"]["value"], r["result"]["dataType"]
        ok = matches(expected, val, typ)
        if not ok and typ in ("date", "time", "timestamp") and rn["status"] == "ok":
            want = us_temporal_to_number(expected)
            got = to_number(rn["result"]["value"])
            ok = want is not None and got is not None and Decimal(want) == got
        (passed if ok else failed).append((rel, line, formula, expected, f"{val!r} ({typ})"))

    validated = 0
    for (rel, line, formula, expected), r in zip(validate_only, vresults):
        res = r.get("result", {})
        if r["status"] == "ok" and res.get("valid"):
            validated += 1
        else:
            err = res.get("error") or r.get("error") or {}
            failed.append((rel, line, formula, expected, f"INVALID {err.get('code')} {err.get('engineCode','')}".strip()))

    lines = [f"# Engine verification — {len(passed)} evaluated OK, {validated} parsed OK "
             f"(environment-dependent), {len(failed)} failed, {len(skipped)} skipped "
             f"(need record context)", ""]
    if failed:
        lines += ["## Failed", "", "| File:line | Formula | Expected | Engine |", "|---|---|---|---|"]
        for rel, line, formula, exp, got in failed:
            esc = lambda s: s.replace("|", "\\|").replace("\r", "¶")
            lines.append(f"| {rel}:{line} | `{esc(formula)}` | `{esc(exp)}` | {esc(got)} |")
    if args.show_skips and skipped:
        lines += ["", "## Skipped", ""] + [f"- {r}:{l} `{f}` — {why}" for r, l, f, why in skipped]
    report = "\n".join(lines)
    if args.report:
        open(args.report, "w").write(report + "\n")
    print(report)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
