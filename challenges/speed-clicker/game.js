// SPEED CLICKER 3000 - the ultimate test of speed
// version 4.2.0 - "no cheating" edition

(function() {
    'use strict';

    const CONFIG = {
        TARGET: 1000,
        TIME_LIMIT: 3000,
        TICK_RATE: 10,
    };

    const _integrity = [
        47, 35, 56, 35, 46, 35, 57, 33, 46, 115,
        33, 41, 29, 37, 118, 47, 113, 29, 42, 118,
        33, 41, 113, 38, 63
    ];
    const _seed = 0x42;

    let _state = {
        _s: 0,
        _t: CONFIG.TIME_LIMIT,
        _running: false,
        _interval: null,
    };

    const btn = document.getElementById('clickBtn');
    const startBtn = document.getElementById('startBtn');
    const scoreEl = document.getElementById('scoreDisplay');
    const timerEl = document.getElementById('timerDisplay');
    const progressEl = document.getElementById('progressBar');
    const resultEl = document.getElementById('result');

    function _updateDisplay() {
        scoreEl.textContent = _state._s;
        timerEl.textContent = (_state._t / 1000).toFixed(2);
        progressEl.style.width = Math.min((_state._s / CONFIG.TARGET) * 100, 100) + '%';
    }

    function _tick() {
        _state._t -= CONFIG.TICK_RATE;
        _updateDisplay();

        if (_state._t <= 0) {
            _endGame();
        }
    }

    function _startGame() {
        _state._s = 0;
        _state._t = CONFIG.TIME_LIMIT;
        _state._running = true;
        resultEl.textContent = '';
        resultEl.className = '';
        btn.textContent = 'CLICK ME!';
        btn.classList.remove('disabled');
        startBtn.style.display = 'none';

        _state._interval = setInterval(_tick, CONFIG.TICK_RATE);
        _updateDisplay();
    }

    function _endGame() {
        clearInterval(_state._interval);
        _state._running = false;
        btn.textContent = 'DONE';
        btn.classList.add('disabled');
        startBtn.style.display = 'block';
        startBtn.textContent = 'TRY AGAIN';

        _checkWin();
    }

    function _checkWin() {
        if (_state._s >= CONFIG.TARGET && _state._t > 0) {
            resultEl.className = 'win';
            resultEl.textContent = _decode(_integrity, _seed);
        } else {
            resultEl.textContent = 'too slow! got ' + _state._s + '/' + CONFIG.TARGET;
        }
    }

    function _decode(arr, key) {
        return arr.map(function(c) { return String.fromCharCode(c ^ key); }).join('');
    }

    function _handleClick() {
        if (!_state._running) return;
        _state._s++;
        _updateDisplay();

        if (_state._s >= CONFIG.TARGET) {
            _endGame();
        }
    }

    btn.addEventListener('click', _handleClick);
    startBtn.addEventListener('click', _startGame);

    // anti-cheat
    Object.defineProperty(window, 'score', {
        get: function() { console.log('nice try :)'); return undefined; },
        set: function() { console.log('nope :)'); },
        configurable: false
    });

    Object.defineProperty(window, 'flag', {
        get: function() { console.log('lol no'); return undefined; },
        set: function() { console.log('not that easy'); },
        configurable: false
    });

    _updateDisplay();
})();
