#!/usr/bin/env python3
"""Spanish cardinals and dates, written out, to digits.

This is D1 from reference/derivations.md, implemented independently so the
derivation in an output can be checked rather than believed. It has no other
job and knows nothing about land.
"""
import re, unicodedata

UNITS = {
 "cero":0,"un":1,"uno":1,"una":1,"dos":2,"tres":3,"cuatro":4,"cinco":5,"seis":6,
 "siete":7,"ocho":8,"nueve":9,"diez":10,"once":11,"doce":12,"trece":13,
 "catorce":14,"quince":15,"dieciseis":16,"diecisiete":17,"dieciocho":18,
 "diecinueve":19,"veinte":20,"veintiuno":21,"veintidos":22,"veintitres":23,
 "veinticuatro":24,"veinticinco":25,"veintiseis":26,"veintisiete":27,
 "veintiocho":28,"veintinueve":29,"treinta":30,"cuarenta":40,"cincuenta":50,
 "sesenta":60,"setenta":70,"ochenta":80,"noventa":90,"cien":100,"ciento":100,
 "doscientos":200,"trescientos":300,"cuatrocientos":400,"quinientos":500,
 "seiscientos":600,"setecientos":700,"ochocientos":800,"novecientos":900,
}
MONTHS = {"enero":1,"febrero":2,"marzo":3,"abril":4,"mayo":5,"junio":6,
          "julio":7,"agosto":8,"setiembre":9,"septiembre":9,"octubre":10,
          "noviembre":11,"diciembre":12}
MON3 = {1:"ENE",2:"FEB",3:"MAR",4:"ABR",5:"MAY",6:"JUN",
        7:"JUL",8:"AGO",9:"SET",10:"OCT",11:"NOV",12:"DIC"}

def fold(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()

def to_int(phrase):
    """'ciento diecinueve mil setecientos sesenta' -> 119760. None if unreadable."""
    toks = [t for t in re.split(r"[^\wáéíóúñ]+", fold(phrase)) if t]
    toks = [t for t in toks if t not in ("y", "de", "metros", "cuadrados")]
    if not toks:
        return None
    total = cur = 0
    for t in toks:
        if t in UNITS:
            cur += UNITS[t]
        elif t == "mil":
            cur = (cur or 1) * 1000
            total += cur
            cur = 0
        elif t in ("millon", "millones"):
            cur = (cur or 1) * 1_000_000
            total += cur
            cur = 0
        else:
            return None
    return total + cur

def to_date(phrase):
    """'once de febrero del dos mil veintiseis' -> '11-FEB-2026'. None if unreadable."""
    f = fold(phrase)
    parts = re.split(r"\bde[l]?\b", f)
    parts = [p.strip() for p in parts if p.strip()]
    if len(parts) < 3:
        return None
    day, month, year = to_int(parts[0]), MONTHS.get(parts[1]), to_int(parts[2])
    if not day or not month or not year:
        return None
    return f"{day:02d}-{MON3[month]}-{year}"

if __name__ == "__main__":
    cases = [
        ("CIENTO SESENTA Y UN MIL CUATROCIENTOS NOVENTA Y SIETE", 161497),
        ("DOSCIENTOS CUARENTA Y TRES MIL OCHOCIENTOS SESENTA", 243860),
        ("OCHENTA Y CUATRO MIL SEISCIENTOS VEINTE", 84620),
        ("CIENTO DIECINUEVE MIL SETECIENTOS SESENTA", 119760),
        ("CUARENTA Y SIETE MIL TRESCIENTOS DIEZ", 47310),
    ]
    bad = 0
    for phrase, want in cases:
        got = to_int(phrase)
        ok = got == want
        bad += not ok
        print(("ok   " if ok else "FAIL "), phrase, "->", got, "" if ok else f"(want {want})")
    for phrase, want in [("once de febrero del dos mil veintiseis", "11-FEB-2026"),
                         ("diecisiete de octubre del dos mil veinticinco", "17-OCT-2025")]:
        got = to_date(phrase)
        ok = got == want
        bad += not ok
        print(("ok   " if ok else "FAIL "), phrase, "->", got, "" if ok else f"(want {want})")
    raise SystemExit(1 if bad else 0)
