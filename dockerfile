FROM python:3.11-slim

WORKDIR /app

# psutilのビルドに必要なツールとライブラリをインストール
RUN apt-get update && apt-get install -y gcc python3-dev && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir discord.py psutil

COPY monitor_bot.py .

CMD ["python", "monitor_bot.py"]