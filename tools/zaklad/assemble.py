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
    margin:0; background:#fff; color:var(--ink); overflow-x:clip;
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
  .vz .sec + .sec{margin-top:clamp(30px,4.5vw,52px)}
  /* full-bleed alternující podklad — odděluje hlavní sekce (jako zig-zag na landingu) */
  .vz .sec--shade{background:#F3F5FA;box-shadow:0 0 0 100vw #F3F5FA;clip-path:inset(0 -100vw);
    padding-top:clamp(22px,2.8vw,36px);padding-bottom:clamp(26px,3.4vw,44px)}
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
    border-right:1px solid #ECECF3;text-align:left;white-space:nowrap;vertical-align:top;
    transition:box-shadow .25s ease}
  @media (prefers-reduced-motion:reduce){ .vz .vz-matrix th,.vz .vz-matrix td{transition:none} }
  .vz .vz-matrix thead th{background:var(--tint);font-weight:700;border-bottom:1px solid var(--rule);
    white-space:normal;min-width:62px;max-width:150px}
  /* velké matice: vše zarovnané vlevo (sjednoceno; tabular-nums drží šířku číslic) */
  .vz .vz-matrix td.num{text-align:left;font-variant-numeric:tabular-nums}
  .vz .vz-matrix td.is-input{background:var(--accent-input)}
  .vz .vz-matrix .vz-stickcol{position:sticky;left:0;background:#fff;z-index:1;font-weight:600;
    border-right:1px solid var(--rule);min-width:104px;box-shadow:1px 0 0 0 var(--hair)}
  .vz .vz-matrix thead .vz-stickcol{z-index:3;background:var(--tint)}
  .vz .vz-matrix tbody tr:nth-child(even) td{background:var(--zebra)}
  .vz .vz-matrix tbody tr:nth-child(even) .vz-stickcol{background:var(--zebra)}
  .vz .vz-matrix tbody tr:nth-child(even) td.is-input{background:var(--accent-input)}
  /* hover ztmavení překryvnou vrstvou — funguje i přes barevné (cellfills) buňky */
  .vz .vz-matrix tbody tr:hover td{box-shadow:inset 0 0 0 999px rgba(42,42,96,.06)}
  .vz .vz-matrix tbody tr:hover .vz-stickcol{box-shadow:1px 0 0 0 var(--hair),inset 0 0 0 999px rgba(42,42,96,.06)}
  /* zvýraznění konektoru (rose) na hover/focus zdroje nebo cíle */
  .vz .vz-matrix tbody tr.is-flowmark td{box-shadow:inset 0 0 0 999px rgba(196,162,192,.30)}
  .vz .vz-matrix tbody tr.is-flowmark .vz-stickcol{box-shadow:1px 0 0 0 var(--hair),inset 0 0 0 999px rgba(196,162,192,.30)}
  /* zdrojový sloupec souhrnu: hover/focus na souhrnném boxu rozsvítí celý sloupec, z nějž
     hodnota vyplývá (a tabulka se k němu případně posune) */
  .vz .vz-matrix .is-colhot{box-shadow:inset 0 0 0 999px rgba(118,168,96,.36)}
  .vz .vz-matrix .vz-stickcol.is-colhot{box-shadow:1px 0 0 0 var(--rule),inset 0 0 0 999px rgba(118,168,96,.36)}
  .vz .vz-matrix thead .is-colhot{box-shadow:inset 0 0 0 999px rgba(118,168,96,.30)}
  .vz .is-colsrc{outline-color:#6F9E57 !important}
  .vz [data-hl-col]{cursor:default}
  /* zónové obarvení řádků parcel (žlutá=jádro, zelená=zázemí) — přebíjí zebru */
  .vz .vz-matrix tbody tr.is-jadro td,.vz .vz-matrix tbody tr.is-jadro .vz-stickcol{background:#F2ECC9}
  .vz .vz-matrix tbody tr.is-zazemi td,.vz .vz-matrix tbody tr.is-zazemi .vz-stickcol{background:#E2EFD9}
  /* věrné barvení buněk dle zdrojového Excelu (vstup oranžová, zelená, modrá…) */
  .vz .vz-matrix td.is-input,.vz .vz-matrix .vz-stickcol.is-input{background:#F0CFA0 !important}
  .vz .vz-matrix td.is-green,.vz .vz-matrix .vz-stickcol.is-green{background:#D4E6C6 !important}
  .vz .vz-matrix td.is-blue,.vz .vz-matrix .vz-stickcol.is-blue{background:#E6ECF6 !important}
  .vz .vz-matrix td.is-blue2,.vz .vz-matrix .vz-stickcol.is-blue2{background:#CBDDF1 !important}
  .vz .vz-matrix td.is-yellow,.vz .vz-matrix .vz-stickcol.is-yellow{background:#F2ECC9 !important}
  .vz .vz-matrix td.is-tan,.vz .vz-matrix .vz-stickcol.is-tan{background:#E6D9BF !important}
  .vz .val.is-green{background:#D4E6C6}
  /* červená čísla (font color z Excelu) */
  .vz .is-red,.vz .vz-matrix td.is-red,.vz .vz-matrix .vz-stickcol.is-red,
  .vz .vz-param__num.is-red,.vz .vz-gbox__num.is-red{color:#C8102E !important}
  /* obal posuvné tabulky: fade + scroll tlačítka zůstávají na hraně viditelné oblasti (ne uvnitř scrollu) */
  .vz .vz-mwrap{position:relative}
  .vz .vz-mwrap::before,.vz .vz-mwrap::after{content:"";position:absolute;top:0;bottom:0;width:34px;
    pointer-events:none;opacity:0;transition:opacity .2s;z-index:2}
  .vz .vz-mwrap::before{left:0;background:linear-gradient(to left,rgba(255,255,255,0),rgba(255,255,255,.92))}
  .vz .vz-mwrap::after{right:0;background:linear-gradient(to right,rgba(255,255,255,0),rgba(255,255,255,.92))}
  .vz .vz-mwrap.can-left::before{opacity:1}
  .vz .vz-mwrap.can-right::after{opacity:1}
  /* levý fade jen u tabulek BEZ ukotveného 1. sloupce (jinak budí dojem fixního sloupce) */
  .vz .vz-mwrap.has-stick::before{display:none}
  .vz .vz-mbtn{position:absolute;top:50%;transform:translateY(-50%);z-index:3;display:none;
    width:38px;height:38px;border-radius:9999px;border:1px solid var(--hair);background:rgba(255,255,255,.95);
    color:var(--ink);font:400 24px/1 system-ui,sans-serif;cursor:pointer;align-items:center;justify-content:center;
    box-shadow:0 4px 14px rgba(20,20,47,.18);-webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px);
    transition:background .15s,box-shadow .15s}
  .vz .vz-mbtn--left{left:7px}
  .vz .vz-mbtn--right{right:7px}
  .vz .vz-mwrap.can-left .vz-mbtn--left{display:inline-flex}
  .vz .vz-mwrap.can-right .vz-mbtn--right{display:inline-flex}
  .vz .vz-mbtn:hover{background:#fff;box-shadow:0 6px 18px rgba(20,20,47,.26)}
  .vz .vz-mbtn:active{transform:translateY(-50%) scale(.94)}
  .vz .vz-mbtn:focus-visible{outline:2px solid var(--link);outline-offset:2px}
  .vz .vz-mbtn svg{display:block}
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
  .vz .vz-sbox{background:var(--sbox-bg,#E7F0E3);border:1px solid var(--sbox-bd,#A8CE9F);border-radius:7px;padding:11px 13px}
  .vz .vz-sbox__label{display:block;font-size:.76rem;color:#3a3a52;line-height:1.3}
  .vz .vz-sbox__num{display:block;margin-top:5px;font-size:1.1rem;font-weight:700;font-variant-numeric:tabular-nums}
  /* souhrnné boxy finále (barva dle zdrojového fillu, volitelně cíl konektoru) */
  .vz .vz-grand{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:14px 0 4px}
  .vz .vz-gbox{background:var(--tint);border:1px solid var(--hair);padding:14px 16px;position:relative}
  .vz .vz-gbox.is-green{background:#D4E6C6;border-color:#A8CE9F}
  .vz .vz-gbox.is-yellow{background:#F2ECC9;border-color:#D8CD7E}
  .vz .vz-gbox.is-blue{background:#E6ECF6;border-color:#B6CDE9}
  .vz .vz-gbox.is-input{background:#F0CFA0;border-color:#D9B57E}
  .vz .vz-gbox__label{display:block;font-size:.82rem;color:#3a3a52;line-height:1.3}
  .vz .vz-gbox__num{display:block;margin-top:5px;font-size:clamp(1.3rem,3.2vw,1.85rem);font-weight:700;font-variant-numeric:tabular-nums;letter-spacing:-.01em}
  /* souhrnné / parametrické boxy: průhledný outline → plynulý náběh zvýraznění (delight) */
  .vz .vz-gbox,.vz .vz-param,.vz .vz-total,.vz .vz-sbox{outline:2px solid transparent;outline-offset:-2px;transition:outline-color .22s ease}
  .vz .vz-gbox.is-flowmark,.vz .vz-param.is-flowmark{outline-color:var(--rose,#C4A2C0)}
  /* zóna: velký nadpis + zelené title bandy dílčích tabulek */
  .vz .vz-zonehead{margin:clamp(38px,5.5vw,64px) 0 0;background:var(--band,#D4E6C6);
    border-top:2px solid var(--band-bd,#88B673);border-bottom:2px solid var(--band-bd,#88B673);
    padding:18px 16px;font-size:clamp(1.3rem,3vw,1.9rem);font-weight:700;
    line-height:1.25;color:var(--ink);text-wrap:balance}
  .vz .vz-zonehead__sub{display:block;margin-top:8px;font-size:.5em;font-weight:500;line-height:1.4;color:#39394f}
  .vz .vz-greenband{margin:22px 0 0;background:var(--band,#D4E6C6);padding:11px 15px;font-size:clamp(1rem,2vw,1.18rem);
    font-weight:700;line-height:1.3;color:var(--ink);text-wrap:balance}
  .vz .vz-greenband--center{text-align:center}
  /* 3 obrázky vedle sebe s popiskem pod (řada figur) */
  .vz .vz-figrow{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:12px 0 2px}
  .vz .vz-figrow figure{margin:0}
  .vz .vz-figrow img{display:block;width:100%;height:clamp(200px,18vw,300px);object-fit:cover;
    border:1px solid var(--hair)}
  .vz .vz-figrow figcaption{margin-top:7px;font-size:.78rem;color:var(--grey);line-height:1.4}
  @media (max-width:760px){ .vz .vz-figrow{grid-template-columns:1fr} .vz .vz-figrow img{height:clamp(200px,52vw,320px)} }
  /* konektor (náhrada původní zahnuté Excel šipky) — kreslí JS od vstupního parametru
     k cílovému souhrnu. Tabulky drží plnou šířku; oblouk volně přesahuje do okraje webu. */
  .vz .vz-flowblock{position:relative}
  .vz .vz-bigribbon{position:absolute;inset:0;width:100%;height:100%;overflow:visible;pointer-events:none;z-index:4}
  .vz .vz-bigribbon path{fill:none;stroke:var(--rose,#C4A2C0);stroke-width:1.7;opacity:.5;stroke-linecap:round;stroke-linejoin:round;transition:stroke-width .15s,opacity .15s}
  .vz .vz-flowblock.is-flowhot .vz-bigribbon path{stroke-width:3.4;opacity:1}
  @media (max-width:820px){ .vz .vz-bigribbon{display:none} }
  /* vstupní parametry jako barevné boxy */
  .vz .vz-params{display:flex;flex-wrap:wrap;gap:10px;margin:12px 0 2px}
  .vz .vz-param{flex:1 1 165px;background:#EEF1F6;border:1px solid var(--hair);border-radius:7px;padding:11px 13px}
  .vz .vz-param.is-input{background:#F0CFA0;border-color:#D9B57E}
  .vz .vz-param.is-green{background:#D4E6C6;border-color:#A8CE9F}
  .vz .vz-param.is-blue{background:#E6ECF6;border-color:#B6CDE9}
  .vz .vz-param__label{display:block;font-size:.76rem;color:#3a3a52;line-height:1.3}
  .vz .vz-param__num{display:block;margin-top:5px;font-size:1.1rem;font-weight:700;font-variant-numeric:tabular-nums}
  /* zvýrazněné info boxy = hranaté obdélníky (sjednoceno se zbytkem tabulek) */
  .vz .vz-total,.vz .vz-sbox,.vz .vz-bm,.vz .vz-param{border-radius:0}
  /* citace ze smlouvy (text místo obrázku) */
  .vz .vz-quote{margin:14px 0 0;padding:18px 20px;background:#FAFAFC;border:1px solid var(--hair);
    border-left:3px solid #88B673;font-size:.86rem;line-height:1.55;color:#2a2a44}
  .vz .vz-quote__head{margin:0 0 12px;font-weight:700;font-size:.98rem}
  .vz .vz-quote__list{margin:0;display:flex;flex-direction:column;gap:10px}
  .vz .vz-quote__list>div{display:grid;grid-template-columns:44px 1fr;gap:4px}
  .vz .vz-quote__list dt{margin:0;font-weight:700;font-variant-numeric:tabular-nums}
  .vz .vz-quote__list dd{margin:0;max-width:60ch;text-wrap:pretty}
  .vz .vz-quote__formula{display:block;text-align:center;font-style:italic;font-weight:700;font-size:1.05rem;margin:9px 0}
  .vz .vz-quote__where{display:block;margin-top:6px;padding-left:16px;color:#444}
  @media (max-width:680px){ .vz .vz-totals{grid-template-columns:1fr} .vz .vz-bmetrics{grid-template-columns:1fr} .vz .vz-quote__list>div{grid-template-columns:34px 1fr} }
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
    /* telefon: textové sloupce smí zalomit do 2 řádků (užší tabulka); čísla drží
       na řádku díky pevné mezeře (NBSP) a Kč/m² připojené přes NBSP */
    .vz .vz-matrix td{white-space:normal}
    .vz .vz-matrix .vz-stickcol{min-width:74px}
    .vz .vz-matrix thead th{min-width:50px;max-width:124px}
  }
  /* obrázky klikatelné na zvětšení */
  .vz figure img{cursor:zoom-in}
  /* lightbox (overlay na body, mimo .vz scope) */
  .lbx{position:fixed;inset:0;z-index:9999;display:none;align-items:center;justify-content:center;background:rgba(16,16,38,.92);padding:clamp(12px,4vw,48px)}
  .lbx.is-open{display:flex}
  .lbx__img{max-width:100%;max-height:88vh;width:auto;height:auto;object-fit:contain;border-radius:6px;box-shadow:0 20px 60px rgba(0,0,0,.5);background:#0c0c1e}
  .lbx__cap{position:absolute;left:0;right:0;bottom:max(12px,env(safe-area-inset-bottom));text-align:center;color:#e8e8f4;font-size:.85rem;padding:0 16px;line-height:1.4;margin:0}
  .lbx__btn{position:absolute;border:0;background:rgba(255,255,255,.12);color:#fff;cursor:pointer;width:46px;height:46px;border-radius:9999px;display:flex;align-items:center;justify-content:center;-webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px)}
  .lbx__btn:hover{background:rgba(255,255,255,.22)}
  .lbx__btn:focus-visible{outline:2px solid #fff;outline-offset:2px}
  .lbx__close{top:18px;right:18px}
  .lbx__prev{left:18px;top:50%;transform:translateY(-50%)}
  .lbx__next{right:18px;top:50%;transform:translateY(-50%)}
  .lbx__btn svg{display:block}
  @media (max-width:680px){ .lbx__prev{left:8px} .lbx__next{right:8px} .lbx__btn{width:40px;height:40px} }
</style>"""

TOPBAR = """<header class="inv-topbar">
  <input type="checkbox" id="inv-nav" class="inv-nav" aria-label="Přepnout menu" />
  <div class="inv-topbar__inner">
    <a class="inv-topbar__brand" href="index.html" aria-label="Startovací Hub, na úvod">
      <img src="assets/brand-logo-white.svg" alt="Startovací Hub" />
    </a>
    <nav class="inv-topnav" aria-label="Podklady pro investory">
      <a class="inv-topnav__link" href="investori-zamer.html">Investiční záměr</a>
      <a class="inv-topnav__link" href="investori-zaklad.html" aria-current="page">Základní údaje</a>
      <a class="inv-topnav__link" href="investori-scenare.html">Základní scénáře</a>
    </nav>
    <button type="button" class="inv-topbar__logout" data-inv-logout>Odhlásit se</button>
    <label for="inv-nav" class="inv-burger" aria-label="Otevřít menu">
      <span class="burger"><span></span><span></span><span></span></span>
    </label>
  </div>
  <nav class="inv-menu" aria-label="Podklady pro investory">
    <div class="inv-menu__inner">
      <a class="inv-menu__brand" href="index.html" aria-label="Startovací Hub, na úvod"><img src="assets/brand-logo-white.svg" alt="Startovací Hub" /></a>
      <div class="inv-menu__nav">
        <a class="inv-menu__link" href="investori-zamer.html">Investiční záměr</a>
        <a class="inv-menu__link" href="investori-zaklad.html" aria-current="page">Základní údaje</a>
        <a class="inv-menu__link" href="investori-scenare.html">Základní scénáře</a>
      </div>
      <div class="inv-menu__foot">
        <button type="button" class="inv-menu__logout" data-inv-logout>Odhlásit se</button>
      </div>
    </div>
  </nav>
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

  /* Vodorovně posuvné tabulky: tlačítka ‹ › pro plynulý posun + fade dle pozice. */
  (function () {
    var wraps = document.querySelectorAll('.vz-mwrap');
    Array.prototype.forEach.call(wraps, function (wrap) {
      var box = wrap.querySelector('.vz-matrix');
      var bl = wrap.querySelector('.vz-mbtn--left');
      var br = wrap.querySelector('.vz-mbtn--right');
      if (!box) return;
      if (box.querySelector('.vz-stickcol')) wrap.classList.add('has-stick');
      function update() {
        var max = box.scrollWidth - box.clientWidth;
        var x = box.scrollLeft;
        wrap.classList.toggle('can-left', max > 4 && x > 4);
        wrap.classList.toggle('can-right', max > 4 && x < max - 4);
      }
      function go(dir) { box.scrollBy({ left: dir * box.clientWidth * 0.8, behavior: 'smooth' }); }
      if (bl) bl.addEventListener('click', function () { go(-1); });
      if (br) br.addEventListener('click', function () { go(1); });
      box.addEventListener('scroll', update, { passive: true });
      window.addEventListener('resize', update);
      update();
    });
  })();

  /* Konektor (náhrada zahnuté Excel šipky): jemný oblouk od vstupního parametru
     (data-flow-source) k cílovému souhrnu (data-flow-target). Vede po pravém okraji
     a volně přesahuje do okraje webu; tabulky drží plnou šířku. Hover/focus zvýrazní
     linku i obě propojené hodnoty. */
  (function () {
    function draw(block) {
      var svg = block.querySelector('.vz-bigribbon');
      var source = block.querySelector('[data-flow-source]');
      var target = block.querySelector('[data-flow-target]');
      if (!svg || !source || !target) return;
      if (window.innerWidth < 820) { svg.innerHTML = ''; return; }
      var b = block.getBoundingClientRect();
      var s = source.getBoundingClientRect();
      var e = target.getBoundingClientRect();
      var W = b.width, H = b.height;
      var sx = W, sy = (s.top - b.top) + s.height / 2;
      var ex = W, ey = (e.top - b.top) + e.height / 2;
      var room = Math.max(40, Math.min(150, window.innerWidth - b.right + 70));
      var maxx = W + room;
      svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
      var c1x = maxx, c1y = sy + (ey - sy) * 0.12;
      var c2x = maxx, c2y = ey - (ey - sy) * 0.12;
      var d = 'M ' + sx + ' ' + sy + ' C ' + c1x + ' ' + c1y + ', ' + c2x + ' ' + c2y + ', ' + ex + ' ' + ey;
      var dx = ex - c2x, dy = ey - c2y, L = Math.sqrt(dx * dx + dy * dy) || 1; dx /= L; dy /= L;
      var px = -dy, py = dx, a = 10;
      var head = 'M ' + (ex - dx * a + px * a) + ' ' + (ey - dy * a + py * a) +
                 ' L ' + ex + ' ' + ey +
                 ' L ' + (ex - dx * a - px * a) + ' ' + (ey - dy * a - py * a);
      svg.innerHTML = '<path d="' + d + '"/><path d="' + head + '"/>';
    }
    function wire(block){
      var source = block.querySelector('[data-flow-source]');
      var target = block.querySelector('[data-flow-target]');
      if (!source || !target) return;
      function on(){ block.classList.add('is-flowhot'); source.classList.add('is-flowmark'); target.classList.add('is-flowmark'); }
      function off(){ block.classList.remove('is-flowhot'); source.classList.remove('is-flowmark'); target.classList.remove('is-flowmark'); }
      [source, target].forEach(function(el){
        el.addEventListener('mouseenter', on); el.addEventListener('mouseleave', off);
        el.setAttribute('tabindex', '0');
        el.addEventListener('focusin', on); el.addEventListener('focusout', off);
      });
    }
    var blocks = document.querySelectorAll('.vz-flowblock');
    function all(){ Array.prototype.forEach.call(blocks, draw); }
    Array.prototype.forEach.call(blocks, wire);
    all();
    window.addEventListener('resize', all);
    window.addEventListener('load', all);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(all);
  })();

  /* Propojení souhrnných boxů se zdrojovým sloupcem: hover/focus na boxu (data-hl-col)
     rozsvítí celý sloupec v příslušné tabulce, z nějž součet vyplývá, a je-li sloupec
     mimo viditelnou oblast, tabulku k němu vodorovně posune. */
  (function () {
    var boxes = document.querySelectorAll('[data-hl-col]');
    if (!boxes.length) return;
    function matrixFor(box){
      var sec = box.closest('section') || document;
      var prev = null;
      Array.prototype.forEach.call(sec.querySelectorAll('.vz-mwrap'), function(mw){
        if (box.compareDocumentPosition(mw) & Node.DOCUMENT_POSITION_PRECEDING) prev = mw;
      });
      return prev ? prev.querySelector('.vz-matrix') : null;
    }
    function reveal(matrix, cell){
      var mr = matrix.getBoundingClientRect(), cr = cell.getBoundingClientRect();
      if (cr.left >= mr.left + 4 && cr.right <= mr.right - 4) return;
      var t = matrix.scrollLeft + (cr.left - mr.left) - matrix.clientWidth / 2 + cr.width / 2;
      matrix.scrollTo({ left: Math.max(0, t), behavior: 'smooth' });
    }
    Array.prototype.forEach.call(boxes, function(box){
      var col = box.getAttribute('data-hl-col');
      var matrix = matrixFor(box);
      if (!matrix || !col) return;
      var cells = matrix.querySelectorAll('[data-col="' + col + '"]');
      if (!cells.length) return;
      var firstBody = matrix.querySelector('tbody [data-col="' + col + '"]') || cells[0];
      function on(){
        box.classList.add('is-colsrc');
        Array.prototype.forEach.call(cells, function(c){ c.classList.add('is-colhot'); });
        reveal(matrix, firstBody);
      }
      function off(){
        box.classList.remove('is-colsrc');
        Array.prototype.forEach.call(cells, function(c){ c.classList.remove('is-colhot'); });
      }
      box.addEventListener('mouseenter', on);
      box.addEventListener('mouseleave', off);
      box.setAttribute('tabindex', '0');
      box.addEventListener('focusin', on);
      box.addEventListener('focusout', off);
    });
  })();

  /* Lightbox: klik na obrázek v podkladech → zvětšení. Esc / pozadí / × zavře, ‹ › a ←/→ navigace. */
  (function () {
    var imgs = Array.prototype.slice.call(document.querySelectorAll('.vz figure img'));
    if (!imgs.length) return;
    var overlay, lbImg, lbCap, idx = -1, lastFocus = null;
    function build(){
      overlay = document.createElement('div');
      overlay.className = 'lbx'; overlay.setAttribute('role', 'dialog'); overlay.setAttribute('aria-modal', 'true'); overlay.setAttribute('aria-label', 'Náhled obrázku');
      overlay.innerHTML =
        '<button class="lbx__btn lbx__close" aria-label="Zavřít"><svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg></button>' +
        '<button class="lbx__btn lbx__prev" aria-label="Předchozí"><svg width="26" height="26" viewBox="0 0 24 24" fill="none"><path d="M15 5l-7 7 7 7" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>' +
        '<img class="lbx__img" alt="">' +
        '<button class="lbx__btn lbx__next" aria-label="Další"><svg width="26" height="26" viewBox="0 0 24 24" fill="none"><path d="M9 5l7 7-7 7" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>' +
        '<p class="lbx__cap"></p>';
      document.body.appendChild(overlay);
      lbImg = overlay.querySelector('.lbx__img'); lbCap = overlay.querySelector('.lbx__cap');
      overlay.addEventListener('click', function(e){ if (e.target === overlay) close(); });
      overlay.querySelector('.lbx__close').addEventListener('click', close);
      overlay.querySelector('.lbx__prev').addEventListener('click', function(e){ e.stopPropagation(); show(idx - 1); });
      overlay.querySelector('.lbx__next').addEventListener('click', function(e){ e.stopPropagation(); show(idx + 1); });
    }
    function capFor(im){ var f = im.closest('figure'), c = f && f.querySelector('figcaption'); return (c && c.textContent.trim()) || im.alt || ''; }
    function show(i){ idx = (i + imgs.length) % imgs.length; var im = imgs[idx]; lbImg.src = im.currentSrc || im.src; lbImg.alt = im.alt || ''; lbCap.textContent = capFor(im); }
    function open(i){ if (!overlay) build(); lastFocus = document.activeElement; show(i); overlay.classList.add('is-open'); document.body.style.overflow = 'hidden'; overlay.querySelector('.lbx__close').focus(); }
    function close(){ if (overlay) overlay.classList.remove('is-open'); document.body.style.overflow = ''; if (lastFocus && lastFocus.focus) lastFocus.focus(); }
    imgs.forEach(function(im, i){
      im.tabIndex = 0; im.setAttribute('role', 'button');
      var al = im.getAttribute('alt');
      im.setAttribute('aria-label', al ? al + ' – zvětšit' : 'Zvětšit obrázek');
      im.addEventListener('click', function(){ open(i); });
      im.addEventListener('keydown', function(e){ if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(i); } });
    });
    document.addEventListener('keydown', function(e){
      if (!overlay || !overlay.classList.contains('is-open')) return;
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowLeft') show(idx - 1);
      else if (e.key === 'ArrowRight') show(idx + 1);
      else if (e.key === 'Tab') {
        var f = overlay.querySelectorAll('.lbx__btn'), first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
  })();
</script>

</body>
</html>
"""

out = HEAD + body + "\n" + SCRIPTS
open(REPO + "/investori-zaklad.html", "w").write(out)
print("investori-zaklad.html written:", len(out), "bytes")
