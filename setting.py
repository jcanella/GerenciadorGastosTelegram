import os
import json

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

USUARIOS = json.loads(
    os.getenv("USUARIOS", "{}")
)
