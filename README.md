# Startovací Hub — landing page

Statická jednostránková landing page. Čisté **HTML a CSS, bez JavaScriptu**.
Styly stavěné na **Tailwind CSS**.

## Spuštění

Web je čistě statický a `assets/styles.css` je už zkompilovaný — žádný build
ani server k zobrazení není nutný. Doporučeno je ale servírovat přes lokální
server (přes `file://` se nenačtou self-hosted fonty a mapa v patičce):

```bash
npx serve .              # nebo
python3 -m http.server 8123
```

Pak otevři `http://localhost:8123`.

## Struktura

```
index.html              # landing stránka
404.html                # „stránka ve výrobě" (cíl všech necílových odkazů)
assets/
  styles.css            # zkompilovaný Tailwind (funguje bez buildu)
  brand-logo-white.svg  # logo
  fonts/                # Atyp Special (woff2, self-hosted)
  images/               # fotky
  videos/               # hero video (mp4, H.264)
src/input.css           # zdroj stylů: @tailwind + design tokeny + @font-face
tailwind.config.js      # brand barvy, font (content: index.html + 404.html)
package.json            # build skripty
```

## Úprava stylů

Třídy se píšou přímo v `index.html`. Po změně tříd nebo tokenů přegeneruj CSS:

```bash
npm install             # jednorázově
npm run build           # vyrobí assets/styles.css
npm run watch           # nebo průběžně
```

Barvy, fonty a spacing jsou CSS proměnné v `src/input.css` (`:root`); brand
barvy jsou navíc namapované v `tailwind.config.js`, takže fungují třídy jako
`bg-plum-deep`, `text-rose`, `border-accent-rule`.

## Odkazy

Landing je samostatný. On-page mechanismy fungují bez JS: scroll šipka
(`#ubytovani`), tečky galerií (`#uby-1`…), lightbox (`#lb-1`…, `:target`),
„nahoru" (`#top`). Kontaktní akce (`mailto:`, `tel:`) a mapa vedou ven.

Všechny odkazy, které by v plném webu mířily na podstránku (menu, „zjistit
více", Rezervovat, Pro investory, Ceník, Novinky, footer akce…), vedou na
**`404.html`** — sdílenou obrazovku „stránka ve výrobě". Z 404 vede „Přejít
na úvod" zpět na `index.html`.
