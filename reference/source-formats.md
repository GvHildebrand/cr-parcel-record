# The four documents, and what each one can answer

Ask a document for something it does not carry and the answer will be invented.
This page says what each input is and where its fields sit, so the mapping in
[`../rules.md`](../rules.md) can be mechanical.

---

## `informe-registral`: Registro Nacional, CONSULTA POR NÚMERO DE FINCA

The registry's own printout for one finca. **The only required input.**

Field labels appear in capitals at the start of a line, and the value follows on
the same line or the lines beneath:

```
MATRÍCULA:                                    PROVINCIA: ... FINCA: ... DERECHO: ...
SEGREGACIONES:                                NATURALEZA:
SITUADA EN EL DISTRITO ... CANTON ... DE LA PROVINCIA DE ...
FINCA SE ENCUENTRA EN ZONA CATASTRADA         LINDEROS: NORTE / SUR / ESTE / OESTE
MIDE:                                         PLANO:
IDENTIFICADOR PREDIAL:                        ANTECEDENTES DOMINIO DE LA FINCA:
VALOR FISCAL:                                 PROPIETARIO:
CEDULA JURIDICA ... EN CALIDAD DE ...          ESTIMACIÓN O PRECIO:
PRESENTACIÓN:                                 FECHA DE INSCRIPCIÓN:
ANOTACIONES SOBRE LA FINCA:                   GRAVAMENES o AFECTACIONES:
```

Each gravamen is a block: a type in capitals, then `CITAS:`, `INICIA EL:`,
`AFECTA A FINCA:`, `CANCELACIONES PARCIALES:`, `ANOTACIONES DEL GRAVAMEN:`, and
for easements also `MONTO:`, `LONGITUD:`, `ANCHO:`, `RUMBO:` and the
`A FAVOR DE` / `EN CONTRA DE` pair.

**What it cannot answer:** anything agreed in a deed that was never presented
to the Registry, the survey area, water rights, or whether any of it is still true today.
It carries `Emitido el <date>` and is a snapshot of that moment.

## `plano-catastrado`: the inscribed survey plan

Carries the plan number `X-NNNNNNN-YYYY`, the surveyed area in digits, the
scale, the surveyor and the inscription date.

**Why it matters:** the surveyed area and the registered area are two different
measurements of the same ground and they disagree more often than not. The gap
is a finding. Section 2 holds both; neither is ever copied into the other.

## `resolucion-aguas`: Dirección de Agua concession resolution

Structured `RESULTANDO` / `CONSIDERANDO` / `POR TANTO` / `RESUELVE`. The grant
is in `RESUELVE` paragraph I, with a table carrying the source, the intake
coordinates with the cartographic sheet and basin number, the authorised uses
and the assigned flow in litres per second. The term is in the sentence above
the table. Conditions follow as numbered paragraphs.

**Two traps.** The concession is granted to a **holder**, for a **named
property**, and neither necessarily matches the finca in the registry report;
section 9 catches the mismatch. And a procedural ruling issued on the way to a
decision, such as an admissibility study (*estudio de admisibilidad*), is not a
grant, however much its filename suggests one. Only a resolution whose
`RESUELVE` says `OTORGAR` is a concession.

## `escritura-extracto`: deed extract

Optional, and the reason section 8 exists. A deed can carry obligations that
the registry never prints: a lease the parties never presented to it, an option
to buy, a reserved right of use. Read every clause for an obligation that
survives the transfer, and put each one in section 8 with its verbatim quote.
