# Spec — „Projekt Startovací hub": 5 závěrečných podsekcí + konektory, hover, lightbox

Datum: 2026-06-28
Soubor cíle: `investori-zaklad.html` (generovaný přes `tools/zaklad/`); dílčí dopady do
`investori-zamer.html` (lightbox) a sdílených `.vz` stylů.

## Cíl

Doplnit na **konec stávající zóny „Projekt Startovací hub"** 5 dalších tabulek z listu
`Základní údaje & výpočty` (`Záměr VPD1_5.xlsx`), věrně dle zdroje. K tomu 3 průřezové
úpravy: (1) výměna dvou ortofoto map, (2) oprava hover zvýraznění řádků tabulek,
(3) lightbox na obrázky v investorských podkladech. Náhrada Excel „šipek" konektorem
(trvalá jemná linka + zvýraznění na hover).

Zdroj pravdy zůstává generátor `tools/zaklad/` — čísla jdou z gridu, žádný ruční přepis.

## 1. Pět nových tabulek (pořadí dle Excelu = pořadí na webu)

Vše se přidá do existující `zonesection("Projekt Startovací hub | …")` v `build_zaklad.py`,
**za** stávající benchmark nájemného (`hub_bench` + `zdroj-odhad-najemneho.jpg`). Bez nového
velkého nadpisu zóny; každá tabulka uvozena žlutým `greenband` s reálným titulkem.

Společné: roční řady = řádky **8–23** (2023–2038), `cellfills=True` (věrné barvy buněk),
souhrnné boxy z řádku **39**. Vstupní boxy nahoře přes `paramstrip` (barva dle fillu buňky).

### #20 Odhadovaný meziroční nárůst příjmů z pronájmu jednotek vzniklých pro projekt Startovací hub
- Vstupy: `BS6` = 52 072 920 Kč (žlutá), `BU6` = 5,00 % (modrá).
- Tabulka (sloupce → hlavičky):
  - `BS` Rok · `BT` Odhadovaný meziroční růst cen pronájmů v jednotlivých letech ·
    `BU` Odhadovaný příjem z pronájmu v jednotlivých letech ·
    `BV` Odhad celkových (akumulovaných) příjmů z pronájmu
- Souhrn: 1 box → `BV39` = **758 206 858 Kč** (žlutá) = **cíl konektoru**.
- Konektor: řádek 2038 (poslední sloupec `BV`, hodnota `BV23` = 758 206 858) → box `BV39`.
- Pozn.: `BV` má nulové roky s Excel formátem `#,##0" Kč [přípravná fáze]"` → na webu
  „0 Kč [přípravná fáze]" (viz §6 — zachování literálu formátu).

### #21 Hrubé porovnání hlavních provozních příjmů a nákladů projektu Startovací hub
- Bez vstupních boxů.
- Tabulka: `BY` Rok · `BZ` Odhadovaný příjem v jednotlivých letech ·
  `CA` Výše zálohy na kupní cenu Areálu v příslušném roce ·
  `CB` Rozdíl mezi příjmy a náklady v jednotlivých letech ·
  `CC` Akumulovaný rozdíl hlavních příjmů a nákladů projektu.
- Souhrn: 2 boxy → `BZ39` = 446 119 167 Kč (zelená, „Cena Areálu po odečtení uhrazených
  záloh na konci roku 2038") + `CB39` = **515 496 858 Kč** (žlutá, „Hlavní příjmy projektu
  Startovací hub do konce roku 2038") = **cíl konektoru**.
- Konektor: `CC23` (515 496 858) → box `CB39`. Zelený box bez konektoru.

### #22 Odhad tržní ceny všech jednotek vzniklých pro projekt Startovací hub
- Vstup: `CL6` = 2 975 300 Kč (modrá, **červený font** — viz §5).
- Tabulka (řádky **10–26**, budovy, ne roky): `CG` Číslo parcely · `CH` Označení ·
  `CI` Název · `CJ` Celkem podlaží · `CK` Počet podlaží vhodných pro rekonstrukci na
  jednotky 1+kk · `CL` Počet jednotek v příslušné budově · `CM` Odhad prodejní ceny všech
  jednotek v příslušné budově. `zonecols` = (CG..CM) → barvení zón (zelená zázemí / žlutá jádro).
  - `CJ15` (štáb, „Celkem podlaží") = „3" má **červený font**.
  - Skupiny budov oddělené prázdnými řádky v Excelu se **slučují** do souvislé tabulky
    (skupiny odliší barva zóny) — odsouhlaseno.
- Souhrn: 2 boxy → `CL39` = 331 (žlutá, „Počet jednotek 1+kk…") + `CM39` =
  **984 824 300 Kč** (žlutá, „Odhadovaná tržní ceny všech jednotek pro rok 2026")
  = **cíl konektoru**.
- Konektor: tabulka je po budovách (ne po letech) — zdroj = sloupec `CM` (poslední
  budova) → box `CM39`. Highlight označí poslední řádek tabulky + box.
- Benchmark pod tabulkou (vzor jako u nájemného):
  - centr. `greenband`: „Odhad tržní ceny jedné jednotky 1+kk o ČPP 21 m² v příslušné
    lokalitě (www.odhad-zdarma.cz, k 18. 1. 2026)";
  - mini-strip: 2 975 300 Kč (`CK42`) / 21 m² (`CL42`) / 141 681 Kč (`CM42`);
  - obrázek `zdroj-odhad-prodejni-ceny.jpg` (už existuje, image025).

### #24 Odhadovaný nárůst tržní ceny jednotek vzniklých pro projekt Startovací hub
- Vstupy: `CP6` = 984 824 300 Kč (žlutá), `CR6` = 5,00 % (modrá).
- Tabulka: `CP` Rok · `CQ` Index zvolený pro růst tržní ceny jednotek 1+kk v lokalitě
  Areálu · `CR` Odhadovaná tržní cena jednotek vzniklých pro projekt Startovací hub.
  (`CQ` ukazuje surový index: 1, 0,05, 0,05 … — věrně dle Excelu.)
- Souhrn: 2 boxy → `CQ39` = 331 + `CR39` = **1 768 602 949 Kč** (žlutá) = **cíl konektoru**.
- Konektor: `CR23` → box `CR39`.

### #25 Rozdíl mezi nákupní cenou Areálu a tržní cenou jednotek vzniklých pro projekt Startovací hub
- Vstupy: `CU6` = 5,0 % (modrá), `CX6` = 984 824 300 Kč (žlutá).
- Tabulka: `CU` Rok · `CV` Přírůstek prodejní ceny · `CW` Prodejní cena zrekonstruovaných
  ubytovacích jednotek · `CX` Kupní cena Areálu při předpokládané inflaci CPI do 5 % ·
  `CY` Kupní cena Areálu k doplacení po započtení uhrazených záloh · `CZ` Rozdíl mezi
  doplatkem kupní ceny Areálu a tržní cenou jednotek vzniklých v jádru projektu Startovací hub.
- Souhrn: 1 box → `CX39` = **1 322 483 783 Kč** (žlutá) = **cíl konektoru**.
- Konektor: `CZ23` (1 322 483 783) → box `CX39`.

## 2. Komponenty (generátor `build_zaklad.py`)

Znovupoužití: `greenband`, `paramstrip`, `matrix(cellfills=True, zonecols=…)`,
`vzmap`, `figrow`.

Nové / upravené:
- `vzgrand(items)` — souhrnné boxy, kde **barva každého boxu plyne ze zdrojového fillu**
  buňky (jako `paramstrip`), a lze jeden box označit jako `data-flow-target` (cíl konektoru).
  `items` = list `(label, coord, is_target?)`. Důvod nového helperu: `vzsummary` má jednu
  barvu pro všechny boxy; tady je potřeba zelený+žlutý box vedle sebe a označení cíle.
- `flowblock(blocks)` — resuscitace existujícího (dormantního) helperu: obalí
  (tabulka + souhrn) do `.vz-flowblock`, přidá `<svg class="vz-bigribbon">`. Zdroj konektoru
  = pravý okraj tabulky na úrovni posledního (2038) řádku; cíl = box s `data-flow-target`.

## 3. Konektor — „trvalá jemná linka" + hover

Náhrada zahnutých Excel šipek. Pro každou z 5 tabulek právě jedna vazba (řádek 2038 →
souhrnný box), dle rozhodnutí „jen Excel šipky".

- **Default:** JS (rozšíření existující `vz-bigribbon` rutiny v `assemble.py`) nakreslí
  **trvalou, jemnou** zaoblenou linku (rose tah, tenký) od pravého okraje tabulky (svisle na
  úrovni posledního datového řádku — 2038, resp. poslední budova u #22) k pravému okraji
  cílového boxu. Oblouk se **klene do pravého okraje** (smí přesáhnout obsah;
  `.vz-flowblock` má rezervu vpravo, `overflow:visible`).
- **Hover / focus / tap** na posledním řádku tabulky *nebo* na cílovém boxu → linka
  **ztmavne a zesílí** a obě hodnoty se **rozsvítí** (jemné zvýraznění). Realizace: JS přidá
  třídu `is-flowhot` na `.vz-flowblock` (řídí vzhled SVG) a `is-flowmark` na zdrojový řádek +
  cílový box. Vazba zdroj↔cíl přes sdílené `data-flow="N"`.
- **Mobil (< 820 px):** linka skrytá (jako dnes `.vz-bigribbon{display:none}`), boxy se
  skládají pod tabulku; zvýraznění na tap funguje dál.
- **Bez JS:** tabulka i boxy fungují, jen bez linky a bez hover-spojení (graceful).

Anchoring pozn.: linka se kotví na **pravý okraj `.vz-mwrap`** (robustní vůči vodorovnému
posuvu tabulky), ne na konkrétní scrollující buňku; zvýraznění (`is-flowmark`) cílí na
skutečný řádek 2038 + box (když je odscrollovaný, highlight prostě není vidět).

## 4. Oprava hover zvýraznění řádků (všechny `.vz-matrix`)

Problém: dnešní `tbody tr:hover td{background:#F0F0FA}` nepřebije buňky s `cellfills`
(`background … !important`), takže barevné buňky na hover neztmavnou.

Řešení: ztmavení **překryvnou vrstvou nezávislou na pozadí** — inset box-shadow:
- `tbody tr:hover td { box-shadow: inset 0 0 0 999px rgba(42,42,96,.055) }`
- `tbody tr:hover .vz-stickcol { box-shadow: 1px 0 0 0 var(--hair), inset 0 0 0 999px rgba(42,42,96,.055) }`
  (zachová pravou dělicí linku stickcolu).
- Odstranit staré hover `background` rules (vč. `is-jadro:hover` / `is-zazemi:hover`),
  protože překryv ztmavuje uniformně přes jakékoli pozadí (bílé i barevné).

Platí pro všechny tabulky na stránce (parcely, smlouva i nové). Subtilní, čitelnost textu zůstává.

## 5. Červená čísla (font color)

Věrně reprodukovat buňky s červeným fontem (`CL6`, `CJ15`).
- `dump_zaklad.py`: doplnit zachycení barvy fontu → pole `"fc"` (rgb, normalizované; ignorovat
  default černou/automatickou).
- `build_zaklad.py`: helper `is_red(r,c)` (font rgb končí na `FF0000`); přidat třídu
  `is-red` do buněk `matrix` a do hodnoty v `paramstrip`/`vzgrand`.
- CSS (`assemble.py`): `.vz .is-red, .vz .vz-matrix td.is-red, .vz .vz-param.is-red .vz-param__num
  { color:#C8102E }` (jasná, čitelná červená). Pozadí buňky zůstává dle fillu.

## 6. Zachování literálu číselného formátu („[přípravná fáze]")

`extract_fmt.py` → `fmt_cell`: místo napevno `" Kč"` / `" m²"` použít **celý kvótovaný
literál** z number-formatu, který jednotku obsahuje (tj. `" Kč [přípravná fáze]"` →
„… Kč [přípravná fáze]"). Pro běžné buňky (`#,##0" Kč"`) výsledek beze změny.
- Po úpravě **re-extrahovat** `grid_fmt.json` + `zaklad_dump.json` a udělat `git diff`
  obou JSONů — potvrdit, že se mění **jen** zamýšlené buňky (přípravná fáze + nově `fc`).
  Žádná regrese ve schválených sekcích.

## 7. Výměna dvou ortofoto map

Nahradit obrázky v breakdown blocích „Tabulky č. 1":
- `Pozemky: jádro projektu Startovací hub` → nový zdroj
  `/Users/kindl/Work/_2026/02 OSA/15 Map/_jadro-projektu.JPG` (2492×1338, žlutá zóna,
  16 496,28 m²) → přepsat `assets/images/investori/zaklad/schema-ortofoto-zony-1.jpg`.
- `Pozemky: jádro + zázemí projektu Startovací hub (celek)` → nový zdroj
  `/Users/kindl/Work/_2026/02 OSA/15 Map/_zazemi-celek.JPG` (2539×1348, zelená zóna,
  34 769,61 m²) → přepsat `assets/images/investori/zaklad/schema-ortofoto-zony-2.jpg`.
- Zmenšit: `sips -s format jpeg -s formatOptions 82 --resampleWidth 2400 <src> --out <dst>`.
- Stejné názvy souborů → `build_zaklad.py` se nemění. Aktualizovat poznámku v
  `assets/images/investori/zaklad/mapping.json` (nový zdroj map).

## 8. Lightbox na obrázky v podkladech

Cíl: klik na obrázek → zvětšení v překryvu (podobně jako galerie). Investorské stránky už
JS používají (měkká brána, scroll tlačítka, ribbon) → zvolen **kompaktní JS lightbox**
(méně markupu než CSS `:target`, jednotný pro obě stránky).

- Chování: klik na obsahový `<img>` (uvnitř `figure` v `.vz`) → tmavý překryv s velkým
  obrázkem + popisek (z `figcaption`/`alt`), tlačítko ×, šipky ‹ › pro průchod obrázky na
  stránce, zavření klávesou Esc / klikem na pozadí / ×, šipky ←/→ pro navigaci.
  Zámek scrollu po dobu otevření. Vizuál v duchu galerie (tmavé pozadí, bílý obrázek).
- Rozsah: **`investori-zaklad.html`** — všechny obsahové obrázky (`.vz-map`, `.vz-figrow`,
  `.vz-figs`, benchmark mapy). Affordance: `cursor:zoom-in`, `tabindex`, `role="button"`,
  `aria-label`. CSS + JS do inline `.vz` bloku / `SCRIPTS` v `assemble.py`.
- **`investori-zamer.html`:** jediný „obrázek" je **interaktivní vrstvená ortofoto mapa**
  (4 vrstvy + hover zóny). Lightbox by zničil interaktivitu → **ponechat beze změny** v tomto
  kroku. (Caveat k revizi: pokud klient chce i tu zvětšovat, řešit zvlášť.)

## 9. Pipeline & build

1. `dump_zaklad.py` (+`fc`), `extract_fmt.py` (literál formátu) → re-extrakce z xlsx
   (spustit z adresáře se sešitem; `SCRATCH=tools/zaklad/data`). Diff JSONů.
2. `build_zaklad.py` → 5 bloků, `vzgrand`, `flowblock`, `is_red`, konektor markup.
3. `assemble.py` → CSS: `.is-red`, hover-overlay fix, doladěný `.vz-bigribbon` (trvalý+hot),
   lightbox CSS; JS: rozšířený ribbon (trvalý + hover highlight), lightbox.
4. `python3 tools/zaklad/build_zaklad.py && python3 tools/zaklad/assemble.py`
5. `npm run build` (pojistka; `.vz` styly jsou inline, ale spustit).
6. Obrázky: resize + přepis 2 ortofoto map, update `mapping.json`.
7. Lightbox do `investori-zamer.html` (ruční, mimo generátor) — pouze pokud se rozsah
   rozšíří; default dle §8 = zamer beze změny.

## 10. Ověření

- Servírovat `python3 -m http.server` (port 8000 už běží), otevřít přes login.
- Vizuálně proti screenshotům: hodnoty, barvy buněk, červená čísla (CL6, CJ15),
  „[přípravná fáze]" řádky, dva souhrnné boxy (#21/#22/#24), benchmark + obrázek pod #22.
- Konektor: trvalá jemná linka u všech 5 tabulek; hover na řádku 2038 / boxu → zesílení +
  rozsvícení obou; mobil < 820 px linku skryje.
- Hover na libovolný řádek tabulky ztmaví **i barevné** buňky.
- Lightbox: klik na každý obrázek v zaklad → zvětšení, navigace, Esc/zavření.
- Nové ortofoto mapy zobrazené ve správných breakdown blocích.
- **Regrese:** schválené sekce (Tabulky č.1/č.2, smlouva, příjmy z pronájmu) vizuálně beze
  změny kromě zamýšlených (ortofoto výměna, hover fix, lightbox).

## Mimo rozsah

- Vypnuté sekce (`section_draft`): lůžka, Nová čtvrť, zdroje — zůstávají vypnuté.
- Křížové vazby mezi tabulkami (zvolено „jen Excel šipky").
- Lightbox interaktivní mapy v `investori-zamer.html` (viz §8 caveat).
