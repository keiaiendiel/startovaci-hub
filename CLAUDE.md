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
investori-scenare.html  # podklady „Základní scénáře" = ruční port listu „Základní scénáře" (S1/S2/S3/Sk/Sx), gated
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
  benchmark + **finále: 5 tabulek** — meziroční nárůst příjmů, hrubé porovnání příjmů/nákladů,
  odhad tržní ceny jednotek + benchmark prodejní ceny, nárůst tržní ceny, rozdíl
  kupní vs. tržní cena; sloupce BS–CZ), zóna *Projekt Startovací hub | lůžka ve sdílených
  pokojích* (sloupce DM–DV: vstupní parametry + matice po budovách A1–A6+C + souhrn
  1 014 lůžek / 60 133 632 Kč rok + vizualizace + pracovní modely ceny/nákladů na lůžko),
  zóna *Projekt Nová čtvrť* (sloupce EH–ES: developerská matice 2023–2038 + grand
  „potenciální hrubý zisk 13 942 639 425 Kč" + hmotové studie + benchmark cen bytů
  creditasre, řádky 188–214). **Zatím vypnuté** (viz `section_draft`): už jen *zdroje*.
  Komponenty (inline `.vz`
  styly v HTML, NE Tailwind): `.vz-matrix` (sticky 1. sloupec + vodorovný posuv + scroll
  tlačítka `.vz-mbtn`), `.vz-map`, `.vz-totals/.vz-summary/.vz-grand` (hranaté souhrnné boxy;
  `vz-grand` = barva dle fillu + cíl konektoru), `.vz-zonehead/.vz-greenband`
  (barevné pásy zóny dle CSS `--band`), `paramstrip`, `.vz-quote` (text smlouvy),
  `.vz-figrow/.vz-figs`, `.sec--shade` (full-bleed oddělení hlavních sekcí). **Věrné
  barvení buněk dle zdrojových Excel fillů** (`cellfills`: oranžová = vstupy, zelená,
  žlutá jádro / zelená zázemí) + **červená čísla** dle font color z Excelu (`is_red`,
  zachyceno v `dump_zaklad.py` jako `fc`). **Konektor místo Excel šipek** (`flowblock`
  + `.vz-bigribbon`): jemná linka od **vstupního parametru** (`data-flow-source` v
  `paramstrip`) k **cílovému souhrnu** (`data-flow-target` ve `vzgrand`) — věrně dle
  původní tabulky (např. CX6→CX39, DV6→DV39, ER6→EQ39). Vede po pravém okraji a volně
  přesahuje do margenu webu (`.vz{overflow-x:clip}`); tabulky drží plnou šířku; hrot dle
  tečny míří do boxu; hover/focus linku zesílí a rozsvítí oba boxy; < 820 px skrytá.
  **Hover souhrnného boxu** (`data-hl-col` ↔ `data-col` na buňkách) rozsvítí celý
  zdrojový sloupec v tabulce a je-li mimo viditelnou oblast, tabulku k němu posune.
  **Matice zarovnané vlevo**; levý bílý fade jen u tabulek bez sticky sloupce (`.has-stick`).
  **Hover řádků** ztmaví i barevné buňky (inset box-shadow overlay). **Lightbox** (`.lbx`,
  JS): klik na obrázek → zvětšení, ‹ ›/←→/Esc, modální focus trap. Obrázky v
  `assets/images/investori/zaklad/` (zmenšené, `mapping.json`).
- **Top bar všech tří podkladů** (`.inv-*` v `input.css`): logo + 3 sekce „Investiční
  záměr / Základní údaje / Základní scénáře" + „Odhlásit se". **Na desktopu** sekce
  inline v liště (`.inv-topnav`, ≥ 820 px), **na telefonu/tabletu** (< 820 px) jen
  **hamburger vpravo nahoře** → tmavé menu (`.inv-menu`, jako landing) s **centrovanými
  položkami** + dole „Odhlásit se". Toggle přes checkbox `#inv-nav.inv-nav` (`:checked ~ .inv-menu`).
  Aktivní sekce = `aria-current="page"`. Lišta na telefonu (i landscape) užší. Po změně
  `.inv-*` tříd `npm run build`. V `investori-zamer.html` jsou na telefonu skryta 3
  zónová tlačítka pod mapou (stačí 3 barevné sekce v legendě).
- **`investori-scenare.html`** = podklady „Základní scénáře". Ruční port listu
  `Základní scénáře` z `Záměr VPD1_5.xlsx` (5 scénářů S1/S2/S3/Sk/Sx; barevné řádky
  dle Excel fillů: S1 žlutá, S2 tan, S3 oranžová). Vodorovně posuvná tabulka
  (`.scn-table`, sticky 1. sloupec se scénářem). „Detail (zde)" zatím → `404.html`.
  Měkká brána + top bar + Atyp Special jako ostatní podklady. Statická (ne z generátoru).
- Když se mění podklady, edituj přímo příslušné HTML (žádné není v Astru);
  „Základní údaje" lze i regenerovat z xlsx přes `tools/zaklad/`.
- ⚠️ **Zdroj pravdy = tabulka (xlsx). Drž se jí.** Čísla, propojení (konektory) i
  zvýraznění (hover) musí PŘESNĚ odpovídat zdroji — **needituj zobrazené hodnoty kvůli
  čitelnosti**, i když něco působí nejednotně (např. „1" / „5,00 %" vs „0,05" v indexových
  sloupcích je věrné zdroji → nech být). Jediná povolená výjimka jsou **obvious textové
  překlepy nekonzistentní uvnitř zdroje** (stejný název jinde správně) — ty sjednoť přes
  `TEXT_FIX` v `build_zaklad.py` (jen názvy, nikdy ne čísla). Auditní ověření: viz
  10-agentní cross-check (čísla 1:1 ve všech zónách potvrzeno 2026-06-28).

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
