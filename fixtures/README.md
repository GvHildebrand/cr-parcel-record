# The fixtures

Three Costa Rican parcels in Guanacaste, as document sets.

**Every file here is constructed.** The layouts reproduce real Costa Rican land
documents and are specified in
[`../reference/source-formats.md`](../reference/source-formats.md). The names,
company names, parcel numbers, plan numbers, dates, amounts and signatures are
invented. No real parcel, owner, notary, surveyor or transaction is described.
Each file repeats this at the end, and
[`../_verify/scan_public_safety.py`](../_verify/scan_public_safety.py) fails the
build if any file loses the notice.

Natural-person identity numbers are omitted throughout, written
`cédula de identidad [omitida]`. Corporate register numbers (`3-101-NNNNNN`) are
kept because the companies are invented and the document is unreadable without
them.

| Folder | Documents | Built to exercise |
|---|---|---|
| `01_liberia_complete` | registry, plan, water | the full path, and the derivations |
| `02_nicoya_sparse` | registry only | `not in source` across a whole section |
| `03_santa-cruz_offrecord` | registry, plan, water, deed | an obligation the registry does not print, four conflicts, a water file about the neighbouring parcel |

## Line numbers are an interface

Outputs cite `[document:line]`, and `_verify/verify_citations.py` resolves every
one of them against these files. **Editing a fixture moves the lines and breaks
the citations.** Add to the end, never the middle, and run `make verify`.
