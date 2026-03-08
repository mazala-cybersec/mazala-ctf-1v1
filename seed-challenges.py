#!/usr/bin/env python3
"""Seed all 8 challenges into the CTF bracket platform.

Requires the bracket platform to be running at BASE (default: http://localhost:3000).
Usage: python3 seed-challenges.py [HOST]
"""
import json
import sys
import urllib.request

ADMIN_SECRET = "change-this-admin-password"
BASE = "http://localhost:3000"
HOST = sys.argv[1] if len(sys.argv) > 1 else "localhost"

CHALLENGES = [
    {
        "title": "Git Leak",
        "description": (
            "A mysterious website has been deployed. Something feels off about the infrastructure...\n\n"
            f"Target: http://{HOST}:3001"
        ),
        "flag": "mazala{g1t_dump_and_r3v3rs3_th3_crypt0}",
        "category": "web",
        "points": 100,
    },
    {
        "title": "Emoji Hell",
        "description": (
            "A developer wrote a flag checker in the strangest way possible. "
            "You have the binary, the 'source code', and a translation guide. "
            "Can you recover the flag?\n\n"
            f"Download files: http://{HOST}:3002"
        ),
        "flag": "mazala{em0j1_c_1s_curs3d}",
        "category": "reversing",
        "points": 150,
    },
    {
        "title": "Speed Clicker 3000",
        "description": (
            "Can you click fast enough to reveal the flag? "
            "1000 clicks in 3 seconds seems impossible... or is it?\n\n"
            f"Target: http://{HOST}:3003"
        ),
        "flag": "mazala{cl1ck_g4m3_h4ck3d}",
        "category": "web",
        "points": 100,
    },
    {
        "title": "MazalaChess",
        "description": (
            "Beat the chess AI to get the flag. The server uses Stockfish, "
            "one of the strongest chess engines in the world. Good luck.\n\n"
            f"Target: http://{HOST}:3004"
        ),
        "flag": "mazala{n3v3r_tru5t_th3_cl13nt_f3n}",
        "category": "web",
        "points": 150,
    },
    {
        "title": "ShopZone",
        "description": (
            "A brand new online shop just launched. "
            "The search functionality seems a bit too flexible...\n\n"
            f"Target: http://{HOST}:3005"
        ),
        "flag": "mazala{sq1i_g0t_u}",
        "category": "web",
        "points": 100,
    },
    {
        "title": "CardCraft",
        "description": (
            "Create personalized greeting cards for your friends! "
            "This card maker app looks harmless enough...\n\n"
            f"Target: http://{HOST}:3006"
        ),
        "flag": "mazala{sst1_pwn3d}",
        "category": "web",
        "points": 150,
    },
    {
        "title": "QuickBite",
        "description": (
            "QuickBite's food ordering platform uses modern auth. "
            "But is the token validation as solid as it seems?\n\n"
            f"Target: http://{HOST}:3007"
        ),
        "flag": "mazala{jwt_4lg_n0n3}",
        "category": "web",
        "points": 150,
    },
    {
        "title": "FreightFlow",
        "description": (
            "FreightFlow's logistics portal lets you upload XML invoices. "
            "The parser seems eager to process your input...\n\n"
            f"Target: http://{HOST}:3008"
        ),
        "flag": "mazala{xxe_r34d_4ny_f1le}",
        "category": "web",
        "points": 150,
    },
]


def main():
    print(f"[*] Seeding {len(CHALLENGES)} challenges (host: {HOST})")

    # Admin login
    print("[*] Logging in as admin...")
    data = json.dumps({"password": ADMIN_SECRET}).encode()
    req = urllib.request.Request(
        f"{BASE}/api/admin/login",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    resp = urllib.request.urlopen(req)
    cookie = resp.headers.get("Set-Cookie", "")
    admin_token = ""
    for part in cookie.split(";"):
        part = part.strip()
        if part.startswith("admin-token="):
            admin_token = part.split("=", 1)[1]
            break

    if not admin_token:
        print("[!] Failed to get admin token")
        return

    print("[+] Admin token acquired")

    # Seed challenges
    added = 0
    for ch in CHALLENGES:
        data = json.dumps(ch).encode()
        req = urllib.request.Request(
            f"{BASE}/api/admin/challenges",
            data=data,
            headers={
                "Content-Type": "application/json",
                "Cookie": f"admin-token={admin_token}",
            },
        )
        try:
            resp = urllib.request.urlopen(req)
            result = json.loads(resp.read())
            print(f"  [+] {result['title']} ({result['category']}, {result['points']}pts)")
            added += 1
        except urllib.error.HTTPError as e:
            err = json.loads(e.read())
            print(f"  [!] Failed: {ch['title']}: {err.get('error', 'unknown')}")

    print(f"\n[+] Done! {added}/{len(CHALLENGES)} challenges seeded.")


if __name__ == "__main__":
    main()
