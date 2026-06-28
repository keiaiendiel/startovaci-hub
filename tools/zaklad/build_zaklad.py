# -*- coding: utf-8 -*-
"""Deterministický generátor obsahu .vz pro investori-zaklad.html.
Čte grid_fmt.json (formátované hodnoty) + zaklad_dump.json (fill barvy) a emituje
HTML tabulek. Čísla jdou přímo z gridu (žádný ruční přepis)."""
import json, os, re, html as _html

SCRATCH = os.environ.get("SCRATCH") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
GRID = {tuple(int(x) for x in k.split(",")): v
        for k, v in json.load(open(SCRATCH + "/grid_fmt.json")).items()}
DUMP = json.load(open(SCRATCH + "/zaklad_dump.json"))
FILL = {(c["row"], c["col"]): c["f"] for c in DUMP["cells"] if c["f"]}
FONT = {(c["row"], c["col"]): c["fc"] for c in DUMP["cells"] if c.get("fc")}
ORANGE = "FFEBC08F"

def is_red(r, c):
    rgb = FONT.get((r, c))
    return bool(rgb and rgb.upper().endswith("FF0000"))

def col2num(s):
    n = 0
    for ch in s:
        n = n * 26 + (ord(ch.upper()) - 64)
    return n

def V(coord):
    """coord like 'AJ6' -> formatted string or '' (suppress #VALUE!)."""
    m = re.match(r'^([A-Z]+)(\d+)$', coord)
    c, r = col2num(m.group(1)), int(m.group(2))
    v = GRID.get((r, c), "")
    if v is None or v == "" or "#VALUE!" in v:
        return ""
    return v

def Vrc(r, c):
    v = GRID.get((r, c), "")
    if v is None or "#VALUE!" in (v or ""):
        return ""
    return v or ""

def is_orange(r, c):
    return FILL.get((r, c)) == ORANGE

GREEN_FILL = "FFC2DCAE"   # zázemí
YELLOW_FILL = "FFECE5A3"  # jádro
# mapování zdrojových fill barev → CSS třídy buněk (věrná reprodukce Excelu)
FILLCLASS = {
    "FFEBC08F": "is-input", "FFEED9A0": "is-input",
    "FFC2DCAE": "is-green", "FFECE5A3": "is-yellow",
    "FFE6ECF6": "is-blue", "FFB6CDE9": "is-blue2",
    "FFD9C7A1": "is-tan",
}
def cell_fill_class(r, c):
    return FILLCLASS.get(FILL.get((r, c)), "")

def row_zone(r, c0, c1):
    """Vrátí třídu řádku podle zónového fillu ve zdroji (žlutá=jádro, zelená=zázemí)."""
    fills = {FILL.get((r, c)) for c in range(c0, c1 + 1)}
    if YELLOW_FILL in fills:
        return "is-jadro"
    if GREEN_FILL in fills:
        return "is-zazemi"
    return ""

def esc(s):
    return _html.escape(str(s), quote=True)

def coord_col(coord):
    """'E39' -> 'E' (písmeno sloupce pro propojení souhrnu se zdrojovým sloupcem)."""
    m = re.match(r'^([A-Z]+)\d+$', str(coord))
    return m.group(1) if m else ""

NUM_RE = re.compile(r'\d')
def is_num(v):
    if not v or not NUM_RE.search(v):
        return False
    # strip digits, spaces, separators, common units -> if little left, it's numeric
    rest = re.sub(r'[\d\s.,%–\-−/]|Kč|m²|HPP|index|ČPP|rok', '', v)
    return len(rest) <= 2

OUT = []
def w(s): OUT.append(s)

# ---------- block emitters ----------
def section(title, tint, blocks, label=None, lede=None, shade=False):
    cls = "sec sec--shade" if shade else "sec"
    w(f'<section class="{cls}" style="--tint:{tint}" aria-label="{esc(label or title)}">')
    w(f'  <h2 class="sechead">{esc(title)}</h2>')
    if lede:
        w(f'  <p class="sec-lede">{esc(lede)}</p>')
    for b in blocks:
        b()
    w('</section>')

def subhead(text):
    return lambda: w(f'  <h3 class="vz-subhead">{esc(text)}</h3>')

def note(text):
    return lambda: w(f'  <p class="foot">{esc(text)}</p>')

def flow(text):
    """Ribbon konektor mezi dvěma bloky — zaoblený rose tah + šipka dolů + popisek.
    Nahrazuje původní Excel šipky: ukazuje tok konkrétní hodnoty do dalšího výpočtu."""
    def _():
        w('  <div class="vz-flow" role="separator" aria-label="navazuje na další výpočet">')
        w('    <svg class="vz-flow__svg" viewBox="0 0 44 50" width="34" height="39" aria-hidden="true">')
        w('      <path class="vz-flow__band" d="M22 3 C 12 16, 32 30, 22 42"/>')
        w('      <path class="vz-flow__head" d="M14 34 L22 44 L30 34"/>')
        w('    </svg>')
        w(f'    <span>{esc(text)}</span>')
        w('  </div>')
    return _

def legend_input():
    return lambda: w('  <p class="vz-legend-input"><span class="vz-swatch"></span>'
                     'hodnoty se žluto-oranžovým podkladem jsou vstupní předpoklady / odhady</p>')

def kv(pairs, inputs=False):
    """pairs: list of (label, coord_or_text, is_input?). value taken from grid if coord."""
    def _():
        w('  <div class="vz-kv">')
        for p in pairs:
            label = p[0]
            val = V(p[1]) if re.match(r'^[A-Z]+\d+$', str(p[1])) else p[1]
            inp = inputs or (len(p) > 2 and p[2])
            cls = "val num" if is_num(val) else "val"
            if inp:
                cls += " is-input"
            if val == "":
                continue
            w('    <div class="row">')
            w(f'      <div class="lab">{esc(label)}</div>')
            w(f'      <div class="{cls}">{esc(val)}</div>')
            w('    </div>')
        w('  </div>')
    return _

def matrix(headers, cols, rows, caption=None, foot=None, zonecols=None, cellfills=False):
    """headers: list of clean header strings (len == len(cols)).
       cols: list of column letters; first is sticky row-header.
       rows: list of int row numbers.
       zonecols: (c0,c1) → obarvit řádky podle zóny (jádro/zázemí) z fillu.
       cellfills: True → každá buňka dostane třídu dle zdrojového fillu (oranžová/zelená/…)."""
    def _():
        if caption:
            w(f'  <h3 class="vz-subhead">{esc(caption)}</h3>')
        w('  <div class="vz-mwrap">')
        w('  <div class="vz-matrix" tabindex="0" role="region" aria-label="'
          + esc(caption or "tabulka") + ' – vodorovně posuvná tabulka">')
        w('    <table>')
        w('      <thead><tr>')
        for i, h in enumerate(headers):
            stick = ' class="vz-stickcol"' if i == 0 else ''
            w(f'        <th scope="col"{stick} data-col="{cols[i]}">{esc(h)}</th>')
        w('      </tr></thead>')
        w('      <tbody>')
        for r in rows:
            first = Vrc(r, col2num(cols[0]))
            if first == "":
                continue
            zcls = row_zone(r, zonecols[0], zonecols[1]) if zonecols else ""
            w(f'        <tr class="{zcls}">' if zcls else '        <tr>')
            for i, cl in enumerate(cols):
                c = col2num(cl)
                v = Vrc(r, c)
                if headers[i] == "Rok":
                    v = re.sub(r'\s', '', v)  # roky bez oddělovače tisíců
                fc = cell_fill_class(r, c) if cellfills else ""
                if i == 0:
                    scls = "vz-stickcol" + ((" " + fc) if fc else "") + (" is-red" if is_red(r, c) else "")
                    w(f'          <th scope="row" class="{scls}" data-col="{cl}">{esc(v)}</th>')
                else:
                    cls = []
                    if is_num(v):
                        cls.append("num")
                    if fc:
                        cls.append(fc)
                    if is_red(r, c):
                        cls.append("is-red")
                    clsattr = f' class="{" ".join(cls)}"' if cls else ''
                    w(f'          <td{clsattr} data-col="{cl}">{esc(v)}</td>')
            w('        </tr>')
        w('      </tbody>')
        w('    </table>')
        w('  </div>')
        w('  <button type="button" class="vz-mbtn vz-mbtn--left" aria-label="Posunout tabulku doleva" tabindex="-1">'
          '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M15 5l-7 7 7 7" fill="none" '
          'stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>')
        w('  <button type="button" class="vz-mbtn vz-mbtn--right" aria-label="Posunout tabulku doprava" tabindex="-1">'
          '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M9 5l7 7-7 7" fill="none" '
          'stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>')
        w('  </div>')
        if foot:
            w(f'  <p class="foot">{esc(foot)}</p>')
    return _

IMGDIR = "assets/images/investori/zaklad/"

def vzmap(fn, caption=None):
    """Mapa na celou šířku + (volitelně) popisek."""
    def _():
        w('  <figure class="vz-map">')
        w(f'    <img src="{IMGDIR}{fn}" alt="{esc(caption or "Mapa Areálu")}" loading="lazy">')
        if caption:
            w(f'    <figcaption>{esc(caption)}</figcaption>')
        w('  </figure>')
    return _

def vztotals(items):
    """Zvýrazněné souhrnné boxy (label + velké číslo). items: (label, coord)."""
    def _():
        w('  <div class="vz-totals">')
        for label, coord in items:
            hl = coord_col(coord)
            w(f'    <div class="vz-total" data-hl-col="{hl}">')
            w(f'      <span class="vz-total__label">{esc(label)}</span>')
            w(f'      <span class="vz-total__num">{esc(V(coord))}</span>')
            w('    </div>')
        w('  </div>')
    return _

def breakdown(title, mapfn, area, arealu, sm):
    """Blok „Pozemky": nadpis + (volitelně) mapa + 3 metriky (m² / podíl Areál / podíl SM)."""
    def _():
        w(f'  <h3 class="vz-subhead">{esc(title)}</h3>')
        if mapfn:
            w(f'  <figure class="vz-map"><img src="{IMGDIR}{mapfn}" alt="{esc(title)}" loading="lazy"></figure>')
        w('  <div class="vz-bmetrics">')
        for lab, coord, mod in [("Zatížené parcely (≈)", area, " vz-bm--area"),
                                ("Podíl na ploše Areálu (≈)", arealu, ""),
                                ("Podíl na plochách SM (≈)", sm, "")]:
            w(f'    <div class="vz-bm{mod}"><span class="vz-bm__label">{esc(lab)}</span>'
              f'<span class="vz-bm__num">{esc(V(coord))}</span></div>')
        w('  </div>')
    return _

def vzsummary(items, bg="#E7F0E3", bd="#A8CE9F"):
    """Řada souhrnných boxů (auto-fit). items: (label, coord). Barva přes bg/bd."""
    def _():
        w(f'  <div class="vz-summary" style="--sbox-bg:{bg};--sbox-bd:{bd}">')
        for label, coord in items:
            w(f'    <div class="vz-sbox" data-hl-col="{coord_col(coord)}"><span class="vz-sbox__label">{esc(label)}</span>'
              f'<span class="vz-sbox__num">{esc(V(coord))}</span></div>')
        w('  </div>')
    return _

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

def zonesection(zonetitle, tint, blocks, label=None, shade=False, band="#D4E6C6", bandbd="#88B673"):
    """Zóna s velkým nadpisem (barevný pruh dle --band) místo běžné sechead."""
    cls = "sec sec--shade" if shade else "sec"
    w(f'<section class="{cls}" style="--tint:{tint};--band:{band};--band-bd:{bandbd}" '
      f'aria-label="{esc(label or zonetitle)}">')
    parts = zonetitle.split(" | ", 1)
    if len(parts) > 1:
        w(f'  <h2 class="vz-zonehead">{esc(parts[0])}'
          f'<span class="vz-zonehead__sub">{esc(parts[1])}</span></h2>')
    else:
        w(f'  <h2 class="vz-zonehead">{esc(zonetitle)}</h2>')
    for b in blocks:
        b()
    w('</section>')

def figrow(items):
    """3 obrázky vedle sebe, popisek pod každým. items: (filename, caption)."""
    def _():
        w('  <div class="vz-figrow">')
        for fn, cap in items:
            w(f'    <figure><img src="{IMGDIR}{fn}" alt="{esc(cap)}" loading="lazy">'
              f'<figcaption>{esc(cap)}</figcaption></figure>')
        w('  </div>')
    return _

def flowblock(blocks):
    """Obal (tabulka + souhrn) — JS dokreslí velký pravý ribbon spojující poslední
    sloupec tabulky s posledním souhrnným boxem (jako zahnutá šipka v originále)."""
    def _():
        w('  <div class="vz-flowblock">')
        for b in blocks:
            b()
        w('    <svg class="vz-bigribbon" aria-hidden="true"></svg>')
        w('  </div>')
    return _

def greenband(text, center=False):
    """Titulní zelený pruh dílčí tabulky."""
    cls = "vz-greenband" + (" vz-greenband--center" if center else "")
    return lambda: w(f'  <p class="{cls}">{esc(text)}</p>')

def paramstrip(items):
    """Vstupní parametry jako boxy; barva dle zdrojového fillu hodnoty.
    items: (label, value_coord, is_source?) — is_source označí box jako počátek konektoru."""
    def _():
        w('  <div class="vz-params">')
        for it in items:
            label, coord = it[0], it[1]
            src = ' data-flow-source' if (len(it) > 2 and it[2]) else ''
            m = re.match(r'^([A-Z]+)(\d+)$', coord)
            c, r = col2num(m.group(1)), int(m.group(2))
            fc = cell_fill_class(r, c)
            red = " is-red" if is_red(r, c) else ""
            w(f'    <div class="vz-param {fc}"{src}><span class="vz-param__label">{esc(label)}</span>'
              f'<span class="vz-param__num{red}">{esc(V(coord))}</span></div>')
        w('  </div>')
    return _

def section_draft(*a, **k):
    """První pokusy (jednotky/lůžka/Nová čtvrť/zdroje) zatím nerenderujeme — čekají na revizi."""
    pass

def figs(items, label="Vizualizace"):
    """items: list of (filename, caption). Vodorovně posuvný proužek figur."""
    def _():
        w(f'  <div class="vz-figs" role="group" aria-label="{esc(label)}">')
        for fn, cap in items:
            w(f'    <figure><img src="{IMGDIR}{fn}" alt="{esc(cap)}" loading="lazy">')
            w(f'      <figcaption>{esc(cap)}</figcaption></figure>')
        w('  </div>')
    return _

# ============================================================
# COVER
# ============================================================
w('<div class="vz">')
w('  <main class="wrap">')
w('    <header class="cover">')
w('      <p class="kicker">Základní údaje &amp; výpočty</p>')
w('      <h1 class="vpd">VPD1</h1>')
w('      <p class="upd">areál Horních kasáren v Klecanech u Prahy (dále jen „Areál")</p>')
w('    </header>')

# ============================================================
# 1) TABULKA SE ZÁKLADNÍMI INFORMACEMI č. 1  (sloupce A–H + mapy + breakdowny)
# ============================================================
parcel_rows = list(range(8, 37))

t1_headers = ["Číslo parcely", "Zkratka", "Výměra parcely v KN",
              "Současným ÚP navrhované využití", "Etapizace výstavby",
              "Výměra parcel zařazených do SM"]
t1_cols = ["C", "D", "E", "F", "G", "H"]

section("Tabulka se základními informacemi č. 1", "#E6ECF6", [
    vzmap("mapa-arealu-masterplan.jpg",
          "Mapa Areálu se schématickým zákresem 1. developerské fáze investičně-realizačního scénáře S1"),
    matrix(t1_headers, t1_cols, parcel_rows, zonecols=(3, 8),
           foot="Plochy SM = plochy smíšené obytné – městské dle současného ÚP. "
                "Žlutě jádro projektu (budovy Startovacího hubu), zeleně zázemí."),
    vztotals([("Celková výměra parcel", "E39"),
              ("Celková výměra ploch SM", "H39")]),
    breakdown("Pozemky: jádro projektu Startovací hub",
              "schema-ortofoto-zony-1.jpg", "C43", "E43", "E45"),
    breakdown("Pozemky: jádro + zázemí projektu Startovací hub (celek)",
              "schema-ortofoto-zony-2.jpg", "C70", "E70", "E72"),
    breakdown("Zázemí projektu Startovací hub (celek mínus jádro)",
              None, "C119", "E119", "E121"),
], label="Tabulka se základními informacemi č. 1 — parcely Areálu a podíly zón")

# ============================================================
# 2) TABULKA SE ZÁKLADNÍMI INFORMACEMI č. 2  (sloupce K–X: stavby, podlaží, HPP)
# ============================================================
t2_headers = ["Číslo parcely",
              "Předpokládaná kolaudace (stavební dokumentace k Areálu je neúplná):",
              "Odhad rozsahu všech zpevněných ploch v Areálu",
              "Současnými stavbami zastavěné plochy v Areálu",
              "Pozemky: jádro projektu Startovací hub",
              "Počet nadzemních podlaží", "Počet podzemních podlaží", "Celkem podlaží",
              "HPP stávajících budov (dle katastru)",
              "HPP jádra projektu Startovací hub",
              "HPP jádra projektu Startovací hub určené pro budování jednotek 1+kk",
              "HPP zázemí projektu Startovací hub",
              "HPP všech budov netvořících jádro projektu Startovací hub",
              "HPP jádra i zázemí projektu Startovací hub"]
t2_cols = ["K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X"]

section("Tabulka se základními informacemi č. 2", "#E6ECF6", [
    matrix(t2_headers, t2_cols, parcel_rows, zonecols=(11, 24),
           caption="Stavby, podlažnost a hrubé podlažní plochy (HPP) po parcelách",
           foot="Žlutě jádro projektu Startovací hub (budovy A1–A6, štáb, hlavní pozemek), "
                "zeleně zázemí projektu."),
    subhead("Souhrn ploch a HPP"),
    vzsummary([("Zpevněné plochy", "M39"),
               ("Zastavěné plochy", "N39"),
               ("Pozemky: jádro projektu SH", "O39")]),
    note("*celkem z ploch SM: 15 %"),
    vzsummary([("HPP stávajících budov", "S39"),
               ("HPP jádra projektu SH", "T39"),
               ("HPP určené pro jednotky 1+kk (SH)", "U39"),
               ("HPP zázemí projektu SH", "V39"),
               ("HPP kolem jádra projektu SH", "W39"),
               ("HPP jádra i zázemí projektu SH", "X39")]),
], label="Tabulka se základními informacemi č. 2 — stavby a HPP", shade=True)

# ============================================================
# 3) ZÓNA: Základní údaje a výpočty vyplývající z uzavřených smluv
# ============================================================
zalohy = matrix(
    ["Rok", "Pořadí", "Splatnost zálohy", "Výše zálohy k uhrazení",
     "Equita na odkup Areálu odložená u majitele"],
    ["AC", "AD", "AE", "AF", "AG"], list(range(8, 24)),
    cellfills=True)

def mimo_zaloha():
    w('  <p class="vz-greenband vz-greenband--center">Mimořádná záloha (tzv. příspěvek na příjezdovou cestu)</p>')
    w('  <div class="vz-kv">')
    w('    <div class="row"><div class="lab">Splatnost do 90 dní od vydání stavebního povolení na novou '
      'cestu se smluvně stanovenými parametry, která bude přiléhat k východní části Areálu</div>'
      f'<div class="val num is-green">{esc(V("AF27"))}</div></div>')
    w('    <div class="row"><div class="lab">Equita na odkup Areálu odložená u majitele po této záloze</div>'
      f'<div class="val num">{esc(V("AG27"))}</div></div>')
    w('  </div>')

cena_params = paramstrip([
    ("Maximální míra inflace do 2039 na úrovni:", "AJ6"),
    ("Sjednaný základ kupní ceny", "AN6"),
    ("Plocha Areálu", "AS6"),
    ("Plochy SM v Areálu", "AU6"),
])

cena_calc = matrix(
    ["Rok", "Od", "Do", "Přírůstek k základu kupní ceny (min. 5 %)*", "Vypočtené navýšení kupní ceny",
     "Kupní cena za celý Areál", "Záloha splatná v příslušném roce", "Celkem uhrazené zálohy (Equita)",
     "Po odečtení záloh zbývá k doplacení", "Cena za m² všech ploch", "Cena za m² všech ploch k doplacení",
     "Cena za m² všech ploch SM", "Cena za m² všech ploch SM k doplacení",
     "Meziroční nárůst ceny Areálu v %", "Kolik % z ceny Areálu uhradit formou zálohy"],
    ["AJ", "AK", "AL", "AM", "AN", "AO", "AP", "AQ", "AR", "AS", "AT", "AU", "AV", "AW", "AX"],
    list(range(8, 24)), cellfills=True,
    foot="*sjednaná kupní cena Areálu se každoročně k 10. 3. navyšuje v souladu s čl. 3 Smlouvy "
         "o 19 250 000 Kč, pokud inflace CPI za předchozí rok nepřekročí 5 %.")

def smlouva_cl3():
    """Citace čl. 3 uzavřené Smlouvy (přepis z původního obrázku do textu)."""
    arts = [
        ("3.1", 'Strana budoucí kupující se zavazuje zaplatit Straně budoucí prodávající za Předmět převodu '
                'kupní cenu ve výši, která bude složena ze základu kupní ceny ve výši <strong>385 000 000,- Kč</strong> '
                '(slovy: <em>tři sta osmdesát pět milionů korun českých</em>) a částky odpovídající míře inflace, '
                'respektive částky stanovené postupem uvedeným níže v čl. 3 a 4 této Smlouvy.'),
        ("3.2", 'Základ kupní ceny ve výši <strong>385 000 000,- Kč</strong> (slovy: <em>tři sta osmdesát pět milionů '
                'korun českých</em>) (dále jen jako „Základ kupní ceny“) <strong>bude každoročně dne 10. března '
                'příslušného roku navýšen</strong> o procento odpovídající počtu procentních bodů meziroční inflace '
                '(dále jen „Míra inflace“) vyhlášené Českým statistickým úřadem za předchozí kalendářní rok, a to po '
                'celou dobu platnosti této Smlouvy až do uzavření Smlouvy o převodu obchodního podílu. K navýšení '
                'Základu kupní ceny nedojde v případě, že již byla učiněna výzva k uzavření Smlouvy o převodu '
                'obchodního podílu dle čl. 2.4 této Smlouvy.'),
        ("3.3", 'V případě, že Míra inflace nepřesáhne za příslušný kalendářní rok 5 procentních bodů, pak se Smluvní '
                'strany dohodly, že za takovýto kalendářní rok se Základ kupní ceny navýší o 5 procentních bodů '
                'počítaných ze Základu kupní ceny (tedy o částku ve výši <strong>19 250 000,- Kč</strong>).'),
        ("3.4", 'Pro vyloučení jakýchkoliv pochybností se sjednává, že v případě záporné Míry inflace se kupní cena '
                'Předmětu převodu nesnižuje, ale uplatní se postup uvedený v článku 3.3 této Smlouvy výše.'),
        ("3.5", 'Za kalendářní rok, ve kterém bude uzavřena tato Smlouva, se bude Základ kupní ceny k 10. 3. '
                'následujícího roku navyšovat pouze poměrným způsobem v souladu s články 3.2 až 3.4 této Smlouvy '
                'v souladu s níže uvedeným vzorcem.'),
    ]
    w('  <blockquote class="vz-quote">')
    w('    <p class="vz-quote__head">3.&nbsp;&nbsp;Kupní cena a způsob jejího určení</p>')
    w('    <dl class="vz-quote__list">')
    for n, t in arts:
        w(f'      <div><dt>{n}</dt><dd>{t}</dd></div>')
    w('      <div><dt>3.6</dt><dd>Výpočet výše navýšení Základu kupní ceny za příslušný rok se řídí následujícím '
      'vzorcem:<span class="vz-quote__formula">VNZ = ZKC × MI × P / 12</span>'
      '<span class="vz-quote__where">kde<br>'
      '<strong>VNZ</strong> je číselně vyjádřené navýšení Základu kupní ceny<br>'
      '<strong>ZKC</strong> je Základ kupní ceny uvedený v této smlouvě<br>'
      '<strong>MI</strong> je příslušná Míra inflace za předchozí rok (minimální dosazovaná hodnota bude 5 %)<br>'
      '<strong>P</strong> je počet celých měsíců trvání této Smlouvy v příslušném roce.</span></dd></div>')
    w('      <div><dt>3.7</dt><dd>Kupní cenu Předmětu převodu tvoří součet Základu kupní ceny a každoročně číselně '
      'vyjádřeného navýšení Základu kupní ceny; přičemž toto číselné vyjádření navýšení Základu kupní ceny je '
      'stanoveno postupem uvedeným výše (dále jen jako „Kupní cena“).</dd></div>')
    w('    </dl>')
    w('  </blockquote>')

zonesection("Základní údaje a výpočty vyplývající z uzavřených smluv", "#EEF1F6", [
    greenband("Sjednané zálohy na kupní cenu Areálu"),
    zalohy,
    mimo_zaloha,
    greenband("Výpočet současné kupní ceny Areálu + predikce budoucí kupní ceny Areálu "
              "na základě uzavřené smlouvy"),
    cena_params,
    cena_calc,
    greenband("Způsob výpočtu navýšení kupní ceny Areálu uvedený v uzavřené Smlouvě", center=True),
    smlouva_cl3,
], label="Základní údaje a výpočty vyplývající z uzavřených smluv")

# ============================================================
# 3) STARTOVACÍ HUB — JEDNOTKY 1+kk
# ============================================================
hub_params = paramstrip([
    ("Odhadované tržní nájemné za jednotku 1+kk (21 m² ČPP), měsíčně bez služeb", "BO6"),
    ("Obsazenost", "BQ6"),
])

hub_prijem = matrix(
    ["Číslo parcely", "Označení", "Název", "1.NP", "2.NP", "3.NP",
     "Odhadovaný počet jednotek v příslušné budově",
     "Měsíční příjem z pronajímání příslušných jednotek",
     "Roční příjem z pronajímání příslušných jednotek"],
    ["BI", "BJ", "BK", "BL", "BM", "BN", "BO", "BP", "BQ"], list(range(10, 27)),
    cellfills=True, zonecols=(61, 69))

hub_souhrn = vzsummary([
    ("Potenciální množství všech jednotek (1+kk)", "BL39"),
    ("Plánovaný počet jednotek (1+kk)", "BO39"),
    ("Odhadovaná měsíční výše příjmů z pronájmu", "BP39"),
    ("Odhadovaná výše ročních příjmů z pronájmu", "BQ39"),
], bg="#F2ECC9", bd="#D8CD7E")

# benchmark: odhad tržního nájemného (odhad-zdarma.cz) — dva odhady
hub_bench = matrix(
    ["Tržní nájemné za měsíc", "Plocha (ČPP)", "Cena za m²"],
    ["BO", "BP", "BQ"], [41, 42], cellfills=True)

# ---- finále: 5 tabulek (BS–CZ) ----
t20_params = paramstrip([
    ("Odhadovaná výše příjmu pro rok 2026", "BS6", True),
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
    ("Hlavní příjmy projektu Startovací hub do konce roku 2038:", "CB39", False),
])

t22_params = paramstrip([
    ("Odhadovaná prodejní cena jedné jednotky 1+kk o ČPP cca 21 m² v příslušné lokalitě "
     "pro rok 2026", "CL6", True),
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
    ("Odhadovaná tržní cena všech jednotek (2026)", "CP6", True),
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
    ("Odhad tržní ceny jednotek vzniklých pro projekt Startovací hub (2026)", "CX6", True),
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

zonesection(
    "Projekt Startovací hub | orientační výpočty týkající se potenciálních příjmů plynoucích "
    "z jádra projektu složeného výhradně z jednotek 1+kk o 21 m² ČPP, které může vzniknout "
    "komplexní rekonstrukcí budov A1 až A6 + C",
    "#FBFAF0", [
        greenband("Odhad příjmů z pronájmu jednotek vzniklých pro projekt Startovací hub"),
        hub_params,
        hub_prijem,
        hub_souhrn,
        subhead("Vizualizace"),
        figrow([
            ("render-jednotka-1kk-interier.jpg", "Vizualizace interiéru: jednotka 1+kk o 21 m² ČPP"),
            ("render-exterier-jadro-vecer.jpg", "Vizualizace exteriéru: jádro projektu Startovací hub"),
            ("render-exterier-plaza.jpg", "Vizualizace exteriéru: budova D – ateliéry / dílny"),
        ]),
        greenband("Odhad tržního nájemného pro jednotku 1+kk o ČPP 21 m² v příslušné lokalitě "
                  "(www.odhad-zdarma.cz, k 18. 1. 2026)", center=True),
        hub_bench,
        vzmap("zdroj-odhad-najemneho.jpg",
              "Odhad tržního nájemného srovnatelné nemovitosti (oceňovací nástroj odhad-zdarma.cz)"),
        # --- finále: 5 tabulek (konektor spojuje vstupní parametr s cílovým souhrnem) ---
        greenband("Odhadovaný meziroční nárůst příjmů z pronájmu jednotek vzniklých pro projekt Startovací hub"),
        flowblock([t20_params, t20_matrix, t20_grand]),
        greenband("Hrubé porovnání hlavních provozních příjmů a nákladů projektu Startovací hub"),
        t21_matrix,
        t21_grand,
        greenband("Odhad tržní ceny všech jednotek vzniklých pro projekt Startovací hub"),
        flowblock([t22_params, t22_matrix, t22_grand]),
        greenband("Odhad tržní ceny jedné jednotky 1+kk o ČPP 21 m² v příslušné lokalitě "
                  "(www.odhad-zdarma.cz, k 18. 1. 2026)", center=True),
        t22_bench,
        vzmap("zdroj-odhad-prodejni-ceny.jpg",
              "Odhad tržní prodejní ceny srovnatelné nemovitosti (oceňovací nástroj odhad-zdarma.cz)"),
        greenband("Odhadovaný nárůst tržní ceny jednotek vzniklých pro projekt Startovací hub"),
        flowblock([t24_params, t24_matrix, t24_grand]),
        greenband("Rozdíl mezi nákupní cenou Areálu a tržní cenou jednotek vzniklých pro projekt Startovací hub"),
        flowblock([t25_params, t25_matrix, t25_grand]),
    ],
    label="Projekt Startovací hub — orientační výpočty příjmů z pronájmu jednotek 1+kk",
    shade=True, band="#E9E2A8", bandbd="#CDBF6E")

# ============================================================
# 4) STARTOVACÍ HUB — LŮŽKA VE SDÍLENÝCH POKOJÍCH (sloupce DM–DV)
# ============================================================
luzka_params = paramstrip([
    ("Index pro převod HPP příslušných budov na ČPP pokojů k ubytovávání hostů", "DP6"),
    ("Počet ČPP na jedno lůžko", "DR6"),
    ("Odhad tržního nájemného za jedno lůžko (měsíčně vč. služeb)", "DT6"),
    ("Odhadované náklady na základní služby v přepočtu na jedno lůžko (měsíčně)", "DU6"),
    ("Obsazenost", "DV6", True),
])
luzka_matrix = matrix(
    ["Číslo parcely", "Označení", "Název", "HPP příslušných budov", "ČPP pokojů s lůžky",
     "Počet lůžek v budově", "Měsíční příjem z pronajímání lůžek", "Měsíční náklad na služby",
     "Příjem projektu očištěný o služby"],
    ["DM", "DN", "DO", "DP", "DQ", "DR", "DT", "DU", "DV"], list(range(10, 27)),
    cellfills=True, zonecols=(117, 126),
    foot="Žlutě jádro projektu Startovací hub, zeleně zázemí. Pokoje s lůžky vznikají dílčí "
         "rekonstrukcí budov A1–A6 + C.")
luzka_grand = vzgrand([
    ("Celkový počet lůžek:", "DR39", False),
    ("Odhadovaná výše měsíčních příjmů:", "DT39", False),
    ("Odhadovaná výše měsíčních nákladů na služby:", "DU39", False),
    ("Odhadovaný roční příjem (očištěný o služby):", "DV39", True),
])

zonesection(
    "Projekt Startovací hub | orientační výpočty týkající se potenciálních příjmů plynoucích "
    "z jádra projektu složeného výhradně ze sdílených pokojů, které může vzniknout dílčí "
    "rekonstrukcí budov A1 až A6 + C",
    "#FBFAF0", [
        greenband("Odhad příjmů z pronájmu lůžek ve sdílených pokojích vzniklých pro projekt Startovací hub"),
        flowblock([luzka_params, luzka_matrix, luzka_grand]),
        subhead("Vizualizace"),
        figs([("render-sdileny-pokoj-interier.jpg",
               "Vizualizace interiéru: sdílený pokoj vybavený lůžky se zvýšenou privátní ochranou")],
             label="Vizualizace sdíleného pokoje"),
        greenband("Odhad tržní ceny ubytování za jedno lůžko ve sdíleném pokoji "
                  "(pracovní model pro investiční záměr, k 1. 5. 2026)", center=True),
        vzmap("zdroj-cena-ubytovani-luzko.jpg",
              "Odhad ceny ubytování za jedno lůžko ve sdíleném pokoji (pracovní model)"),
        greenband("Odhad provozních nákladů (voda, elektřina, teplo) na jedno lůžko "
                  "(pracovní model, k 1. 5. 2026)", center=True),
        vzmap("zdroj-naklady-luzko.jpg",
              "Odhad provozních nákladů na jedno lůžko v přepočtu na měsíc (pracovní model)"),
    ],
    label="Projekt Startovací hub — orientační výpočty příjmů z pronájmu lůžek ve sdílených pokojích",
    band="#E9E2A8", bandbd="#CDBF6E")

# ============================================================
# 5) NOVÁ ČTVRŤ (sloupce EH–ES; benchmark bytů EH–EN, řádky 188–214)
# ============================================================
nc_params = paramstrip([
    ("Zastavitelnost Areálu", "EH6"),
    ("Podlažnost pro plochy SM v rámci Areálu", "EJ6"),
    ("Plochy SM v Areálu", "EK6"),
    ("Kolik % z maxima HPP dle současného ÚP se podaří zrealizovat", "EL6"),
    ("Index pro převod HPP na ČPP", "EM6"),
    ("Index meziročního nárůstu cen stavebních prací", "EN6"),
    ("Podíl projekčních / přípravných prací", "EO6"),
    ("Odhadovaná cena za vybudování 1 m² ČPP (2026)", "EP6"),
    ("Index meziročního nárůstu prodejní ceny bytů", "EQ6"),
    ("Odhadovaná tržní cena m² ČPP (2026, novostavby)", "ER6", True),
])
nc_matrix = matrix(
    ["Rok", "Kupní cena celého areálu", "Nárůst ceny bytových jednotek v lokalitě",
     "HPP (m²)", "ČPP (m²)", "Index meziroč. nárůstu cen stavebních prací",
     "Odhadovaný náklad na výstavbu příslušných ČPP", "Odhadovaná cena projekčních / přípravných prací",
     "Index nárůstu prodejních cen bytů", "Odhadovaná prodejní cena všech ČPP v Areálu",
     "Odhadovaná pořizovací cena Areálu vč. stavebních a projekčních prací",
     "Teoretický hrubý zisk z rozprodeje rozvinutého Areálu"],
    ["EH", "EI", "EJ", "EK", "EL", "EM", "EN", "EO", "EP", "EQ", "ER", "ES"],
    list(range(8, 24)), cellfills=True)
nc_grand = vzgrand([
    ("Potenciální hrubý zisk před zdaněním z rozprodeje stavební činností plně rozvinutého "
     "Areálu v roce 2038 v souladu se zvolenými parametry:", "EQ39", True),
])
nc_bench = matrix(
    ["Název", "Dispozice", "Plocha (m²)", "Podlaží", "Cena (Kč)", "Cena za m²"],
    ["EH", "EI", "EJ", "EK", "EL", "EN"], list(range(188, 215)),
    cellfills=True,
    foot="Průměrná cena za m²: 140 393 Kč. Uvedené ceny jsou informativní (závazná je smluvní "
         "dokumentace prodejce). Zdroj: www.creditasre.cz/projekty/klecanska-alej k 22. 9. 2025.")

zonesection(
    "Projekt Nová čtvrť | orientační výpočty hrubých příjmů a nákladů developerského rozvoje "
    "celého Areálu do podoby nové městské čtvrti",
    "#EEF3FA", [
        greenband("Odhad hrubých příjmů a nákladů ve vztahu k developerskému rozvoji celého Areálu"),
        flowblock([nc_params, nc_matrix, nc_grand]),
        subhead("Vizualizace a hmotové studie"),
        figs([("schema-hmota-letecky-1.jpg", "Hmotová studie Nové čtvrti – letecký pohled (1)"),
              ("schema-hmota-letecky-2.jpg", "Hmotová studie Nové čtvrti – letecký pohled (2)"),
              ("schema-hmota-letecky-3.jpg", "Hmotová studie Nové čtvrti – letecký pohled (3)"),
              ("schema-zony-zakres.jpg", "Schéma zón se zákresem budov")],
             label="Hmotové studie Nové čtvrti"),
        greenband("Nabídkové ceny bytů v novostavbách v příslušné lokalitě (benchmark tržní ceny m² ČPP)"),
        nc_bench,
        vzmap("zdroj-nabidka-bytu-web.jpg",
              "Nabídkové ceny bytů v novostavbě poblíž Areálu (www.creditasre.cz, k 22. 9. 2025)"),
    ],
    label="Projekt Nová čtvrť — orientační výpočty developerského rozvoje Areálu",
    shade=True, band="#CBDDF1", bandbd="#8BB9E4")

# ============================================================
# 6) ZDROJE & PŘEDPOKLADY
# ============================================================
def zdroje():
    items=[
        "Odhad tržního nájemného pro jednotku 1+kk (21 m² ČPP) vychází z nabídek v příslušné lokalitě.",
        "Odhad tržní ceny jedné jednotky 1+kk (21 m² ČPP) vychází z porovnání s lokalitou.",
        "Část odhadů (zejm. pronájem lůžek) byla vytvořena pro projekt aplikací ChatGPT (1. 5. 2026).",
        "Nabídkové ceny bytů v novostavbách: www.creditasre.cz/projekty/klecanska-alej (k 22. 9. 2025).",
        "Způsob výpočtu navýšení kupní ceny Areálu je uveden v uzavřené Smlouvě (čl. 3).",
    ]
    w('  <ul class="vz-sources">')
    for it in items:
        w(f'    <li>{esc(it)}</li>')
    w('  </ul>')

zdroje_figs = figs([
    ("zdroj-nabidka-bytu-web.jpg", "Nabídkové ceny bytů v novostavbě poblíž Areálu (creditasre.cz)"),
    ("zdroj-odhad-najemneho.jpg", "Odhad tržního nájemného nemovitosti (oceňovací nástroj)"),
    ("zdroj-odhad-prodejni-ceny.jpg", "Odhad tržní prodejní ceny nemovitosti (oceňovací nástroj)"),
    ("zdroj-cena-ubytovani-luzko.jpg", "Odhad ceny ubytování za lůžko ve sdíleném pokoji (model)"),
    ("zdroj-naklady-luzko.jpg", "Odhad provozních nákladů na jedno lůžko (model)"),
    ("zdroj-smlouva-vypocet-navyseni.jpg", "Způsob výpočtu navýšení kupní ceny Areálu (ze smlouvy)"),
], label="Podkladové materiály")

section_draft("Zdroje a předpoklady", "#F6E6EC", [
    zdroje,
    subhead("Podkladové materiály"),
    zdroje_figs,
], lede="Orientační výpočty stojí na níže uvedených předpokladech a externích zdrojích.")

# ============================================================
# FOOTER
# ============================================================
w('    <footer class="vzver">')
w('      <p>verze 2p8iaz6 · aktualizace č. 2026-06-15-2p8iaz6</p>')
w('      <p>[PRACOVNÍ VERZE 2p8iaz6 z 15. 6. 2026]</p>')
w('    </footer>')
w('  </main>')
w('</div>')

open(SCRATCH + "/body.html", "w").write("\n".join(OUT))
print("body.html written:", len("\n".join(OUT)), "bytes,", len(OUT), "lines")
