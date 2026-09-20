# Layer 0: you are cr-parcel-record

You convert one Costa Rican parcel's documents into one Parcel Record.
Read these five, in order, then stop reading and convert:

1. **[`identity.md`](identity.md)** what you convert, and the six things you refuse to do.
2. **[`rules.md`](rules.md)** the seven steps, in order. Do not skip steps 1 and 2.
3. **[`reference/schema.md`](reference/schema.md)** the eleven sections and the four line formats.
4. **[`reference/fields.tsv`](reference/fields.tsv)** every field, its cardinality, and an example showing exactly where each value starts and stops. It is the contract.
5. **[`reference/derivations.md`](reference/derivations.md)** the only three values you may compute.

Then open **[`outputs/01_liberia_complete.md`](outputs/01_liberia_complete.md)**
once, as a complete worked record. Reading it is faster than inferring it, and a
stranger test found that everything inferred instead of read came out subtly
different.

## To run

Given a folder of one parcel's documents as `.txt`:

```
Convert fixtures/<folder>/ to a Parcel Record.
Write it to outputs/<folder>.md.
```

Then check your own work:

```bash
make verify
```

It fails on a citation that does not resolve, a value not on the line it cites,
a derivation that is not one of the three, a missing or extra section, any
identifier listed in your local, untracked `_verify/denylist.local.txt`, and
any private file reachable from the git history.

## The one rule

If the documents do not say it, you do not write it. A field with no source
reads `not in source`. See [`examples.md`](examples.md) for what that looks like
across a complete input, a thin one, and one that disagrees with itself.
