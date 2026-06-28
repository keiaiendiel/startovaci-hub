# „Projekt Startovací hub" finále — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Doplnit na konec zóny „Projekt Startovací hub" v `investori-zaklad.html` 5 tabulek z xlsx (věrně, vč. červených čísel a konektorů místo Excel šipek) + výměnu 2 ortofoto map, opravu hover zvýraznění řádků a lightbox na obrázky.

**Architecture:** Stránka se generuje deterministicky z xlsx přes `tools/zaklad/` (extraktory → `build_zaklad.py` → `assemble.py` → `investori-zaklad.html`). Data jdou z gridu, žádný ruční přepis. Nové tabulky = další bloky v existující `zonesection`; konektor + lightbox = pár řádků JS v shellu (`assemble.py`).

**Tech Stack:** Python 3 + openpyxl (extrakce), čistý Python string-builder (generátor), HTML + inline CSS (`.vz` styly) + vanilla JS, Tailwind (build jen pojistka).

## Global Constraints

- Zdroj pravdy = generátor `tools/zaklad/`; čísla se NEpřepisují ručně, jdou z `grid_fmt.json`.
- Repo: `/Users/kindl/Work/_2026/02 OSA/11 WWW/startovaci-hub` (dále `REPO`). Sešit: `/Users/kindl/Work/_2026/02 OSA/Záměr VPD1_5.xlsx` (dále adresář `XLSXDIR`).
- Pořadí tabulek dle Excelu: #20 (BS–BV), #21 (BY–CC), #22 (CG–CM), #24 (CP–CR), #25 (CU–CZ). Vše roční řady = řádky 8–23 (2023–2038); #22 = budovy řádky 10–26. Souhrny řádek 39.
- Věrnost: `cellfills=True`, červená čísla = font color `…FF0000` → třída `is-red`, literál number-formatu se zachová (`" Kč [přípravná fáze]"`).
- Konektor = trvalá jemná linka + hover (zvýraznění poslední řádek + cílový box); skrytá < 820 px; bez JS graceful.
- Práce na větvi z `main`; bez `git push`. Commit messages končí:
  `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>` a `Claude-Session: …` (dle harnessu).
- Po jakékoli změně tříd v HTML/CSS spustit `npm run build` (pojistka; `.vz` styly jsou inline).
- Vypnuté sekce (`section_draft`: lůžka, Nová čtvrť, zdroje) zůstávají vypnuté. `investori-zamer.html` se v tomto plánu nemění.

---

### Task 1: Extraktory — font color + literál number-formatu, re-extrakce

**Files:**
- Modify: `REPO/tools/zaklad/dump_zaklad.py`
- Modify: `REPO/tools/zaklad/extract_fmt.py`
- Regenerate (output): `REPO/tools/zaklad/data/zaklad_dump.json`, `REPO/tools/zaklad/data/grid_fmt.json`, `grid.tsv`, `zaklad_images.json`

**Interfaces:**
- Produces: v `zaklad_dump.json` dostanou červené buňky klíč `"fc"` (rgb stringu končící `FF0000`). V `grid_fmt.json` nulové buňky s formátem `#,##0" Kč [přípravná fáze]"` mají hodnotu `"0 Kč [přípravná fáze]"`.

- [ ] **Step 1: dump_zaklad.py — zachytit červený font**

V `REPO/tools/zaklad/dump_zaklad.py`, uvnitř smyčky `for c in row:` (kde se počítá `bold`), za blok `try: bold=…` přidej:

```python
        fc=None
        try:
            col=c.font.color
            rgb=getattr(col,"rgb",None) if col is not None else None
            if isinstance(rgb,str) and rgb.upper().endswith("FF0000"):
                fc=rgb
        except: pass
```

A řádek, který přidává buňku do `cells`, změň z:

```python
        if v is not None or fill:
            cells.append({"c":c.coordinate,"row":c.row,"col":c.column,"v":(str(v) if v is not None else None),"f":fill,"b":bold})
```

na:

```python
        if v is not None or fill:
            d={"c":c.coordinate,"row":c.row,"col":c.column,"v":(str(v) if v is not None else None),"f":fill,"b":bold}
            if fc: d["fc"]=fc
            cells.append(d)
```

- [ ] **Step 2: extract_fmt.py — zachovat celý literál formátu**

V `REPO/tools/zaklad/extract_fmt.py` přidej pod `def decimals_from(fmt):` novou funkci:

```python
def literal_suffix(nf):
    # vrať celý kvótovaný literál, který obsahuje jednotku (Kč / m²)
    for lit in re.findall(r'"([^"]*)"', nf or ""):
        if "Kč" in lit or "m2" in lit or "m²" in lit:
            return lit
    return None
```

V `fmt_cell` nahraď blok:

```python
    unit=None
    if "Kč" in nf: unit="Kč"
    elif "m2" in nf or "m²" in nf: unit="m²"
    if nf=="General":
        dec=0 if float(v).is_integer() else 2
    else:
        dec=decimals_from(nf)
    neg=v<0; av=abs(v)
    s=f"{av:,.{dec}f}".replace(",","§").replace(".",",").replace("§",NBSP)
    if neg: s="−"+s
    if unit: s=s+NBSP+unit
    return s
```

za:

```python
    suffix=literal_suffix(nf)
    if nf=="General":
        dec=0 if float(v).is_integer() else 2
    else:
        dec=decimals_from(nf)
    neg=v<0; av=abs(v)
    s=f"{av:,.{dec}f}".replace(",","§").replace(".",",").replace("§",NBSP)
    if neg: s="−"+s
    if suffix:
        s=s+NBSP+suffix.replace("m2","m²").strip()
    return s
```

- [ ] **Step 3: Re-extrakce z xlsx**

```bash
cd "/Users/kindl/Work/_2026/02 OSA" && SCRATCH="/Users/kindl/Work/_2026/02 OSA/11 WWW/startovaci-hub/tools/zaklad/data" python3 "/Users/kindl/Work/_2026/02 OSA/11 WWW/startovaci-hub/tools/zaklad/dump_zaklad.py" && SCRATCH="/Users/kindl/Work/_2026/02 OSA/11 WWW/startovaci-hub/tools/zaklad/data" python3 "/Users/kindl/Work/_2026/02 OSA/11 WWW/startovaci-hub/tools/zaklad/extract_fmt.py"
```
Expected: vypíše `cells with content/fill: …` a `grid.tsv written: …`, bez chyby.

- [ ] **Step 4: Ověřit rozsah změn (žádná regrese)**

```bash
cd "/Users/kindl/Work/_2026/02 OSA/11 WWW/startovaci-hub" && python3 - <<'PY'
import json
g={tuple(int(x) for x in k.split(',')):v for k,v in json.load(open("tools/zaklad/data/grid_fmt.json")).items()}
d=json.load(open("tools/zaklad/data/zaklad_dump.json"))
fc={(c["row"],c["col"]):c.get("fc") for c in d["cells"] if c.get("fc")}
def col(s):
    n=0
    for ch in s: n=n*26+(ord(ch)-64)
    return n
print("CL6 grid:", g.get((6,col("CL"))), "| fc:", fc.get((6,col("CL"))))
print("CJ15 grid:", g.get((15,col("CJ"))), "| fc:", fc.get((15,col("CJ"))))
print("BV8 grid:", g.get((8,col("BV"))))
print("BV23 grid:", g.get((23,col("BV"))))
print("red cells total:", len(fc))
PY
git diff --stat tools/zaklad/data/grid_fmt.json tools/zaklad/data/zaklad_dump.json
```
Expected: `CL6 grid: 2 975 300 Kč | fc: FFFF0000`; `CJ15 grid: 3 | fc: FFFF0000`; `BV8 grid: 0 Kč [přípravná fáze]`; `BV23 grid: 758 206 858 Kč`; `red cells total:` malé číslo (jen pár buněk). `git diff --stat` ukáže jen tyto dva JSONy; změny odpovídají přípravné fázi + přidaným `fc`.

- [ ] **Step 5: Commit**

```bash
cd "/Users/kindl/Work/_2026/02 OSA/11 WWW/startovaci-hub" && git add tools/zaklad/dump_zaklad.py tools/zaklad/extract_fmt.py tools/zaklad/data/grid_fmt.json tools/zaklad/data/zaklad_dump.json tools/zaklad/data/grid.tsv tools/zaklad/data/zaklad_images.json && git commit -m "zaklad extraktory: font color (červená čísla) + zachování literálu formátu (přípravná fáze)"
```

---

### Task 2: Výměna dvou ortofoto map

**Files:**
- Overwrite: `REPO/assets/images/investori/zaklad/schema-ortofoto-zony-1.jpg` (zdroj `XLSXDIR/15 Map/_jadro-projektu.JPG`)
- Overwrite: `REPO/assets/images/investori/zaklad/schema-ortofoto-zony-2.jpg` (zdroj `XLSXDIR/15 Map/_zazemi-celek.JPG`)
- Modify: `REPO/assets/images/investori/zaklad/mapping.json`

**Interfaces:**
- Produces: stejné názvy souborů → `build_zaklad.py` se nemění; breakdown bloky „Pozemky: jádro…" a „…jádro + zázemí…" zobrazí nové mapy.

- [ ] **Step 1: Zmenšit a přepsat obrázky**

```bash
cd "/Users/kindl/Work/_2026/02 OSA/11 WWW/startovaci-hub" && sips -s format jpeg -s formatOptions 82 --resampleWidth 2400 "/Users/kindl/Work/_2026/02 OSA/15 Map/_jadro-projektu.JPG" --out assets/images/investori/zaklad/schema-ortofoto-zony-1.jpg && sips -s format jpeg -s formatOptions 82 --resampleWidth 2400 "/Users/kindl/Work/_2026/02 OSA/15 Map/_zazemi-celek.JPG" --out assets/images/investori/zaklad/schema-ortofoto-zony-2.jpg
```

- [ ] **Step 2: Ověřit rozměry**

```bash
cd "/Users/kindl/Work/_2026/02 OSA/11 WWW/startovaci-hub" && sips -g pixelWidth -g pixelHeight assets/images/investori/zaklad/schema-ortofoto-zony-1.jpg assets/images/investori/zaklad/schema-ortofoto-zony-2.jpg | grep -i "pixel\|^/"
```
Expected: oba soubory `pixelWidth: 2400`, výška ~1289 (jádro) / ~1274 (zázemí).

- [ ] **Step 3: Aktualizovat mapping.json**

V `REPO/assets/images/investori/zaklad/mapping.json` změň dvě hodnoty:
```json
    "schema-ortofoto-zony-1.jpg": "15 Map/_jadro-projektu.JPG = Pozemky: jádro (16 496,28 m²)",
    "schema-ortofoto-zony-2.jpg": "15 Map/_zazemi-celek.JPG = Pozemky: jádro + zázemí (34 769,61 m²)",
```

- [ ] **Step 4: Commit**

```bash
cd "/Users/kindl/Work/_2026/02 OSA/11 WWW/startovaci-hub" && git add assets/images/investori/zaklad/schema-ortofoto-zony-1.jpg assets/images/investori/zaklad/schema-ortofoto-zony-2.jpg assets/images/investori/zaklad/mapping.json && git commit -m "zaklad: výměna ortofoto map jádro / jádro+zázemí za nové podklady"
```

---

### Task 3: build_zaklad.py — helpery (is_red, vzgrand) + červená v matrix/paramstrip

**Files:**
- Modify: `REPO/tools/zaklad/build_zaklad.py`

**Interfaces:**
- Consumes: `DUMP["cells"]` s klíčem `fc` (Task 1), `cell_fill_class`, `col2num`, `V`, `esc`, `w`.
- Produces: `is_red(r,c) -> bool`; `vzgrand(items)` kde `items=[(label, coord, is_target_bool)]` emituje `.vz-grand` s `.vz-gbox` (barva dle fillu, cíl má `data-flow-target`). `matrix`/`paramstrip` přidávají `is-red` na červené hodnoty.

- [ ] **Step 1: Přidat FONT mapu a is_red()**

V `REPO/tools/zaklad/build_zaklad.py` za řádek `FILL = {(c["row"], c["col"]): c["f"] for c in DUMP["cells"] if c["f"]}` přidej:

```python
FONT = {(c["row"], c["col"]): c["fc"] for c in DUMP["cells"] if c.get("fc")}
def is_red(r, c):
    rgb = FONT.get((r, c))
    return bool(rgb and rgb.upper().endswith("FF0000"))
```

- [ ] **Step 2: Červená v `matrix` (td i stickcol)**

V `matrix._` ve větvi `if i == 0:` změň:
```python
                    scls = "vz-stickcol" + ((" " + fc) if fc else "")
                    w(f'          <th scope="row" class="{scls}">{esc(v)}</th>')
```
na:
```python
                    scls = "vz-stickcol" + ((" " + fc) if fc else "") + (" is-red" if is_red(r, c) else "")
                    w(f'          <th scope="row" class="{scls}">{esc(v)}</th>')
```
A v `else:` větvi za `if fc: cls.append(fc)` přidej:
```python
                    if is_red(r, c):
                        cls.append("is-red")
```

- [ ] **Step 3: Červená v `paramstrip`**

Nahraď tělo `paramstrip._` smyčky:
```python
        for label, coord in items:
            m = re.match(r'^([A-Z]+)(\d+)$', coord)
            c, r = col2num(m.group(1)), int(m.group(2))
            fc = cell_fill_class(r, c)
            w(f'    <div class="vz-param {fc}"><span class="vz-param__label">{esc(label)}</span>'
              f'<span class="vz-param__num">{esc(V(coord))}</span></div>')
```
za:
```python
        for label, coord in items:
            m = re.match(r'^([A-Z]+)(\d+)$', coord)
            c, r = col2num(m.group(1)), int(m.group(2))
            fc = cell_fill_class(r, c)
            red = " is-red" if is_red(r, c) else ""
            w(f'    <div class="vz-param {fc}"><span class="vz-param__label">{esc(label)}</span>'
              f'<span class="vz-param__num{red}">{esc(V(coord))}</span></div>')
```

- [ ] **Step 4: Přidat helper `vzgrand`**

Za funkci `vzsummary(...)` přidej:
```python
def vzgrand(items):
    """Souhrnné boxy s barvou dle zdrojového fillu buňky; volitelně cíl konektoru.
    items: list (label, coord, is_target?)."""
    def _():
        w('  <div class="vz-grand">')
        for it in items:
            label, coord = it[0], it[1]
            tgt = len(it) > 2 and it[2]
            m = re.match(r'^([A-Z]+)(\d+)$', coord)
            c, r = col2num(m.group(1)), int(m.group(2))
            fc = cell_fill_class(r, c)
            red = " is-red" if is_red(r, c) else ""
            attr = ' data-flow-target' if tgt else ''
            w(f'    <div class="vz-gbox {fc}"{attr}>')
            w(f'      <span class="vz-gbox__label">{esc(label)}</span>')
            w(f'      <span class="vz-gbox__num{red}">{esc(V(coord))}</span>')
            w('    </div>')
        w('  </div>')
    return _
```

- [ ] **Step 5: Ověřit, že generátor stále běží**

```bash
cd "/Users/kindl/Work/_2026/02 OSA/11 WWW/startovaci-hub" && python3 tools/zaklad/build_zaklad.py && grep -c "is-red" tools/zaklad/data/body.html
```
Expected: `body.html written: …`; `grep -c "is-red"` ≥ 1 (CJ15 v tabulce č.2 / jiné červené v už generovaných sekcích, pokud jsou). Žádná chyba.

- [ ] **Step 6: Commit**

```bash
cd "/Users/kindl/Work/_2026/02 OSA/11 WWW/startovaci-hub" && git add tools/zaklad/build_zaklad.py tools/zaklad/data/body.html && git commit -m "zaklad generátor: is_red + vzgrand + červená v matrix/paramstrip"
```

---

### Task 4: build_zaklad.py — 5 tabulek na konec zóny „Projekt Startovací hub"

**Files:**
- Modify: `REPO/tools/zaklad/build_zaklad.py` (sekce „STARTOVACÍ HUB — JEDNOTKY 1+kk")

**Interfaces:**
- Consumes: `matrix`, `paramstrip`, `vzgrand`, `flowblock`, `greenband`, `vzmap`, `zonesection`.
- Produces: HTML 5 tabulek v `body.html` uvnitř existující `zonesection` zóny hubu.

- [ ] **Step 1: Definovat bloky 5 tabulek**

V `build_zaklad.py` za definici `hub_bench = matrix(...)` (před voláním `zonesection(...)` pro hub) vlož:

```python
# ---- finále: 5 tabulek (BS–CZ) ----
t20_params = paramstrip([
    ("Odhadovaná výše příjmu pro rok 2026", "BS6"),
    ("Odhadovaný meziroční růst ceny pronájmů", "BU6"),
])
t20_matrix = matrix(
    ["Rok", "Odhadovaný meziroční růst cen pronájmů v jednotlivých letech",
     "Odhadovaný příjem z pronájmu v jednotlivých letech",
     "Odhad celkových (akumulovaných) příjmů z pronájmu"],
    ["BS", "BT", "BU", "BV"], list(range(8, 24)), cellfills=True)
t20_grand = vzgrand([
    ("Odhadovaná výše všech příjmů z pronájmu jednotlivých jednotek v rámci projektu "
     "Startovací hub do konce roku 2038:", "BV39", True),
])

t21_matrix = matrix(
    ["Rok", "Odhadovaný příjem v jednotlivých letech",
     "Výše zálohy na kupní cenu Areálu v příslušném roce",
     "Rozdíl mezi příjmy a náklady v jednotlivých letech",
     "Akumulovaný rozdíl hlavních příjmů a nákladů projektu"],
    ["BY", "BZ", "CA", "CB", "CC"], list(range(8, 24)), cellfills=True)
t21_grand = vzgrand([
    ("Cena Areálu po odečtení uhrazených záloh na konci roku 2038:", "BZ39", False),
    ("Hlavní příjmy projektu Startovací hub do konce roku 2038:", "CB39", True),
])

t22_params = paramstrip([
    ("Odhadovaná prodejní cena jedné jednotky 1+kk o ČPP cca 21 m² v příslušné lokalitě "
     "pro rok 2026", "CL6"),
])
t22_matrix = matrix(
    ["Číslo parcely", "Označení", "Název", "Celkem podlaží",
     "Počet podlaží vhodných pro rekonstrukci na jednotky 1+kk",
     "Počet jednotek v příslušné budově",
     "Odhad prodejní ceny všech jednotek v příslušné budově"],
    ["CG", "CH", "CI", "CJ", "CK", "CL", "CM"], list(range(10, 27)),
    cellfills=True, zonecols=(85, 93))
t22_grand = vzgrand([
    ("Počet jednotek 1+kk vzniklých pro Startovací hub:", "CL39", False),
    ("Odhadovaná tržní ceny všech jednotek pro rok 2026:", "CM39", True),
])
t22_bench = matrix(
    ["Odhadovaná tržní cena jednotky 1+kk", "Plocha (ČPP)", "Cena za m²"],
    ["CK", "CL", "CM"], [42], cellfills=True)

t24_params = paramstrip([
    ("Odhadovaná tržní cena všech jednotek (2026)", "CP6"),
    ("Zvolený index pro meziroční růst ceny nemovitostí v příslušné lokalitě", "CR6"),
])
t24_matrix = matrix(
    ["Rok", "Index zvolený pro růst tržní ceny jednotek 1+kk v lokalitě Areálu",
     "Odhadovaná tržní cena jednotek vzniklých pro projekt Startovací hub"],
    ["CP", "CQ", "CR"], list(range(8, 24)), cellfills=True)
t24_grand = vzgrand([
    ("Počet jednotek 1+kk vybudovaných pro Startovací hub:", "CQ39", False),
    ("Odhadovaná tržní cena jednotek vybudovaných pro Startovací hub v roce 2038:",
     "CR39", True),
])

t25_params = paramstrip([
    ("Odhadovaný průměrný meziroční růst ceny nemovitostí v lokalitě Areálu mezi roky "
     "2026 až 2038", "CU6"),
    ("Odhad tržní ceny jednotek vzniklých pro projekt Startovací hub (2026)", "CX6"),
])
t25_matrix = matrix(
    ["Rok", "Přírůstek prodejní ceny",
     "Prodejní cena zrekonstruovaných ubytovacích jednotek",
     "Kupní cena Areálu při předpokládané inflaci CPI do 5 %",
     "Kupní cena Areálu k doplacení po započtení uhrazených záloh",
     "Rozdíl mezi doplatkem kupní ceny Areálu a tržní cenou jednotek vzniklých "
     "v jádru projektu Startovací hub"],
    ["CU", "CV", "CW", "CX", "CY", "CZ"], list(range(8, 24)), cellfills=True)
t25_grand = vzgrand([
    ("Odhadovaný rozdíl mezi prodejní cenou jednotek vzniklých pro projekt Startovací "
     "hub a doplatkem kupní ceny za Areál v roce 2038:", "CX39", True),
])
```

- [ ] **Step 2: Přidat bloky do `zonesection` zóny hubu**

V existujícím volání `zonesection("Projekt Startovací hub | …", "#FBFAF0", [ … ], …)` přidej do seznamu bloků **za** poslední `vzmap("zdroj-odhad-najemneho.jpg", …)` tyto položky (čárka za vzmap, pak):

```python
        greenband("Odhadovaný meziroční nárůst příjmů z pronájmu jednotek vzniklých pro projekt Startovací hub"),
        t20_params,
        flowblock([t20_matrix, t20_grand]),
        greenband("Hrubé porovnání hlavních provozních příjmů a nákladů projektu Startovací hub"),
        flowblock([t21_matrix, t21_grand]),
        greenband("Odhad tržní ceny všech jednotek vzniklých pro projekt Startovací hub"),
        t22_params,
        flowblock([t22_matrix, t22_grand]),
        greenband("Odhad tržní ceny jedné jednotky 1+kk o ČPP 21 m² v příslušné lokalitě "
                  "(www.odhad-zdarma.cz, k 18. 1. 2026)", center=True),
        t22_bench,
        vzmap("zdroj-odhad-prodejni-ceny.jpg",
              "Odhad tržní prodejní ceny srovnatelné nemovitosti (oceňovací nástroj odhad-zdarma.cz)"),
        greenband("Odhadovaný nárůst tržní ceny jednotek vzniklých pro projekt Startovací hub"),
        t24_params,
        flowblock([t24_matrix, t24_grand]),
        greenband("Rozdíl mezi nákupní cenou Areálu a tržní cenou jednotek vzniklých pro projekt Startovací hub"),
        t25_params,
        flowblock([t25_matrix, t25_grand]),
```

- [ ] **Step 3: Build + ověřit přítomnost hodnot a struktury**

```bash
cd "/Users/kindl/Work/_2026/02 OSA/11 WWW/startovaci-hub" && python3 tools/zaklad/build_zaklad.py && python3 - <<'PY'
b=open("tools/zaklad/data/body.html").read()
for s in ["758 206 858","515 496 858","984 824 300","1 768 602 949","1 322 483 783",
          "446 119 167","2 975 300","141 681","přípravná fáze","data-flow-target","vz-flowblock"]:
    print(("OK " if s in b else "!! "), s, b.count(s))
PY
```
Expected: všechny řádky `OK …`; `data-flow-target` count = 5, `vz-flowblock` count = 5.

- [ ] **Step 4: Commit**

```bash
cd "/Users/kindl/Work/_2026/02 OSA/11 WWW/startovaci-hub" && git add tools/zaklad/build_zaklad.py tools/zaklad/data/body.html && git commit -m "zaklad: 5 závěrečných tabulek zóny Projekt Startovací hub (BS–CZ)"
```

---

### Task 5: assemble.py — CSS (is-red, hover overlay fix, vz-grand, ribbon, flowmark, lightbox)

**Files:**
- Modify: `REPO/tools/zaklad/assemble.py` (řetězec `STYLE`)

**Interfaces:**
- Consumes: třídy z generátoru (`is-red`, `vz-grand`/`vz-gbox`, `data-flow-target`, `vz-flowblock`, `vz-bigribbon`, `figure img`).
- Produces: vizuál červených čísel, uniformní hover ztmavení, souhrnné boxy, trvalou+hot linku, zvýraznění `is-flowmark`, lightbox `.lbx`.

- [ ] **Step 1: Červená čísla**

V `STYLE` za řádek `.vz .val.is-green{background:#D4E6C6}` přidej:
```css
  .vz .is-red,.vz .vz-matrix td.is-red,.vz .vz-matrix .vz-stickcol.is-red,
  .vz .vz-param__num.is-red,.vz .vz-gbox__num.is-red{color:#C8102E !important}
```

- [ ] **Step 2: Oprava hover ztmavení (přebije i barevné buňky)**

Nahraď tyto čtyři řádky:
```css
  .vz .vz-matrix tbody tr:hover td{background:#F0F0FA}
  .vz .vz-matrix tbody tr:hover .vz-stickcol{background:#F0F0FA}
```
(a níže)
```css
  .vz .vz-matrix tbody tr.is-jadro:hover td,.vz .vz-matrix tbody tr.is-jadro:hover .vz-stickcol{background:#ECE4B4}
  .vz .vz-matrix tbody tr.is-zazemi:hover td,.vz .vz-matrix tbody tr.is-zazemi:hover .vz-stickcol{background:#D4E7C7}
```
za (překryvná vrstva nezávislá na pozadí + zvýraznění konektoru):
```css
  .vz .vz-matrix tbody tr:hover td{box-shadow:inset 0 0 0 999px rgba(42,42,96,.06)}
  .vz .vz-matrix tbody tr:hover .vz-stickcol{box-shadow:1px 0 0 0 var(--hair),inset 0 0 0 999px rgba(42,42,96,.06)}
  .vz .vz-matrix tbody tr.is-flowmark td{box-shadow:inset 0 0 0 999px rgba(196,162,192,.30)}
  .vz .vz-matrix tbody tr.is-flowmark .vz-stickcol{box-shadow:1px 0 0 0 var(--hair),inset 0 0 0 999px rgba(196,162,192,.30)}
```

- [ ] **Step 3: Souhrnné boxy `vz-grand`**

Za blok `.vz .vz-summary{…}` / `.vz .vz-sbox{…}` / `.vz .vz-sbox__num{…}` přidej:
```css
  /* souhrnné boxy finále (barva dle fillu) */
  .vz .vz-grand{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:14px 0 4px}
  .vz .vz-gbox{background:var(--tint);border:1px solid var(--hair);padding:14px 16px;position:relative}
  .vz .vz-gbox.is-green{background:#D4E6C6;border-color:#A8CE9F}
  .vz .vz-gbox.is-yellow{background:#F2ECC9;border-color:#D8CD7E}
  .vz .vz-gbox.is-blue{background:#E6ECF6;border-color:#B6CDE9}
  .vz .vz-gbox.is-input{background:#F0CFA0;border-color:#D9B57E}
  .vz .vz-gbox__label{display:block;font-size:.82rem;color:#3a3a52;line-height:1.3}
  .vz .vz-gbox__num{display:block;margin-top:5px;font-size:clamp(1.3rem,3.2vw,1.85rem);font-weight:700;font-variant-numeric:tabular-nums;letter-spacing:-.01em}
  .vz .vz-gbox.is-flowmark{outline:2px solid var(--rose,#C4A2C0);outline-offset:-2px}
```

- [ ] **Step 4: Doladit ribbon (trvalý jemný + hot) a cílit na `vz-grand`**

Nahraď blok velkého ribbonu:
```css
  .vz .vz-flowblock{position:relative}
  .vz .vz-flowblock > .vz-mwrap, .vz .vz-flowblock > .vz-summary{margin-right:78px}
  .vz .vz-bigribbon{position:absolute;inset:0;width:100%;height:100%;overflow:visible;pointer-events:none;z-index:1}
  .vz .vz-bigribbon path{fill:none;stroke:var(--rose,#C4A2C0);stroke-width:4.5;stroke-linecap:round;stroke-linejoin:round}
  @media (max-width:820px){ .vz .vz-flowblock > .vz-mwrap, .vz .vz-flowblock > .vz-summary{margin-right:0} .vz .vz-bigribbon{display:none} }
```
za:
```css
  .vz .vz-flowblock{position:relative}
  .vz .vz-flowblock > .vz-mwrap, .vz .vz-flowblock > .vz-grand{margin-right:84px}
  .vz .vz-bigribbon{position:absolute;inset:0;width:100%;height:100%;overflow:visible;pointer-events:none;z-index:1}
  .vz .vz-bigribbon path{fill:none;stroke:var(--rose,#C4A2C0);stroke-width:1.6;opacity:.55;stroke-linecap:round;stroke-linejoin:round;transition:stroke-width .15s,opacity .15s}
  .vz .vz-flowblock.is-flowhot .vz-bigribbon path{stroke-width:3.4;opacity:1}
  @media (max-width:820px){ .vz .vz-flowblock > .vz-mwrap, .vz .vz-flowblock > .vz-grand{margin-right:0} .vz .vz-bigribbon{display:none} }
```

- [ ] **Step 5: Lightbox CSS + zoom-in afordance**

Na konec `STYLE` před uzavírací `</style>` přidej:
```css
  /* obrázky klikatelné na zvětšení */
  .vz figure img{cursor:zoom-in}
  /* lightbox (mimo .vz scope — overlay na body) */
  .lbx{position:fixed;inset:0;z-index:9999;display:none;align-items:center;justify-content:center;background:rgba(16,16,38,.92);padding:clamp(12px,4vw,48px)}
  .lbx.is-open{display:flex}
  .lbx__img{max-width:100%;max-height:88vh;width:auto;height:auto;object-fit:contain;border-radius:6px;box-shadow:0 20px 60px rgba(0,0,0,.5);background:#0c0c1e}
  .lbx__cap{position:absolute;left:0;right:0;bottom:max(12px,env(safe-area-inset-bottom));text-align:center;color:#e8e8f4;font-size:.85rem;padding:0 16px;line-height:1.4;margin:0}
  .lbx__btn{position:absolute;border:0;background:rgba(255,255,255,.12);color:#fff;cursor:pointer;width:46px;height:46px;border-radius:9999px;display:flex;align-items:center;justify-content:center;-webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px)}
  .lbx__btn:hover{background:rgba(255,255,255,.22)}
  .lbx__btn:focus-visible{outline:2px solid #fff;outline-offset:2px}
  .lbx__close{top:18px;right:18px}
  .lbx__prev{left:18px;top:50%;transform:translateY(-50%)}
  .lbx__next{right:18px;top:50%;transform:translateY(-50%)}
  .lbx__btn svg{display:block}
  @media (max-width:680px){ .lbx__prev{left:8px} .lbx__next{right:8px} .lbx__btn{width:40px;height:40px} }
```

- [ ] **Step 6: Assemble + ověřit CSS přítomnost**

```bash
cd "/Users/kindl/Work/_2026/02 OSA/11 WWW/startovaci-hub" && python3 tools/zaklad/assemble.py && python3 - <<'PY'
h=open("investori-zaklad.html").read()
for s in ["is-flowhot",".vz-gbox","rgba(196,162,192",".lbx__img","stroke-width:1.6","color:#C8102E"]:
    print(("OK " if s in h else "!! "), s)
PY
```
Expected: všechny `OK …`.

- [ ] **Step 7: Commit**

```bash
cd "/Users/kindl/Work/_2026/02 OSA/11 WWW/startovaci-hub" && git add tools/zaklad/assemble.py investori-zaklad.html && git commit -m "zaklad styly: červená čísla, hover overlay fix, vz-grand, jemný+hot ribbon, lightbox CSS"
```

---

### Task 6: assemble.py — JS konektor (trvalá linka + hover highlight)

**Files:**
- Modify: `REPO/tools/zaklad/assemble.py` (řetězec `SCRIPTS`)

**Interfaces:**
- Consumes: `.vz-flowblock`, `.vz-mwrap`, `.vz-matrix tbody tr` (poslední = zdroj), `[data-flow-target]`.
- Produces: trvalou linku + třídy `is-flowhot`/`is-flowmark` na hover/focus.

- [ ] **Step 1: Nahradit IIFE velkého ribbonu**

Ve `SCRIPTS` nahraď celý blok `/* Velký pravý ribbon: … */ (function () { … })();` tímto:
```javascript
  /* Konektor (náhrada Excel šipek): trvalá jemná linka tabulka → cílový souhrnný box;
     hover/focus na posledním řádku nebo boxu linku zvýrazní a obě hodnoty rozsvítí. */
  (function () {
    function lastRow(block){ var r=block.querySelectorAll('.vz-matrix tbody tr'); return r.length?r[r.length-1]:null; }
    function draw(block) {
      var svg=block.querySelector('.vz-bigribbon'), wrap=block.querySelector('.vz-mwrap'),
          target=block.querySelector('[data-flow-target]');
      if(!svg||!wrap||!target) return;
      if(window.innerWidth<820){ svg.innerHTML=''; return; }
      var b=block.getBoundingClientRect(), t=wrap.getBoundingClientRect(), e=target.getBoundingClientRect();
      var row=lastRow(block), r=row?row.getBoundingClientRect():t;
      var W=b.width, H=b.height;
      var sx=t.right-b.left, sy=(r.top-b.top)+r.height/2;
      var ex=e.right-b.left, ey=(e.top-b.top)+e.height/2;
      var bow=64;
      svg.setAttribute('viewBox','0 0 '+W+' '+H);
      var c1x=sx+bow, c1y=sy+(ey-sy)*0.30, c2x=ex+bow, c2y=ey-(ey-sy)*0.30;
      var d='M '+sx+' '+sy+' C '+c1x+' '+c1y+', '+c2x+' '+c2y+', '+ex+' '+ey;
      var a=9, head='M '+(ex-a)+' '+(ey-a)+' L '+ex+' '+ey+' L '+(ex-a)+' '+(ey+a);
      svg.innerHTML='<path d="'+d+'"/><path d="'+head+'"/>';
    }
    function wire(block){
      var target=block.querySelector('[data-flow-target]'), row=lastRow(block);
      if(!target||!row) return;
      function on(){ block.classList.add('is-flowhot'); row.classList.add('is-flowmark'); target.classList.add('is-flowmark'); }
      function off(){ block.classList.remove('is-flowhot'); row.classList.remove('is-flowmark'); target.classList.remove('is-flowmark'); }
      [row,target].forEach(function(el){
        el.addEventListener('mouseenter',on); el.addEventListener('mouseleave',off);
        el.addEventListener('focusin',on); el.addEventListener('focusout',off);
      });
      target.tabIndex=0;
    }
    var blocks=document.querySelectorAll('.vz-flowblock');
    function all(){ Array.prototype.forEach.call(blocks,draw); }
    Array.prototype.forEach.call(blocks,wire);
    all();
    window.addEventListener('resize',all);
    window.addEventListener('load',all);
    if(document.fonts&&document.fonts.ready) document.fonts.ready.then(all);
  })();
```

- [ ] **Step 2: Assemble + ověřit**

```bash
cd "/Users/kindl/Work/_2026/02 OSA/11 WWW/startovaci-hub" && python3 tools/zaklad/assemble.py && grep -c "is-flowhot\|data-flow-target\|lastRow" investori-zaklad.html
```
Expected: ≥ 3 (JS i markup přítomné).

- [ ] **Step 3: Commit**

```bash
cd "/Users/kindl/Work/_2026/02 OSA/11 WWW/startovaci-hub" && git add tools/zaklad/assemble.py investori-zaklad.html && git commit -m "zaklad JS: konektor — trvalá linka + hover zvýraznění (náhrada Excel šipek)"
```

---

### Task 7: assemble.py — JS lightbox

**Files:**
- Modify: `REPO/tools/zaklad/assemble.py` (řetězec `SCRIPTS`)

**Interfaces:**
- Consumes: `.vz figure img`, `figcaption`.
- Produces: overlay `.lbx` (vytvořený za běhu), klik/Enter otevře, Esc/×/pozadí zavře, ‹ › a ←/→ navigace.

- [ ] **Step 1: Přidat IIFE lightboxu**

Ve `SCRIPTS` před uzavírací `</script>` přidej:
```javascript
  /* Lightbox: klik na obrázek v podkladech → zvětšení. Esc / pozadí / × zavře, ‹ › a ←/→ navigace. */
  (function () {
    var imgs=Array.prototype.slice.call(document.querySelectorAll('.vz figure img'));
    if(!imgs.length) return;
    var overlay, lbImg, lbCap, idx=-1;
    function build(){
      overlay=document.createElement('div');
      overlay.className='lbx'; overlay.setAttribute('role','dialog'); overlay.setAttribute('aria-modal','true');
      overlay.innerHTML=
        '<button class="lbx__btn lbx__close" aria-label="Zavřít"><svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg></button>'+
        '<button class="lbx__btn lbx__prev" aria-label="Předchozí"><svg width="26" height="26" viewBox="0 0 24 24" fill="none"><path d="M15 5l-7 7 7 7" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>'+
        '<img class="lbx__img" alt="">'+
        '<button class="lbx__btn lbx__next" aria-label="Další"><svg width="26" height="26" viewBox="0 0 24 24" fill="none"><path d="M9 5l7 7-7 7" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>'+
        '<p class="lbx__cap"></p>';
      document.body.appendChild(overlay);
      lbImg=overlay.querySelector('.lbx__img'); lbCap=overlay.querySelector('.lbx__cap');
      overlay.addEventListener('click',function(e){ if(e.target===overlay) close(); });
      overlay.querySelector('.lbx__close').addEventListener('click',close);
      overlay.querySelector('.lbx__prev').addEventListener('click',function(e){ e.stopPropagation(); show(idx-1); });
      overlay.querySelector('.lbx__next').addEventListener('click',function(e){ e.stopPropagation(); show(idx+1); });
    }
    function capFor(im){ var f=im.closest('figure'), c=f&&f.querySelector('figcaption'); return (c&&c.textContent.trim())||im.alt||''; }
    function show(i){ idx=(i+imgs.length)%imgs.length; var im=imgs[idx]; lbImg.src=im.currentSrc||im.src; lbImg.alt=im.alt||''; lbCap.textContent=capFor(im); }
    function open(i){ if(!overlay) build(); show(i); overlay.classList.add('is-open'); document.body.style.overflow='hidden'; }
    function close(){ if(overlay) overlay.classList.remove('is-open'); document.body.style.overflow=''; }
    imgs.forEach(function(im,i){
      im.tabIndex=0; im.setAttribute('role','button');
      if(!im.getAttribute('aria-label')) im.setAttribute('aria-label','Zvětšit obrázek');
      im.addEventListener('click',function(){ open(i); });
      im.addEventListener('keydown',function(e){ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); open(i); } });
    });
    document.addEventListener('keydown',function(e){
      if(!overlay||!overlay.classList.contains('is-open')) return;
      if(e.key==='Escape') close();
      else if(e.key==='ArrowLeft') show(idx-1);
      else if(e.key==='ArrowRight') show(idx+1);
    });
  })();
```

- [ ] **Step 2: Assemble + ověřit**

```bash
cd "/Users/kindl/Work/_2026/02 OSA/11 WWW/startovaci-hub" && python3 tools/zaklad/assemble.py && grep -c "lbx__img\|capFor\|Zvětšit obrázek" investori-zaklad.html
```
Expected: ≥ 2.

- [ ] **Step 3: Commit**

```bash
cd "/Users/kindl/Work/_2026/02 OSA/11 WWW/startovaci-hub" && git add tools/zaklad/assemble.py investori-zaklad.html && git commit -m "zaklad JS: lightbox na obrázky podkladů (klik = zvětšení)"
```

---

### Task 8: Finální build + vizuální ověření + regrese

**Files:**
- Regenerate: `REPO/investori-zaklad.html`
- Build: `REPO/assets/styles.css` (pojistka)

**Interfaces:**
- Consumes: vše předchozí.

- [ ] **Step 1: Plný build řetězec**

```bash
cd "/Users/kindl/Work/_2026/02 OSA/11 WWW/startovaci-hub" && python3 tools/zaklad/build_zaklad.py && python3 tools/zaklad/assemble.py && npm run build
```
Expected: oba python skripty napíšou počty bytů; `npm run build` projde (Tailwind „Done").

- [ ] **Step 2: Server odpovídá**

```bash
cd "/Users/kindl/Work/_2026/02 OSA/11 WWW/startovaci-hub" && curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/investori-zaklad.html
```
Expected: `200` (server z úvodu session běží; jinak `python3 -m http.server 8000 &`).

- [ ] **Step 3: Vizuální kontrola proti screenshotům** (ruční / přes `verify` skill)

Přihlásit se přes `investori.html`, projít konec zóny „Projekt Startovací hub" a zkontrolovat:
  - 5 tabulek ve správném pořadí, hodnoty == screenshoty (758 206 858; 446 119 167 + 515 496 858; 331 + 984 824 300; 1 768 602 949; 1 322 483 783).
  - Červená čísla: `CL6` (2 975 300 Kč vstup #22) a „3" u štábu (#22 tabulka).
  - „[přípravná fáze]" u nulových řádků akumulace (#20).
  - Souhrnné boxy: #21 zelený+žlutý, #22/#24 dva žluté, #20/#25 jeden žlutý.
  - Benchmark pod #22 + obrázek `zdroj-odhad-prodejni-ceny.jpg`.
  - Konektor: trvalá jemná linka u všech 5; hover na posledním řádku / boxu → linka zesílí + obě hodnoty se rozsvítí; okno < 820 px linku skryje.
  - Hover na libovolný řádek tabulky ztmaví **i barevné** buňky (ne jen bílé).
  - Lightbox: klik na každý obrázek → zvětšení; ‹ ›, ←/→, Esc.
  - Nové ortofoto mapy v breakdown blocích „Pozemky: jádro" / „…jádro + zázemí".

- [ ] **Step 4: Regrese schválených sekcí**

V prohlížeči ověřit, že Tabulky č.1/č.2, smlouva a příjmy z pronájmu vypadají beze změny (kromě záměrných: ortofoto výměna, hover fix, lightbox afordance/cursor).

- [ ] **Step 5: Commit (pokud npm run build změnil styles.css)**

```bash
cd "/Users/kindl/Work/_2026/02 OSA/11 WWW/startovaci-hub" && git add investori-zaklad.html assets/styles.css && git commit -m "zaklad: finální build (Projekt Startovací hub finále)" || echo "nic k commitu"
```

- [ ] **Step 6: Aktualizovat CLAUDE.md**

V `REPO/CLAUDE.md` v sekci o `investori-zaklad.html` přesun z „Hotové sekce" doplnit 5 nových tabulek a zmínit konektor (trvalá linka + hover) a lightbox. Commit:
```bash
cd "/Users/kindl/Work/_2026/02 OSA/11 WWW/startovaci-hub" && git add CLAUDE.md && git commit -m "CLAUDE.md: zaklad — finále zóny Startovací hub (5 tabulek, konektor, lightbox)"
```

---

## Notes / rizika

- **Re-extrakce (Task 1)** přepíše `grid_fmt.json`/`zaklad_dump.json` celého listu. `git diff --stat` musí ukázat jen tyto soubory a změny smysluplné (přípravná fáze + `fc`). Pokud se objeví neočekávané změny ve formátování jiných buněk, zkontroluj `literal_suffix` (nezahrnovat formáty bez jednotky).
- **Konektor a horizontální posuv tabulky:** linka se kotví na pravý okraj `.vz-mwrap` (ne na scrollující buňku) → robustní; zvýraznění řádku se při odscrollování prostě nezobrazí.
- **#22** je po budovách: „poslední řádek" pro konektor je Dílny (CM prázdné) — linka i tak vede tabulka → box `CM39`. Akceptováno.
- **`investori-zamer.html`** se nemění (interaktivní mapa, viz spec §8).
