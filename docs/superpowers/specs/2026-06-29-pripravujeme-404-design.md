# Rozdělení „ve výrobě" a 404 — design

Datum: 2026-06-29

## Problém

`404.html` dnes plní dvě role najednou: zobrazuje velké „404" **a** nese titulek
„Tahle stránka je ve výrobě". Všechny interní odkazy na ještě nehotové podstránky
(menu, „Pronajmout", footer akce, uzly ve `struktura-webu.html`, „Detail" ve
scénářích…) míří sem. To slévá dvě různé situace:

- **stránka existuje, ale není hotová** („ve výrobě"),
- **stránka neexistuje** (skutečná 404, kterou servíruje hosting pro neznámé URL).

## Řešení

Dvě stránky se **stejným vizuálem** (sdílené třídy `.hub-404*`), liší se obsahem.

### 1. `pripravujeme.html` (nový) — „ve výrobě"

- Kopie dnešní `404.html`, ale **bez** elementu `.hub-404__code` (žádné „404").
- Titulek zůstává **„Tahle stránka je ve výrobě"**, lede „Pracujeme na ní, brzy
  bude hotová."
- CTA „Přejít na úvod" → `index.html`.
- `<title>` + meta description ve znění „ve výrobě"; `robots: noindex` zachováno.
- Odkazy v hlavičce (menu, „Pronajmout", účet) míří na `pripravujeme.html`.

### 2. `404.html` (přepis) — skutečná 404

- **Ponechá** velké **„404"** (`.hub-404__code`).
- Titulek **„Tahle stránka neexistuje"**, lede „Možná byla přesunutá, nebo tu
  nikdy nebyla."
- `<title>` → „Stránka nenalezena · Startovací Hub Klecany"; meta description
  upravená; `robots: noindex` zachováno.
- CTA → `index.html`; odkazy v hlavičce míří na `pripravujeme.html`.
- Soubor **zůstává `404.html`**, aby ho hosting automaticky bral jako error
  stránku. Na tuto stránku se schválně odnikud neodkazuje.

### 3. Přesměrování odkazů

Všechny stávající `href="404.html"` v `index.html`, `galerie.html`,
`struktura-webu.html`, `investori-scenare.html` → `pripravujeme.html`. Každý z
nich je „in production" odkaz.

### 4. Build

Přidat `pripravujeme.html` do `content` v `tailwind.config.js`, pak `npm run
build`. Nové třídy nepřibývají (obě stránky používají existující markup), držíme
ale konvenci.

### 5. Dokumentace

`CLAUDE.md`: zdokumentovat rozdělení — `404.html` = neexistující stránky,
`pripravujeme.html` = cíl necílových („ve výrobě") odkazů.

## Vědomá rozhodnutí

- **CSS třídy `.hub-404*` nepřejmenovávám.** Slouží jako sdílený vizuál obou
  stránek; přejmenování nepřináší nic funkčního a jen zvětšuje zásah. Doplním jen
  komentář v `src/input.css`, že styl sdílí 404 i „připravujeme".
- **Skutečná 404 není v `struktura-webu.html`** — není to navigovatelná stránka,
  ale chybový fallback. Uzly se statusem „ve výrobě" už správně míří na
  `pripravujeme.html`.
