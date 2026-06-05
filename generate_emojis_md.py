"""
Generate EMOJIS.md from client/emoji_data.py.
Run from the repo root: python generate_emojis_md.py
Auto-run by Claude Code after any edit to client/emoji_data.py.
"""
import re, sys, os
from collections import defaultdict, OrderedDict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'client'))
import emoji_data as e

src = open(os.path.join(os.path.dirname(__file__), 'client', 'emoji_data.py'),
           encoding='utf-8').read().splitlines()

# --- Build reverse map: type -> keywords ---
type_to_kws = defaultdict(list)
for kw, t in e._ICON_KEYWORDS.items():
    type_to_kws[t].append(kw)

# --- Parse ordered sections from the keywords dict ---
kw_start = next(i for i, l in enumerate(src) if '_ICON_KEYWORDS = {' in l)
kw_end   = next(i for i, l in enumerate(src) if i > kw_start and l == '}')

HEADER_RE = re.compile(r'\s*#\s*[─]+\s*(.+?)\s*[─]*\s*$')
ENTRY_RE  = re.compile(r'^\s*"([^"]+)"\s*:\s*"([^"]+)"')

events = []
for i in range(kw_start, kw_end):
    hm = HEADER_RE.match(src[i])
    if hm and '─' in src[i]:
        events.append(('section', hm.group(1).strip()))
    elif ENTRY_RE.match(src[i]):
        em = ENTRY_RE.match(src[i])
        events.append(('entry', em.group(2)))

section_types = OrderedDict()
current_section = 'General'
seen_types = set()

for tag, val in events:
    if tag == 'section':
        current_section = val
        if current_section not in section_types:
            section_types[current_section] = []
    elif tag == 'entry':
        if val not in seen_types and not val.startswith('flag_'):
            seen_types.add(val)
            if current_section not in section_types:
                section_types[current_section] = []
            section_types[current_section].append(val)

for t in e._ICON_EMOJIS:
    if t.startswith('flag_') or t in seen_types:
        continue
    if 'Uncategorized' not in section_types:
        section_types['Uncategorized'] = []
    section_types['Uncategorized'].append(t)

# --- Generate markdown ---
lines = []
lines.append('# 🏷️ Label Printer — Emoji Keyword Reference')
lines.append('')
lines.append('All keywords that auto-detect an emoji icon when typed in the label text.')
lines.append('Detection is **case-insensitive** and uses whole-word matching —')
lines.append('the **longest matching keyword wins** (e.g. "polar bear" beats "bear").')
lines.append('')

non_flag_types = [t for t in e._ICON_EMOJIS if not t.startswith('flag_')]
flag_types     = [t for t in e._ICON_EMOJIS if     t.startswith('flag_')]
lines.append('**%d keywords → %d emoji types** (%d country flags listed separately)' % (
    len(e._ICON_KEYWORDS), len(e._ICON_EMOJIS), len(flag_types)))
lines.append('')
lines.append('---')
lines.append('')

# Table of contents
lines.append('## Contents')
lines.append('')
for section in section_types:
    if not section_types[section]:
        continue
    anchor = re.sub(r'-+', '-', re.sub(r'[^a-z0-9-]', '-', section.lower())).strip('-')
    lines.append('- [%s](#%s)' % (section, anchor))
lines.append('- [Country Flags](#country-flags)')
lines.append('')
lines.append('---')
lines.append('')

# Sections
for section, types_in_section in section_types.items():
    if not types_in_section:
        continue
    lines.append('## %s' % section)
    lines.append('')
    lines.append('| Emoji | Keywords |')
    lines.append('|---|---|')
    for t in types_in_section:
        em  = e._ICON_EMOJIS.get(t, '')
        kws = sorted(type_to_kws.get(t, []), key=lambda k: (len(k.split()), k))
        kw_str = ', '.join(kws) if kws else '*(no direct keywords)*'
        lines.append('| %s | %s |' % (em, kw_str))
    lines.append('')

# Country flags
lines.append('## Country Flags')
lines.append('')
lines.append('All country and territory flags are supported via `flag_XX` keywords')
lines.append('where `XX` is the two-letter ISO country code (lowercase).')
lines.append('Flags require **Noto Color Emoji** installed to render.')
lines.append('')
lines.append('| Emoji | Keyword | Country |')
lines.append('|---|---|---|')

flag_comments = {}
for line in src:
    m = re.match(r'\s*"flag_([a-z]+)".*#\s*\S+\s+(.+)', line)
    if m:
        flag_comments[m.group(1)] = m.group(2).strip()

for t in sorted(flag_types):
    code    = t[5:]
    em      = e._ICON_EMOJIS.get(t, '')
    country = flag_comments.get(code, '')
    lines.append('| %s | `flag_%s` | %s |' % (em, code, country))

lines.append('')
lines.append('---')
lines.append('')
lines.append('*Auto-generated from `client/emoji_data.py` — do not edit manually.*')

output = '\n'.join(lines)
out_path = os.path.join(os.path.dirname(__file__), 'EMOJIS.md')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(output)
print('EMOJIS.md updated: %d keywords, %d types, %d lines' % (
    len(e._ICON_KEYWORDS), len(e._ICON_EMOJIS), len(lines)))
