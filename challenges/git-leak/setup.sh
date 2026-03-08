#!/bin/bash
# Challenge 1: "The Git Leak" - Setup Script
# Creates a web directory with an exposed .git history
# Players must: find .git -> dig history -> find encrypt.py -> reverse it -> decrypt flag

set -e

CHALLENGE_DIR="$(cd "$(dirname "$0")" && pwd)"
DEPLOY_DIR="$CHALLENGE_DIR/deploy"
FLAG='mazala{g1t_dump_and_r3v3rs3_th3_crypt0}'
ENCRYPTED_FLAG="a9febeed8eb2cb822c8623929a80c0f2c4e7e80ee801ffe6e3ff016afe240b3e1dc326d40618dc"

# clean previous build
rm -rf "$DEPLOY_DIR"
mkdir -p "$DEPLOY_DIR"
cd "$DEPLOY_DIR"

git init
git config user.email "dev@mazala-ctf.local"
git config user.name "CTF Dev"

# ============================================================
# Commit 1: Initial website
# ============================================================
cat > index.html << 'HTMLEOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mazala CTF - Welcome</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Courier New', monospace;
            background: #0a0a0a;
            color: #00ff41;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            text-align: center;
            padding: 2rem;
        }
        h1 { font-size: 3rem; margin-bottom: 1rem; }
        p { font-size: 1.2rem; color: #888; margin-bottom: 0.5rem; }
        .blink { animation: blink 1s infinite; }
        @keyframes blink { 50% { opacity: 0; } }
    </style>
</head>
<body>
    <div class="container">
        <h1>MAZALA CTF</h1>
        <p>Welcome to the arena.</p>
        <p>There's nothing to see here... or is there?</p>
        <p class="blink">_</p>
    </div>
</body>
</html>
HTMLEOF

git add index.html
git commit -m "Initial commit - website launch"

# ============================================================
# Commit 2: Dev accidentally commits the encryption tool
# ============================================================
cat > encrypt.py << 'PYEOF'
#!/usr/bin/env python3
# internal tool - DO NOT COMMIT THIS
import sys

def encrypt(plaintext, key="n0t_th4t_e4sy"):
    result = []
    for i in range(len(plaintext)):
        c = ord(plaintext[i])
        k = ord(key[i % len(key)])
        # XOR with key
        c = c ^ k
        # shift by position
        c = (c + i * 3) % 256
        # flip bits
        c = c ^ 0xAA
        result.append(c)
    return bytes(result).hex()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <plaintext>")
        sys.exit(1)
    print(encrypt(sys.argv[1]))
PYEOF

git add encrypt.py
git commit -m "added encryption tool (temp)"

# ============================================================
# Commit 3: Dev generates encrypted flag and saves it
# ============================================================
echo "$ENCRYPTED_FLAG" > flag.enc
git add flag.enc
git commit -m "save encrypted flag for safekeeping"

# ============================================================
# Commit 4: Dev realizes mistake, removes sensitive files
# ============================================================
git rm encrypt.py
git commit -m "oops removed sensitive file"

# ============================================================
# Commit 5: Dev removes encrypted flag too (or so they think)
# ============================================================
git rm flag.enc
git commit -m "cleanup - removed all flag related stuff"

# ============================================================
# Commit 6: Final "clean" state
# ============================================================
cat >> index.html << 'ADDEOF'
<!-- v2.0 - cleaned up, nothing to worry about -->
ADDEOF

git add index.html
git commit -m "v2.0 - production ready"

echo ""
echo "============================================"
echo " Challenge 1 built successfully!"
echo " Deploy dir: $DEPLOY_DIR"
echo " "
echo " Serve with:"
echo "   cd $DEPLOY_DIR && python3 -m http.server 8001"
echo " "
echo " .git is exposed at http://localhost:8001/.git/"
echo "============================================"
