# Investorská stránka „Základní údaje & výpočty" — design spec

Datum: 2026-06-28 · větev `feat/investori-zaklad`

## Cíl
Druhá gated investorská stránka (`investori-zaklad.html`), sourozenec
`investori-zamer.html`. **Věrný (1:1) převod** listu „Základní údaje & výpočty"
ze `Záměr VPD1_5.xlsx` do čisté, webově funkční podoby. **Zachovat veškerý smysl
a všechna data**; volně přeuspořádat (šířky sloupců, velikosti, pořadí) tak, aby
to bylo graficky správné. Extrémně horizontální Excel (380 řádků × 152 sloupců) →
**lineární narativ se sekcemi pod sebou**.

## Zdroj dat (deterministicky)
- Primární: `openpyxl` dump listu → `grid_fmt.json` (česky formátované hodnoty) +
  `zaklad_dump.json` (hodnoty, fill barvy, bold, merge). Žádný ruční přepis čísel.
- Build = **deterministický Python generátor** (`build_zaklad.py`) čte grid a emituje
  HTML tabulek → nula transkripčních chyb. Čisté nadpisy sloupců se ručně kultivují,
  ale **čísla jdou přímo z gridu**.
- Geometrie/podoba šipek: z HTML exportu + `.fld` PNG.

## Navigace & shell
- Stejná měkká brána (`localStorage['vpd1-auth']`, SHA-256 allowlist), stejný
  `inv-topbar`, `.vz` wrapper, Atyp Special, brand tmavá první paint.
- **Segmentový přepínač** `.inv-seg` v `inv-topbar__actions` vlevo od „Odhlásit":
  dva `<a>` — „Investiční záměr" ↔ „Základní údaje". Čistě odkazy → funguje bez JS.
  Přidat na **obě** stránky (aktivní zvýrazněný).
- Záznam do `struktura-webu.html` (status „na heslo"). Aktualizovat `CLAUDE.md`.

## Obsahová struktura (pod sebe)
1. **Cover** — kicker „Základní údaje & výpočty", titul „VPD1".
2. **Areál — parcely & plochy** — inventura parcel (tab. č.1 + č.2, široké → `.vz-matrix`),
   souhrn ploch/HPP, breakdowny jádro / jádro+zázemí / zázemí (m² + podíly %).
3. **Smlouvy — kupní cena Areálu** — sjednané zálohy; výpočet + predikce kupní ceny
   2023–2039 (široká `.vz-matrix`); mimořádná záloha; pozn. o navýšení.
4. **Startovací hub — jednotky 1+kk** — příjmy z pronájmu (per-parcela), meziroční
   nárůst (matrix), hrubé porovnání příjmů/nákladů (matrix), tržní cena jednotek
   (per-parcela), nárůst tržní ceny (matrix), rozdíl vs kupní cena (matrix), souhrny;
   vizualizace (rendery).
5. **Startovací hub — lůžka / sdílené pokoje** — vstupy + odhad příjmů (per-parcela),
   souhrny; vizualizace.
6. **Nová čtvrť** — hrubé příjmy/náklady developmentu 2023–2038 (široká `.vz-matrix`),
   headline hrubý zisk (13,9 mld. Kč); benchmark byty v novostavbě; vizualizace.
7. **Zdroje & předpoklady** — ↓↓↓ benchmark odkazy (creditasre…), ChatGPT odhady.
8. **Footer** — verze 2p8iaz6.

## Komponenty (`src/input.css`, `@layer components`)
- Reuse: `.sec/.sechead/.row/.lab/.val/.foot/figure/.cover/.verstamp/.vzver`.
- `.vz-matrix` — obal `overflow-x:auto`; `<table>` tabular-nums; **sticky 1. sloupec**;
  hlavička = roky/metriky; edge-fade náznak posuvu; mobil = swipe.
- `.vz-zoneband` — barevný předěl zóny (5 zón).
- `.inv-seg` / `.inv-seg__item` — segmentový přepínač v topbaru.
- token `--accent-input` (oranžová) + legenda „■ vstupní předpoklad / odhad".

## Barvy (sjednocení na brand paletu)
- Buňky s fill `EBC08F` (149×) = vstupní/odhadové → `.is-input` → `--accent-input`.
- Zóny: zelená `C2DCAE`→brand zelená; žlutá `ECE5A3`→brand žlutá; béžová `D9C7A1`→
  teplý neutrál; modré info `E6ECF6`/`B6CDE9`→ stávající modrá. Tinty doladit živě.

## Obrázky
- Separátní složka `assets/images/investori/zaklad/` (snadná výměna). Rendery downscale
  ~2400px / JPEG q82 (`sips`); dedup (021=022, 030=031; ikony 2 unikáty); čitelná jména
  + `mapping.json`. Šipky → **nahrazeny ribbony** (CSS/SVG), ne raster.

## Ribbony (místo šipek)
- 13 původních šipek = konektory mezi hodnotami. Ve vertikálním layoutu → ribbon
  spojující konkrétní hodnoty (případně šipka na konci) dle původního smyslu/směru.
  **Opticky kontrolovat** na renderu (headless screenshot).

## Číselné formáty
- %, Kč, m², „m² HPP", „Kč / m²", index, datum — český formatter (mezera tisíce,
  čárka desetinná). `#VALUE!` → potlačit (prázdné).

## Build & verifikace
- `npm run build` (Tailwind). Lokální server. Headless screenshoty desktop+mobil.
- Workflow: adversarní kontrola čísel vs zdroj + vizuální/responzivní/a11y review.

## Mimo rozsah
- Skutečné zabezpečení brány (zůstává měkká). Astro sync (stránka jen zde).
