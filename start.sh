#!/bin/bash
# Mazala CTF 1v1 — Challenge Startup Script
# Usage: ./start.sh [HOST]
#   HOST = IP/hostname for challenge descriptions (default: localhost)

set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"
HOST="${1:-localhost}"

cleanup() {
    echo ""
    echo "[*] Shutting down..."
    cd "$ROOT" && docker compose stop 2>/dev/null || true
    echo "[*] All services stopped."
    exit 0
}
trap cleanup INT TERM

echo "============================================"
echo "  MAZALA CTF 1v1 — CHALLENGES"
echo "  Host: $HOST"
echo "============================================"
echo ""

# ── Step 1: Build all Docker challenge images ──
echo "[1/2] Building Docker challenge images..."
cd "$ROOT"
docker compose build
echo ""
echo "  [+] All 8 challenge images built"

# ── Step 2: Start all challenges ──
echo "[2/2] Starting challenge containers..."
docker compose up -d
echo ""

echo "============================================"
echo "  CHALLENGES RUNNING"
echo ""
echo "  1. Git Leak        → http://$HOST:3001"
echo "  2. Emoji Hell      → http://$HOST:3002"
echo "  3. Speed Clicker   → http://$HOST:3003"
echo "  4. MazalaChess     → http://$HOST:3004"
echo "  5. ShopZone (SQLi) → http://$HOST:3005"
echo "  6. CardCraft (SSTI)→ http://$HOST:3006"
echo "  7. QuickBite (JWT) → http://$HOST:3007"
echo "  8. FreightFlow(XXE)→ http://$HOST:3008"
echo ""
echo "  Use with: https://github.com/mazala-cybersec/mazala-ctf-bracket"
echo "============================================"
echo ""
echo "Press Ctrl+C to stop all services."

docker compose logs -f
