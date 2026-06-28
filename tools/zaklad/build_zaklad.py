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
ORANGE = "FFEBC08F"

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

def esc(s):
    return _html.escape(str(s), quote=True)

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
def section(title, tint, blocks, label=None, lede=None):
    w(f'<section class="sec" style="--tint:{tint}" aria-label="{esc(label or title)}">')
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

def matrix(headers, cols, rows, caption=None, foot=None):
    """headers: list of clean header strings (len == len(cols)).
       cols: list of column letters; first is sticky row-header.
       rows: list of int row numbers."""
    def _():
        if caption:
            w(f'  <h3 class="vz-subhead">{esc(caption)}</h3>')
        w('  <div class="vz-matrix" tabindex="0" role="region" aria-label="'
          + esc(caption or "tabulka") + ' – vodorovně posuvná tabulka">')
        w('    <table>')
        w('      <thead><tr>')
        for i, h in enumerate(headers):
            scope = 'col'
            w(f'        <th scope="{scope}"{" class=\"vz-stickcol\"" if i==0 else ""}>{esc(h)}</th>')
        w('      </tr></thead>')
        w('      <tbody>')
        for r in rows:
            first = Vrc(r, col2num(cols[0]))
            if first == "":
                continue
            w('        <tr>')
            for i, cl in enumerate(cols):
                c = col2num(cl)
                v = Vrc(r, c)
                if headers[i] == "Rok":
                    v = re.sub(r'\s', '', v)  # roky bez oddělovače tisíců
                if i == 0:
                    w(f'          <th scope="row" class="vz-stickcol">{esc(v)}</th>')
                else:
                    cls = []
                    if is_num(v):
                        cls.append("num")
                    clsattr = f' class="{" ".join(cls)}"' if cls else ''
                    w(f'          <td{clsattr}>{esc(v)}</td>')
            w('        </tr>')
        w('      </tbody>')
        w('    </table>')
        w('  </div>')
        if foot:
            w(f'  <p class="foot">{esc(foot)}</p>')
    return _

IMGDIR = "assets/images/investori/zaklad/"
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
# 1) AREÁL — PARCELY & PLOCHY
# ============================================================
parcel_headers = ["Parcela","Zkratka","Výměra (KN)","Využití dle ÚP","Etap.","Výměra v SM",
                  "Účel / název","Zpevněné","Zastavěné","Pozemky jádro","NP","PP","Podlaží",
                  "HPP stávajících","HPP jádra","HPP pro 1+kk","HPP zázemí","HPP mimo jádro","HPP jádra+zázemí"]
parcel_cols = ["C","D","E","F","G","H","L","M","N","O","P","Q","R","S","T","U","V","W","X"]
parcel_rows = list(range(8,37))

plochy = kv([
    ("Celková výměra parcel","E39"),
    ("Celková výměra ploch SM","H39"),
    ("Zpevněné plochy","M39"),
    ("Zastavěné plochy","N39"),
    ("Pozemky: jádro projektu Startovací hub","O39"),
    ("HPP stávajících budov","S39"),
    ("HPP jádra projektu Startovací hub","T39"),
    ("HPP určené pro jednotky 1+kk","U39"),
    ("HPP zázemí projektu Startovací hub","V39"),
    ("HPP budov mimo jádro","W39"),
    ("HPP jádra i zázemí projektu Startovací hub","X39"),
])

def podily():
    rows=[("Jádro projektu Startovací hub","C43","E43","E45"),
          ("Jádro + zázemí (celek)","C70","E70","E72"),
          ("Zázemí (celek − jádro)","C119","E119","E121")]
    w('  <h3 class="vz-subhead">Podíly zón na Areálu</h3>')
    w('  <div class="vz-matrix" role="region" aria-label="Podíly zón">')
    w('    <table><thead><tr>'
      '<th scope="col" class="vz-stickcol">Zóna</th>'
      '<th scope="col">Zatížené parcely (≈)</th>'
      '<th scope="col">Podíl na ploše Areálu</th>'
      '<th scope="col">Podíl na plochách SM</th>'
      '</tr></thead><tbody>')
    for name,a,b,c in rows:
        w(f'      <tr><th scope="row" class="vz-stickcol">{esc(name)}</th>'
          f'<td class="num">{esc(V(a))}</td><td class="num">{esc(V(b))}</td><td class="num">{esc(V(c))}</td></tr>')
    w('    </tbody></table></div>')

section("Areál · parcely a plochy", "#E6ECF6", [
    matrix(parcel_headers, parcel_cols, parcel_rows,
           caption="Inventura parcel (tab. č. 1 a č. 2)",
           foot="Plochy SM = plochy smíšené obytné – městské dle současného ÚP."),
    subhead("Souhrn ploch a HPP"),
    plochy,
    note("*celkem z ploch SM: 15 %"),
    podily,
])

# ============================================================
# 2) SMLOUVY — KUPNÍ CENA AREÁLU
# ============================================================
cena_inputs = kv([
    ("Maximální míra inflace uvažovaná do roku 2039","AJ6"),
    ("Sjednaný základ kupní ceny","AN6"),
    ("Plocha Areálu","AS6"),
    ("Plochy SM v Areálu","AU6"),
], inputs=True)

zalohy = matrix(
    ["Rok","Pořadí","Splatnost zálohy","Výše zálohy","Equita odložená u majitele"],
    ["AC","AD","AE","AF","AG"], list(range(8,24)),
    caption="Sjednané zálohy na kupní cenu Areálu")

cena_calc = matrix(
    ["Rok","Od","Do","Přírůstek (min. 5 %)","Vypočtené navýšení","Kupní cena za celý Areál",
     "Záloha splatná v roce","Celkem uhrazené zálohy","Po odečtení záloh zbývá",
     "Cena/m² všech ploch","Cena/m² k doplacení","Cena/m² SM","Cena/m² SM k doplacení",
     "Meziroční nárůst","% zálohy z ceny"],
    ["AJ","AK","AL","AM","AN","AO","AP","AQ","AR","AS","AT","AU","AV","AW","AX"],
    list(range(8,24)),
    caption="Výpočet současné a predikce budoucí kupní ceny Areálu (2023–2038)",
    foot="*sjednaná kupní cena Areálu se každoročně k 10. 3. navyšuje v souladu s čl. 3 Smlouvy "
         "o 19 250 000 Kč, pokud inflace CPI za předchozí rok nepřekročí 5 %.")

def mimo_zaloha():
    w('  <h3 class="vz-subhead">Mimořádná záloha</h3>')
    w('  <div class="vz-kv"><div class="row">'
      f'<div class="lab">{esc("Mimořádná záloha (příspěvek na příjezdovou cestu) — splatnost do 90 dní od vydání stavebního povolení na novou cestu se smluvně stanovenými parametry přiléhající k východní části Areálu")}</div>'
      f'<div class="val num">{esc(V("AF27"))}</div></div>'
      f'<div class="row"><div class="lab">Equita odložená u majitele po této záloze</div>'
      f'<div class="val num">{esc(V("AG27"))}</div></div></div>')

section("Smlouvy · kupní cena Areálu", "#ECE6F6", [
    legend_input(),
    subhead("Vstupní parametry"),
    cena_inputs,
    zalohy,
    flow("Celkem uhrazené zálohy (Equita) → snižují částku „Po odečtení záloh zbývá k doplacení"),
    cena_calc,
    mimo_zaloha,
], label="Základní údaje a výpočty vyplývající z uzavřených smluv")

# ============================================================
# 3) STARTOVACÍ HUB — JEDNOTKY 1+kk
# ============================================================
j_inputs = kv([
    ("Odhadované tržní nájemné za jednotku 1+kk (21 m² ČPP) měsíčně","BO6"),
    ("Obsazenost","BQ6"),
    ("Odhadovaná prodejní cena jedné jednotky 1+kk (2026)","CL6"),
    ("Zvolený index meziročního růstu ceny nemovitostí","CR6"),
], inputs=True)

j_prijem = matrix(
    ["Parcela","Označení","Název","1.NP","2.NP","3.NP","Počet jednotek","Měsíční příjem","Roční příjem"],
    ["BI","BJ","BK","BL","BM","BN","BO","BP","BQ"], list(range(10,27)),
    caption="Odhad příjmů z pronájmu jednotek (po budovách)")

j_narust = matrix(
    ["Rok","Meziroční růst","Příjem v daném roce","Akumulované příjmy"],
    ["BS","BT","BU","BV"], list(range(8,24)),
    caption="Odhadovaný meziroční nárůst příjmů z pronájmu")

j_porovnani = matrix(
    ["Rok","Příjem v roce","Záloha na kupní cenu","Rozdíl příjmů a nákladů","Akumulovaný rozdíl"],
    ["BY","BZ","CA","CB","CC"], list(range(8,24)),
    caption="Hrubé porovnání hlavních provozních příjmů a nákladů")

j_trzni = matrix(
    ["Parcela","Označení","Název","Celkem podlaží","Podlaží pro rekonstrukci","Počet jednotek","Tržní cena jednotek v budově"],
    ["CG","CH","CI","CJ","CK","CL","CM"], list(range(10,27)),
    caption="Odhad tržní ceny jednotek (po budovách, 2026)")

j_trzni_narust = matrix(
    ["Rok","Index růstu","Odhadovaná tržní cena všech jednotek"],
    ["CP","CQ","CR"], list(range(8,24)),
    caption="Odhadovaný nárůst tržní ceny jednotek")

j_rozdil = matrix(
    ["Rok","Přírůstek prodejní ceny","Prodejní cena jednotek","Kupní cena Areálu","K doplacení po zálohách","Rozdíl (trh − doplatek)"],
    ["CU","CV","CW","CX","CY","CZ"], list(range(8,24)),
    caption="Rozdíl mezi kupní cenou Areálu a tržní cenou jednotek")

j_souhrn = kv([
    ("Odhadované příjmy z pronájmu jednotek do konce roku 2038","BV39"),
    ("Cena Areálu po odečtení uhrazených záloh (konec 2038)","BZ39"),
    ("Hlavní příjmy projektu Startovací hub do konce 2038","CB39"),
    ("Odhadovaný rozdíl mezi prodejní cenou jednotek a doplatkem (2038)","CX39"),
])

section("Startovací hub · jednotky 1+kk", "#E7F0E3", [
    subhead("Vstupní parametry"),
    j_inputs,
    flow("Tržní nájemné × obsazenost → odhad ročních příjmů po jednotlivých budovách"),
    j_prijem,
    j_narust,
    j_porovnani,
    j_trzni,
    j_trzni_narust,
    j_rozdil,
    flow("Akumulované příjmy a tržní cena jednotek → souhrnné ukazatele projektu"),
    subhead("Souhrn"),
    j_souhrn,
    subhead("Vizualizace"),
    figs([("render-jednotka-1kk-interier.jpg", "Vizualizace interiéru: jednotka 1+kk o 21 m² ČPP"),
          ("render-exterier-jadro-vecer.jpg", "Vizualizace exteriéru: jádro projektu Startovací hub")]),
], label="Projekt Startovací hub — orientační výpočty příjmů z pronájmu jednotek 1+kk")

# ============================================================
# 4) STARTOVACÍ HUB — LŮŽKA
# ============================================================
l_inputs = kv([
    ("Index převodu HPP na ČPP pokojů s lůžky","DP6"),
    ("Počet ČPP na jedno lůžko","DR6"),
    ("Odhad tržního nájemného za jedno lůžko (měsíčně)","DT6"),
    ("Odhadované náklady na služby na jedno lůžko (měsíčně)","DU6"),
    ("Obsazenost","DV6"),
], inputs=True)

l_prijem = matrix(
    ["Parcela","Označení","Název","HPP budovy","ČPP pokojů","Počet lůžek","Měsíční příjem","Měsíční náklad na služby","Roční příjem očištěný o služby"],
    ["DM","DN","DO","DP","DQ","DR","DT","DU","DV"], list(range(10,27)),
    caption="Odhad příjmů z pronájmu lůžek ve sdílených pokojích (po budovách)")

l_souhrn = kv([
    ("Celkový počet lůžek","DR39"),
    ("Odhadovaná výše měsíčních příjmů","DT39"),
    ("Odhadovaná výše měsíčních nákladů na služby","DU39"),
    ("Odhadovaný roční příjem","DV39"),
])

section("Startovací hub · lůžka ve sdílených pokojích", "#F1EADF", [
    subhead("Vstupní parametry"),
    l_inputs,
    l_prijem,
    subhead("Souhrn"),
    l_souhrn,
    subhead("Vizualizace"),
    figs([("render-sdileny-pokoj-interier.jpg", "Vizualizace interiéru: sdílený pokoj s lůžky se zvýšenou privátní ochranou")]),
], label="Projekt Startovací hub — orientační výpočty příjmů z pronájmu lůžek")

# ============================================================
# 5) NOVÁ ČTVRŤ
# ============================================================
n_inputs = kv([
    ("Zastavitelnost Areálu","EH6"),
    ("Podlažnost pro plochy SM","EJ6"),
    ("Plochy SM v Areálu","EK6"),
    ("Kolik % z maxima HPP dle ÚP se podaří zrealizovat","EL6"),
    ("Index pro převod HPP na ČPP","EM6"),
    ("Index meziročního nárůstu cen stavebních prací","EN6"),
    ("Podíl projekčních / přípravných prací","EO6"),
    ("Odhadovaná cena za vybudování 1 m² ČPP (2026)","EP6"),
    ("Index meziročního nárůstu prodejní ceny bytů","EQ6"),
    ("Odhadovaná tržní cena m² ČPP (2026, novostavby)","ER6"),
], inputs=True)

n_matrix = matrix(
    ["Rok","Kupní cena areálu","Nárůst cen bytů","HPP","ČPP","Index stav. prací",
     "Náklad na výstavbu ČPP","Projekční / přípravné práce","Index prodejních cen",
     "Prodejní cena všech ČPP","Pořizovací cena vč. prací","Teoretický hrubý zisk"],
    ["EH","EI","EJ","EK","EL","EM","EN","EO","EP","EQ","ER","ES"], list(range(8,24)),
    caption="Odhad hrubých příjmů a nákladů developerského rozvoje Areálu (2023–2038)")

def n_headline():
    w('  <div class="vz-headline">')
    w(f'    <span class="vz-headline__label">Potenciální hrubý zisk před zdaněním z rozprodeje plně rozvinutého Areálu (2038)</span>')
    w(f'    <span class="vz-headline__num">{esc(V("EQ39"))}</span>')
    w(f'    <span class="vz-headline__sub">Průměrná cena za m²: {esc(V("EN41"))}</span>')
    w('  </div>')

bench = matrix(
    ["Název","Dispozice","Plocha","Podlaží","Cena","Vybavení","Dostupnost"],
    ["EH","EI","EJ","EK","EL","EM","EN"], list(range(188,201)),
    caption="Nabídkové ceny bytů v novostavbách poblíž Areálu (benchmark)",
    foot="Zdroj: www.creditasre.cz/projekty/klecanska-alej k 22. 9. 2025.")

section("Nová čtvrť", "#E7F0E3", [
    subhead("Vstupní parametry"),
    n_inputs,
    n_matrix,
    flow("Prodejní cena všech ČPP − pořizovací cena včetně prací → teoretický hrubý zisk"),
    n_headline,
    bench,
    subhead("Vizualizace a hmotové studie"),
    figs([("render-exterier-plaza.jpg", "Vizualizace exteriéru: Nová čtvrť"),
          ("schema-hmota-letecky-1.jpg", "Hmotová studie – letecký pohled (1)"),
          ("schema-hmota-letecky-2.jpg", "Hmotová studie – letecký pohled (2)"),
          ("schema-hmota-letecky-3.jpg", "Hmotová studie – letecký pohled (3)"),
          ("schema-zony-zakres.jpg", "Schéma zón se zákresem budov"),
          ("schema-ortofoto-zony-1.jpg", "Ortofoto se zákresem zón (1)"),
          ("schema-ortofoto-zony-2.jpg", "Ortofoto se zákresem zón (2)")]),
], label="Projekt Nová čtvrť — orientační výpočty")

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

section("Zdroje a předpoklady", "#F6E6EC", [
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
