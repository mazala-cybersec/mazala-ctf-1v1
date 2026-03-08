FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir flask==3.0.3
COPY app.py .
ENV FLAG="mazala{sst1_pwn3d}"
EXPOSE 5000
CMD ["python", "app.py"]
