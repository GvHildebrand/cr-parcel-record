#!/usr/bin/env python3
"""Break the outputs on purpose and confirm each check catches it.

A verifier that has never failed is a verifier nobody has tested. Each case
below copies the repo to a temporary directory, injects one fault, and asserts
that the named script exits non-zero. If a case passes clean, the check is
asleep and this script fails the build.

The copy uses _verify/denylist.example.txt as its local denylist, so the
public-safety cases behave the same on every machine, whether or not a real
local denylist exists.
"""
import subprocess, sys, tempfile, shutil, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

CASES = [
 ("verify_citations.py", "an invented flow rate",
  "outputs/01_liberia_complete.md",
  "- **caudal_asignado_ls**: 0.35", "- **caudal_asignado_ls**: 0.95"),

 ("verify_citations.py", "a citation pointing at the wrong line",
  "outputs/01_liberia_complete.md",
  "- **matricula**: 141882---000  `[informe-registral:4]`",
  "- **matricula**: 141882---000  `[informe-registral:8]`"),

 ("verify_citations.py", "a citation pointing past the end of the file",
  "outputs/02_nicoya_sparse.md",
  "`[informe-registral:48]`", "`[informe-registral:9999]`"),

 ("verify_citations.py", "an owner name normalised to how it is usually spelled",
  "outputs/03_santa-cruz_offrecord.md",
  "- **value_a**: INVERSIONES PALO VERDE SOCIEDAD ANONIMA  `[informe-registral:30]`",
  "- **value_a**: Inversiones Palo Verde S.A.  `[informe-registral:30]`"),

 ("verify_shape.py", "a dropped section",
  "outputs/02_nicoya_sparse.md",
  "## 9. Conflicts between sources", "### 9. Conflicts between sources"),

 ("verify_shape.py", "a field reported twice",
  "outputs/01_liberia_complete.md",
  "- **valor_fiscal**: 47,310,400.00 COLONES  `[informe-registral:27]`",
  "- **valor_fiscal**: 47,310,400.00 COLONES  `[informe-registral:27]`\n"
  "- **valor_fiscal**: 47,310,400.00 COLONES  `[informe-registral:27]`"),

 ("verify_derivations.py", "hectares computed wrongly",
  "outputs/01_liberia_complete.md",
  "`derived: 243860 m2 / 10000 = 24.3860 ha`",
  "`derived: 243860 m2 / 10000 = 2.4386 ha`"),

 ("verify_derivations.py", "a term read as longer than the document says",
  "outputs/01_liberia_complete.md",
  "11-FEB-2026 + 10 years = 11-FEB-2036",
  "11-FEB-2026 + 10 years = 11-FEB-2046"),

 ("verify_derivations.py", "a number phrase that is not what the document printed",
  "outputs/02_nicoya_sparse.md",
  "`derived: OCHENTA Y CUATRO MIL SEISCIENTOS VEINTE = 84620`",
  "`derived: NOVENTA Y CUATRO MIL SEISCIENTOS VEINTE = 94620`"),

 ("verify_derivations.py", "a fourth kind of derivation",
  "outputs/01_liberia_complete.md",
  "- **medida_ha**: 24.3860  `derived: 243860 m2 / 10000 = 24.3860 ha`",
  "- **medida_ha**: 24.3860  `derived: comparable parcels in Liberia average 24 ha`"),

 ("verify_no_judgement.py", "a verdict about the land",
  "outputs/02_nicoya_sparse.md",
  "No gravamen blocks are printed. That is what the registry states.",
  "No gravamen blocks are printed. The title is clean title and marketable."),

 ("verify_no_judgement.py", "a claim from outside the documents",
  "outputs/01_liberia_complete.md",
  "- **naturaleza**: TERRENO DE PASTO Y BOSQUE SECUNDARIO  `[informe-registral:8]`",
  "- **naturaleza**: TERRENO DE PASTO Y BOSQUE SECUNDARIO\n\nParcels in this district are typically held by corporations."),

 ("verify_shape.py", "a field key the contract does not name",
  "outputs/01_liberia_complete.md",
  "- **valor_fiscal**: 47,310,400.00 COLONES  `[informe-registral:27]`",
  "- **valor_fiscal**: 47,310,400.00 COLONES  `[informe-registral:27]`\n"
  "- **market_value_usd**: 92,000  `[informe-registral:27]`"),

 ("scan_public_safety.py", "a fixture carrying a refused structural shape",
  "fixtures/03_santa-cruz_offrecord/escritura-extracto.txt",
  "TERCERO - ARRENDAMIENTO AGRICOLA VIGENTE:",
  "CLAUSULA CENTINELA DE ESTRUCTURA\n\nTERCERO - ARRENDAMIENTO AGRICOLA VIGENTE:"),

 ("scan_public_safety.py", "a folio from the wrong province",
  "outputs/01_liberia_complete.md",
  "- **matricula**: 141882---000", "- **matricula**: 7-00731508-000"),

 ("scan_public_safety.py", "a denylisted identifier",
  "outputs/01_liberia_complete.md",
  "- **naturaleza**: TERRENO DE PASTO Y BOSQUE SECUNDARIO",
  "- **naturaleza**: quetzalcoatlus sentinel phrase"),
]

def run(script, cwd):
    return subprocess.run([sys.executable, f"_verify/{script}"],
                          cwd=cwd, capture_output=True, text=True)

def main():
    # every check must pass on the real repo first
    clean = []
    for script in sorted({c[0] for c in CASES}):
        r = run(script, ROOT)
        if r.returncode != 0:
            clean.append(f"{script} fails on the unmodified repo:\n{r.stdout}{r.stderr}")
    if clean:
        print("FAIL  self-test")
        for c in clean: print("   ", c)
        return 1

    asleep = []
    for script, name, relpath, old, new in CASES:
        with tempfile.TemporaryDirectory() as tmp:
            work = pathlib.Path(tmp)/"repo"
            shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns(".git"))
            shutil.copy(work/"_verify"/"denylist.example.txt",
                        work/"_verify"/"denylist.local.txt")
            target = work/relpath
            text = target.read_text()
            if old not in text:
                asleep.append(f"{script}: case '{name}' could not be injected "
                              f"({relpath} no longer contains the anchor)")
                continue
            target.write_text(text.replace(old, new, 1))
            if run(script, work).returncode == 0:
                asleep.append(f"{script}: did NOT catch '{name}'")
    if asleep:
        print("FAIL  self-test")
        for a in asleep: print("   ", a)
        return 1
    print(f"ok    self-test    {len(CASES)} injected faults, every one caught")
    return 0

sys.exit(main())
