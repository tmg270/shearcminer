#!/usr/bin/env python3
from pathlib import Path
p = Path('src/shear_hash.h')
t = p.read_text()
t = t.replace('"0.1.7"', '"shitcunt_v0.1"')
t = t.replace('"shear-miner"', '"shitcunt_v0.1"')
p.write_text(t)
for line in p.read_text().splitlines():
    if 'SHEAR_MINER_NAME' in line or 'SHEAR_VERSION' in line:
        print(line)
