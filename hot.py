#!/usr/bin/env python3
import pathlib, sys
root = pathlib.Path('.').resolve()
h = root / 'src' / 'shear_hash.h'
c = root / 'src' / 'shear_hash.c'
p2 = root / 'src' / 'shear_miner_p2.inc'
for f in (h, c, p2):
    if not f.exists():
        sys.exit('run this inside shear_cminer-main')

ht = h.read_text()
if 'shear_hash_ready' not in ht:
    old = 'void shear_hash_from_mid(const uint32_t mid[8], const unsigned char header[SHEAR_HEADER_LEN],\n                         uint64_t nonce, unsigned char out[32]);'
    new = (
        'void shear_prep_round(unsigned char rest[21], unsigned char msg[SHEAR_ROUND_LEN],\n'
        '                      const unsigned char header[SHEAR_HEADER_LEN]);\n'
        'void shear_hash_ready(const uint32_t mid[8], unsigned char rest[21], unsigned char msg[SHEAR_ROUND_LEN],\n'
        '                      uint64_t nonce, unsigned char out[32]);\n' + old
    )
    if old not in ht:
        sys.exit('unexpected shear_hash.h')
    h.write_text(ht.replace(old, new, 1))

ready = '''
void shear_prep_round(unsigned char rest[21], unsigned char msg[SHEAR_ROUND_LEN],
                      const unsigned char header[SHEAR_HEADER_LEN]) {
  memcpy(rest, header + 107, 21);
  memcpy(msg + 32, SHEAR_PERSONAL, 12);
  memcpy(msg + 45, header, SHEAR_HEADER_LEN);
}

void shear_hash_ready(const uint32_t mid[8], unsigned char rest[21], unsigned char msg[SHEAR_ROUND_LEN],
                      uint64_t nonce, unsigned char out[32]) {
  rest[5] = (unsigned char)nonce;
  rest[6] = (unsigned char)(nonce >> 8);
  rest[7] = (unsigned char)(nonce >> 16);
  rest[8] = (unsigned char)(nonce >> 24);
  rest[9] = (unsigned char)(nonce >> 32);
  rest[10] = (unsigned char)(nonce >> 40);
  rest[11] = (unsigned char)(nonce >> 48);
  rest[12] = (unsigned char)(nonce >> 56);
  memcpy(msg + 157, rest + 5, 8);
  uint32_t st[8];
  memcpy(st, mid, 32);
  sha256_finish(st, rest, 21, SHEAR_OPEN_LEN, out);
  for (int r = 0; r < SHEAR_HASH_ROUNDS; r++) {
    memcpy(msg, out, 32);
    msg[44] = (unsigned char)('0' + r);
    sha256_oneshot(msg, SHEAR_ROUND_LEN, out);
  }
}
'''
ct = c.read_text()
if 'shear_hash_ready' not in ct:
    needle = 'const char *shear_hash_backend(void) { return sha256_backend_name(); }'
    if needle not in ct:
        sys.exit('unexpected shear_hash.c')
    c.write_text(ct.replace(needle, ready + '\n' + needle, 1))

pt = p2.read_text()
old = '''  uint32_t mid[8];
  unsigned char header[SHEAR_HEADER_LEN];
  unsigned char hash[32];'''
new = '''  uint32_t mid[8];
  unsigned char header[SHEAR_HEADER_LEN];
  unsigned char rest[21];
  unsigned char msg[SHEAR_ROUND_LEN];
  unsigned char hash[32];
  int bits = 8;'''
if old not in pt:
    sys.exit('unexpected worker locals')
pt = pt.replace(old, new, 1)
old = '''      memcpy(header, job.header, SHEAR_HEADER_LEN);
      shear_open_midstate(mid, header);'''
new = '''      memcpy(header, job.header, SHEAR_HEADER_LEN);
      shear_open_midstate(mid, header);
      shear_prep_round(rest, msg, header);
      bits = job.share_bits;'''
if old not in pt:
    sys.exit('unexpected job reload')
pt = pt.replace(old, new, 1)
old = '''      shear_hash_from_mid(mid, header, n, hash);
      local++;
      if (shear_meets_target(hash, job.share_bits)) {'''
new = '''      shear_hash_ready(mid, rest, msg, n, hash);
      local++;
      if (hash[0] == 0 && shear_meets_target(hash, bits)) {'''
if old not in pt:
    sys.exit('unexpected inner hash')
pt = pt.replace(old, new, 1)
p2.write_text(pt)
print('hot loop patched')
