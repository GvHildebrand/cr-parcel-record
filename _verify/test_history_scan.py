#!/usr/bin/env python3
"""Rule 6 reads the git history. This proves it can fail.

test_verifiers.py copies the repository without .git, so the history rules never
run there and would pass vacuously. This builds one throwaway repository per
case, each carrying one thing that must never be published, and asserts the
scanner refuses each one.
"""
import subprocess, sys, tempfile, shutil, pathlib, os

ROOT = pathlib.Path(__file__).resolve().parent.parent

def sh(*args, cwd, **kw):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, **kw)

def build(tmp, mutate):
    """A minimal repo carrying the scanner and its lists, then one commit."""
    work = pathlib.Path(tmp)/"repo"
    shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns(".git", "__pycache__"))
    # the example list stands in for a local one; .gitignore keeps it out of commits
    shutil.copy(work/"_verify"/"denylist.example.txt",
                work/"_verify"/"denylist.local.txt")
    env = dict(os.environ,
               GIT_AUTHOR_NAME="T", GIT_AUTHOR_EMAIL="t@users.noreply.github.com",
               GIT_COMMITTER_NAME="T", GIT_COMMITTER_EMAIL="t@users.noreply.github.com")
    sh("git", "init", "-q", cwd=work, env=env)
    sh("git", "add", "-A", cwd=work, env=env)
    sh("git", "commit", "-q", "-m", "initial", cwd=work, env=env)
    mutate(work, env)
    return work

CASES = []

def case(name):
    def deco(fn): CASES.append((name, fn)); return fn
    return deco

@case("a private file reachable from a commit")
def _(work, env):
    (work/"memory").mkdir(exist_ok=True)
    (work/"memory"/"notes.md").write_text("working notes\n")
    sh("git", "add", "-f", "memory/notes.md", cwd=work, env=env)
    sh("git", "commit", "-q", "-m", "add notes", cwd=work, env=env)
    # and then remove it, the way someone would think removes it
    sh("git", "rm", "-q", "memory/notes.md", cwd=work, env=env)
    sh("git", "commit", "-q", "-m", "remove notes", cwd=work, env=env)

@case("a denylisted identifier in a commit message")
def _(work, env):
    (work/"docs"/"x.md").write_text("x\n")
    sh("git", "add", "-A", cwd=work, env=env)
    sh("git", "commit", "-q", "-m",
       "note: quetzalcoatlus sentinel phrase appears here", cwd=work, env=env)

@case("a fixture fixed at the tip but still readable in an earlier commit")
def _(work, env):
    f = work/"fixtures"/"03_santa-cruz_offrecord"/"escritura-extracto.txt"
    good = f.read_text()
    f.write_text(good.replace("TERCERO - ARRENDAMIENTO AGRICOLA VIGENTE:",
                              "CLAUSULA CENTINELA DE ESTRUCTURA\n\n"
                              "TERCERO - ARRENDAMIENTO AGRICOLA VIGENTE:"))
    sh("git", "add", "-A", cwd=work, env=env)
    sh("git", "commit", "-q", "-m", "a fixture", cwd=work, env=env)
    f.write_text(good)                      # put it back, the way someone would
    sh("git", "add", "-A", cwd=work, env=env)
    sh("git", "commit", "-q", "-m", "fix the fixture", cwd=work, env=env)

@case("a personal mail address as the commit author")
def _(work, env):
    addr = "someone" + "@" + "gmail" + ".com"   # assembled, so this file is not itself a hit
    bad = dict(env, GIT_AUTHOR_EMAIL=addr, GIT_COMMITTER_EMAIL=addr)
    (work/"docs"/"y.md").write_text("y\n")
    sh("git", "add", "-A", cwd=work, env=bad)
    sh("git", "commit", "-q", "-m", "ordinary message", cwd=work, env=bad)

def main():
    # the scanner must pass on a clean throwaway repo first
    with tempfile.TemporaryDirectory() as tmp:
        work = build(tmp, lambda w, e: None)
        r = sh(sys.executable, "_verify/scan_public_safety.py", cwd=work)
        if r.returncode != 0:
            print("FAIL  history-scan\n    clean throwaway repo already fails:\n" + r.stdout)
            return 1
        if "history scanned" not in r.stdout:
            print("FAIL  history-scan\n    the history was not scanned at all:\n" + r.stdout)
            return 1

    asleep = []
    for name, mutate in CASES:
        with tempfile.TemporaryDirectory() as tmp:
            work = build(tmp, mutate)
            if sh(sys.executable, "_verify/scan_public_safety.py", cwd=work).returncode == 0:
                asleep.append(f"did NOT catch {name}")
    if asleep:
        print("FAIL  history-scan")
        for a in asleep: print("   ", a)
        return 1
    print(f"ok    history-scan {len(CASES)} history faults injected, every one caught")
    return 0

sys.exit(main())
