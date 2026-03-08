#!/usr/bin/env python3
"""
Solution for Challenge 2: "Emoji Hell"

Players receive:
  - check        (compiled binary)
  - source.emoji (pure emoji source code)
  - emoji_map.txt (rosetta stone - maps emojis to C keywords/operators/numbers)

Steps to solve:
1. Look at source.emoji — pure emoji chaos
2. Open emoji_map.txt — maps emojis to C constructs
3. Cross-reference to deobfuscate. Variable names are ??? so they must be inferred from context
4. Reconstructed logic:

   static unsigned int key[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xCA, 0xFE};
   static int expected[] = {179, 205, 198, 145, 170, 164, 171, 207, 219, 232,
                            170, 218, 141, 219, 239, 237, 201, 178, 207, 235,
                            224, 177, 271, 177, 187};
   flag_len = 25;

   for each char i:
       result = (input[i] ^ key[i % 6]) + i
       if result != expected[i]: fail

5. Reverse: input[i] = (expected[i] - i) ^ key[i % 6]
"""

key = [0xDE, 0xAD, 0xBE, 0xEF, 0xCA, 0xFE]
expected = [179, 205, 198, 145, 170, 164, 171, 207, 219, 232,
            170, 218, 141, 219, 239, 237, 201, 178, 207, 235,
            224, 177, 271, 177, 187]

flag = ""
for i in range(len(expected)):
    c = (expected[i] - i) ^ key[i % len(key)]
    flag += chr(c)

print(f"Flag: {flag}")
