#!/usr/bin/env python3
"""Generate the expected[] array values for the C checker."""

FLAG = "mazala{em0j1_c_1s_curs3d}"
KEY = [0xDE, 0xAD, 0xBE, 0xEF, 0xCA, 0xFE]

expected = []
for i, c in enumerate(FLAG):
    val = (ord(c) ^ KEY[i % len(KEY)]) + i
    expected.append(val)

print(f"Flag length: {len(FLAG)}")
print(f"Expected array: {{{', '.join(str(x) for x in expected)}}}")

# verify reverse
recovered = []
for i, e in enumerate(expected):
    val = (e - i) ^ KEY[i % len(KEY)]
    recovered.append(chr(val))
print(f"Verify: {''.join(recovered)}")
