#!/usr/bin/env python3
"""Re-compute every derived value independently, and refuse any fourth kind.

reference/derivations.md allows three operations and no others. For each
`derived:` in an output this script re-runs the arithmetic from scratch, checks
the starting phrase really is on the cited line, and checks the field's stated
value equals what the arithmetic produces. A derivation that is not one of the
three is a failure, because that is where a converter starts inventing.
"""
import re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from spanish_numbers import to_int, to_date, fold

ROOT = pathlib.Path(__file__).resolve().parent.parent
CITE = re.compile(r"`\[([a-z-]+):(\d+)(?:-(\d+))?\]`")
LINE = re.compile(r"^\s*-\s+\*\*([a-z0-9_]+)\*\*:\s*(\S+)\s+`derived:\s*(.+?)`")
INPUT_LINE = re.compile(r"^Input:\s*`?([^`\n]+?)`?\s*$", re.M)

def input_dir(out_path):
    """Where this record's documents are.

    Taken from the record's own `Input:` line, so a record converted from any
    folder can be verified, not only one under fixtures/. Relative paths
    resolve against the repository root. Falls back to fixtures/<name>/ for a
    record written before the Input line was required.
    """
    m = INPUT_LINE.search(out_path.read_text())
    if m:
        raw = m.group(1).strip().rstrip("/")
        p = pathlib.Path(raw)
        p = p if p.is_absolute() else ROOT/p
        if p.is_dir():
            return p
    return ROOT/"fixtures"/out_path.name[:-3]

MON = {"ENE":1,"FEB":2,"MAR":3,"ABR":4,"MAY":5,"JUN":6,
       "JUL":7,"AGO":8,"SET":9,"OCT":10,"NOV":11,"DIC":12}
MON3 = {v:k for k,v in MON.items()}

# D1 words -> integer ; D1 words -> date ; D2 m2 -> ha ; D3 date + years
D1_INT  = re.compile(r"^(?P<words>[^=]+?)\s*=\s*(?P<n>\d+)$")
D1_DATE = re.compile(r"^(?P<words>[^=]+?)\s*=\s*(?P<d>\d{2}-[A-Z]{3}-\d{4})$")
D2      = re.compile(r"^(?P<n>[\d.]+)\s*m2\s*/\s*10000\s*=\s*(?P<ha>[\d.]+)\s*ha$")
D3      = re.compile(r"^(?P<d>\d{2}-[A-Z]{3}-\d{4})\s*\+\s*(?P<y>\d+)\s*years?\s*=\s*"
                     r"(?P<out>\d{2}-[A-Z]{3}-\d{4})$")

def cited_lines(fdir, raw):
    out = []
    for doc, a, b in CITE.findall(raw):
        p = fdir/f"{doc}.txt"
        if not p.exists():
            continue
        ls = p.read_text().splitlines()
        a, b = int(a), int(b or a)
        out.extend(ls[a-1:b])
    return fold(" ".join(out))

def check_step(step, hay, fails, where):
    """Return the step's result value as a string, or None if the step is invalid."""
    m = D2.match(step)
    if m:
        n, ha = float(m.group("n")), m.group("ha")
        want = f"{n/10000:.4f}"
        if want != ha:
            fails.append(f"{where}  D2 arithmetic: {n}/10000 = {want}, output says {ha}")
        return ha
    m = D3.match(step)
    if m:
        d, y, out = m.group("d"), int(m.group("y")), m.group("out")
        dd, mon, yy = d.split("-")
        want = f"{dd}-{mon}-{int(yy)+y}"
        if want != out:
            fails.append(f"{where}  D3 arithmetic: {d} + {y} years = {want}, output says {out}")
        return out
    m = D1_DATE.match(step)
    if m:
        words, d = m.group("words").strip(), m.group("d")
        got = to_date(words)
        if got is None:
            fails.append(f"{where}  D1 could not read the date phrase {words!r}")
        elif got != d:
            fails.append(f"{where}  D1 date: {words!r} = {got}, output says {d}")
        if fold(words) not in hay:
            fails.append(f"{where}  D1 phrase {words!r} is not on the cited line")
        return d
    m = D1_INT.match(step)
    if m:
        words, n = m.group("words").strip(), m.group("n")
        got = to_int(words)
        if got is None:
            fails.append(f"{where}  D1 could not read the number phrase {words!r}")
        elif str(got) != n:
            fails.append(f"{where}  D1 number: {words!r} = {got}, output says {n}")
        if fold(words) not in hay:
            fails.append(f"{where}  D1 phrase {words!r} is not on the cited line")
        return n
    fails.append(f"{where}  not one of the three allowed derivations: {step!r}")
    return None

def main():
    fails, n_der = [], 0
    for out in sorted((ROOT/"outputs").glob("*.md")):
        fdir = input_dir(out)
        for ln, raw in enumerate(out.read_text().splitlines(), 1):
            m = LINE.match(raw)
            if not m:
                if "derived:" in raw:
                    fails.append(f"{out.name}:{ln}  a derivation this script cannot parse")
                continue
            n_der += 1
            key, stated, expr = m.group(1), m.group(2), m.group(3)
            where = f"{out.name}:{ln}  field '{key}'"
            hay = cited_lines(fdir, raw)
            result = None
            for step in [s.strip() for s in expr.split(";")]:
                result = check_step(step, hay, fails, where)
            if result is not None and result != stated:
                fails.append(f"{where}  arithmetic ends at {result}, but the field says {stated}")
    if fails:
        print("FAIL  derivations")
        for f in fails: print("   ", f)
        return 1
    print(f"ok    derivations  {n_der} derived values re-computed from scratch, all agree")
    return 0

sys.exit(main())
