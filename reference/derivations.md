# The three derivations, and nothing else

A derived value is one the documents do not print but that follows from a value
they do print, by an operation with exactly one possible answer. Three
operations qualify. The list is closed. Anything not on it is invention, and
invention fails the run.

Every derived value in the output carries `derived: <the arithmetic>` and cites
the line it started from.

**Chaining.** Where one derivation feeds another, the steps go in one
`derived:` block separated by a semicolon, left to right, and the last step's
result is the field's value:

```
derived: once de febrero del dos mil veintiseis = 11-FEB-2026; 11-FEB-2026 + 10 years = 11-FEB-2036
```

Write the words without accents inside a `derived:` block. The phrase before the
first `=` must appear on the cited line, accents and all; the check folds them.

---

## D1: Spanish number and date words to digits

Costa Rican registry reports print the area in words, and resolutions print their
date in words. Both resolve the same way: one phrase, one possible reading.

```
MIDE: DOSCIENTOS CUARENTA Y TRES MIL OCHOCIENTOS SESENTA METROS CUADRADOS
```

`medida_literal` carries the words exactly as printed. `medida_m2` carries
`243860`, written as:

```
derived: DOSCIENTOS CUARENTA Y TRES MIL OCHOCIENTOS SESENTA = 243860
```

A date resolves identically:

```
derived: once de febrero del dos mil veintiseis = 11-FEB-2026
```

Reversible, deterministic, no new information. If any word in the phrase cannot
be resolved, the field is `not in source` and the phrase goes to section 11.

## D2: Square metres to hectares

```
derived: 243860 m2 / 10000 = 24.3860 ha
```

**Exactly four decimal places**, zero-padded, no rounding up, no "about 24 ha".
`24.386` is wrong where `24.3860` is right, and `verify_derivations.py` fails
on it. Runs only on a
`medida_m2` that D1 produced or that a document printed in digits.

## D3: Resolution date plus literal term to expiry date

Water concessions print the date and the term, never the expiry.

```
Resolution dated 11-FEB-2026, term "DIEZ AÑOS"
derived: 11-FEB-2026 + 10 years = 11-FEB-2036
```

Both inputs must appear verbatim in the document and both must be cited. If the
term is printed as a range, conditionally, or in any form other than a whole
number of years, `vencimiento` is `not in source` and the wording goes to
section 11.

---

## What is not a derivation

Each of these has a plausible-looking answer, and each would be a fabricated
fact. They are the ways this converter could lie.

| Tempting | Why it is invention |
|---|---|
| Total area across several fincas | The documents describe one parcel each. A total is a new claim about a set the registry never formed. |
| "Unencumbered", "clean title", "no liens" | A conclusion, not a field. Section 5 lists what the registry prints; a reader decides what it means. |
| Road frontage from the boundary text | `LINDEROS` names neighbours, not lengths. Any metre figure not printed is made up. |
| A cantón inferred from the finca number | Province is encoded in the number. Cantón is not. |
| Colones to dollars | Needs a rate the document does not carry, on a date the document does not state. |
| "Current owner" | The registry prints the owner **as of the emission date**. The report is a snapshot; the word "current" adds a claim about today. |
| Normalising `SOCIEDAD ANONIMA` to `S.A.` | A name spelled the way it usually is, instead of the way it appeared. Section 9 exists for this. |
| An expiry date from a term that is not whole years | D3 refuses it on purpose. |
| Filling `plano_area_m2` from `medida_m2` | The registry area and the survey area are different measurements, and the gap between them is the finding. Copying one into the other destroys it. |
