from flask import Flask, request, jsonify, render_template
import chess
import chess.engine
import random
import os
import uuid
import time

app = Flask(__name__)

FLAG = os.environ.get("FLAG", "mazala{n3v3r_tru5t_th3_cl13nt_f3n}")
STOCKFISH_PATH = os.environ.get("STOCKFISH_PATH", "/usr/games/stockfish")

# In-memory game storage
games = {}


def get_bot_move(board):
    """Bot uses Stockfish"""
    try:
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        result = engine.play(board, chess.engine.Limit(time=0.5, depth=10))
        engine.quit()
        return result.move
    except Exception:
        # Fallback: random move
        legal = list(board.legal_moves)
        return random.choice(legal) if legal else None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/game/start", methods=["POST"])
def start_game():
    game_id = str(uuid.uuid4())
    board = chess.Board()

    games[game_id] = {
        "board": board,
        "started": time.time(),
        "moves": 0
    }

    return jsonify({
        "game_id": game_id,
        "fen": board.fen(),
        "message": "Game started. You are white.",
        "status": "playing"
    })


@app.route("/api/game/move", methods=["POST"])
def make_move():
    data = request.get_json() or {}
    game_id = data.get("game_id")
    move_uci = data.get("move")
    client_fen = data.get("fen")

    if not game_id or game_id not in games:
        return jsonify({"error": "invalid game_id"}), 400

    game = games[game_id]
    board = game["board"]

    # Sync board state from client for smooth gameplay
    if client_fen:
        try:
            board.set_fen(client_fen)
        except ValueError:
            pass

    if board.is_game_over():
        result = get_game_result(board, game)
        del games[game_id]
        return jsonify(result)

    # Validate and apply player move
    try:
        move = chess.Move.from_uci(move_uci)
        if move not in board.legal_moves:
            promo_move = chess.Move.from_uci(move_uci + "q")
            if promo_move in board.legal_moves:
                move = promo_move
            else:
                return jsonify({"error": "illegal move"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "invalid move format"}), 400

    board.push(move)
    game["moves"] += 1

    # Check if game is over after player move
    if board.is_game_over():
        result = get_game_result(board, game)
        del games[game_id]
        return jsonify(result)

    # Bot move
    bot_move = get_bot_move(board)

    if bot_move:
        board.push(bot_move)
        game["moves"] += 1

    # Check if game is over after bot move
    if board.is_game_over():
        result = get_game_result(board, game)
        del games[game_id]
        return jsonify(result)

    return jsonify({
        "fen": board.fen(),
        "bot_move": bot_move.uci() if bot_move else None,
        "status": "playing",
        "move_count": game["moves"]
    })


@app.route("/api/game/resign", methods=["POST"])
def resign():
    data = request.get_json() or {}
    game_id = data.get("game_id")

    if game_id and game_id in games:
        del games[game_id]

    return jsonify({"message": "You resigned. Better luck next time!", "status": "resigned"})


def get_game_result(board, game):
    result = board.result()

    if result == "1-0":
        return {
            "fen": board.fen(),
            "status": "win",
            "message": "Checkmate! You won!",
            "flag": FLAG,
            "result": result
        }
    elif result == "0-1":
        return {
            "fen": board.fen(),
            "status": "lose",
            "message": "Checkmate. The bear destroyed you.",
            "result": result
        }
    else:
        return {
            "fen": board.fen(),
            "status": "draw",
            "message": "It's a draw.",
            "result": result
        }


@app.before_request
def cleanup_old_games():
    now = time.time()
    stale = [gid for gid, g in games.items() if now - g["started"] > 3600]
    for gid in stale:
        del games[gid]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
