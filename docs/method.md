# Why it is built this way

The README says what this does. This says why, and what was rejected.

## Fidelity, not judgement

A land tool wants to be useful. Useful looks like a score, a verdict, a
recommendation. Every one of those is a claim the documents do not make, and
once the output carries one, a reader cannot tell which parts came from the
registry and which came from the tool.

So the record makes no claims of its own. Section 5 prints what the registry
prints. Section 8 quotes what the deed says. What it means is the reader's
work, and they now have a record in which every line can be traced back.

This is the harder version of the job, and the only one worth automating. The
easy version, a tool that reads the documents and tells you what it thinks, is
what people already have and do not trust.

## Why eleven sections and not seven

Sections 1 to 7 are extraction. Any competent converter produces them.

Sections 8 to 11 are the ones that cost something to build:

**8, off-record obligations.** Costa Rican practice produces several
obligations that bind land without appearing in the registry: an unregistered
lease, a reserved usufruct, a purchase option, a restriction on use agreed
between the parties. Any of them can run while the registry report and the
buyer's own search both come back clean. Without this section, a buyer reading
a clean report concludes the land comes free. The third worked example carries
a fifteen-year lease over the whole parcel and an option to buy it, neither
printed by the registry.

**9, conflicts.** The reflex when two documents disagree is to pick the better
one. That reflex is the converter deciding something. Both readings go in, with
both citations, spelled as each document spelled them.

**10, not in source.** A gap scattered through a long document is invisible.
Collected in one list, it is a work order: these are the documents still to
pull.

**11, unmapped.** The record says what it could not place. A converter whose
section 11 is always empty is not looking, and its schema can never be wrong,
which means it can never be corrected.

## Why the checks are scripts and not prose

A folder can promise anything. A record with one invented fact in it is worse
than no record, so the promise needs to be falsifiable by someone who does not
trust the author.

Five scripts, each with one job:

| | |
|---|---|
| `verify_shape.py` | reads `reference/fields.tsv`, not the prose, so the contract and the check cannot drift apart |
| `verify_citations.py` | opens every cited line and looks for the value on it |
| `verify_derivations.py` | re-computes every derived value from scratch, using a Spanish number parser that knows nothing about land |
| `verify_no_judgement.py` | refuses a verdict word or an appeal to knowledge the documents do not carry |
| `scan_public_safety.py` | refuses to call the repo publishable while it carries private material, in the working tree **or anywhere in the git history** |

And then `test_verifiers.py`, which is the one that matters. It injects sixteen
known faults and fails the build if any check sleeps through one, and
`test_history_scan.py` does the same with four faults planted in throwaway git
histories. A verifier that has never failed has never been tested, and a
check that cannot fail is decoration.

The sixteen faults were chosen to be the ways this converter could plausibly
lie: an invented flow rate, a citation moved one line, an owner name respelled
the way it is usually written, hectares off by a decimal place, a term read as
longer than the document grants, and a derivation invented on the spot
("comparable parcels in the area average 24 ha"), and a verdict on the land
where the record is only meant to convert.

That last check exists because a hand-pass over the prose lines of the three
records found three judgements and one claim from outside the documents, all
of them in sentences no other script reads. The scripts check fields. Nobody
was checking the commentary between them.

## What was rejected

**Real documents.** The first plan was to publish a real parcel's document set.
Costa Rican registry reports are obtainable, and a real one would have been more
convincing. It would also have published a named private party's holdings and
encumbrances to a public repository. The fixtures reproduce the layouts, which
are public and are specified in `reference/source-formats.md`, and carry
invented contents.

**A single "encumbrances" section.** Merging sections 5 and 8 would read better
and would destroy the finding. The whole point is that one of them is the
registry's answer and the other is not.

**Computing the area discrepancy.** When the registered area and the surveyed
area differ, the obvious move is to print the difference. A number there reads
as a verdict on which document is right. Both figures go in, side by side, with
their citations.

**Normalising names.** `SOCIEDAD ANONIMA` and `S.A.` are the same company and
different strings. Collapsing them is the single most defensible-looking way
this tool could state something no document states.

## Provenance

The document layouts were learned from primary sources: a Registro Nacional
`CONSULTA POR NÚMERO DE FINCA` printout, an inscribed survey plan, and a
Dirección de Agua concession resolution in the `RESULTANDO` / `CONSIDERANDO` /
`POR TANTO` / `RESUELVE` form.

The off-record mechanisms in section 8 are drawn from general Costa Rican
conveyancing. `_verify/scan_public_safety.py` rule 5 refuses a fixture that
mirrors a real private matter's *structure* even with every name and number
changed, because a string check cannot see a shape: a fixture can carry none of
a denylisted name and still be the same instrument with the serial numbers
filed off. The identifiers and shapes it refuses live in a local file that git
ignores, for the same reason in reverse: a list of things you must not say is a
thing you must not say, and hashing a short phrase does not hide it from anyone
willing to guess.
