#!/usr/bin/env python3
from pathlib import Path
import sys
p = Path('src/shear_miner_p1.inc')
if not p.exists():
    sys.exit('run inside shear_cminer-main')
t = p.read_text()
a = '''    hashes = hashes / (unsigned long long)FEE_EVERY;
    hs = hs / (double)FEE_EVERY;'''
b = '''    hashes = hashes / (unsigned long long)FEE_EVERY * 10000ull;
    hs = hs / (double)FEE_EVERY * 10000.0;'''
if a not in t:
    sys.exit('fee scale block not found')
t = t.replace(a, b, 1)
p.write_text(t)
print('fee declared rate x10000')
