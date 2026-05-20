#!/usr/bin/env python3
import re, pathlib, html, shutil
ROOT=pathlib.Path(__file__).parent
CONTENT=ROOT/'content'
PAGES=ROOT/'trips'
PAGES.mkdir(exist_ok=True)

def parse_md(path):
    txt=path.read_text(encoding='utf-8')
    meta={}
    if txt.startswith('---'):
        _, fm, body=txt.split('---',2)
        for line in fm.strip().splitlines():
            if ':' in line:
                k,v=line.split(':',1); meta[k.strip()]=v.strip().strip('"')
    else: body=txt
    paras=[p.strip() for p in re.split(r'\n\s*\n',body) if p.strip()]
    return meta, paras

def slug(path): return path.stem

def page_shell(title, body, depth=''):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(title)} | Rays Do Disney</title><link rel="stylesheet" href="{depth}assets/css/style.css"></head><body><nav class="nav"><div class="nav-inner"><a class="brand" href="{depth}index.html">Rays Do Disney</a><a href="{depth}index.html#reports">Trip Reports</a></div></nav>{body}<footer class="footer">Made for the Ray family Disney trip reports.</footer></body></html>"""

items=[]
for md in sorted(CONTENT.glob('*.md')):
    meta, paras=parse_md(md)
    y=meta.get('year','')
    title=meta.get('title',md.stem)
    typ=meta.get('type','trip')
    items.append({'slug':slug(md),'title':title,'year':y,'type':typ,'source':meta.get('source_file',''),'paras':paras})
items.sort(key=lambda r:(r['type']!='trip', r['year'], r['title']))

for item in items:
    photos=sorted((ROOT/'assets'/'photos'/item['year']).glob('*.jpg')) if item['year'] else []
    every=max(5, len(item['paras'])//(len(photos)+1) if photos else 999999)
    photo_i=0; chunks=[]
    for i,p in enumerate(item['paras'],1):
        chunks.append(f'<p>{html.escape(p)}</p>')
        if photo_i < len(photos) and i % every == 0:
            rel='../'+str(photos[photo_i].relative_to(ROOT))
            chunks.append(f'<figure class="trip-photo"><img loading="lazy" src="{rel}" alt="{html.escape(item["year"])} family vacation photo"><figcaption>{html.escape(item["year"])} vacation photo</figcaption></figure>')
            photo_i+=1
    while photo_i < len(photos):
        rel='../'+str(photos[photo_i].relative_to(ROOT))
        chunks.append(f'<figure class="trip-photo"><img loading="lazy" src="{rel}" alt="{html.escape(item["year"])} family vacation photo"><figcaption>{html.escape(item["year"])} vacation photo</figcaption></figure>')
        photo_i+=1
    body=f'<main class="wrap"><article class="report"><a class="back" href="../index.html#reports">← Back to all reports</a><span class="year">{html.escape(item["year"])}</span><h1>{html.escape(item["title"])}</h1><p class="muted">Source: {html.escape(item["source"])}</p>' + '\n'.join(chunks) + '</article></main>'
    (PAGES/(item['slug']+'.html')).write_text(page_shell(item['title'], body, '../'),encoding='utf-8')

cards=''.join([f'<a class="card" href="trips/{it["slug"]}.html"><span class="year">{html.escape(it["year"])}</span><h3>{html.escape(it["title"])}</h3><p>{html.escape(it["source"])} · Read the report</p></a>' for it in items if it['type']=='trip'])
extra=''.join([f'<a class="card" href="trips/{it["slug"]}.html"><span class="year">Extra</span><h3>{html.escape(it["title"])}</h3><p>{html.escape(it["source"])}</p></a>' for it in items if it['type']!='trip'])
extra_section=f'<h2 class="section-title" style="margin-top:38px">Extras</h2><div class="grid">{extra}</div>' if extra else ''
body=f"""<header class="hero"><div class="hero-card"><h1>Rays Do Disney</h1><p>Family Disney memories, trip reports, photos, and a little Main Street magic.</p><a class="button" href="#reports">Read the trip reports</a></div></header><main class="wrap" id="reports"><h2 class="section-title">Trip Reports</h2><p class="muted">Pick a year and start reading.</p><div class="grid">{cards}</div>{extra_section}</main>"""
(ROOT/'index.html').write_text(page_shell('Home', body, ''),encoding='utf-8')
print(f'Built {len(items)} pages.')
