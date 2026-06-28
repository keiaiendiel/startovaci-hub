# sh-web-landing-html — CLAUDE.md

Operativní handoff pro budoucí sessions. Stručně, načítá se do každé konverzace.

## Co to je

Ruční **HTML + CSS** konverze **landing page** Startovacího Hubu + malý
**investorský pod-web** (login + dva listy podkladů). Čistě statické, styly přes
**Tailwind CSS**. Landing je **bez JavaScriptu**; jediná výjimka je měkká brána
investorského pod-webu (kontrola hesla). Slouží klientovi jako samostatná, snadno
hostovatelná verze.

⚠️ **Zdroj pravdy je sourozenecký Astro repo** `~/Work/_2026/02 OSA/11 WWW/sh-web`
(jeho `src/pages/index.astro` = landing, `src/components/Footer.astro` = patička).
Tahle složka je ruční **zrcadlo jen landingu**. Když se změní landing v Astru,
promítni změny sem; když klient chce úpravu tady, drž to konzistentní s Astrem.

## Stack

| | |
|---|---|
| Styly | Tailwind CSS 3.4.17, zdroj `src/input.css` → build do `assets/styles.css` |
| Tailwind config | `tailwind.config.js`, `content` = `index.html`, `404.html`, `investori.html`, `investori-zamer.html`, `investori-zaklad.html`, `struktura-webu.html`, `galerie.html`; brand barvy mapované na CSS proměnné (`bg-plum-deep`, `text-rose`, …) |
| Tokeny + komponenty | `src/input.css`: `:root` tokeny + `@layer components` (`.hero-ctas`, `.hero-cta`, `.sec-title/.sec-lede/.sec-cta`, `.ucards/.ucard*`, `.gal/.gallery*`, `.foot-act/.foot-label`, `.hub-404*`, `.menu/.burger`, `.to-top`, `.inv-topbar*/.inv-login*/.inv-btn`, `.inv-seg` přepínač). Pozn.: `.vz*` styly „Základních údajů" (`.vz-matrix/.vz-map/.vz-summary/.vz-zonehead/.vz-greenband/.vz-quote/.vz-figrow/.sec--shade` aj.) žijí **inline** v `investori-zaklad.html`, ne v Tailwindu. |
| Fonty | self-hosted Atyp Special (woff2) v `assets/fonts/`, `@font-face` v `input.css` |
| JS | Landing ŽÁDNÝ: menu = CSS checkbox (`#navtoggle`), galerie = scroll-snap + kotvy + scroll-driven aktivní tečka (`view-timeline`) + `::scroll-button` šipky, hero = `<video autoplay muted loop playsinline>`, „nahoru" = scroll-driven animace. Plynulé přechody = `@view-transition` (cross-document, bez JS). **Výjimka:** investorský pod-web má pár řádků JS (měkká brána heslem). |
| Média | `assets/images/hub/...` (zrcadlo `sh-web/public/images/hub`), hero video `assets/videos/*.mp4` (H.264, ne `.mov` jako Astro) |

## Soubory

```
index.html              # landing
404.html                # „stránka ve výrobě" , cíl všech necílových odkazů
investori.html          # přihlášení do podkladů (login heslem, měkká brána)
investori-zamer.html    # podklady „Investiční záměr" = věrný port „Záměr VPD1_5 - web.html" (gated)
investori-zaklad.html   # podklady „Základní údaje & výpočty" = generovaný 1:1 port listu z xlsx (gated)
struktura-webu.html     # mapa webu (strom se statusy: v provozu/ve výrobě/na heslo)
src/input.css           # zdroj stylů (edituj tady, ne styles.css)
assets/styles.css       # zkompilovaný Tailwind (commit-nutý, funguje bez buildu)
assets/images/investori/zona-vse.jpg        # ortofoto-podklad interaktivní mapy záměru
assets/images/investori/zona-{ctvrt,jadro,zazemi}.jpg  # 3 barevné zónové překryvy
assets/images/investori/zaklad/         # obrázky „Základních údajů" (rendery/schémata/zdroje) + mapping.json
tools/zaklad/           # generační pipeline „Základních údajů" (openpyxl dump → build → assemble)
assets/{fonts,images,videos,brand-logo-white.svg}
tailwind.config.js, package.json, README.md
```

## Struktura landingu (musí zrcadlit Astro `index.astro`)

Hero (video + scrim; centro BrandLogo + lede „your perfect living & working space"
+ 2 liquid-glass pilulky „Pronajmout apartmán/lůžko" ukotvené dole, **mezera mezi
nimi přesně na středu stránky** přes 2 poloviční grid sloupce, šířka dle obsahu)
→ zig-zag sekce **Ubytování** (úvod na celou šířku + 2 karty `.ucard`: Privátní
apartmány, Sdílené pokoje) → **Zázemí** (foto vlevo) → **Doprava** „15 minut na
metro." (foto vpravo) → **Stipendia** (foto vlevo) → **patička** (2 sloupce:
kontakty/adresa/nav | mapa) + **rezervační pruh** dole (3 CTA).

⚠️ Aktuální Astro landing NEMÁ galerie teaser, ceník teaser ani finální CTA banner
a ribbon dlaždice pod herem jsou zakomentované , tady to taky není. Nepřidávej je,
dokud to nepřibude i v Astru.

## Odkazy (důležité pravidlo)

Landing je samostatný. **Každý odkaz, který by v plném webu mířil na podstránku**
(menu, „Zjistit více", Pronajmout, Struktura webu, footer akce, Ceník, Novinky…)
vede na **`404.html`** (sdílená „ve výrobě" obrazovka; z ní vede „Přejít na úvod"
→ `index.html`). **Výjimky:** footer **„Pro investory" → `investori.html`** a
**„Struktura webu" → `struktura-webu.html`** (reálné stránky; struktura je mapa
webu, kde necílové podstránky nesou status „ve výrobě" a vedou na `404.html`).
**On-page** mechanismy zůstávají funkční: scroll šipka (`#ubytovani`), tečky
galerií (`#upa-1`/`#usp-1`/`#zaz-1`/…), „nahoru" (`#top`); `mailto:`/`tel:`/Google
Mapy vedou ven.

## Investorský pod-web (`investori*.html`)

- **`investori.html`** = login. Měkká brána (jako Astro v002): `crypto.subtle`
  SHA-256 hesla (hash `2250c0…`; samotné heslo drž mimo repo — viz interní
  předání) proti allowlistu → otisk do
  `localStorage['vpd1-auth']` → redirect na `investori-zamer.html`. ⚠️ Není to
  skutečné zabezpečení (obsah je v HTML); jen zábrana. Vyžaduje secure context
  (https / localhost). Heslo měň přepočtem SHA-256 v obou HTML (allowlist `ALLOW`).
- **`investori-zamer.html`** = podklady. **Věrný port** `~/Work/_2026/02 OSA/Záměr
  VPD1_5 - web.html` (tabulkový list z Excelu): ponechán 1:1 vč. modro-šedé palety
  `.vz`, jen font → Atyp Special, vložené ortofoto a slim top bar (Na úvod /
  Odhlásit). Brána skryje obsah (`html.inv-wait .vz`), bez JS ukáže `<noscript>`.
- **`investori-zaklad.html`** = podklady „Základní údaje & výpočty". Druhý list
  z `Záměr VPD1_5.xlsx` (list `Základní údaje & výpočty`), **generovaný deterministicky**
  (openpyxl → grid → HTML; skripty `tools/zaklad/`, data v `tools/zaklad/data/*.json`).
  **Staví se sekci po sekci dle revizí klienta** (každou tabulku schvaluje zvlášť).
  Hotové sekce: *Tabulka se zákl. informacemi č. 1* (masterplan mapa + parcely A–H +
  „Pozemky" breakdowny s ortofoto mapami + souhrnné boxy), *č. 2* (sloupce K–X:
  stavby/podlažnost/HPP, barevné řádky jádro/zázemí), zóna *Základní údaje a výpočty
  vyplývající z uzavřených smluv* (zálohy + výpočet/predikce kupní ceny + citace
  smlouvy čl. 3), zóna *Projekt Startovací hub* (příjmy z pronájmu + vizualizace +
  benchmark). **Zatím vypnuté** (čekají na revizi — viz `section_draft` v generátoru):
  lůžka, Nová čtvrť, zdroje. Komponenty (inline `.vz` styly v HTML, NE Tailwind):
  `.vz-matrix` (sticky 1. sloupec + vodorovný posuv + scroll tlačítka `.vz-mbtn`),
  `.vz-map`, `.vz-totals/.vz-summary` (hranaté souhrnné boxy), `.vz-zonehead/.vz-greenband`
  (barevné pásy zóny dle CSS `--band`), `paramstrip`, `.vz-quote` (text smlouvy),
  `.vz-figrow/.vz-figs`, `.sec--shade` (full-bleed oddělení hlavních sekcí). **Věrné
  barvení buněk dle zdrojových Excel fillů** (`cellfills`: oranžová = vstupy, zelená,
  žlutá jádro / zelená zázemí). **Ribbony místo Excel šipek = rozpracováno** (helpery
  `.vz-flow`/`.vz-flowblock` v generátoru jsou dormantní, vizuál se ještě ladí). Obrázky
  v `assets/images/investori/zaklad/` (zmenšené, `mapping.json` pro snadnou výměnu).
- V top baru obou stránek je **segmentový přepínač** (`.inv-seg`) „Investiční záměr
  ↔ Základní údaje" (dva odkazy, bez JS) — po přidání tříd nezapomeň `npm run build`.
- Když se mění podklady, edituj přímo příslušné HTML (žádné není v Astru);
  „Základní údaje" lze i regenerovat z xlsx přes `tools/zaklad/`.

## Workflow úprav

```bash
npm install            # jednorázově
npm run build          # input.css → assets/styles.css (po změně tříd v HTML/CSS)
python3 -m http.server # servíruj (přes file:// se nenačtou fonty/iframe)
```

Po přidání nové třídy do kteréhokoli HTML (`index`, `404`, `investori*`) VŽDY
`npm run build` (jinak ji Tailwind nevygeneruje / purge ji smaže). Nové obrázky
kopíruj z `sh-web/public/images/hub/...` do `assets/images/hub/...` se stejnou
cestou. Velké obrázky pro web zmenši (např. `sips -s format jpeg -s formatOptions
82 --resampleWidth 2400 vstup.png --out výstup.jpg`).

## Sync z Astra , na co koukat

- Hero copy/CTA: `sh-web/src/pages/index.astro` (`.lp-hero__quick`, lede).
- Sekce (titulky, lede, pořadí, galerie): `sections` + `ubytovaniCards` v
  `index.astro` frontmatteru.
- Patička: `sh-web/src/components/Footer.astro` (kontakty, nav tlačítka,
  rezervační pruh, „verze 0.0.NNN").
- 404 obrazovka: `sh-web/src/pages/404.astro` (`.hub-404*`).
