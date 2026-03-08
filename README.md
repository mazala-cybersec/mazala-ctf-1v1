<div align="center">

```
  ╔══════════════════════════════════════════════════════╗
  ║                                                      ║
  ║   ███╗   ███╗ █████╗ ███████╗ █████╗ ██╗      █████╗ ║
  ║   ████╗ ████║██╔══██╗╚══███╔╝██╔══██╗██║     ██╔══██╗║
  ║   ██╔████╔██║███████║  ███╔╝ ███████║██║     ███████║║
  ║   ██║╚██╔╝██║██╔══██║ ███╔╝  ██╔══██║██║     ██╔══██║║
  ║   ██║ ╚═╝ ██║██║  ██║███████╗██║  ██║███████╗██║  ██║║
  ║   ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝║
  ║                                                      ║
  ║          C T F   1 v 1   C H A L L E N G E S         ║
  ║                                                      ║
  ╚══════════════════════════════════════════════════════╝
```

**8 Dockerized CTF challenges for head-to-head 1v1 speed duels.**

Web exploitation, reverse engineering, crypto — each solvable in 5-10 minutes.

Designed for live on-stage competitions with [mazala-ctf-bracket](https://github.com/mazala-cybersec/mazala-ctf-bracket).

[![MIT License](https://img.shields.io/badge/License-MIT-gold.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://docker.com)

</div>

---

## Challenges

| # | Name | Category | Difficulty | Port | Author | Description |
|---|---|---|---|---|---|---|
| 1 | **Git Leak** | Web / Crypto | Medium | 3001 | [@ByamB4](https://github.com/ByamB4) | Exposed `.git` directory with encrypted flag in commit history |
| 2 | **Emoji Hell** | Reversing | Medium | 3002 | [@ByamB4](https://github.com/ByamB4) | C flag checker obfuscated with emoji `#define` macros |
| 3 | **Speed Clicker 3000** | Web / JS | Easy | 3003 | [@ByamB4](https://github.com/ByamB4) | Impossible clicking game — flag hidden in JS source |
| 4 | **MazalaChess** | Web | Hard | 3004 | [@ByamB4](https://github.com/ByamB4) | Beat Stockfish AI — or find the client-side trust vulnerability |
| 5 | **ShopZone** | Web (SQLi) | Easy | 3005 | [@enhbold](https://github.com/enhbold) | SQL injection in product search |
| 6 | **CardCraft** | Web (SSTI) | Medium | 3006 | [@enhbold](https://github.com/enhbold) | Server-side template injection in greeting card maker |
| 7 | **QuickBite** | Web (JWT) | Medium | 3007 | [@enhbold](https://github.com/enhbold) | JWT `alg:none` token forgery in food ordering app |
| 8 | **FreightFlow** | Web (XXE) | Medium | 3008 | [@enhbold](https://github.com/enhbold) | XML external entity injection in invoice upload |

---

## Quick Start

```bash
git clone https://github.com/mazala-cybersec/mazala-ctf-1v1.git
cd mazala-ctf-1v1
docker compose up -d
```

All 8 challenges will be available on ports `3001-3008`.

### With the Bracket Platform

For a full tournament experience with live brackets, player registration, and match management:

```bash
# 1. Set up the bracket platform
git clone https://github.com/mazala-cybersec/mazala-ctf-bracket.git
cd mazala-ctf-bracket
make setup && make dev

# 2. In another terminal, start the challenges
cd mazala-ctf-1v1
docker compose up -d

# 3. Seed challenges into the bracket platform
python3 seed-challenges.py
```

### Startup Script

```bash
chmod +x start.sh
./start.sh              # localhost
./start.sh 192.168.1.10 # custom host IP
```

---

## Challenge Details

### 1. Git Leak
A static website with an exposed `.git` directory. Players must dump the git repo, dig through commit history, find an encrypted flag and encryption script in deleted commits, then reverse the XOR/shift/flip encryption.

**Solve path:** Find `.git/` → git-dumper → git log → extract `flag.enc` + `encrypt.py` → reverse crypto → flag

### 2. Emoji Hell
A C program that checks if a flag is correct, but every keyword and operator is `#define`'d to an emoji. Players must deobfuscate the emoji soup, understand the check logic (XOR with key + position offset), then reverse it.

**Solve path:** Map emoji defines → extract arrays → reverse `(char ^ key) + i == expected[i]` → flag

### 3. Speed Clicker 3000
A browser clicking game requiring 1000 clicks in 3 seconds (impossible). Console hacks (`window.score`, `window.flag`) are anti-cheat traps. The real flag is XOR-encoded in the minified JS source.

**Solve path:** Read source → find encoded array + XOR key → decode → flag

### 4. MazalaChess
A chess game against Stockfish. The server trusts the client-sent FEN (board state). Players can send a rigged FEN to start in a winning position.

**Solve path:** Intercept request → modify FEN → checkmate in one → flag

### 5. ShopZone
An online shop with a vulnerable search bar. Classic SQL injection to extract the flag from the database.

**Solve path:** `' UNION SELECT` → dump flag table → flag

### 6. CardCraft
A greeting card generator using server-side templates. The card message field is vulnerable to SSTI, allowing code execution.

**Solve path:** `{{config}}` or `{{''.__class__.__mro__}}` → RCE → read flag → flag

### 7. QuickBite
A food ordering app with JWT auth. The server accepts `alg: none` tokens, allowing players to forge admin tokens without a secret.

**Solve path:** Decode JWT → change `alg` to `none` + `role` to `admin` → strip signature → flag

### 8. FreightFlow
A logistics portal accepting XML invoice uploads. The XML parser processes external entities, enabling file reads from the server.

**Solve path:** `<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///flag.txt">]>` → flag

---

## Project Structure

```
mazala-ctf-1v1/
  challenges/
    git-leak/           Web challenge — exposed .git + crypto
    emoji-hell/         Reversing — emoji-obfuscated C
    speed-clicker/      Web/JS — impossible click game
    chess/              Web — client-side trust vuln
    sqli/               Web — SQL injection
    ssti/               Web — server-side template injection
    jwt/                Web — JWT alg:none forgery
    xxe/                Web — XML external entity injection
  docker-compose.yml    All 8 services with security hardening
  seed-challenges.py    Seed into mazala-ctf-bracket platform
  start.sh              One-command startup script
```

---

## Security Hardening

All containers run with:

- `no-new-privileges` — prevents privilege escalation
- `cap_drop: ALL` — drops all Linux capabilities
- Memory limits (128-256MB) and CPU limits (0.5 cores)
- PID limits (64-128) to prevent fork bombs
- Read-only filesystems where possible
- Empty DNS to prevent outbound resolution
- Isolated Docker network

---

## Creating Your Own Challenges

Each challenge follows a simple pattern:

1. Create a directory under `challenges/`
2. Add a `Dockerfile` that exposes port `5000`
3. Add the service to `docker-compose.yml`
4. Add the challenge info to `seed-challenges.py`

Example minimal challenge:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
EXPOSE 5000
CMD ["python3", "app.py"]
```

---

## License

[MIT](LICENSE) — Built by [Mazala Cybersec](https://github.com/mazala-cybersec)
