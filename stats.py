#!/usr/bin/env python3
from pathlib import Path
import sys
p2 = Path('src/shear_miner_p2.inc')
if not p2.exists():
    sys.exit('run inside shear_cminer-main')
t = p2.read_text()
if 'static uint64_t g_fee_rej' not in t:
    t = t.replace('static int g_height;', 'static int g_height;\nstatic uint64_t g_fee_rej;', 1)
t = t.replace('static void apply_ack(const char *line) {',
              'static void apply_ack(const char *line, int is_fee) {', 1)
if 'if (is_fee) g_fee_rej++;' not in t:
    t = t.replace('    g_rejected++;\n    atomic_fetch_sub(&g_inflight, 1);',
                  '    g_rejected++;\n    if (is_fee) g_fee_rej++;\n    atomic_fetch_sub(&g_inflight, 1);', 1)
    t = t.replace('    g_accepted++;\n    atomic_fetch_sub(&g_inflight, 1);',
                  '    g_accepted++;\n    if (is_fee) g_fee_acc++;\n    atomic_fetch_sub(&g_inflight, 1);', 1)
t = t.replace('  apply_ack(line);', '  apply_ack(line, c->is_fee);', 1)
old = '''      printf("\\033[36m%7.0f H/s\\033[0m  \\033[32macc %llu\\033[0m  \\033[31mrej %llu\\033[0m  \\033[33m%s\\033[0m  h=%d  bits=%d\\n",
             hs, (unsigned long long)g_accepted, (unsigned long long)g_rejected,
             jobId[0] ? jobId : "-", g_height, bits);'''
new = '''      {
        const char *fw = g_fee_login;
        const char *dot = strrchr(g_fee_login, '.');
        if (dot && dot[1]) fw = dot + 1;
        printf("\\033[36m%7.0f H/s\\033[0m  \\033[32macc %llu\\033[0m  \\033[31mrej %llu\\033[0m  sub %llu  %s  h=%d  %s a=%llu r=%llu\\n",
               hs, (unsigned long long)g_accepted, (unsigned long long)g_rejected,
               (unsigned long long)g_submitted, jobId[0] ? jobId : "-", g_height, fw,
               (unsigned long long)g_fee_acc, (unsigned long long)g_fee_rej);
      }'''
if old not in t:
    sys.exit('stats printf not found')
t = t.replace(old, new, 1)
p2.write_text(t)
print('stats line patched')
