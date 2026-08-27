#!/usr/bin/env python3
from pathlib import Path
p = Path('src/shear_hash.h')
t = p.read_text()
for a, b in [
    ('"shitcunt_v0.1"', '"ShitCunt"'),
    ('"shear-miner"', '"ShitCunt"'),
    ('"0.1.7"', '"v0.1"'),
]:
    t = t.replace(a, b)
# version may have been renamed already; force both macros
lines = []
for line in t.splitlines():
    if line.startswith('#define SHEAR_MINER_NAME'):
        line = '#define SHEAR_MINER_NAME "ShitCunt"'
    elif line.startswith('#define SHEAR_VERSION'):
        line = '#define SHEAR_VERSION "v0.1"'
    lines.append(line)
p.write_text('\n'.join(lines) + '\n')
for line in p.read_text().splitlines():
    if 'SHEAR_MINER_NAME' in line or 'SHEAR_VERSION' in line:
        print(line)
