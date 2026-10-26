#!/usr/bin/env python3
"""Compose the launcher's steel carapace from the existing Niri theme."""
from pathlib import Path
import re

root = Path(__file__).resolve().parent
bar = root / 'assets'
carapace = (bar / 'carapace.svg').read_text()
inner = re.sub(r'^.*?<svg[^>]*>', '', carapace, count=1, flags=re.S).rsplit('</svg>', 1)[0]
# Each reuse has independent gradient IDs.
def rail(prefix, y, flip=False):
    markup = re.sub(r'id="([^"]+)"', lambda m: f'id="{prefix}{m[1]}"', inner)
    markup = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{prefix}{m[1]})', markup)
    return f'<g transform="translate(0 {y})'+(' scale(1 -1)' if flip else '')+f'"><svg width="560" height="76" viewBox="0 0 640 84" preserveAspectRatio="none">{markup}</svg></g>'

svg=['''<svg xmlns="http://www.w3.org/2000/svg" width="560" height="580" viewBox="0 0 560 580">
<defs>
<linearGradient id="body" x2="0" y2="1"><stop stop-color="#202e38"/><stop offset=".18" stop-color="#0b141c"/><stop offset=".75" stop-color="#080e14"/><stop offset="1" stop-color="#1d2a33"/></linearGradient>
<linearGradient id="metal"><stop stop-color="#070c11"/><stop offset=".24" stop-color="#617581"/><stop offset=".42" stop-color="#c7d4dc"/><stop offset=".5" stop-color="#718794"/><stop offset=".78" stop-color="#24333d"/><stop offset="1" stop-color="#05090c"/></linearGradient>
<linearGradient id="rib"><stop stop-color="#17252e"/><stop offset=".36" stop-color="#aebdc6"/><stop offset=".49" stop-color="#d1dbe0"/><stop offset=".57" stop-color="#5c707c"/><stop offset="1" stop-color="#0b141b"/></linearGradient>
<linearGradient id="cavity" x2="0" y2="1"><stop stop-color="#0d1821"/><stop offset=".5" stop-color="#080e14"/><stop offset="1" stop-color="#101b24"/></linearGradient>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><path d="M0 3.5 H4" stroke="#b6d2e4" stroke-opacity=".018"/></pattern>
</defs>
<path d="M38 18 Q7 18 13 68 L19 140 Q8 290 19 440 L13 516 Q7 562 42 566 H518 Q553 562 547 516 L541 440 Q552 290 541 140 L547 68 Q553 18 522 18 Z" fill="#010407" stroke="#010407" stroke-width="9"/>
<path d="M38 20 Q12 20 16 68 L24 140 Q15 290 24 440 L16 516 Q12 560 42 560 H518 Q548 560 544 516 L536 440 Q545 290 536 140 L544 68 Q548 20 522 20 Z" fill="url(#body)" stroke="#7e929f" stroke-width="1.4"/>
<path d="M44 58 Q31 74 34 108 V480 Q31 504 48 522 H512 Q529 504 526 480 V108 Q529 74 516 58 Z" fill="url(#cavity)" stroke="#00060a" stroke-width="5"/>
<path d="M44 60 Q35 80 36 108 V480 Q35 502 49 520 H511 Q525 502 524 480 V108 Q525 80 516 60" fill="none" stroke="#728a99" stroke-opacity=".4"/>
<rect x="38" y="70" width="484" height="448" fill="url(#scan)"/>
''']
# Paired spinal conduits down the side walls, with individual engraved ribs.
for mirror in [False, True]:
    svg.append('<g'+(' transform="translate(560 0) scale(-1 1)"' if mirror else '')+'>')
    svg.append('<path d="M26 51 C40 92 11 160 22 232 S14 390 25 470 Q34 503 24 533" fill="none" stroke="#000509" stroke-width="17"/>')
    svg.append('<path d="M26 51 C40 92 11 160 22 232 S14 390 25 470 Q34 503 24 533" fill="none" stroke="url(#metal)" stroke-width="13"/>')
    for i,y in enumerate(range(76,510,8)):
        x=22 + (3 if 138<y<224 or 400<y<480 else 0)
        svg.append(f'<path d="M{x-7} {y} Q{x+2} {y+5} {x+7} {y+1}" fill="none" stroke="#040a10" stroke-width="4"/>')
        svg.append(f'<path d="M{x-7} {y-1} Q{x+2} {y+4} {x+7} {y}" fill="none" stroke="url(#rib)" stroke-width="2.6"/>')
    svg.append('</g>')
svg += [rail('top_',0), rail('bottom_',580,True)]
# Small inset seams connect the list to the armored rails.
svg.append('<path d="M43 76 H517 M43 504 H517" stroke="#9bb3c2" stroke-opacity=".16"/>')
svg.append('</svg>')
(root/'shell.svg').write_text('\n'.join(svg))

