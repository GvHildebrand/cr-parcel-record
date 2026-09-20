#!/usr/bin/env python3
"""Refuse to call this repository publishable while it carries private material.

Six rules. Any hit is a failure, and the failure names the file and the line so
it can be fixed rather than argued with.

  1. No identifier from the local denylist. The fixtures imitate the FORMAT of
     real Costa Rican documents, and whoever works with real documents has
     names and numbers that must never reach a public copy. Those go in
     _verify/denylist.local.txt, which is git-ignored and never published: a
     list of things you must not say is itself a thing you must not say, and
     hashing does not hide a short string from anyone willing to guess.
     _verify/denylist.example.txt shows the format with invented entries.
     Without a local file this rule is skipped, and the scan says so.
  2. No generic secret from _verify/denylist-patterns.txt: local paths, API key
     prefixes, personal mail. Stored as regular expressions, matched without
     regard to case.
  3. No Costa Rican natural-person id number (N-NNNN-NNNN). Corporate ids
     (3-101-NNNNNN) are register numbers of invented companies and are allowed.
  4. No folio from a province the fixtures do not use. A folio-shaped string in
     a fixture, or in the output built from it, must carry that fixture's own
     province digit. Anywhere else it must carry a province some fixture uses.
  5. No fixture reproduces the STRUCTURE of a real private matter, even with
     every name and number changed. Rules 1 to 4 check strings. A document can
     carry none of them and still be the same instrument with the serial
     numbers filed off. The shapes to refuse are read from the same local file
     as rule 1 (`shape:` lines), because naming them would describe the matter.
  6. The git history is scanned too: commit messages, author and committer
     identities, and every path that has ever been committed. A file removed
     from the working tree is still published if a commit reaches it; a commit
     message is published in full; every commit carries the author's mail
     address, which is how a personal address ends up in a public repository;
     and **every version of every file is still there**. Fixing a file at the
     tip does not unpublish what it used to say. Rule 6 reads every blob that
     any commit can reach, which is the only reading that matches what a clone
     actually hands over.

Local file format, one entry per line, `#` for comments:

    id: <a phrase of one to six words>      matched case-insensitively
    sha256: <hex of the lower-cased phrase> the same, for an entry kept hashed
    shape: <a phrase> | <what it is>        refused inside fixtures/ only
"""
import re, sys, pathlib, hashlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "__pycache__"}
LOCAL = "_verify/denylist.local.txt"
SELF = {LOCAL, "_verify/denylist.example.txt", "_verify/denylist-patterns.txt",
        "_verify/scan_public_safety.py", "_verify/test_verifiers.py",
        "_verify/test_history_scan.py"}
PRIVATE_PATHS = ("memory/",)

CEDULA  = re.compile(r"\b[1-9]-\d{4}-\d{4}\b")
FOLIO   = re.compile(r"\b([1-7])-0{0,2}\d{5,6}\s*-?\s*0{3}\b")
WORD    = re.compile(r"[^\W_]+", re.UNICODE)
NOTICE  = "CONSTRUCTED FIXTURE"
PROVINCES = {"SAN JOSE": "1", "SAN JOSÉ": "1", "ALAJUELA": "2", "CARTAGO": "3",
             "HEREDIA": "4", "GUANACASTE": "5", "PUNTARENAS": "6",
             "LIMON": "7", "LIMÓN": "7"}
PROV_LINE = re.compile(r"PROVINCIA:\s*([A-ZÁÉÍÓÚÑ ]+?)\s+FINCA:")

def lines(name):
    p = ROOT/name
    if not p.exists():
        return None
    return [l.strip() for l in p.read_text().splitlines()
            if l.strip() and not l.lstrip().startswith("#")]

def load_local():
    """Identifiers (plain and hashed) and structural shapes, or None if absent."""
    raw = lines(LOCAL)
    if raw is None:
        return None
    ids, hashes, shapes = set(), set(), []
    for l in raw:
        kind, _, val = l.partition(":")
        kind, val = kind.strip().lower(), val.strip()
        if kind == "id" and val:
            ids.add(" ".join(WORD.findall(val.lower())))
        elif kind == "sha256" and val:
            hashes.add(val.lower())
        elif kind == "shape" and val:
            pat, _, what = val.partition("|")
            shapes.append((pat.strip().lower(), what.strip() or "a refused shape"))
        elif re.fullmatch(r"[0-9a-f]{64}", l):      # a bare hash line
            hashes.add(l)
    return ids, hashes, shapes

def windows(text, n_max=6):
    """Every run of 1..n_max words, lower-cased, as the denylist stores them."""
    toks = [m.group(0).lower() for m in WORD.finditer(text)]
    for i in range(len(toks)):
        for n in range(1, min(n_max, len(toks)-i) + 1):
            yield " ".join(toks[i:i+n])

def files():
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or any(part in SKIP_DIRS for part in p.parts):
            continue
        rel = p.relative_to(ROOT).as_posix()
        if rel in SELF or rel.startswith(PRIVATE_PATHS):
            continue
        yield p, rel

def fixture_provinces():
    """{fixture folder name: province digit}, read from each registry report."""
    out = {}
    for rep in sorted((ROOT/"fixtures").glob("*/informe-registral.txt")):
        m = PROV_LINE.search(rep.read_text())
        if m and m.group(1).strip() in PROVINCES:
            out[rep.parent.name] = PROVINCES[m.group(1).strip()]
    return out

def allowed_province(rel, fixprov):
    """The province digits a folio in this file may carry."""
    parts = rel.split("/")
    if parts[0] == "fixtures" and len(parts) > 2 and parts[1] in fixprov:
        return {fixprov[parts[1]]}
    if parts[0] == "outputs" and rel.endswith(".md") and parts[-1][:-3] in fixprov:
        return {fixprov[parts[-1][:-3]]}
    return set(fixprov.values())

def git(*args):
    try:
        return subprocess.run(["git", "-C", str(ROOT), *args],
                              capture_output=True, text=True, timeout=60).stdout
    except Exception:
        return ""

def main():
    local = load_local()
    ids, hashes, shapes = local if local else (set(), set(), [])
    patterns = [re.compile(p, re.I) for p in (lines("_verify/denylist-patterns.txt") or [])]
    fixprov = fixture_provinces()
    hits = []

    def check_text(text, where):
        if ids or hashes:
            for w in windows(text):
                if w in ids or hashlib.sha256(w.encode()).hexdigest() in hashes:
                    hits.append(f"{where}  a denylisted identifier (a "
                                f"{len(w.split())}-word phrase)")
        for pat in patterns:
            if pat.search(text):
                hits.append(f"{where}  generic secret matching {pat.pattern!r}")

    def check_shapes(text, where):
        low = text.lower()
        for pat, what in shapes:
            if pat in low:
                hits.append(f"{where}  reproduces a refused structure: {what}. "
                            f"Rules 1-4 would not catch this: change the "
                            f"mechanism, not the names.")

    # rules 1-4, working tree
    for p, rel in files():
        try:
            text = p.read_text()
        except UnicodeDecodeError:
            continue
        ok_prov = allowed_province(rel, fixprov)
        for n, line in enumerate(text.splitlines(), 1):
            check_text(line, f"{rel}:{n}")
            for m in CEDULA.finditer(line):
                hits.append(f"{rel}:{n}  natural-person id number {m.group(0)!r}")
            for m in FOLIO.finditer(line):
                if m.group(1) not in ok_prov:
                    hits.append(f"{rel}:{n}  folio {m.group(0)!r} from province "
                                f"{m.group(1)}, which this file's fixture does "
                                f"not use")

    # rule 5, fixtures only
    for p in sorted((ROOT/"fixtures").rglob("*.txt")):
        check_shapes(p.read_text(), p.relative_to(ROOT).as_posix())

    for p in sorted((ROOT/"fixtures").rglob("*.txt")):
        if NOTICE not in p.read_text():
            hits.append(f"{p.relative_to(ROOT).as_posix()}  missing the {NOTICE} notice")

    # rule 6, history
    history_checked = False
    log = git("log", "--all", "--format=%H%n%B%n--end--")
    if log.strip():
        history_checked = True
        check_text(log, "git history (a commit message)")
        who = git("log", "--all", "--format=%an <%ae>%n%cn <%ce>")
        check_text(who, "git history (an author or committer identity)")
        # every blob any commit can reach, because a clone hands over all of them
        listing = git("rev-list", "--objects", "--all").splitlines()
        blobs = [l.split(" ", 1) for l in listing if " " in l]
        for sha, path in blobs:
            if path in SELF or path.startswith(PRIVATE_PATHS):
                continue
            body = git("cat-file", "-p", sha)
            if not body:
                continue
            check_text(body, f"git history ({path} at {sha[:8]})")
            if path.startswith("fixtures/"):
                before = len(hits)
                check_shapes(body, f"git history  {path} at {sha[:8]}")
                if len(hits) > before:
                    hits.append(f"git history  {path} at {sha[:8]}: fixing the "
                                f"file at the tip does not unpublish what it used "
                                f"to say; the history has to be rebuilt.")

        ever = set(git("log", "--pretty=format:", "--name-only", "--all").split())
        for path in sorted(ever):
            if path.startswith(PRIVATE_PATHS) or path == LOCAL:
                hits.append(f"git history  {path} has been committed. Removing it "
                            f"from the working tree does not unpublish it; the "
                            f"history must be rewritten before this repo is pushed.")

    if local is None:
        print(f"note  public safety: no {LOCAL}, so rules 1 and 5 (private "
              f"identifiers and shapes) were skipped. Copy "
              f"_verify/denylist.example.txt to start one.")
    if hits:
        print("FAIL  public safety")
        for h in sorted(set(hits)): print("   ", h)
        return 1
    n_files = sum(1 for _ in files())
    listed = (f"{len(ids) + len(hashes)} local identifiers, {len(shapes)} local "
              f"shapes" if local else "no local denylist")
    print(f"ok    public safety {n_files} files, {listed}, {len(patterns)} secret "
          f"patterns, history {'scanned' if history_checked else 'ABSENT'}, 0 hits")
    return 0

sys.exit(main())
