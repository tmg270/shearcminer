@echo off
gcc -O3 -march=native -msha -msse4.1 -flto -fomit-frame-pointer -s -o shear_cminer.exe src/shear_miner.c src/shear_hash.c src/sha256.c src/sha256_dispatch.c src/sha256_ni.c -lws2_32 -pthread
if errorlevel 1 exit /b 1
shear_cminer.exe --selftest
