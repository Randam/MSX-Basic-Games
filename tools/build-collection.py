"""Render the static collection page from the curated collection.json. No network needed."""
from pathlib import Path
from html import escape as e
import json,re
root=Path(__file__).resolve().parents[1];dist=root/'dist';items=json.loads((dist/'collection.json').read_text());base=(dist/'msx-basic.html').read_text()
brand_count=len(set(x['brand'] for x in items))
head=base[:base.index('</head>')]
head=re.sub(r'<title>.*?</title>','<title>Mijn MSX-verzameling — Jer’s MSX</title>',head)
head=head.replace('msx-basic.html','verzameling.html').replace('Ontdek de MSX-standaard &amp; MSX-BASIC — Jer’s MSX','Mijn MSX-verzameling — Jer’s MSX').replace('Ontdek de MSX-standaard & MSX-BASIC — Jer’s MSX','Mijn MSX-verzameling — Jer’s MSX')
old='Ontdek de MSX-standaard en de generaties MSX, MSX2, MSX2+ en turbo R. Met Jeroens programma’s, tijdschriften en een speelbare BASIC-listing.'
head=head.replace(old,f'{len(items)} computers, {brand_count} merken en een persoonlijk MSX-verhaal. Ontdek de verzameling van Jeroen Derwort, van de Philips VG-8020 tot de Panasonic turbo R.')
head=head.replace('social-msxbasic.jpg','social-collection.jpg').replace('Jer’s MSX: 27 originele BASIC-games, met het MSX-logo en Airplane op een Philips-computer met beeldbuis.',f'Mijn MSX-verzameling: {len(items)} computers en {brand_count} merken, met de Panasonic FS-A1ST, Philips VG-8020 en Yamaha SX-100.')
head+='<link rel="stylesheet" href="collection.css?v=20261025b">\n'
header=base[base.index('<header'):base.index('<main')].replace('class="active" aria-current="page" href="msx-basic.html"','href="msx-basic.html"')
header=header.replace('</nav>','<a class="active" aria-current="page" href="verzameling.html">Mijn verzameling</a></nav>') if 'href="verzameling.html"' not in header else header.replace('href="verzameling.html"','class="active" aria-current="page" href="verzameling.html"')
footer=base[base.index('<footer'):base.index('<script type="module" src="learn.js"')]
brands=sorted(set(x['brand'] for x in items));groups=['MSX1','MSX2','MSX2+','MSX turbo R','Compatible']
options=''.join(f'<option value="{e(b)}">{e(b)}</option>' for b in brands)
filters=''.join(f'<button type="button" data-generation="{e(g)}" aria-pressed="false">{e(g)}</button>' for g in groups)
labels={'philips-vg-8020':'Mijn eerste MSX','philips-vg-8235':'Mijn oorspronkelijke MSX2','panasonic-fs-a1st':'Nu op mijn bureau','yamaha-sx-100':'Mijn favoriete vormgeving','toshiba-hx-10':'Omgebouwd naar MSX2+'}
cards=[]
for n,x in enumerate(items,1):
 title=e(x['title']);id=e(x['id']);desc=x['description'];first=re.split(r'(?<=[.!?])\s+',desc)[0]
 facts=''.join(f'<div><dt>{k}</dt><dd>{e(x[key])}</dd></div>' for k,key in [('Bijzonderheden','features'),('Mijn aanpassingen','changes')] if x[key])
 badge=f'<span class="personal-tag">{labels[x["id"]]}</span>' if x['id'] in labels else ''
 description=''.join(f'<p>{e(p)}</p>' for p in desc.split('\n\n'))
 cards.append(f'''<article class="collection-card" id="{id}" data-brand="{e(x['brand'])}" data-generation="{e(x['generationGroup'])}">
<a class="collection-photo" href="{e(x['image'])}" target="_blank" rel="noopener" aria-label="Bekijk de foto van {title} groter"><img src="{e(x['image'])}" alt="Modelfoto van de {title}" width="600" height="400" loading="lazy" decoding="async"><span aria-hidden="true">↗</span></a>
<div class="collection-card-body"><div class="card-kicker"><span>{e(x['generation'])}</span><span>{x['year']}</span></div><h3>{title}</h3>{badge}<p class="card-preview">{e(first)}</p><dl class="computer-specs"><div><dt>Merk</dt><dd>{e(x['brand'])}</dd></div><div><dt>RAM</dt><dd>{e(x['ram'])}</dd></div></dl>
<details><summary>Het verhaal &amp; de details <span aria-hidden="true">+</span></summary><div class="computer-story">{description}{'<dl class="extra-specs">'+facts+'</dl>' if facts else ''}<a class="model-source" href="{e(x['reference'])}" target="_blank" rel="noopener">Meer over dit model ↗</a><p class="photo-credit">Modelfoto: <a href="{e(x['photoSource'])}" target="_blank" rel="noopener">{e(x['photoCredit'])}</a></p></div></details></div></article>''')
page=f'''{head}</head><body>{header}<main class="collection-page">
<section class="collection-hero"><div><p class="eyebrow">JEROEN DERWORT / DE HARDWARE</p><h1>Mijn MSX-<br>verzameling<span class="orange">.</span></h1><p class="collection-lead">Op de MSX zette ik mijn eerste stappen als programmeur en gamemaker. Mijn oorspronkelijke MSX2 heb ik altijd bewaard. Inmiddels verzamel ik vooral de verschillen: de merken, de vormen en de eigenzinnige ideeën.</p><a class="text-link" href="#computers">Bekijk de computers <span aria-hidden="true">↓</span></a></div><figure class="collection-hero-photo"><span class="hero-photo-label">NU OP MIJN BUREAU</span><img src="assets/collection/panasonic-fs-a1st.jpg" alt="Modelfoto van de Panasonic FS-A1ST MSX turbo R" width="1280" height="872" fetchpriority="high"><figcaption><strong>Panasonic FS-A1ST</strong><span>MSX turbo R · 1990 · Mijn exemplaar: 512 kB RAM</span></figcaption></figure></section>
<div class="collection-stats" aria-label="De verzameling in cijfers"><div><strong>{len(items):02d}</strong><span>COMPUTERS</span></div><div><strong>{len(brands):02d}</strong><span>MERKEN</span></div><div><strong>1983—2025</strong><span>VAN HOME­COMPUTER TOT LAPTOP</span></div><p>Elk model heeft iets bijzonders.<br>Dat maakt het verzamelen zo leuk.</p></div>
<aside class="photo-note"><span aria-hidden="true">↗</span><p><strong>De modellen in beeld.</strong> De foto’s tonen de verschillende computertypes, niet mijn eigen exemplaren. De verhalen en genoemde aanpassingen gaan wel over mijn verzameling.</p></aside>
<section id="computers" aria-labelledby="computers-title"><div class="collection-heading"><div><p class="eyebrow">DE COLLECTIE</p><h2 id="computers-title">Alle computers.<br>Elk een eigen verhaal.</h2></div><p>Van een ingebouwde telefoon en een thermische printer tot een FM-synthesizer. De MSX-standaard liet ruimte voor heel verschillende computers.</p></div>
<div class="collection-tools" hidden><div class="collection-inputs"><label>Zoek in de verzameling<input id="collection-search" type="search" placeholder="Model, merk of bijzonderheid…" autocomplete="off"></label><label>Merk<select id="collection-brand"><option value="">Alle merken</option>{options}</select></label></div><div class="generation-filters" role="group" aria-label="Filter op MSX-generatie"><button type="button" data-generation="" aria-pressed="true">Alles</button>{filters}</div><div class="filter-status"><p id="collection-count" role="status" aria-live="polite">{len(items)} computers</p><button id="reset-collection" type="button">Wis filters ↺</button></div></div>
<div class="collection-grid">{''.join(cards)}</div><p id="collection-empty" hidden>Geen computers gevonden. Probeer een andere zoekterm of wis de filters.</p></section>
<section class="collection-origin"><div><p class="eyebrow">EEN VERZAMELING MET EEN VERHAAL</p><h2>Het begon met<br>een Philips.</h2></div><div><p>Op de VG-8020 leerde ik begin jaren ’90 programmeren. Die verkocht ik toen de VG-8235 kwam. Mijn oorspronkelijke MSX2 is altijd gebleven; later vond ik ook weer een VG-8020. Vanuit die herinneringen groeide de verzameling uit tot al deze verschillende modellen.</p><p>Deze pagina is gebaseerd op <a href="https://www.jeroenderwort.nl/msx-computer-verzameling/" target="_blank" rel="noopener">mijn collectieoverzicht op jeroenderwort.nl ↗</a>. De persoonlijke beschrijvingen en aanpassingen komen uit dat overzicht; aanvullende modelinformatie is gebaseerd op de gelinkte bronnen. Via de details bij iedere computer vind je de fotovermelding en meer informatie over het model.</p><a class="text-link" href="msx-basic.html#msx-standaard">Lees meer over de MSX-standaard ↗</a></div></section>
<section class="back-to-play"><p class="eyebrow">VAN HARDWARE NAAR SOFTWARE</p><h2>Speel mijn eigen BASIC-games.</h2><a class="solid-button" href="index.html#speelkamer">Naar de speelkamer ↗</a></section></main>{footer}<script type="module" src="collection.js?v=20261025b"></script><script defer src="analytics.js?v=20261026"></script></body></html>'''
(dist/'verzameling.html').write_text(page)
# Keep collection counters consistent in the homepage and social composition.
home=dist/'index.html'
home.write_text(re.sub(r'(?<=id="collection-invitation-title">)\d+ computers',f'{len(items)} computers',home.read_text()))
social=root/'tools/social-collection.html'
social.write_text(re.sub(r'\d+ computers\. \d+ merken\.',f'{len(items)} computers. {brand_count} merken.',social.read_text()))
print(f'Rendered {len(items)} computers / {len(brands)} brands')
