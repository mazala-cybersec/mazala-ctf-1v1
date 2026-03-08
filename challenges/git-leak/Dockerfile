FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
WORKDIR /challenge
COPY setup.sh .
RUN bash setup.sh
WORKDIR /challenge/deploy
EXPOSE 5000
CMD ["python3", "-m", "http.server", "5000", "--bind", "0.0.0.0"]
