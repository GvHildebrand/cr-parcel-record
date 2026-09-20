#!/usr/bin/env python3
"""Every Parcel Record carries the same sections, and no field the contract
does not name.

The contract is reference/fields.tsv. This script reads it, not the prose.

Two checks. The first was here from the start: the section list and the
single-valued fields. The second was added after a stranger test found that the
worked outputs emitted five field keys the contract had never heard of, and
nothing noticed, which made "fields.tsv is the contract" untrue. A contract
nobody checks in both directions is a description.
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

def load_contract():
    rows = [l.split("\t") for l in
            (ROOT/"reference/fields.tsv").read_text().strip().splitlines()[1:]]
    sections, one_fields, known = [], {}, set()
    for no, title, key, card, kind, src, example in rows:
        if (no, title) not in sections:
            sections.append((no, title))
        known.add(key)
        if card == "one":
            one_fields.setdefault((no, title), []).append(key)
    return sections, one_fields, known

def headings(text):
    return [(m.group(1), m.group(2).strip())
            for m in re.finditer(r"^## (\d+)\. (.+)$", text, re.M)]

def field_keys(text):
    return [m.group(1) for m in re.finditer(r"^\s*-\s+\*\*([a-z0-9_]+)\*\*:", text, re.M)]

def main():
    sections, one_fields, known = load_contract()
    outputs = sorted((ROOT/"outputs").glob("*.md"))
    if not outputs:
        print("FAIL  no outputs to check"); return 1
    failures = []
    for out in outputs:
        text = out.read_text()
        got = headings(text)
        if got != sections:
            failures.append(f"{out.name}: section list differs\n"
                            f"    expected {sections}\n    got      {got}")
            continue
        keys = field_keys(text)
        for sec, expected in one_fields.items():
            for key in expected:
                n = keys.count(key)
                if n != 1:
                    failures.append(f"{out.name}: field '{key}' appears {n} times, expected 1")
        for key in sorted(set(keys) - known):
            failures.append(f"{out.name}: field '{key}' is not in reference/fields.tsv. "
                            f"Either the record invented a field or the contract is behind.")
    if failures:
        print("FAIL  shape")
        for f in failures: print("   ", f)
        return 1
    print(f"ok    shape        {len(outputs)} outputs, {len(sections)} sections each, "
          f"identical order, every field key in the contract")
    return 0

sys.exit(main())
