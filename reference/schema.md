# The output contract

A Parcel Record has **eleven sections, always all eleven, always in this order**,
whatever the input looked like. A section with nothing to report says so; it is
never dropped, and no section is ever added.

The machine-readable field list is [`fields.tsv`](fields.tsv). It is the
authority. This file explains the record's structure;
[`field-definitions.md`](field-definitions.md) defines every field in it. `_verify/verify_shape.py` reads the TSV, not
this page, so the two cannot drift without the check failing.

## The line format

Every field in the output is one line, in one of four forms.

**A fact taken from a document:**

```
- **caudal_asignado_ls**: 0.35  `[resolucion-aguas:49]`
```

The citation is `[<document>:<line>]`. The document is a filename in the input
folder, without its extension. The line is a 1-indexed line number in that file.
The value must appear on that line. `verify_citations.py` opens the file, goes to
the line, and looks for the value. If it is not there, the run fails.

**A value the documents did not answer:**

```
- **plano_area_m2**: not in source
```

Not "unknown", not "N/A", not an estimate, not the registry figure borrowed from
a different field. The exact string `not in source`, and the field key is also
listed in section 10 so a reader can see the gaps in one place.

**A value computed from a cited fact:**

```
- **medida_m2**: 243860  `derived: DOSCIENTOS CUARENTA Y TRES MIL OCHOCIENTOS SESENTA = 243860` from `[informe-registral:18]`
```

Only three operations are allowed to derive anything, and they are listed in
[`derivations.md`](derivations.md). Everything else is invention. A derived value
always shows its arithmetic and always cites the fact it started from.

**A field whose source documents disagree:**

```
- **propietario**: conflict, see section 9
```

The Parcel Record never picks a winner. Both readings go in section 9 with both
citations.

## The eleven sections

| # | Section | What it holds | Empty form |
|---|---|---|---|
| 1 | Identity | Which parcel this is: matrícula, location, nature, predial id | never empty: matrícula is required |
| 2 | Extent | How big, which survey plan, and the four boundaries | fields say `not in source` |
| 3 | Holder | Who is registered, in what capacity, since when | fields say `not in source` |
| 4 | Chain of title | Which fincas this one came from; segregations | `NO HAY` verbatim, or `not in source` |
| 5 | Charges on the record | Every gravamen and afectación the registry prints | `GRAVAMENES o AFECTACIONES: NO HAY` |
| 6 | Pending entries | Anotaciones: filings not yet registered | `ANOTACIONES SOBRE LA FINCA: NO HAY` |
| 7 | Water | The concession, if a resolution is in the input | `no water document in input` |
| 8 | Off-record obligations | Things that bind the land and are **not** in the registry | with a deed: `none found in the deed supplied`. Without one: **`NOT ASSESSED`**, never `none` |
| 9 | Conflicts between sources | Same field, two documents, two answers | `none` |
| 10 | Not in source | Every field key the documents did not answer | `none` |
| 11 | Unmapped | Input the schema had no field for | `none` |

## Why sections 8, 9 and 11 exist

They are the difference between a translator and an extractor.

**Section 8** exists because a registry report that prints no charges is not
proof that land comes free of obligations. An unregistered lease, a reserved
usufruct, a purchase option, a restriction on use agreed between the parties:
any of these can bind the land while the registry report and the buyer's own
search both come back clean. A reader who sees only sections 5 and 6 will
draw the wrong conclusion. Section 8 is where the deed extract gets read, and
where its absence is reported as `NOT ASSESSED` rather than `none`.

**Section 9** exists because normalising a name is the commonest way a converter
lies. If the registry says `INVERSIONES PALO VERDE SOCIEDAD ANONIMA` and the
deed says `Inversiones Palo Verde S.A.`, the Parcel Record reports both, spelled
as each document spelled them, and does not decide.

**Section 11** exists because a silent omission is worse than a visible gap. If
the input carries something the schema has no field for, it is quoted here with
the reason no field took it. A reader can then see whether the schema is wrong.

## What a Parcel Record is not

It does not value the land, score it, rate it, recommend anything, or say whether
to buy. Those are judgements, and this folder produces none. It converts a
document set into a record whose every line can be checked against a line of the
input. What the record means is the reader's work.
