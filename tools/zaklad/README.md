# tools/zaklad — generátor stránky „Základní údaje & výpočty"

Deterministicky generuje `investori-zaklad.html` z dat extrahovaných z
`Záměr VPD1_5.xlsx` (list **Základní údaje & výpočty**). Čísla jdou přímo z
gridu → žádný ruční přepis.

## Regenerace HTML (z již extrahovaných dat)
```bash
python3 tools/zaklad/build_zaklad.py     # data/*.json -> data/body.html
python3 tools/zaklad/assemble.py         # data/body.html -> ../../investori-zaklad.html
npm run build                            # pokud přibyla Tailwind třída
```
Úpravy obsahu/struktury/nadpisů → edituj `build_zaklad.py` (specifikace tabulek)
nebo inline `.vz` styly v `assemble.py`. Pak spusť oba skripty.

## Re-extrakce z xlsx (když se změní Excel)
Vyžaduje `openpyxl`. Nastav cestu k sešitu a spusť:
```bash
SCRATCH=tools/zaklad/data python3 tools/zaklad/dump_zaklad.py    # hodnoty+fills+merge -> zaklad_dump.json
SCRATCH=tools/zaklad/data python3 tools/zaklad/extract_fmt.py    # česky formátované hodnoty -> grid_fmt.json
```
(oba čtou `Záměr VPD1_5.xlsx` z aktuálního adresáře — spouštěj z místa, kde sešit je,
nebo uprav cestu ve skriptu).

## Soubory
- `data/grid_fmt.json` — formátované hodnoty buněk (zdroj čísel pro HTML)
- `data/zaklad_dump.json` — hodnoty + fill barvy + bold + merge
- `build_zaklad.py` — specifikace sekcí/tabulek → `data/body.html`
- `assemble.py` — shell (brána, topbar, inline `.vz` CSS) + body → finální HTML
- `dump_zaklad.py`, `extract_fmt.py` — extraktory z xlsx
