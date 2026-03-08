FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir flask==3.0.3
COPY app.py .
ENV FLAG="mazala{sq1i_g0t_u}"
EXPOSE 5000
RUN adduser --disabled-password --gecos '' ctf
USER ctf
CMD ["python", "app.py"]
