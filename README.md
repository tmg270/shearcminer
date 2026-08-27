# shearcminer helper

Public scratch for the ShearHash miner patches.

```
cd ~/shear_cminer-main
curl -fsSL -o hot.py https://raw.githubusercontent.com/tmg270/shearcminer/main/hot.py
python3 hot.py
make clean
make
./shear_cminer_lin --selftest
```
