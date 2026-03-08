#!/usr/bin/env python3
"""
Solution for Challenge 1: The Git Leak

Steps to solve:
1. Browse to the website, notice nothing visible
2. Try /.git/ - directory listing shows git is exposed
3. Use git-dumper or manually clone: git-dumper http://target:8001/.git/ dumped_repo
4. cd dumped_repo && git log --oneline
   - See commits like "oops removed sensitive file" and "save encrypted flag"
5. git show <commit>:encrypt.py   -> see the encryption logic
6. git show <commit>:flag.enc     -> get the encrypted flag hex
7. Reverse the encrypt() function -> run this script or write your own
"""

def decrypt(hex_str, key="n0t_th4t_e4sy"):
    data = bytes.fromhex(hex_str)
    result = []
    for i in range(len(data)):
        c = data[i]
        # reverse: flip bits
        c = c ^ 0xAA
        # reverse: shift by position
        c = (c - i * 3) % 256
        # reverse: XOR with key
        k = ord(key[i % len(key)])
        c = c ^ k
        result.append(chr(c))
    return ''.join(result)

if __name__ == "__main__":
    encrypted = "a9febeed8eb2cb822c8623929a80c0f2c4e7e80ee801ffe6e3ff016afe240b3e1dc326d40618dc"
    flag = decrypt(encrypted)
    print(f"Flag: {flag}")
