#ifndef SHEAR_HASH_H
#define SHEAR_HASH_H

#include <stddef.h>
#include <stdint.h>

#define SHEAR_HASH_ROUNDS 8
#define SHEAR_HEADER_LEN 128
#define SHEAR_PERSONAL "ShearHash-v1"
#define SHEAR_ALGO "ShearHash"
#define SHEAR_CLIENT "ShearHash"
#define SHEAR_MINER_NAME "ShitCunt"
#define SHEAR_VERSION "v0.1"
#define SHEAR_OPEN_LEN (12u + 9u + SHEAR_HEADER_LEN)
#define SHEAR_ROUND_LEN (32u + 12u + 1u + SHEAR_HEADER_LEN)

void shear_hash(const unsigned char header[SHEAR_HEADER_LEN], unsigned char out[32]);
void shear_open_midstate(uint32_t mid[8], const unsigned char header[SHEAR_HEADER_LEN]);
void shear_prep_round(unsigned char rest[21], unsigned char msg[SHEAR_ROUND_LEN],
                      const unsigned char header[SHEAR_HEADER_LEN]);
void shear_hash_ready(const uint32_t mid[8], unsigned char rest[21], unsigned char msg[SHEAR_ROUND_LEN],
                      uint64_t nonce, unsigned char out[32]);
void shear_hash_from_mid(const uint32_t mid[8], const unsigned char header[SHEAR_HEADER_LEN],
                         uint64_t nonce, unsigned char out[32]);
void shear_hash_hex(const unsigned char hash[32], char hex[65]);
int shear_meets_target(const unsigned char hash[32], int bits);
int shear_leading_zero_bits(const unsigned char hash[32]);
int shear_selftest(char got_hex[65]);
void shear_set_nonce(unsigned char header[SHEAR_HEADER_LEN], uint64_t nonce);
const char *shear_hash_backend(void);

extern const unsigned char SHEAR_SELFTEST_HEADER[SHEAR_HEADER_LEN];
extern const char SHEAR_SELFTEST_HASH[];

#endif
