# What each field means

One line per field, in the order of [`fields.tsv`](fields.tsv). Where a field is
routinely misread, the misreading is named, because that is the one that ends up
in the output.

## 1. Identity

| Field | Definition |
|---|---|
| `matricula` | The registry's own identifier for this parcel, as printed, including the derecho suffix. Not the same as the finca number alone. |
| `provincia` | The province named in the report. The leading digit of the finca number encodes it; the field takes the printed word, not the digit. |
| `canton` | The canton, as printed, with its number. Not derivable from the finca number. |
| `distrito` | The district, as printed, with its number. |
| `naturaleza` | What the registry says the land is. A legal classification, not a survey of what grows there. |
| `identificador_predial` | The cadastral identifier. Encodes province, canton, district and finca; it is copied, never assembled. |
| `zona_catastrada` | Whether the parcel sits in a surveyed zone, as the full printed sentence. Affects whether a survey plan can exist. |
| `emitido_el` | When the report was produced. **The whole record is a snapshot of this moment.** Nothing in it is evidence about today. |

## 2. Extent

| Field | Definition |
|---|---|
| `medida_literal` | The registered area exactly as the registry writes it, in words. |
| `medida_m2` | The same figure in digits, by derivation D1. Marked derived, never presented as printed. |
| `medida_ha` | Hectares, by derivation D2. Four decimals, no rounding. |
| `plano_catastrado` | The survey plan number the registry associates with the parcel, or `NO HAY` if the registry says there is none. |
| `plano_area_m2` | The area printed on the survey plan itself. **A different measurement from `medida_m2`.** Never copied from it, and the two disagreeing is a finding, not an error. |
| `lindero_norte/sur/este/oeste` | The boundary description for each side, verbatim. These name neighbours and features. Where a length appears it is part of the printed text; a length that does not appear is not inferred. |

## 3. Holder

| Field | Definition |
|---|---|
| `propietario` | The registered proprietor, spelled as the report spells it. |
| `propietario_id` | Their register number. `3-101-NNNNNN` is a corporation. |
| `propietario_capacidad` | The capacity in which they hold: owner, trustee, usufructuary. **`EN CALIDAD DE FIDUCIARIO` means the registered owner holds for someone else**, which is a different fact from owning. |
| `estimacion_o_precio` | The value declared in the instrument that registered the transfer. A tax and fee figure, not a market price and not what anyone paid. |
| `valor_fiscal` | The registry's fiscal value. Also not a market price. |
| `presentacion` | The filing reference of the instrument that produced this registration. |
| `fecha_inscripcion` | When that instrument was registered. |

## 4. Chain of title

| Field | Definition |
|---|---|
| `antecedentes` | The fincas this one came from, one entry each. Two entries means this parcel is a joining of two. |
| `segregaciones` | Whether parts have been split off. `SI HAY` means the parcel today is smaller than its history suggests. |
| `localizaciones_folio_real` | Localisations recorded since 1994, as printed. |

## 5. Charges on the record

| Field | Definition |
|---|---|
| `gravamenes_o_afectaciones` | The registry's own yes/no, verbatim. |
| `gravamen` | One block per charge, in the order printed. Sub-fields are whatever the block carries: `tipo`, `citas`, `inicia_el`, `afecta_a_finca`, and for easements `monto`, `longitud`, `ancho`, `rumbo`, `a_favor_de`, `en_contra_de`. A block carrying a field the schema has not named is reported anyway and the field name is taken from the document. |

`RESERVAS LEY AGUAS`, `LEY CAMINOS` and `LEY FORESTAL` are statutory reserves
that sit on a great deal of Costa Rican land. They are charges and are reported
as charges. `MONTO` on an easement is the instrument's nominal valuation of that
easement, not a debt.

## 6. Pending entries

| Field | Definition |
|---|---|
| `anotaciones_sobre_la_finca` | Whether filings are pending against the parcel, verbatim. `SI HAY` means something is in process that the ownership and charge sections do not yet reflect. |

## 7. Water

| Field | Definition |
|---|---|
| `resolucion` | The resolution number granting the concession. |
| `expediente` | The file number. `-A` marks surface water. |
| `concesionario` | Who the concession runs **to**. A concession is granted to a party, not attached to the land, so this need not be the owner. |
| `concesionario_id` | Their register number. |
| `fuente` | The water source, as named. |
| `punto_toma_hoja` / `_cuenca` | The cartographic sheet and basin number of the intake point. |
| `punto_toma_latitud` / `_longitud` | The intake coordinates as printed, in the projection the resolution uses. Not converted. |
| `caudal_asignado_ls` | Litres per second **granted**, which is routinely less than was requested. The requested figure is not this field. |
| `usos_autorizados` | The authorised uses. A concession for one use does not authorise another. |
| `periodo_de_uso` | Hours per day and months per year, as printed. A grant of 0.35 l/s for 6 months is not a year-round grant. |
| `plazo_literal` | The term, in the resolution's own words. |
| `fecha_resolucion` | The resolution's date, as printed, usually in words. |
| `vencimiento` | Expiry, by derivation D3. Refused unless the term is a whole number of years. |
| `obra_calibradora` | The calibrating works condition, if imposed. Non-compliance is generally grounds for cancellation, which the resolution states in its own words. |
| `inmueble_asociado` | The property the concession names. **Compare it to `matricula`.** If they differ, the concession is about another parcel. |

## 8. Off-record obligations

| Field | Definition |
|---|---|
| `obligation` | What the land is bound to, in a sentence. |
| `quote` | The clause's own words, verbatim. |
| `why_off_record` | What the document itself says about why this does not appear in the registry, verbatim. A deed may state it plainly (`no fue presentado al Registro`). Where the document says nothing about it, the field is `not in source`. |
| `amount` | As printed, in the document's own words and currency. |
| `beneficiary` | Who the obligation runs to. |
| `appears_in_registry` | `no` only after looking at section 5 and finding nothing matching. `unknown` when there is no registry report to look in. Never inferred. |

## 9. Conflicts

| Field | Definition |
|---|---|
| `field` | The field key the documents disagree about. |
| `value_a`, `value_b`, `value_c` | Each document's answer, spelled as that document spelled it, each with its citation. No winner, no merge, no note on which is more likely. |

## 10. Not in source

Every field key that reads `not in source`, listed together. This is the
work order: the documents still to obtain.

## 11. Unmapped

| Field | Definition |
|---|---|
| `quote` | The input line no field accepted, verbatim. |
| `source` | Its citation. |
| `why_no_field` | Which section would have taken it and what the schema is missing. This is how the schema gets corrected. |
