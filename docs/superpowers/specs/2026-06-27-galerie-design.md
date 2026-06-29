# Galerie + 2 opravy — design / spec

Datum: 2026-06-27. Schváleno uživatelem ("lets go").

## Cíl
Nová **plně funkční** stránka `galerie.html` s vizualizacemi ze složky
`_SH_WEB_IMAGE_UPDATE/Startovaci Hub All Viz/_SEL`, bez duplicit. Plus dvě drobné
opravy: blikání hero/lišta CTA „Pronajmout" a desaturace 3 barev zón v investorské
tabulce.

## A) galerie.html
Shell jako `struktura-webu.html`: `body.page-sub`, fixní `.site-header` (bílá „stuck"
lišta po odscrollování banneru přes `.sub-hero` view-timeline), `.to-top`, patička
z landingu. Bez JS (lightbox přes CSS `:target`).

- **Banner** `.sub-hero` + ribbon, titulek „Galerie".
- **Sticky pod-navigace** `.gnav` (sticky `top: 54px`, pod stuck lištou): chip
  odkazy `Ubytování` · `Zázemí` · `Doprava` · `Okolí`. Plynulý scroll = CSS
  `scroll-behavior` (už globálně) + `scroll-margin-top` na sekcích.
- **Mřížka** `.ggrid`: 3 sloupce desktop / 2 tablet / 2 (1) mobil; dlaždice 4/3
  `object-cover`, zaoblení r=7. Čistá mřížka bez popisků; sub-bloky mají nadpisy.

### Sekce (75 fotek)
- **Ubytování** (#ubytovani): sub-blok *Apartmány* (14) + *Sdílené pokoje / co-living* (18)
- **Zázemí** (#zazemi): sub-blok *Komunita* (11) + *Coworking* (8)
- **Doprava** (#doprava): 5
- **Okolí** (#okoli): exteriér 19

„výběr" (landing/extra unikáty) rozpuštěn do Apartmánů/Co-livingu dle motivu.

### Lightbox `:target` (bez JS)
Dlaždice = `<a id="g-N" href="#lb-N">`. Overlay `<div id="lb-N" class="lb">` se
zobrazí přes `.lb:target`. Uvnitř: full `<img object-contain loading=lazy>`,
backdrop+✕ → `href="#g-N"` (zavře, vrátí na dlaždici), ‹/› → `#lb-(N∓1)` řetězeně
přes celou galerii (1↔75 wrap), počitadlo „N / 75". Dlaždice i overlay sdílejí
jeden optimalizovaný soubor → 1 stažení/obrázek.

### Obrázky
75 vybraných → `assets/images/galerie/<sekce>/<slug>.jpg`, `sips -Z 2000 -s format
jpeg -s formatOptions 82` (downscale only). Web-safe ASCII slugy.

**Vyřazeno (44 z 119):** 35 obsahových duplikátů (md5), 4 „před" snímky
(`restaurace-před`, `1kk-před`, `1kk-pora`, `01-3kk-před`), 5 nahrazených starších
verzí (`coliving-kitchen/-bathroom` bez `-update`; `cowork-interier-sal-c`
empty/základní/update1 → ponechán jen `-update2`).

## B) Oprava blikání CTA „Pronajmout"
`.hdr-cta` má `opacity` v `transition` shorthandu a zároveň scroll-driven
`hdr-cta-in` animuje `opacity` → konflikt o stejnou vlastnost (flicker, Safari).
Fix v `src/input.css`: odebrat `opacity` z transition `.hdr-cta` (ověřit
systematickým laděním). Týká se landingu i pod-stránek.

## C) Desaturace investorských barev (−25 % sat)
`investori-zamer.html`: `#7CBAF3→#8BB9E4`, `#F1EA8C→#E4DF99`, `#A3D697→#A8CE9F`
v `.zonebtn--{ctvrt,jadro,zazemi}` i inline `--c:` legendy. Mapové překryvy
`zona-*.jpg` zůstávají v originále.

## D) Zapojení
`Galerie` 404→`galerie.html` v menu (`index.html`, `struktura-webu.html`,
`galerie.html`); ve stromu `struktura-webu` status prep→live. Přidat `galerie.html`
do `tailwind.config.js` `content`. `npm run build`.

## Ověření
`npm run build` projde; `python3 -m http.server`; curl 200 na galerie.html;
vizuální kontrola gridu + lightboxu + subnav scrollu; flicker pryč; barvy tlumené.
