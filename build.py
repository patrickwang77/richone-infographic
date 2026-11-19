"""Build the deck from src/template.html + data/*.json.

Outputs
  index.html     full HTML document (GitHub Pages / any static host)
  artifact.html  body-only fragment (claude.ai artifact, which supplies its own <html>/<head>)
"""
import json, pathlib

here = pathlib.Path(__file__).parent
t = (here / 'src' / 'template.html').read_text(encoding='utf-8')

def load(name):
    s = json.dumps(json.loads((here / 'data' / name).read_text(encoding='utf-8')),
                   ensure_ascii=False, separators=(',', ':'))
    assert '</' not in s
    return s

page = t.replace('/*SCENE_DATA*/', load('scene.json')).replace('/*WIND_DATA*/', load('wind.json'))

# fragment for the artifact
(here / 'artifact.html').write_text(page, encoding='utf-8')

# full document: everything up to </style> is head material, the rest is body
cut = page.index('</style>') + len('</style>')
head, body = page[:cut], page[cut:]
doc = ('<!doctype html>\n<html lang="zh-Hant-TW">\n<head>\n' + head +
       '\n<meta name="description" content="青埔禾林 RICH ONE 雙塔的 3D 基地環境分析：區位、量體、日照、陰影、風場、視野、交通、實價行情與站前開發。">\n'
       '</head>\n<body>\n' + body + '\n</body>\n</html>\n')
(here / 'index.html').write_text(doc, encoding='utf-8')
print('index.html', len(doc.encode('utf-8')), 'bytes; artifact.html', len(page.encode('utf-8')), 'bytes')
