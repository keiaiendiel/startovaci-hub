# -*- coding: utf-8 -*-
"""Sestaví investori-zaklad.html: shell + inline .vz styly + vygenerované tělo."""
import os
SCRATCH = os.environ.get("SCRATCH") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
REPO = os.environ.get("REPO") or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
body = open(SCRATCH + "/body.html").read()

STYLE = r"""<style>
  .vz,.vz *{box-sizing:border-box}
  .vz{
    --ink:#2A2A60; --hair:#9696B9; --rule:#2A2A60; --grey:#7F7F7F; --link:#4351AD;
    --accent-input:#F0CFA0; --zebra:#FAFAFC;
    margin:0; background:#fff; color:var(--ink);
    font-family:'Atyp Special',system-ui,-apple-system,'Segoe UI',Arial,sans-serif;
    font-variant-numeric:tabular-nums lining-nums;
    -webkit-text-size-adjust:100%; -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility;
  }
  .vz .wrap{width:calc(100% - 2 * var(--gutter));max-width:var(--container-wide);margin:0 auto;padding:34px 0 72px}
  .vz a{color:var(--link)}
  /* cover */
  .vz .cover{margin:0 0 26px}
  .vz .kicker{font-size:clamp(1.05rem,2.4vw,1.35rem);font-weight:700;margin:0;letter-spacing:.005em}
  .vz .vpd{font-size:clamp(2.9rem,11vw,5rem);font-weight:700;line-height:.92;margin:.04em 0 .14em;letter-spacing:-.01em}
  .vz .upd{font-size:clamp(.85rem,1.6vw,1rem);margin:0;color:var(--ink)}
  /* section */
  .vz .sec{margin:0}
  .vz .sec + .sec{margin-top:clamp(26px,4vw,44px)}
  .vz .sechead{
    margin:0;background:var(--tint);
    border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);
    font-size:clamp(1.05rem,2.1vw,1.2rem);font-weight:700;line-height:1.3;padding:13px 15px;text-wrap:balance;
  }
  .vz .sec-lede{margin:12px 15px 0;font-size:clamp(.85rem,1.5vw,.95rem);line-height:1.5;color:#3a3a52;max-width:80ch}
  .vz .vz-subhead{margin:24px 15px 6px;font-size:clamp(.95rem,1.7vw,1.08rem);font-weight:700;color:var(--ink)}
  /* label→value (kv) — reuse .row grid */
  .vz .vz-kv{margin:6px 0 0;border-top:1px solid var(--hair)}
  .vz .row{display:grid;grid-template-columns:1.25fr 1fr}
  .vz .lab,.vz .val{
    padding:11px 15px;font-size:clamp(.875rem,1.5vw,.95rem);line-height:1.35;
    border-bottom:1px solid var(--hair);overflow-wrap:anywhere;text-wrap:balance;
  }
  .vz .lab{background:#fff}
  .vz .val{background:var(--tint)}
  .vz .val.num{font-weight:700;font-variant-numeric:tabular-nums;text-align:right}
  .vz .val.is-input{background:var(--accent-input)}
  .vz .val a{color:var(--link);text-decoration:underline;text-underline-offset:2px;overflow-wrap:anywhere}
  .vz .foot{font-style:italic;font-size:.8rem;line-height:1.45;color:#444;margin:9px 15px 0;max-width:100ch}
  /* legend pro vstupní buňky */
  .vz .vz-legend-input{display:flex;align-items:center;gap:8px;margin:8px 15px 0;font-size:.8rem;color:#444}
  .vz .vz-swatch{display:inline-block;width:14px;height:14px;border-radius:3px;background:var(--accent-input);border:1px solid rgba(0,0,0,.14);flex:none}
  /* ---- široká matice: vodorovný posuv + ukotvený 1. sloupec ---- */
  .vz .vz-matrix{position:relative;overflow-x:auto;margin:8px 0 0;border:1px solid var(--hair);
    -webkit-overflow-scrolling:touch;scrollbar-width:thin;scroll-snap-type:none}
  .vz .vz-matrix:focus-visible{outline:2px solid var(--link);outline-offset:2px}
  .vz .vz-matrix table{border-collapse:separate;border-spacing:0;width:max-content;min-width:100%;
    font-size:.8rem;line-height:1.3}
  .vz .vz-matrix th,.vz .vz-matrix td{padding:7px 10px;border-bottom:1px solid var(--hair);
    border-right:1px solid #ECECF3;text-align:left;white-space:nowrap;vertical-align:top}
  .vz .vz-matrix thead th{background:var(--tint);font-weight:700;border-bottom:1px solid var(--rule);
    white-space:normal;min-width:62px;max-width:150px}
  .vz .vz-matrix td.num{text-align:right;font-variant-numeric:tabular-nums}
  .vz .vz-matrix td.is-input{background:var(--accent-input)}
  .vz .vz-matrix .vz-stickcol{position:sticky;left:0;background:#fff;z-index:1;font-weight:600;
    border-right:1px solid var(--rule);min-width:104px;box-shadow:1px 0 0 0 var(--hair)}
  .vz .vz-matrix thead .vz-stickcol{z-index:3;background:var(--tint)}
  .vz .vz-matrix tbody tr:nth-child(even) td{background:var(--zebra)}
  .vz .vz-matrix tbody tr:nth-child(even) .vz-stickcol{background:var(--zebra)}
  .vz .vz-matrix tbody tr:nth-child(even) td.is-input{background:var(--accent-input)}
  .vz .vz-matrix tbody tr:hover td{background:#F0F0FA}
  .vz .vz-matrix tbody tr:hover .vz-stickcol{background:#F0F0FA}
  /* zónové obarvení řádků parcel (žlutá=jádro, zelená=zázemí) — přebíjí zebru */
  .vz .vz-matrix tbody tr.is-jadro td,.vz .vz-matrix tbody tr.is-jadro .vz-stickcol{background:#F2ECC9}
  .vz .vz-matrix tbody tr.is-zazemi td,.vz .vz-matrix tbody tr.is-zazemi .vz-stickcol{background:#E2EFD9}
  .vz .vz-matrix tbody tr.is-jadro:hover td,.vz .vz-matrix tbody tr.is-jadro:hover .vz-stickcol{background:#ECE4B4}
  .vz .vz-matrix tbody tr.is-zazemi:hover td,.vz .vz-matrix tbody tr.is-zazemi:hover .vz-stickcol{background:#D4E7C7}
  /* věrné barvení buněk dle zdrojového Excelu (vstup oranžová, zelená, modrá…) */
  .vz .vz-matrix td.is-input,.vz .vz-matrix .vz-stickcol.is-input{background:#F0CFA0 !important}
  .vz .vz-matrix td.is-green,.vz .vz-matrix .vz-stickcol.is-green{background:#D4E6C6 !important}
  .vz .vz-matrix td.is-blue,.vz .vz-matrix .vz-stickcol.is-blue{background:#E6ECF6 !important}
  .vz .vz-matrix td.is-blue2,.vz .vz-matrix .vz-stickcol.is-blue2{background:#CBDDF1 !important}
  .vz .vz-matrix td.is-yellow,.vz .vz-matrix .vz-stickcol.is-yellow{background:#F2ECC9 !important}
  .vz .vz-matrix td.is-tan,.vz .vz-matrix .vz-stickcol.is-tan{background:#E6D9BF !important}
  .vz .val.is-green{background:#D4E6C6}
  .vz .vz-matrix::after{content:"";position:absolute;top:0;right:0;width:24px;height:100%;
    pointer-events:none;background:linear-gradient(to right,rgba(255,255,255,0),rgba(255,255,255,.85))}
  /* headline číslo */
  .vz .vz-headline{margin:14px 0 0;padding:18px;background:var(--tint);
    border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);display:flex;flex-direction:column;gap:5px}
  .vz .vz-headline__label{font-size:.85rem;color:#3a3a52;max-width:70ch}
  .vz .vz-headline__num{font-size:clamp(1.7rem,5vw,2.6rem);font-weight:700;line-height:1;letter-spacing:-.015em;font-variant-numeric:tabular-nums}
  .vz .vz-headline__sub{font-size:.8rem;color:var(--grey)}
  /* zdroje */
  .vz .vz-sources{margin:10px 15px 0;padding:0 0 0 1.1em;font-size:.88rem;line-height:1.55}
  .vz .vz-sources li{margin:0 0 7px}
  /* vizualizace — vodorovně posuvný „filmstrip" s pevnou výškou (bez JS).
     Pevná výška + width:auto → různé poměry stran sdílí stejnou výšku řádku. */
  .vz .vz-figs{display:flex;gap:14px;overflow-x:auto;margin:8px 0 2px;padding:2px 15px 12px;
    scroll-snap-type:x mandatory;scrollbar-width:thin;-webkit-overflow-scrolling:touch;align-items:flex-start}
  .vz .vz-figs figure{flex:0 0 auto;margin:0;scroll-snap-align:start;max-width:680px}
  .vz .vz-figs img{display:block;height:clamp(200px,26vw,300px);width:auto;max-width:680px;
    border:1px solid var(--hair);border-radius:7px;background:#f1f1f6}
  .vz .vz-figs figcaption{margin-top:7px;font-size:.78rem;color:var(--grey);line-height:1.4;max-width:680px}
  /* ribbon konektor (náhrada Excel šipek): tok konkrétní hodnoty do dalšího výpočtu.
     Zaoblený rose tah + šipka dolů, v duchu brand .ribbon. */
  .vz .vz-flow{display:flex;align-items:center;justify-content:center;gap:13px;margin:14px 15px 6px}
  .vz .vz-flow__svg{flex:none;overflow:visible}
  .vz .vz-flow__band,.vz .vz-flow__head{fill:none;stroke:var(--rose,#C4A2C0);stroke-width:3;
    stroke-linecap:round;stroke-linejoin:round}
  .vz .vz-flow span{font-size:.78rem;font-weight:600;color:#8d6a86;line-height:1.35;max-width:64ch}
  @media (max-width:680px){ .vz .vz-flow{gap:9px} .vz .vz-flow span{font-size:.74rem} }
  /* mapy na celou šířku (masterplan + ortofoto breakdowny) */
  .vz .vz-map{margin:12px 0 0}
  .vz .vz-map img{display:block;width:100%;height:auto;border:1px solid var(--hair);border-radius:8px;background:#f1f1f6}
  .vz .vz-map figcaption{margin:8px 2px 0;font-size:.8rem;color:var(--grey);font-style:italic;line-height:1.4}
  /* zvýrazněné souhrnné boxy (Celková výměra…) */
  .vz .vz-totals{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:16px 0 4px}
  .vz .vz-total{background:#E7F0E3;border:1px solid #A8CE9F;border-radius:8px;padding:14px 16px}
  .vz .vz-total__label{display:block;font-size:.82rem;color:#3a3a52;line-height:1.3}
  .vz .vz-total__num{display:block;margin-top:4px;font-size:clamp(1.35rem,3.4vw,1.9rem);font-weight:700;font-variant-numeric:tabular-nums;letter-spacing:-.01em}
  /* breakdown metriky (Pozemky: jádro / zázemí …) */
  .vz .vz-bmetrics{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:12px 0 2px}
  .vz .vz-bm{background:var(--tint);border:1px solid var(--hair);border-radius:7px;padding:11px 13px}
  .vz .vz-bm--area{background:#E7F0E3;border-color:#A8CE9F}
  .vz .vz-bm__label{display:block;font-size:.74rem;color:var(--grey);line-height:1.3}
  .vz .vz-bm__num{display:block;margin-top:5px;font-size:1.15rem;font-weight:700;font-variant-numeric:tabular-nums}
  /* zelené souhrnné boxy (auto-fit řada) */
  .vz .vz-summary{display:grid;grid-template-columns:repeat(auto-fit,minmax(165px,1fr));gap:10px;margin:12px 0 2px}
  .vz .vz-sbox{background:#E7F0E3;border:1px solid #A8CE9F;border-radius:7px;padding:11px 13px}
  .vz .vz-sbox__label{display:block;font-size:.76rem;color:#3a3a52;line-height:1.3}
  .vz .vz-sbox__num{display:block;margin-top:5px;font-size:1.1rem;font-weight:700;font-variant-numeric:tabular-nums}
  /* zóna: velký nadpis + zelené title bandy dílčích tabulek */
  .vz .vz-zonehead{margin:clamp(38px,5.5vw,64px) 0 0;background:#D4E6C6;border-top:2px solid #88B673;
    border-bottom:2px solid #88B673;padding:18px 16px;font-size:clamp(1.3rem,3vw,1.9rem);font-weight:700;
    line-height:1.25;color:var(--ink);text-wrap:balance}
  .vz .vz-greenband{margin:22px 0 0;background:#D4E6C6;padding:11px 15px;font-size:clamp(1rem,2vw,1.18rem);
    font-weight:700;line-height:1.3;color:var(--ink);text-wrap:balance}
  .vz .vz-greenband--center{text-align:center}
  /* vstupní parametry jako barevné boxy */
  .vz .vz-params{display:flex;flex-wrap:wrap;gap:10px;margin:12px 0 2px}
  .vz .vz-param{flex:1 1 165px;background:#EEF1F6;border:1px solid var(--hair);border-radius:7px;padding:11px 13px}
  .vz .vz-param.is-input{background:#F0CFA0;border-color:#D9B57E}
  .vz .vz-param.is-green{background:#D4E6C6;border-color:#A8CE9F}
  .vz .vz-param.is-blue{background:#E6ECF6;border-color:#B6CDE9}
  .vz .vz-param__label{display:block;font-size:.76rem;color:#3a3a52;line-height:1.3}
  .vz .vz-param__num{display:block;margin-top:5px;font-size:1.1rem;font-weight:700;font-variant-numeric:tabular-nums}
  @media (max-width:680px){ .vz .vz-totals{grid-template-columns:1fr} .vz .vz-bmetrics{grid-template-columns:1fr} }
  /* verze dole */
  .vz .vzver{display:flex;flex-direction:column;align-items:center;gap:4px;margin:44px 0 8px;text-align:center}
  .vz .vzver p{margin:0;color:var(--grey);font-size:.7rem;letter-spacing:.02em}
  .vz .vzver p:last-child{font-weight:700}
  /* mobil */
  @media (max-width:680px){
    .vz .wrap{padding:22px 0 44px}
    .vz .vz-kv .row{display:flex;flex-wrap:wrap;align-items:baseline;column-gap:7px;row-gap:1px;padding:8px 15px}
    .vz .vz-kv .row:nth-of-type(even){background:var(--tint)}
    .vz .vz-kv .lab{border-bottom:0;padding:0;font-weight:500;background:transparent;line-height:1.32}
    .vz .vz-kv .val{padding:0;background:transparent;line-height:1.32;border-bottom:0;text-align:left}
    .vz .vz-kv .val.is-input{background:transparent;font-weight:700;color:#9a6a1e}
    .vz .sechead{padding:11px 14px}
    .vz .vz-subhead{margin:18px 14px 6px}
  }
</style>"""

TOPBAR = """<header class="inv-topbar">
  <div class="inv-topbar__inner">
    <a class="inv-topbar__brand" href="index.html" aria-label="Startovací Hub, na úvod">
      <img src="assets/brand-logo-white.svg" alt="Startovací Hub" />
    </a>
    <span class="inv-topbar__title">Podklady pro investory</span>
    <div class="inv-topbar__actions">
      <nav class="inv-seg" aria-label="Přepnout podklad">
        <a class="inv-seg__item" href="investori-zamer.html">Investiční záměr</a>
        <a class="inv-seg__item" href="investori-zaklad.html" aria-current="page">Základní údaje</a>
      </nav>
      <button type="button" class="inv-topbar__logout" data-inv-logout>Odhlásit se</button>
    </div>
  </div>
</header>"""

HEAD = """<!doctype html>
<html lang="cs" class="inv-wait">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="format-detection" content="telephone=no">
<meta name="robots" content="noindex, nofollow">
<style>html{background:#14142f}</style>
<meta name="description" content="Základní údaje a výpočty k investičnímu záměru VPD1, areál Horních kasáren v Klecanech. Podklady pro investory.">
<title>Základní údaje &amp; výpočty · VPD1 · podklady pro investory</title>

<!-- Měkká brána: bez platného otisku zpět na login (jako investori-zamer). -->
<style>html.inv-wait .vz{visibility:hidden}</style>
<script>
  (function () {
    var ALLOW = ['2250c0a01e81a5c7c27c6a9632b9f92faed24cfba6868421b7311472982a1b06'];
    var ok = false;
    try { ok = ALLOW.indexOf(localStorage.getItem('vpd1-auth')) !== -1; } catch (e) {}
    if (!ok) { location.replace('investori.html'); }
    else { document.documentElement.classList.remove('inv-wait'); }
  })();
</script>

<link rel="preload" as="font" type="font/woff2" href="assets/fonts/AtypText-Special-Medium.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="assets/fonts/AtypText-Special-Bold.woff2" crossorigin>
<link rel="stylesheet" href="assets/styles.css">

<!--
  Základní údaje & výpočty VPD1 — web verze listu „Základní údaje & výpočty" z tabulky
  Záměr VPD1_5.xlsx (verze 2p8iaz6, 15. 6. 2026). Sourozenec investori-zamer.html:
  stejná měkká brána, top bar (s přepínačem), Atyp Special. Data generována deterministicky
  z Excelu (openpyxl); čísla 1:1, čisté nadpisy sloupců, sekce poskládané pod sebe.
-->
""" + STYLE + """
</head>
<body>

""" + TOPBAR + """

<noscript>
  <p style="max-width:680px;margin:48px auto;padding:0 20px;font:500 1rem/1.6 'Atyp Special',system-ui,-apple-system,sans-serif;color:#2A2A60;text-align:center">
    Podklady pro investory se zobrazí jen se zapnutým JavaScriptem.
  </p>
</noscript>

"""

SCRIPTS = """
<script>
  /* Odhlášení: smaž otisk a zpět na login. */
  (function () {
    var btn = document.querySelector('[data-inv-logout]');
    if (!btn) return;
    btn.addEventListener('click', function () {
      try { localStorage.removeItem('vpd1-auth'); } catch (e) {}
      location.href = 'investori.html';
    });
  })();
</script>

</body>
</html>
"""

out = HEAD + body + "\n" + SCRIPTS
open(REPO + "/investori-zaklad.html", "w").write(out)
print("investori-zaklad.html written:", len(out), "bytes")
