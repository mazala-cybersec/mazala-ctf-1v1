FROM python:3.11-slim

RUN apt-get update && apt-get install -y stockfish && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV STOCKFISH_PATH=/usr/games/stockfish
ENV FLAG=mazala{ch3ss_m4st3r_0r_r3qu3st_t4mp3r3r}

EXPOSE 5000

CMD ["python", "app.py"]
