// MazalaChess - Game Client

const PIECES = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
};

const FILES = 'abcdefgh';

let gameId = null;
let chess = null;
let selectedSquare = null;
let playerColor = 'w';
let isThinking = false;
let moveHistory = [];
let pendingPromotion = null;

function startGame() {
    fetch('/api/game/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
    })
    .then(r => r.json())
    .then(data => {
        if (data.error) {
            setStatus(data.error);
            return;
        }
        gameId = data.game_id;
        chess = new Chess();
        selectedSquare = null;
        moveHistory = [];
        isThinking = false;

        document.getElementById('resign-btn').disabled = false;
        document.getElementById('flag-display').classList.add('hidden');
        document.getElementById('moves-list').innerHTML = '';
        document.getElementById('move-count').textContent = '0';

        renderBoard();
        setStatus('Your turn — you are White');
        setTurn('White to move');
        setGameStatus('Playing');
    });
}

function renderBoard() {
    const board = document.getElementById('board');
    board.innerHTML = '';

    for (let rank = 7; rank >= 0; rank--) {
        for (let file = 0; file < 8; file++) {
            const sq = document.createElement('div');
            const isLight = (rank + file) % 2 === 1;
            const squareName = FILES[file] + (rank + 1);

            sq.className = `square ${isLight ? 'square-light' : 'square-dark'}`;
            sq.dataset.square = squareName;

            const piece = chess.get(squareName);
            if (piece) {
                const pieceEl = document.createElement('span');
                const key = piece.color === 'w' ? piece.type.toUpperCase() : piece.type.toLowerCase();
                pieceEl.textContent = PIECES[key] || '';
                pieceEl.className = `piece ${piece.color === 'w' ? 'white-piece' : 'black-piece'}`;
                sq.appendChild(pieceEl);
            }

            // Highlight selected square
            if (selectedSquare === squareName) {
                sq.classList.add('selected');
            }

            // Highlight legal moves
            if (selectedSquare) {
                const moves = chess.moves({ square: selectedSquare, verbose: true });
                const targetMove = moves.find(m => m.to === squareName);
                if (targetMove) {
                    if (targetMove.captured) {
                        sq.classList.add('legal-capture');
                    } else {
                        sq.classList.add('legal-move');
                    }
                }
            }

            // Highlight king in check
            if (piece && piece.type === 'k' && chess.in_check() && piece.color === chess.turn()) {
                sq.classList.add('in-check');
            }

            sq.addEventListener('click', () => onSquareClick(squareName));
            board.appendChild(sq);
        }
    }
}

function onSquareClick(square) {
    if (isThinking || !gameId) return;
    if (chess.turn() !== playerColor) return;

    const piece = chess.get(square);

    if (selectedSquare) {
        // Try to make a move
        const moves = chess.moves({ square: selectedSquare, verbose: true });
        const targetMove = moves.find(m => m.to === square);

        if (targetMove) {
            // Check for pawn promotion
            if (targetMove.flags.includes('p') || (targetMove.piece === 'p' && (square[1] === '8' || square[1] === '1'))) {
                pendingPromotion = { from: selectedSquare, to: square };
                document.getElementById('promotion-modal').classList.remove('hidden');
                return;
            }
            makeMove(selectedSquare, square);
        } else if (piece && piece.color === playerColor) {
            // Select different piece
            selectedSquare = square;
            renderBoard();
        } else {
            selectedSquare = null;
            renderBoard();
        }
    } else {
        // Select a piece
        if (piece && piece.color === playerColor) {
            selectedSquare = square;
            renderBoard();
        }
    }
}

function selectPromotion(piece) {
    document.getElementById('promotion-modal').classList.add('hidden');
    if (pendingPromotion) {
        makeMove(pendingPromotion.from, pendingPromotion.to, piece);
        pendingPromotion = null;
    }
}

function makeMove(from, to, promotion) {
    const moveObj = { from: from, to: to };
    if (promotion) moveObj.promotion = promotion;

    // Capture board state before applying move
    const fenBeforeMove = chess.fen();

    const move = chess.move(moveObj);
    if (!move) {
        selectedSquare = null;
        renderBoard();
        return;
    }

    selectedSquare = null;
    const uci = from + to + (promotion || '');

    // Add to move history
    addMoveToHistory(move, 'white');
    renderBoard();

    // Send to server
    isThinking = true;
    setStatus('Bear is thinking...');
    setTurn('Black to move');

    fetch('/api/game/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ game_id: gameId, move: uci, fen: fenBeforeMove })
    })
    .then(r => r.json())
    .then(data => {
        isThinking = false;

        if (data.error) {
            chess.undo();
            renderBoard();
            setStatus(data.error);
            return;
        }

        document.getElementById('move-count').textContent = data.move_count || 0;

        if (data.status === 'win') {
            handleGameEnd(data);
            return;
        }
        if (data.status === 'lose') {
            handleGameEnd(data);
            return;
        }
        if (data.status === 'draw') {
            handleGameEnd(data);
            return;
        }

        // Always sync board from server state
        if (data.fen) {
            chess.load(data.fen);
        }

        renderBoard();
        setStatus('Your turn');
        setTurn('White to move');

        if (chess.in_check()) {
            setStatus('You are in check!');
        }
    })
    .catch(err => {
        isThinking = false;
        setStatus('Connection error. Try again.');
    });
}

function addMoveToHistory(move, color) {
    if (color === 'white') {
        moveHistory.push({ num: moveHistory.length + 1, white: move.san, black: null });
    } else {
        if (moveHistory.length > 0) {
            moveHistory[moveHistory.length - 1].black = move.san;
        }
    }
    renderMoveHistory();
}

function renderMoveHistory() {
    const list = document.getElementById('moves-list');
    list.innerHTML = moveHistory.map(m =>
        `<div class="move-pair">` +
        `<span class="move-num">${m.num}.</span>` +
        `<span class="white-move">${m.white || ''}</span>` +
        `<span class="black-move">${m.black || ''}</span>` +
        `</div>`
    ).join('');
    list.scrollTop = list.scrollHeight;
}

function handleGameEnd(data) {
    // Sync board
    if (data.fen) chess.load(data.fen);
    renderBoard();

    document.getElementById('resign-btn').disabled = true;
    setGameStatus('Game Over');
    setTurn('');

    if (data.status === 'win') {
        setStatus('🎉 You won! Checkmate!');
        if (data.flag) {
            const flagDiv = document.getElementById('flag-display');
            flagDiv.innerHTML = `<h3>🏆 FLAG CAPTURED</h3><div class="flag-text">${data.flag}</div>`;
            flagDiv.classList.remove('hidden');
        }
    } else if (data.status === 'lose') {
        setStatus('💀 Checkmate. You lost.');
    } else if (data.status === 'draw') {
        setStatus('🤝 Draw. No flag for you.');
    }

    gameId = null;
}

function resignGame() {
    if (!gameId) return;

    fetch('/api/game/resign', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ game_id: gameId })
    })
    .then(r => r.json())
    .then(data => {
        setStatus('You resigned. Try again!');
        setGameStatus('Resigned');
        setTurn('');
        document.getElementById('resign-btn').disabled = true;
        gameId = null;
    });
}

function setStatus(msg) {
    document.getElementById('status').textContent = msg;
}

function setTurn(msg) {
    document.getElementById('turn-indicator').textContent = msg;
}

function setGameStatus(msg) {
    document.getElementById('game-status').textContent = msg;
}

// Bind buttons
document.getElementById('new-game-btn').addEventListener('click', startGame);
document.getElementById('resign-btn').addEventListener('click', resignGame);
