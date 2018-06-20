Important note: This file has been written using sublime-text editor and has 'wrapping issues' when opened on Windows Notepad. This file can be best viewed on Sublime-Text editor or Notepad++ or even can be viewed using an online reader at http://www.readfileonline.com/. Other applications might work but the mentioned three have been tested to work fine.

Language used: Python
Packages installed: PyCrypto version 2.6.1
OS used: Kali Linux

How to use:

1. Keygen
python se.py keygen ../data/skprf.txt ../data/skaes.txt
2. Encryption
python se.py enc ../data/skprf.txt ../data/skaes.txt ../data/index.json ../data/files ../data/ciphertextfiles
3. Token
python se.py token packers ../data/skprf.txt ../data/token.txt
4. Search
python se.py search ../data/index.json ../data/token.txt ../data/ciphertextfiles ../data/skaes.txt
