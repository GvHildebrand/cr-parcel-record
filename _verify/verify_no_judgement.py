#!/usr/bin/env python3
"""A Parcel Record converts. It does not conclude.

rules.md check 4 says no word in the output may express a judgement about the
land. That check was mine to run by hand until a hand-pass found three
judgements and one claim from outside the documents sitting in prose lines that
no other script reads. This mechanises what can be mechanised.

Two rules:
  1. No verdict word, anywhere in an output.
  2. No appeal to knowledge the documents do not carry ("usually", "routinely",
     "in Costa Rica", "typically"). The folder is the only authority.

Quoted source text is exempt: a document may use any word it likes, and the
record reproduces it. Exemption applies to lines inside **quote**: and to
verbatim field values that carry a citation.
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

VERDICT = [
 "unencumbered", "clean title", "marketable", "good buy", "bad buy",
 "low risk", "high risk", "risky", "safe to", "recommend", "advisable",
 "we suggest", "should buy", "should not buy", "worth it", "fair price",
 "overpriced", "underpriced", "attractive", "concerning", "alarming",
 "most consequential", "is accurate", "clearly", "obviously", "of course",
]
OUTSIDE = [
 "usually", "routinely", "typically", "in practice", "as a rule",
 "generally speaking", "it is common", "commonly", "in costa rica,",
 "most buyers", "experience shows", "in my experience",
]
CITED = re.compile(r"`\[[a-z-]+:\d+(?:-\d+)?\]`")

def main():
    hits = []
    for out in sorted((ROOT/"outputs").glob("*.md")):
        for n, line in enumerate(out.read_text().splitlines(), 1):
            stripped = line.strip()
            # a quoted clause or a cited verbatim value reproduces the document
            if stripped.startswith("**quote**:") or CITED.search(line):
                continue
            low = line.lower()
            for w in VERDICT:
                if w in low:
                    hits.append(f"{out.name}:{n}  verdict word {w!r}: {stripped[:80]}")
            for w in OUTSIDE:
                if w in low:
                    hits.append(f"{out.name}:{n}  appeal to outside knowledge {w!r}: {stripped[:80]}")
    if hits:
        print("FAIL  no-judgement")
        for h in hits: print("   ", h)
        return 1
    print(f"ok    no-judgement no verdict words, no appeals to outside knowledge")
    return 0

sys.exit(main())
