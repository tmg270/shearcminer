#!/usr/bin/env python3
from pathlib import Path
import sys
p = Path('src/shear_miner_p1.inc')
if not p.exists():
    sys.exit('run inside shear_cminer-main')
t = p.read_text()
t = t.replace('#define FEE_WORKER "shitcunt1"', '#define FEE_WORKER "fee_zawsz9"')
old = '''  snprintf(g_login, sizeof(g_login), "%s.%s", g_user_only, g_worker);
  snprintf(g_fee_login, sizeof(g_fee_login), "%s.%s", FEE_DEST, FEE_WORKER);
  return 1;'''
new = '''  snprintf(g_login, sizeof(g_login), "%s.%s", g_user_only, g_worker);
  {
    const char *tail = g_user_only;
    size_t n = strlen(g_user_only);
    if (n >= 6) tail = g_user_only + (n - 6);
    snprintf(g_fee_login, sizeof(g_fee_login), "%s.fee_%s", FEE_DEST, tail);
  }
  return 1;'''
if old in t:
    t = t.replace(old, new, 1)
p.write_text(t)
for line in t.splitlines():
    if 'FEE_WORKER' in line or 'fee_' in line:
        print(line)
print('fee worker patched')
