# Quickstart

Five minutes, from clone to a checked record.

## 1. Prove the folder works before you trust it

```bash
make verify
```

Eight checks against three worked examples. The last two break things on
purpose, sixteen faults in the outputs and fixtures and four in throwaway git
histories, and fail if any check misses one.

## 2. Look at one pair

```bash
cat fixtures/03_santa-cruz_offrecord/informe-registral.txt
cat outputs/03_santa-cruz_offrecord.md
```

Pick any line of the output, take its citation, and open it yourself:

```bash
sed -n '19,25p' fixtures/03_santa-cruz_offrecord/escritura-extracto.txt
```

That is the whole mechanism. `_verify/` runs that check across every line so you
do not have to, but you can always do it by hand.

## 3. Convert your own parcel

Make a folder with one parcel's documents as plain text. Use these names:

| File | What it is | Required |
|---|---|---|
| `informe-registral.txt` | the registry printout for the parcel | yes |
| `plano-catastrado.txt` | the inscribed survey plan | no |
| `resolucion-aguas.txt` | the water concession resolution | no |
| `escritura-extracto.txt` | the deed extract | no |

From a PDF:

```bash
pdftotext -layout informe-registral.pdf informe-registral.txt
```

Keep `-layout`. The registry printout is a table, and without it the columns
collapse and the line numbers stop meaning anything.

Then, with this folder loaded as a Claude project or given to any agent:

> Convert `<your folder>/` to a Parcel Record. Write it to `outputs/<name>.md`.

Then `make verify` again.

## What you get back

Eleven sections, always all eleven, in the same order every time. Values carry
`[document:line]`. Values the documents did not answer read `not in source` and
are listed again in section 10. Values two documents answer differently go in
section 9 with both spellings and no winner. Anything the schema had no field
for is quoted in section 11.

## What to look at first

**Section 8.** It holds obligations that bind the land and do not appear in the
registry. On the third example it holds a fifteen-year agricultural lease over
the whole parcel, plus the tenant's option to buy it, neither of which was ever
filed at the Registry.

A registry report that shows no charges is not proof that land comes free of
obligations. Section 8 is where that gets said out loud, and when no deed was
supplied it says `NOT ASSESSED` rather than `none`.

## If it will not run

| | |
|---|---|
| `no such document` | a citation names a file that is not in the input folder. Check the filenames in the table above. |
| `field X cites [doc:N] but [...] is not on those lines` | the text moved. If you edited a fixture in the middle, the line numbers shifted. Add at the end, never the middle. |
| `not one of the three allowed derivations` | a computed value that reference/derivations.md does not allow. It has to become `not in source`. |
| `a denylisted identifier` | something listed in your local `_verify/denylist.local.txt` reached the repo or its history. The format is in `_verify/denylist.example.txt`. |
