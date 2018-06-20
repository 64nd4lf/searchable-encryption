Implementing searchable encryption in Python

How to use:

1. Keygen
python se.py keygen ../data/skprf.txt ../data/skaes.txt
2. Encryption
python se.py enc ../data/skprf.txt ../data/skaes.txt ../data/index.json ../data/files ../data/ciphertextfiles
3. Token
python se.py token packers ../data/skprf.txt ../data/token.txt
4. Search
python se.py search ../data/index.json ../data/token.txt ../data/ciphertextfiles ../data/skaes.txt
