# Parcel Record: finca 5-097553-000

Input: `fixtures/02_nicoya_sparse/`
Documents read: `informe-registral`

## 1. Identity

- **matricula**: 097553---000  `[informe-registral:4]`
- **provincia**: GUANACASTE  `[informe-registral:6]`
- **canton**: 2-NICOYA  `[informe-registral:9]`
- **distrito**: 3-MANSION  `[informe-registral:9]`
- **naturaleza**: TERRENO DE AGRICULTURA  `[informe-registral:8]`
- **identificador_predial**: 502030097553__  `[informe-registral:21]`
- **zona_catastrada**: FINCA NO SE ENCUENTRA EN ZONA CATASTRADA  `[informe-registral:11]`
- **emitido_el**: 12-09-2026 a las 10:07 horas  `[informe-registral:48]`

## 2. Extent

- **medida_literal**: OCHENTA Y CUATRO MIL SEISCIENTOS VEINTE METROS CUADRADOS  `[informe-registral:18]`
- **medida_m2**: 84620  `derived: OCHENTA Y CUATRO MIL SEISCIENTOS VEINTE = 84620` from `[informe-registral:18]`
- **medida_ha**: 8.4620  `derived: 84620 m2 / 10000 = 8.4620 ha` from `[informe-registral:18]`
- **plano_catastrado**: NO HAY  `[informe-registral:19]`
- **plano_area_m2**: not in source
- **lindero_norte**: SUCESION DE J. VALVERDE  `[informe-registral:13]`
- **lindero_sur**: CAMINO PUBLICO  `[informe-registral:14]`
- **lindero_este**: RIO MORACIA  `[informe-registral:15]`
- **lindero_oeste**: RESTO RESERVADO  `[informe-registral:16]`

## 3. Holder

- **propietario**: AGROPECUARIA TEMPISQUE SECO SOCIEDAD ANONIMA  `[informe-registral:30]`
- **propietario_id**: 3-101-209884  `[informe-registral:31]`
- **propietario_capacidad**: EN CALIDAD DE DUEÑO  `[informe-registral:31]`
- **estimacion_o_precio**: TRES MILLONES DE COLONES  `[informe-registral:32]`
- **valor_fiscal**: 9,842,000.00 COLONES  `[informe-registral:27]`
- **presentacion**: 1996-00118340-01  `[informe-registral:35]`
- **fecha_inscripcion**: 14-NOV-1996  `[informe-registral:36]`

## 4. Chain of title

- **antecedentes**: 5-00041226 000   FOLIO REAL  `[informe-registral:25]`
- **segregaciones**: SI HAY  `[informe-registral:7]`
- **localizaciones_folio_real**: NO HAY  `[informe-registral:20]`

## 5. Charges on the record

- **gravamenes_o_afectaciones**: NO HAY  `[informe-registral:45]`

No gravamen blocks are printed. That is what the registry states. What a
registry report cannot cover is in section 8.

## 6. Pending entries

- **anotaciones_sobre_la_finca**: SI HAY  `[informe-registral:38]`

### anotacion 1
- **anotacion_citas**: 2026-00551903-01  `[informe-registral:40]`
- **presentado_el**: 03-AGO-2026  `[informe-registral:41]`
- **naturaleza_del_documento**: INFORMACION POSESORIA  `[informe-registral:42]`
- **estado**: EN PROCESO  `[informe-registral:43]`

## 7. Water

no water document in input.

- **resolucion**: not in source
- **expediente**: not in source
- **concesionario**: not in source
- **concesionario_id**: not in source
- **fuente**: not in source
- **punto_toma_hoja**: not in source
- **punto_toma_cuenca**: not in source
- **punto_toma_latitud**: not in source
- **punto_toma_longitud**: not in source
- **caudal_asignado_ls**: not in source
- **usos_autorizados**: not in source
- **periodo_de_uso**: not in source
- **plazo_literal**: not in source
- **fecha_resolucion**: not in source
- **vencimiento**: not in source
- **obra_calibradora**: not in source
- **inmueble_asociado**: not in source

## 8. Off-record obligations

**NOT ASSESSED.** No deed extract was supplied. A registry report cannot show
an obligation filed outside it, so the silence of sections 5 and 6 is not
evidence that none exists. To assess this section, supply `escritura-extracto`.

## 9. Conflicts between sources

none. Only one document was supplied, so no field has two answers.

## 10. Not in source

- plano_area_m2
- resolucion
- expediente
- concesionario
- concesionario_id
- fuente
- punto_toma_hoja
- punto_toma_cuenca
- punto_toma_latitud
- punto_toma_longitud
- caudal_asignado_ls
- usos_autorizados
- periodo_de_uso
- plazo_literal
- fecha_resolucion
- vencimiento
- obra_calibradora
- inmueble_asociado

## 11. Unmapped

none

Section 11 of this record used to carry four lines: the pending filing's
citation, its date, its document type and its state. The schema had no fields
for them and said so. The schema was then extended with the `anotacion` block
above, and they have fields. That is what section 11 is for.
