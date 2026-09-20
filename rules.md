# Rules: the procedure, in order

Run these seven steps in order, every time. Steps 1 and 2 are what keep the
later steps honest; skipping them is how a converter starts answering from
memory instead of from the folder.

---

## Step 1: Inventory the input

List every file in the input folder and classify each one against
[`reference/source-formats.md`](reference/source-formats.md):

| File | Classified as | Lines |
|---|---|---|

Classify by **contents, not filename**. A file called `water concession.pdf` is
routinely an admissibility ruling, not a grant. Open it: only a resolution whose
`RESUELVE` paragraph says `OTORGAR` is a concession, and anything else is
classified as what it is, then reported in section 11.

A file you cannot classify is listed here, read for nothing, and quoted in
section 11. **No registry report in the folder: stop.** Say so and produce
nothing; the record is built on the matrícula and there is no substitute.

Every document in `fixtures/` ends with a fenced `CONSTRUCTED FIXTURE` notice
that says the file is not a real document. That block is not part of the
document. Do not read fields from it, do not cite it, and do not report it in
section 11. It sits after the document body precisely so that adding it does not
move any line number an output already cites.

## Step 2: Number the lines

Work from a line-numbered copy of each input. Every citation you write is
`[<document>:<line>]`, and the verifier resolves it against exactly these
numbers. Cite the line the value sits on, not the line of the label above it,
when the two differ.

## Step 3: Fill the fields, in the order of `fields.tsv`

Walk [`reference/fields.tsv`](reference/fields.tsv) top to bottom. For each
field, go to the document named in `source_doc` and look for it. Three outcomes,
and no others:

- **Found** → write the value and the citation.
- **The document is absent from the input** → `not in source`, and add the key
  to section 10.
- **The document is present and does not carry it** → `not in source`, and add
  the key to section 10.

Write values verbatim. Capitals stay capitals. `NO HAY` stays `NO HAY` and is
never translated to "none" or "no". A date printed `17-ENE-2025` is written
`17-ENE-2025`.

For a `many` field, one block per instance, in the order the document prints
them. Do not sort, merge or deduplicate: two gravámenes that look identical are
two entries, and collapsing them removes one.

### Where a value starts and stops

The commonest ambiguity, and the reason `fields.tsv` carries an `example`
column. Line 31 of a registry report reads:

```
CEDULA JURIDICA 3-101-448290 EN CALIDAD DE DUEÑO
```

That line answers two fields. `propietario_id` takes `3-101-448290`.
`propietario_capacidad` takes `EN CALIDAD DE DUEÑO`, not `DUEÑO`, because the
capacity is the whole phrase and `DUEÑO` alone reads as a different claim in a
report where the next parcel says `EN CALIDAD DE FIDUCIARIO`.

**When in doubt, the `example` column in `fields.tsv` is the answer.** It shows
exactly what the value looks like, including where it starts.

### A block field

`gravamen`, `anotacion`, `off_record_obligation`, `conflict` and `unmapped` are
blocks, not single values. One block per instance, in the order the document
prints them, each headed and then filled with sub-fields:

```
### gravamen 1
- **tipo**: RESERVAS LEY AGUAS  `[informe-registral:42]`
- **citas**: 335-11904-01-0901-001  `[informe-registral:43]`
- **inicia_el**: 21-MAR-1978  `[informe-registral:44]`
```

Take only the sub-fields the block actually prints; a block that carries no
`monto` has no `monto` line. Sub-fields are named in `fields.tsv`. **A block
carrying a label `fields.tsv` does not name is still reported**, with the field
key taken from the document in lower snake case, and the new key added to
`fields.tsv` in the same change. `verify_shape.py` fails on a key the contract
does not know, in either direction.

## Step 4: Derive only what may be derived

Three operations, in [`reference/derivations.md`](reference/derivations.md).
Each derived value shows its arithmetic and cites its starting fact. If a value
tempts you and it is not one of the three, it is `not in source`.

## Step 5: Read the deed for what the registry cannot show

If the input has a deed extract, read every clause and ask one question of each:
**does this create an obligation that survives the sale?**

A lease the Registry never saw. A usufruct reserved to the seller. An option to
buy held by someone else. A restriction on use. An obligation to a third party.

The deed often says so itself, in the clause: *no fue presentado al Registro*.
That sentence is the `why_off_record` field.

Each one goes in section 8 as a block:

```
- **obligation**: <what it binds the land to>
  **quote**: "<the clause's own words>"
  **source**: `[escritura-extracto:NN]`
  **amount**: <as printed, or not in source>
  **beneficiary**: <as printed, or not in source>
  **appears_in_registry**: no | yes | unknown
```

`appears_in_registry` is answered by looking: search section 5 for a charge that
matches this obligation. `no` means you looked and found none. `unknown` means
there is no registry report to look in. Never leave it inferred.

## Step 6: Record conflicts, resolve none

Any field two documents answer differently goes in section 9:

```
- **field**: <field_key>
  **value_a**: <as document A printed it>  `[doc-a:NN]`
  **value_b**: <as document B printed it>  `[doc-b:NN]`
```

and the field itself in its own section reads `conflict, see section 9`.

The four that recur:

1. **Owner name** spelled differently across documents.
2. **Registered area vs surveyed area.** Both go in section 2; the gap is not
   computed, because a difference presented as a number reads as a judgement
   about which is right.
3. **Water concession holder vs registered owner.** A concession runs to a
   person, not with the land.
4. **The property named in the water resolution vs the finca in the registry
   report.** A concession granted on folio X is not evidence about folio Y.

## Step 7: Empty the pockets

Before writing the file, go back through every input line you did not cite. For
each, one of two things is true: it is boilerplate, or it is something the
schema has no field for. Quote the second kind in section 11:

```
- **quote**: "<the line>"
  **source**: `[doc:NN]`
  **why_no_field**: <which section would have taken it, and what is missing>
```

Section 11 is how the schema gets fixed. A converter whose section 11 is always
empty is not looking.

---

## The check before you hand it over

1. Eleven sections, in order, none missing, none added.
2. Every value either carries a citation, carries a derivation with its
   arithmetic, or reads `not in source`.
3. Every field key that reads `not in source` also appears in section 10.
4. No word in the output expresses a judgement about the land.
5. Section 11 has been written after an actual re-read, not left empty by
   default.

`make verify` runs checks 1, 2, 3 and most of 4 mechanically:
`_verify/verify_no_judgement.py` refuses verdict words and appeals to outside
knowledge, including in the prose between fields, which is where they hide.
Check 5 is yours, and no script can do it.
