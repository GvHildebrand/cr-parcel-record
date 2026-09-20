# Stranger test

The rule this repository is built under says a README is not done until it
has been measured on a stranger, with the record kept in the repo. Two
tests: a fresh AI session given only the repo and a task, and one human outsider,
timed. The author testing it on themselves does not count, because the author
fills in the gaps.

The point is to measure a README, not to argue for it.

---

## Test A: fresh AI session, unseen input

**Date:** 2026-09-20
**Setup:** a session with no knowledge of this repository, given the repository
path and one instruction: convert a parcel's documents into whatever this
repository produces. It was told not to read `outputs/` until after writing its
own result, and not to ask questions.

**The input it was given had a feature none of the three worked examples has:** a
`HIPOTECA DE PRIMER GRADO` carrying `MONTO`, `ACREEDOR` and `PLAZO: NOVENTA Y
SEIS MESES`. The schema does not name `acreedor` or `plazo`, and ninety-six
months is not a whole number of years.

**Result: it produced a correct record.** Verified by running this repository's
own checks against its output, on a clean clone:

```
ok    shape        1 outputs, 11 sections each, identical order
ok    citations    59 citations resolved, every value found on the line it cites
ok    derivations  2 derived values re-computed from scratch, all agree
ok    no-judgement no verdict words, no appeals to outside knowledge
```

**The part that matters.** It took the unnamed sub-field names from the document
rather than dropping them, and then it refused the obvious derivation:

> No expiry is computed for the mortgage. `INICIA EL: 18-MAR-2022` plus
> `PLAZO: NOVENTA Y SEIS MESES` is not one of the three allowed derivations, and
> the schema has no field for it.

March 2022 plus ninety-six months is March 2030. It is a single line of
arithmetic, it would have looked authoritative, and no document in the folder
says it. D3 refuses terms that are not whole years, and the refusal held in a
session that had never seen this repository before.

**Time to first understanding:** one file. `README.md` answered what the repo
does and how to run it. But the tester drew a distinction worth keeping: *"how
to run it is not how to produce a correct record"*, and that took eight more
files.

**Time to first result:** 16 tool calls to a written record, 18 including
self-verification.

**Verdict: no.** Five minutes buys a verifiable record, not a correct one.

### What it found, and what was done

| # | Finding | Fixed |
|---|---|---|
| 1 | No block format for section 5 anywhere. `rules.md` templates sections 8, 9 and 11 and not 5; `fields.tsv` said `gravamen many` and stopped. The tester guessed a format. It passed every check. | `rules.md` now carries a worked block template |
| 2 | **"fields.tsv is the contract" was false.** The worked outputs emitted `tipo`, `citas`, `monto`, `a_favor_de` and `descripcion`, none of which were in the contract, and nothing noticed. | `fields.tsv` now names every sub-field, and `verify_shape.py` fails on any key the contract does not know, in either direction |
| 3 | Where a verbatim value starts was undefined. `propietario_capacidad` read `DUEÑO` for the tester and `EN CALIDAD DE DUEÑO` in the worked records. Both passed. | `fields.tsv` gained an `example` column showing every value exactly; `rules.md` explains the case |
| 4 | **`QUICKSTART.md` promised something the code could not do.** It said to convert your own folder and run `make verify`, but the verifier hard-coded `fixtures/<output-name>/`, so a parcel outside the repo could never be checked. | the verifiers now read the record's own `Input:` line; a record pointing anywhere on disk verifies |
| 5 | `CLAUDE.md`'s reading list omitted `reference/schema.md`, the file that defines the eleven sections, then said "stop reading and convert". | added, along with a pointer to one complete worked record |
| 6 | D2's four-decimal rule and the semicolon chaining syntax existed only inside `verify_derivations.py`. | both written into `reference/derivations.md` |
| 7 | The repository changed while the tester was reading it. | an artifact of testing during a build, not a defect |

Finding 2 is the one that mattered. The central claim of this folder is that the
contract is a file a reader can open, and the check that was supposed to enforce
it only ever read the single-valued fields. The contract and the records had
already drifted, and nothing would have caught it.

The tester's own suggestion, that `CLAUDE.md` should point at a complete worked
record because *"everything I got wrong lives only in outputs/, which the docs
tell you to read last"*, is now the last line of `CLAUDE.md`'s reading list.

## Test B: one human outsider, timed

**Not yet run.** This one cannot be delegated. It needs a person who has not
seen the repository, a timer, and a note of where they stopped.

What to record: how long until they knew what the repo does, how long until they
had a result, and every point at which they had to guess. Add it here. Until it
is here, this README has had one of its two tests.
