#!/data/data/com.termux/files/usr/bin/bash
set -e

pkg update -y
pkg install -y python git openssl-tool

python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "[OK] Termux setup complete. Заполните .env и запустите: python main.py"
