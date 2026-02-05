import json
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import WorksheetNotFound, SpreadsheetNotFound

USUARIOS = json.loads(str(os.getenv("USUARIOS", "{}")))
GOOGLE_CREDENTIALS = json.loads(str(os.getenv("GOOGLE_CREDENTIALS")))
print(GOOGLE_CREDENTIALS)
# ===============================
# GOOGLE SHEETS CLIENT (GLOBAL)
# ===============================

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    GOOGLE_CREDENTIALS,
    SCOPE
)

client = gspread.authorize(creds)

def get_sheet(nome_aba: str, chat_id: int):
    chat_id = str(chat_id)
    if chat_id not in USUARIOS:
        raise Exception("❌ Usuário não autorizado")

    planilha_nome = USUARIOS[chat_id]["planilha"]

    try:
        spreadsheet = client.open(planilha_nome)
    except SpreadsheetNotFound:
        raise Exception(f"❌ Planilha '{planilha_nome}' não encontrada")

    try:
        return spreadsheet.worksheet(nome_aba)
    except WorksheetNotFound:
        abas = [ws.title for ws in spreadsheet.worksheets()]
        raise Exception(
            f"❌ Aba '{nome_aba}' não encontrada.\n"
            f"📄 Abas existentes: {abas}"
        )


