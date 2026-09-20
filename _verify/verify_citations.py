#!/usr/bin/env python3
"""Every citation resolves, and the value it carries is on the line it cites.

Reads each output, finds every [document:line] and [document:a-b], opens that
fixture file, and looks for the value there. A citation that points at a line
which does not contain the value is the failure this tool exists to prevent.
"""
import re, sys, pathlib, unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
CITE = re.compile(r"`\[([a-z-]+):(\d+)(?:-(\d+))?\]`")
FIELD = re.compile(r"^\s*-\s+\*\*([a-z0-9_]+)\*\*:\s*(.+)$")

def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip().lower()

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

def lines_of(path):
    return path.read_text().splitlines()

def cited_text(fdir, doc, a, b):
    p = fdir/f"{doc}.txt"
    if not p.exists():
        return None, f"no such document: {p.relative_to(ROOT)}"
    ls = lines_of(p)
    b = b or a
    if a < 1 or b > len(ls):
        return None, f"{doc}.txt has {len(ls)} lines, citation asks for {a}-{b}"
    return " ".join(ls[a-1:b]), None

def strip_annotations(value):
    """Remove the citation, the derivation block and trailing conflict notes."""
    value = CITE.sub("", value)
    value = re.sub(r"`derived:[^`]*`", "", value)
    value = re.sub(r"\bfrom\b\s*(,|and|\s)*", " ", value)
    value = re.sub(r"\(conflict,\s*see section \d+\)", "", value)
    return value.strip(" ,`—-")

def main():
    failures, checked = [], 0
    for out in sorted((ROOT/"outputs").glob("*.md")):
        fdir = input_dir(out)
        for n, raw in enumerate(out.read_text().splitlines(), 1):
            cites = CITE.findall(raw)
            if not cites:
                continue
            # 1. every citation must resolve to real lines
            texts = []
            for doc, a, b in cites:
                text, err = cited_text(fdir, doc, int(a), int(b) if b else None)
                checked += 1
                if err:
                    failures.append(f"{out.name}:{n}  {err}")
                else:
                    texts.append(text)
            if not texts:
                continue
            # 2. a field line's value must appear in what it cites.
            # Derived values are checked by verify_derivations.py instead:
            # a derived value is by definition not printed in the source.
            if "derived:" in raw:
                continue
            m = FIELD.match(raw)
            if not m:
                continue
            key, value = m.group(1), strip_annotations(m.group(2))
            if not value or value in ("not in source",):
                continue
            hay = norm(" ".join(texts))
            needle = norm(value)
            if needle in hay:
                continue
            toks = [t for t in re.split(r"[^\w.,/-]+", needle) if t]
            missing = [t for t in toks if t not in hay]
            if missing:
                failures.append(
                    f"{out.name}:{n}  field '{key}' cites "
                    f"{[f'{d}:{a}' for d,a,_ in cites]} but "
                    f"{missing} is not on those lines")
    if failures:
        print("FAIL  citations")
        for f in failures: print("   ", f)
        return 1
    print(f"ok    citations    {checked} citations resolved, "
          f"every value found on the line it cites")
    return 0

sys.exit(main())
