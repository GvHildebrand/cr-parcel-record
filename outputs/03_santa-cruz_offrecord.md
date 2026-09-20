# Parcel Record: finca 5-162094-000

Input: `fixtures/03_santa-cruz_offrecord/`
Documents read: `informe-registral`, `plano-catastrado`, `resolucion-aguas`, `escritura-extracto`

## 1. Identity

- **matricula**: 162094---000  `[informe-registral:4]`
- **provincia**: GUANACASTE  `[informe-registral:6]`
- **canton**: 3-SANTA CRUZ  `[informe-registral:9]`
- **distrito**: 6-TEMPATE  `[informe-registral:9]`
- **naturaleza**: TERRENO DE CULTIVO Y CHARRAL  `[informe-registral:8]`
- **identificador_predial**: 503060162094__  `[informe-registral:21]`
- **zona_catastrada**: FINCA SE ENCUENTRA EN ZONA CATASTRADA  `[informe-registral:11]`
- **emitido_el**: 12-09-2026 a las 11:18 horas  `[informe-registral:57]`

## 2. Extent

- **medida_literal**: CIENTO DIECINUEVE MIL SETECIENTOS SESENTA METROS CUADRADOS  `[informe-registral:18]`
- **medida_m2**: 119760  `derived: CIENTO DIECINUEVE MIL SETECIENTOS SESENTA = 119760` from `[informe-registral:18]`
- **medida_ha**: 11.9760  `derived: 119760 m2 / 10000 = 11.9760 ha` from `[informe-registral:18]`
- **plano_catastrado**: G-0987441-2023  `[informe-registral:19]`
- **plano_area_m2**: 118,430.00 M2  `[plano-catastrado:11]`  (conflict, see section 9)
- **lindero_norte**: INVERSIONES PALO VERDE S.A. Y QUEBRADA LAJAS  `[informe-registral:13]`
- **lindero_sur**: CALLE PUBLICA Y DESARROLLOS BAHIA POTRERO S.A.  `[informe-registral:14]`
- **lindero_este**: DESARROLLOS BAHIA POTRERO S.A.  `[informe-registral:15]`
- **lindero_oeste**: QUEBRADA LAJAS Y FINCA AGRICOLA EL GUAPINOL S.A.  `[informe-registral:16]`

## 3. Holder

- **propietario**: conflict, see section 9
- **propietario_id**: 3-101-661027  `[informe-registral:31]`
- **propietario_capacidad**: EN CALIDAD DE DUEÑO  `[informe-registral:31]`
- **estimacion_o_precio**: TREINTA Y OCHO MILLONES DE COLONES  `[informe-registral:32]`
- **valor_fiscal**: 62,904,150.00 COLONES  `[informe-registral:27]`
- **presentacion**: 2019-00281446-01  `[informe-registral:35]`
- **fecha_inscripcion**: 14-MAY-2019  `[informe-registral:36]`

## 4. Chain of title

- **antecedentes**: 5-00098412 000   FOLIO REAL  `[informe-registral:25]`
- **segregaciones**: NO HAY  `[informe-registral:7]`
- **localizaciones_folio_real**: NO HAY  `[informe-registral:20]`

## 5. Charges on the record

- **gravamenes_o_afectaciones**: SI HAY  `[informe-registral:39]`

### gravamen 1
- **tipo**: RESERVAS LEY AGUAS  `[informe-registral:42]`
- **citas**: 341-08877-01-0433-001  `[informe-registral:43]`
- **inicia_el**: 04-JUN-1981  `[informe-registral:44]`
- **afecta_a_finca**: 5-00162094 -000  `[informe-registral:45]`
- **cancelaciones_parciales**: NO HAY  `[informe-registral:46]`
- **anotaciones_del_gravamen**: NO HAY  `[informe-registral:47]`

### gravamen 2
- **tipo**: RESERVAS LEY FORESTAL  `[informe-registral:49]`
- **citas**: 341-08877-01-0434-001  `[informe-registral:50]`
- **inicia_el**: 04-JUN-1981  `[informe-registral:51]`
- **afecta_a_finca**: 5-00162094 -000  `[informe-registral:52]`
- **cancelaciones_parciales**: NO HAY  `[informe-registral:53]`
- **anotaciones_del_gravamen**: NO HAY  `[informe-registral:54]`

No mortgage, no easement and no other security for a debt is printed. The two
blocks above are statutory reserves.

## 6. Pending entries

- **anotaciones_sobre_la_finca**: NO HAY  `[informe-registral:38]`

## 7. Water

The water document in this input names a different finca from the one this
record describes. Its fields are reported because the document is in the input;
whether it says anything about finca 5-162094-000 is answered in section 9.

- **resolucion**: R-1903-2025-AGUAS-MINAE  `[resolucion-aguas:3]`
- **expediente**: 22071-A  `[resolucion-aguas:5]`
- **concesionario**: DESARROLLOS BAHIA POTRERO SOCIEDAD ANONIMA  `[resolucion-aguas:24]`
- **concesionario_id**: 3-101-502774  `[resolucion-aguas:25]`
- **fuente**: Quebrada Lajas  `[resolucion-aguas:35-37]`
- **punto_toma_hoja**: Belen  `[resolucion-aguas:31]`
- **punto_toma_cuenca**: 62-05  `[resolucion-aguas:30]`
- **punto_toma_latitud**: 263.880  `[resolucion-aguas:36]`
- **punto_toma_longitud**: 347.114  `[resolucion-aguas:36]`
- **caudal_asignado_ls**: 0.18  `[resolucion-aguas:36]`
- **usos_autorizados**: Abrevadero  `[resolucion-aguas:36]`
- **periodo_de_uso**: 16 horas diarias, 9 meses al año.  `[resolucion-aguas:39]`
- **plazo_literal**: QUINCE AÑOS  `[resolucion-aguas:26]`
- **fecha_resolucion**: diecisiete de octubre del dos mil veinticinco  `[resolucion-aguas:7-8]`
- **vencimiento**: 17-OCT-2040  `derived: diecisiete de octubre del dos mil veinticinco = 17-OCT-2025; 17-OCT-2025 + 15 years = 17-OCT-2040` from `[resolucion-aguas:7-8]` and `[resolucion-aguas:26]`
- **obra_calibradora**: not in source
- **inmueble_asociado**: 5-162093-000  `[resolucion-aguas:15]`

## 8. Off-record obligations

### off_record_obligation 1
- **obligation**: The whole parcel is under an agricultural lease that the buyer takes over.
- **quote**: "La compradora acepta y se subroga en el contrato de arrendamiento agrícola suscrito el primero de marzo del dos mil veintiuno entre la vendedora y GANADERIA HERMANOS ZUÑIGA SOCIEDAD ANONIMA, cédula jurídica 3-101-388901, por un plazo de QUINCE AÑOS, sobre la totalidad de la finca, por una renta anual de OCHO MIL DOLARES"
- **source**: `[escritura-extracto:19-23]`
- **why_off_record**: Dicho contrato no fue presentado al Registro y no consta en el informe registral  `[escritura-extracto:24-25]`
- **amount**: OCHO MIL DOLARES  `[escritura-extracto:23]`
- **beneficiary**: GANADERIA HERMANOS ZUÑIGA SOCIEDAD ANONIMA  `[escritura-extracto:21]`
- **appears_in_registry**: no. Section 5 lists two statutory reserves and no lease.

### off_record_obligation 2
- **obligation**: The tenant holds an option to buy the parcel.
- **quote**: "El contrato de arrendamiento citado en la cláusula anterior otorga al arrendatario una opción de compra sobre la finca, ejercitable durante los últimos doce meses del plazo, por un precio de CUATROCIENTOS VEINTE MIL DOLARES."
- **source**: `[escritura-extracto:27-31]`
- **why_off_record**: not in source
- **amount**: CUATROCIENTOS VEINTE MIL DOLARES  `[escritura-extracto:30]`
- **beneficiary**: el arrendatario  `[escritura-extracto:27-28]`
- **appears_in_registry**: no. No such option is printed in section 5 or section 6.

## 9. Conflicts between sources

### conflict 1
- **field**: propietario
- **value_a**: INVERSIONES PALO VERDE SOCIEDAD ANONIMA  `[informe-registral:30]`
- **value_b**: INVERSIONES PALO VERDE S.A.  `[plano-catastrado:16]`
- **value_c**: Inversiones Palo Verde S.A.  `[escritura-extracto:7]`

### conflict 2
- **field**: area
- **value_a**: CIENTO DIECINUEVE MIL SETECIENTOS SESENTA METROS CUADRADOS  `[informe-registral:18]`
- **value_b**: 118,430.00 M2  `[plano-catastrado:11]`
- **value_c**: ciento diecinueve mil setecientos sesenta metros cuadrados  `[escritura-extracto:16-17]`

The registry and the deed print the same figure. The inscribed survey prints a
different one. No arithmetic is performed on the difference.

### conflict 3
- **field**: inmueble_asociado
- **value_a**: 162094---000  `[informe-registral:4]`
- **value_b**: 5-162093-000  `[resolucion-aguas:15]`

The matrícula this record describes and the finca the concession was granted on
are not the same finca.

### conflict 4
- **field**: concesionario
- **value_a**: INVERSIONES PALO VERDE SOCIEDAD ANONIMA  `[informe-registral:30]`
- **value_b**: DESARROLLOS BAHIA POTRERO SOCIEDAD ANONIMA  `[resolucion-aguas:24]`

The registered owner and the party the concession runs to are not the same
party.

## 10. Not in source

- obra_calibradora
- why_off_record (off_record_obligation 2)

## 11. Unmapped

- **quote**: "SEXTO: La vendedora manifiesta que sobre la finca no pesa hipoteca alguna inscrita, lo cual consta en el informe registral adjunto."
  **source**: `[escritura-extracto:36-37]`
  **why_no_field**: a declaration by a party, not a registry fact. No section takes it.

- **quote**: "AGROPECUARIA LAS LAJAS SOCIEDAD ANONIMA, cédula jurídica 3-101-704512, en calidad de compradora."
  **source**: `[escritura-extracto:10-11]`
  **why_no_field**: section 3 records the registered holder as the registry prints it. The schema has no field for a buyer under an instrument not yet reflected in the registry, so a reader cannot see that a transfer is in flight.

- **quote**: "QUINTO: El precio de la venta es de CUARENTA Y DOS MILLONES DE COLONES"
  **source**: `[escritura-extracto:33]`
  **why_no_field**: section 3 carries the price declared in the instrument the registry already holds. The schema has no field for the price in a deed the registry has not yet seen.

- **quote**: "PROTOCOLO TOMO 19 FOLIO 42 FRENTE"
  **source**: `[escritura-extracto:2]`
  **why_no_field**: the deed's place in the notary's protocol. Section 4 records the finca the parcel came from but has no field for the instrument.

- **quote**: "Otorgada ante la notaria pública Licda. A. Rojas Peralta, carné 21884"
  **source**: `[escritura-extracto:4]`
  **why_no_field**: no field for the authorising notary.

- **quote**: "SETIMO: La compradora declara haber inspeccionado la finca y conocer su estado de ocupación actual."
  **source**: `[escritura-extracto:39-40]`
  **why_no_field**: a declaration by a party. Section 8 records obligations the deed states, not what a party says they knew.

- **quote**: "ESCALA: 1:1500"
  **source**: `[plano-catastrado:12]`
  **why_no_field**: no field for the plan's scale.

- **quote**: "FECHA DE LEVANTAMIENTO: SETIEMBRE 2023"
  **source**: `[plano-catastrado:13]`
  **why_no_field**: no field for when the survey was carried out.

- **quote**: "SEGUNDO: Que el edicto ED-0774-2025 fue publicado en el Diario Oficial La Gaceta número 191"
  **source**: `[resolucion-aguas:17-18]`
  **why_no_field**: section 7 has no field for the edict or for whether oppositions were filed.
