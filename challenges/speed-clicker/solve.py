#!/usr/bin/env python3
"""
Solution for Challenge 4: "The Fastest Fingers"

Players receive: a web page with a clicking game (1000 clicks in 3 seconds)

Intended solve (5 min):
1. Try the game — impossible to click 1000 times in 3 sec
2. Try window.score = 1000 → get taunted "nope :)"
3. Realize: the button has a click handler, just fire events!
4. Open console:
     document.getElementById('startBtn').click();
     for(let i=0;i<1000;i++) document.getElementById('clickBtn').click();
5. Flag appears on screen

Alt solve (read source):
1. View game.js source
2. Find hex array [0x2f, 0x23, ...] and key 0x42
3. XOR decode in console
"""

# Alt solve: XOR decode
encoded = [0x2f, 0x23, 0x38, 0x23, 0x2e, 0x23, 0x39, 0x21, 0x2e, 0x73,
           0x21, 0x29, 0x1d, 0x25, 0x76, 0x2f, 0x71, 0x1d, 0x2a, 0x76,
           0x21, 0x29, 0x71, 0x26, 0x3f]
key = 0x42
flag = ''.join(chr(c ^ key) for c in encoded)
print(f"Flag: {flag}")
