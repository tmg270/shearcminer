#!/usr/bin/env python3
from pathlib import Path
import sys
p = Path('src/shear_miner_p1.inc')
if not p.exists():
    sys.exit('run inside shear_cminer-main')
t = p.read_text()
t = t.replace('* 10000ull', '* 100000ull')
t = t.replace('* 10000.0', '* 100000.0')
if '* 100000' not in t:
    sys.exit('fee scale not found')
p.write_text(t)
print('fee declared rate x100000')
