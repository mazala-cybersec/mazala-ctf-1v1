FROM python:3.11-slim
WORKDIR /app
COPY dist/ .
EXPOSE 5000
CMD ["python3", "-m", "http.server", "5000", "--bind", "0.0.0.0"]
