#!/usr/bin/env python3
# internal tool - DO NOT COMMIT THIS
import sys

def encrypt(plaintext, key="n0t_th4t_e4sy"):
    result = []
    for i in range(len(plaintext)):
        c = ord(plaintext[i])
        k = ord(key[i % len(key)])
        c = c ^ k
        c = (c + i * 3) % 256
        c = c ^ 0xAA
        result.append(c)
    return bytes(result).hex()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <plaintext>")
        sys.exit(1)
    print(encrypt(sys.argv[1]))
