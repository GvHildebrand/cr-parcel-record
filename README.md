# cr-parcel-record

**Converts the document set for one Costa Rican parcel into one Parcel
Record: eleven fixed sections, every line citing the document line it came
from, and every gap marked instead of filled.**

Scope: Costa Rica, one parcel at a time, four document types (registry report,
survey plan, water concession resolution, deed extract). Nothing else.

It does not value land, score it, or advise on it. It converts.

**The reason it exists**, from the worked case in
[`outputs/03_santa-cruz_offrecord.md`](outputs/03_santa-cruz_offrecord.md):

> The registry report showed nothing but statutory reserves.
> The deed handed over a fifteen-year agricultural lease on the whole parcel,
> never filed at the Registry, with a purchase option on top of it.

A buyer reading only the registry sees land they can use. Section 8 of the
record is where the tenant appears.

## Quickstart

```bash
git clone <this repo> && cd cr-parcel-record
make verify
```

That runs every check against the three worked examples. Then, to convert your
own documents:

1. Drop this folder into a Claude project, or point any agent at it.
2. Put one parcel's documents in a folder as plain text, named
   `informe-registral.txt`, `plano-catastrado.txt`, `resolucion-aguas.txt`,
   `escritura-extracto.txt`. Only the first is required.
3. Say: **"Convert this folder to a Parcel Record."**
4. Check the result with `make verify`.

Details in [QUICKSTART.md](QUICKSTART.md). For agents, [AGENTS.md](AGENTS.md).

## What the checks prove

```
note  public safety: no _verify/denylist.local.txt, so rules 1 and 5 (private identifiers and shapes) were skipped. Copy _verify/denylist.example.txt to start one.
ok    public safety 34 files, no local denylist, 6 secret patterns, history scanned, 0 hits
ok    shape        3 outputs, 11 sections each, identical order, every field key in the contract
ok    citations    194 citations resolved, every value found on the line it cites
ok    parser       spanish number and date parser self-test passes
ok    derivations  8 derived values re-computed from scratch, all agree
ok    no-judgement no verdict words, no appeals to outside knowledge
ok    self-test    16 injected faults, every one caught
ok    history-scan 4 history faults injected, every one caught
```

The last two lines are the ones that matter. `_verify/test_verifiers.py` breaks
the outputs on purpose, sixteen ways, and `_verify/test_history_scan.py` builds
throwaway repositories carrying things that must never be published. Both fail
the build if a check sleeps through a fault.

Among the twenty: an invented flow rate, a citation moved to the wrong line,
an owner name respelled the way it is usually written, hectares computed
wrongly, a derivation that is not one of the three allowed, a verdict about the
land where the record is only meant to convert, a fixture rebuilt in the shape
of a real instrument, a private file deleted from the working tree but still
reachable from a commit, and a personal mail address as the commit author.

## The folder

| | |
|---|---|
| [`identity.md`](identity.md) | what it converts, and the six things it refuses to do |
| [`rules.md`](rules.md) | the seven steps, in order |
| [`examples.md`](examples.md) | the three worked pairs and what each one proves |
| [`reference/`](reference/) | the contract: the field list, the schema, what every field means, the three allowed derivations, the four document formats |
| [`fixtures/`](fixtures/) | three parcels as documents |
| [`outputs/`](outputs/) | the three records they produce |
| [`_verify/`](_verify/) | the checks, and the tests that the checks work |
| [`docs/`](docs/) | why it is built this way, and the stranger test record |

The translator is the first four. `_verify/` decides nothing: delete it and the
conversion still works; you check the citations by hand instead. Which you
can, because a citation is a filename and a line number:

```bash
$ sed -n '19,25p' fixtures/03_santa-cruz_offrecord/escritura-extracto.txt
```

## Measured, not argued

A fresh session that had never seen this repository was given one unseen parcel
and told to convert it. Its record passed every content check: eleven sections
in order, 59 citations all resolving, both derivations correct.

The input carried a mortgage with a term of ninety-six months. Adding that to
the start date gives March 2030, it is one line of arithmetic, and no document
in the folder says it. The session refused it, because ninety-six months is not
a whole number of years and `reference/derivations.md` allows three operations
and no more.

Record in [`docs/readme-test.md`](docs/readme-test.md), including the test not
yet run.

## Three rules the record follows

**Nothing is invented.** Every value appears in a document, or was derived by
one of three operations that show their arithmetic, or reads `not in source`.

**Nothing is dropped.** Input the schema has no field for is quoted in section
11 with the reason. A silent omission is worse than a visible gap.

**Nothing is resolved.** When two documents disagree, both readings go in
section 9, spelled as each document spelled them. The record does not decide
which is right, and it never normalises a name.

## Fixtures are constructed

Every document in `fixtures/` reproduces a real Costa Rican document layout
with invented contents. No real parcel, owner or transaction is described.
Natural-person identity numbers are omitted throughout.
[`_verify/scan_public_safety.py`](_verify/scan_public_safety.py) fails the build
if that stops being true.

If you work with real documents, list their names, numbers and clause shapes in
`_verify/denylist.local.txt` (format in
[`_verify/denylist.example.txt`](_verify/denylist.example.txt)). Git ignores
that file, so it is never published, and the scan refuses any of its entries
anywhere in the repository or its history. Without it, the scan says that part
was skipped.

## Licence

MIT. See [LICENSE](LICENSE).
