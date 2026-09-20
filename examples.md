# Three inputs, three outputs, one shape

Each pair below is a folder in [`fixtures/`](fixtures/) and a file in
[`outputs/`](outputs/). All three outputs carry the same eleven sections in the
same order. `make verify` proves it, and proves every line of every output
against the input that produced it.

Every document in `fixtures/` is constructed. The layouts are real and are
documented in [`reference/source-formats.md`](reference/source-formats.md); the
names, numbers and parcels are invented. Each file says so at the end.

---

## 1. A complete input: [`01_liberia_complete`](fixtures/01_liberia_complete/)

Registry report, survey plan, water concession. Everything the schema asks for
is somewhere in the folder.

**What it proves:** a full input produces a full record. Section 10 is empty.
Eight values are derived and each shows its arithmetic.

**The one thing worth looking at:** section 11. The survey plan states its own
purpose, `PARA EFECTOS DE RECTIFICACION DE MEDIDA`: this plan exists because
the area was corrected. The schema has no field for it, so instead of dropping
it, the record quotes it and says which section should have taken it. That is
how the contract gets fixed rather than quietly failed.

## 2. A thin input: [`02_nicoya_sparse`](fixtures/02_nicoya_sparse/)

One registry report. No survey plan, no water file, no deed.

**What it proves:** the shape does not shrink to fit the input. Every water
field is present and reads `not in source`, and all eighteen are listed again in
section 10. A reader can see the gaps without hunting for them.

**The distinction the record keeps:** `plano_catastrado` reads `NO HAY`, because
the registry was asked and answered. `plano_area_m2` reads `not in source`,
because no survey plan was supplied. Those are different facts and a converter
that blurs them has lost the plot.

**And the loop that section 11 exists to close.** This record's section 11 once
carried four lines: a pending filing's citation, its date, its document type and
its state. The schema had no fields for them, so instead of dropping them the
record quoted each one and named what was missing. The schema now has an
`anotacion` block, those four lines are fields in section 6, and section 11 is
empty. That is the loop working: an unmapped line became a field.

## 3. An input that disagrees with itself: [`03_santa-cruz_offrecord`](fixtures/03_santa-cruz_offrecord/)

Registry report, survey plan, water concession, deed extract. This is the one
that matters.

**What the registry says:** no mortgage, no easement, no pending filings. Two
statutory reserves. Sections 5 and 6 have nothing else to report.

**What the deed says**, in a clause that ends by stating its own invisibility:

> "por un plazo de QUINCE AÑOS, sobre la totalidad de la finca, por una renta
> anual de OCHO MIL DOLARES ... Dicho contrato no fue presentado al Registro y
> no consta en el informe registral"

The whole parcel is let for fifteen years, the tenant holds an option to buy it
for US$420,000, and the registry prints neither. Section 8 carries both with the
clauses verbatim, the amounts, the beneficiaries, and `appears_in_registry: no`,
answered by looking at section 5, not by guessing.

Three more things the record catches and resolves for nobody:

- The owner's name is spelled three ways across three documents. Section 9 holds
  all three. The record does not pick one.
- The registered area is 119,760 m² and the surveyed area is 118,430 m². Both
  are in section 2. The difference is not computed, because a number would read
  as a verdict on which document is right.
- The water resolution in the folder was granted on finca **5-162093-000**, to a
  different company. This record is finca **5-162094-000**. Section 7 reports
  the document because it is in the input; section 9 says it is about the
  neighbour.

**What it proves:** the tenant who comes with the land is not in the registry,
and is in the record. That is the only reason to build a converter instead of
reading the documents yourself at two in the morning.
