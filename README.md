# shear_cminer

Public Windows+Linux source.

Download zip: https://github.com/tmg270/shearcminer/archive/refs/heads/main.zip

MSYS2 MinGW64:

```
gcc -O3 -march=native -msha -msse4.1 -flto -fomit-frame-pointer -s -o shear_cminer.exe src/shear_miner.c src/shear_hash.c src/sha256.c src/sha256_dispatch.c src/sha256_ni.c -lws2_32 -pthread
shear_cminer.exe --selftest
shear_cminer.exe --pool pool.shear.digital:1111 --user she1YOURID.win5950 --threads 32 --backend sha-ni
```
