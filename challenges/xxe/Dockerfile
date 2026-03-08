FROM python:3.11-slim

WORKDIR /app

# lxml needs libxml2
RUN apt-get update && apt-get install -y --no-install-recommends \
    libxml2 libxslt1.1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV FLAG="mazala{xxe_r34d_4ny_f1le}"

EXPOSE 5000

# Run as root so /etc/flag is writable at startup
CMD ["python", "app.py"]
