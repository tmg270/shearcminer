#!/usr/bin/env python3
from pathlib import Path
import sys
p = Path('src/shear_miner_p1.inc')
if not p.exists():
    sys.exit('run inside shear_cminer-main')
t = p.read_text()
needle = '''  double hs = (double)hashes / elapsed;
  int n = snprintf(line, sizeof(line),'''
put = '''  double hs = (double)hashes / elapsed;
  if (c->is_fee) {
    hashes = hashes / (unsigned long long)FEE_EVERY;
    hs = hs / (double)FEE_EVERY;
  }
  int n = snprintf(line, sizeof(line),'''
if needle not in t:
    sys.exit('submit block not found')
if 'if (c->is_fee)' not in t:
    t = t.replace(needle, put, 1)
p.write_text(t)
print('fee hashrate scaled 1/20')
