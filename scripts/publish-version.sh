#!/usr/bin/env bash
#
# Verzovaný snapshot designu Startovacího Hubu (statický web).
#
# Web běží na GitHub Pages z větve `main` (root):
#   https://keiaiendiel.github.io/startovaci-hub/          = aktuální (root, = main)
#   https://keiaiendiel.github.io/startovaci-hub/vNNNPI/   = zmrazené snapshoty
#   https://keiaiendiel.github.io/startovaci-hub/verze.html = přehled všech verzí
#
# Snapshot = kopie všech HTML stránek + vlastní (verzově specifické) styles.css
# + fonty + loga. TĚŽKÁ MÉDIA (assets/images ~67 MB, assets/videos ~23 MB) se
# NEkopírují — sdílí se z rootu přes ../assets (proto se v HTML přepíše
# assets/images|videos → ../assets/...). Per verzi tak přibude jen ~200 kB.
# Kompromis (jako u sourozeneckého sh-webu): pozdější změna obrázku/videa v rootu
# se promítne i do starších verzí (sdílený root). Pro design-iterace, kde se mění
# hlavně layout/CSS/copy, je to v pohodě.
#
# Použití:
#   scripts/publish-version.sh 001PI ["krátký popis verze"]
#       → vytvoří/přepíše složku v001PI/ z AKTUÁLNÍHO stavu pracovního stromu
#         a přegeneruje verze.html (přehled). Do gitu skript NESAHÁ — zkontroluj,
#         zacommituj a zmerguj do main (Pages se přebuildí ~1 min).
#
set -euo pipefail

ARG="${1:?Zadej označení verze, např. 001PI}"
NOTE="${2:-}"
ROOT="$(git rev-parse --show-toplevel)"
DIR="v${ARG}"
DEST="$ROOT/$DIR"
TODAY="$(date +%F)"

cd "$ROOT"

echo "→ build CSS"
npm run build >/dev/null

echo "→ snapshot $DIR (z aktuálního stavu)"
rm -rf "$DEST"
mkdir -p "$DEST/assets"

# HTML stránky: odkazy na těžká média přepiš na sdílený root (../assets).
# verze.html (přehled) se do snapshotu nekopíruje.
shopt -s nullglob
for f in "$ROOT"/*.html; do
  base="$(basename "$f")"
  [ "$base" = "verze.html" ] && continue
  sed -e 's#assets/images/#../assets/images/#g' \
      -e 's#assets/videos/#../assets/videos/#g' \
      "$f" > "$DEST/$base"
done

# Lehké lokální assety: verzově specifické CSS + fonty + loga (zůstávají v assets/).
cp "$ROOT/assets/styles.css" "$DEST/assets/styles.css"
cp -R "$ROOT/assets/fonts" "$DEST/assets/fonts"
cp "$ROOT"/assets/brand-logo-*.svg "$DEST/assets/" 2>/dev/null || true

# Metadata verze (datum se zafixuje při vytvoření; popis volitelný).
printf '%s|%s|%s\n' "$DIR" "$TODAY" "$NOTE" > "$DEST/version.txt"

# Přegeneruj přehled verzí (verze.html) ze všech v*PI/version.txt — sestupně.
echo "→ přehled verze.html"
{
  cat <<'HTML_HEAD'
<!doctype html>
<html lang="cs">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <style>html{background:#14142f}</style>
  <title>Verze designu · Startovací Hub</title>
  <meta name="robots" content="noindex" />
  <link rel="preload" as="font" type="font/woff2" href="assets/fonts/AtypText-Special-Medium.woff2" crossorigin />
  <link rel="preload" as="font" type="font/woff2" href="assets/fonts/AtypText-Special-Bold.woff2" crossorigin />
  <link rel="stylesheet" href="assets/styles.css" />
  <style>
    .vrs{min-height:100svh;display:grid;place-items:center;padding:clamp(64px,10vw,128px) var(--gutter);
      color:#fff;background:radial-gradient(circle at 50% -8%,hsl(calc(var(--hue) + 44) 34% 64% / .30) 0,transparent 58%),
      linear-gradient(160deg,hsl(var(--hue) 41% 13%) 0,hsl(var(--hue) 37% 19%) 100%)}
    .vrs__in{width:100%;max-width:640px}
    .vrs__h{margin:0 0 6px;font-weight:600;font-size:clamp(1.9rem,3vw,2.4rem);letter-spacing:-.02em}
    .vrs__sub{margin:0 0 36px;color:rgba(255,255,255,.66);font-size:1.05rem}
    .vrs__list{list-style:none;margin:0;padding:0;display:grid;gap:12px}
    .vrs__item{display:flex;align-items:center;justify-content:space-between;gap:16px;
      padding:18px 22px;border-radius:14px;text-decoration:none;color:#fff;
      border:1px solid rgba(255,255,255,.16);background:rgba(255,255,255,.05);
      transition:background .18s ease,border-color .18s ease,transform .18s ease}
    .vrs__item:hover{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.4);transform:translateY(-2px)}
    .vrs__item--root{border-color:var(--rose)}
    .vrs__label{font-weight:700;font-size:1.15rem}
    .vrs__meta{display:block;margin-top:2px;color:rgba(255,255,255,.6);font-size:.92rem;font-weight:400}
    .vrs__go{flex-shrink:0;display:inline-flex;align-items:center;gap:6px;color:var(--rose);font-weight:700}
  </style>
</head>
<body>
  <main class="vrs">
    <div class="vrs__in">
      <h1 class="vrs__h">Verze designu</h1>
      <p class="vrs__sub">Archiv jednotlivých verzí webu Startovacího Hubu. Klikni a otevři.</p>
      <ul class="vrs__list">
        <li><a class="vrs__item vrs__item--root" href="./"><span><span class="vrs__label">Aktuální</span><span class="vrs__meta">živá verze (root) — vždy nejnovější</span></span><span class="vrs__go">Otevřít →</span></a></li>
HTML_HEAD

  # glob přes pole (zachová mezery v cestě); sestupně = od nejnovější verze
  metas=( "$ROOT"/v*PI/version.txt )
  for ((mi=${#metas[@]}-1; mi>=0; mi--)); do
    meta="${metas[$mi]}"
    [ -e "$meta" ] || continue
    IFS='|' read -r vlabel vdate vnote < "$meta"
    metaline="$vdate"
    [ -n "$vnote" ] && metaline="$vdate — $vnote"
    printf '        <li><a class="vrs__item" href="%s/"><span><span class="vrs__label">%s</span><span class="vrs__meta">%s</span></span><span class="vrs__go">Otevřít →</span></a></li>\n' \
      "$vlabel" "$vlabel" "$metaline"
  done

  cat <<'HTML_TAIL'
      </ul>
    </div>
  </main>
</body>
</html>
HTML_TAIL
} > "$ROOT/verze.html"

echo "✓ hotovo"
echo "  Lokální náhled:  http://127.0.0.1:8000/$DIR/   (přehled: /verze.html)"
echo "  Po commitu + merge do main:"
echo "    https://keiaiendiel.github.io/startovaci-hub/$DIR/"
echo "    https://keiaiendiel.github.io/startovaci-hub/verze.html"
