import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import WorksheetNotFound, SpreadsheetNotFound
from config import USUARIOS


def get_sheet(nome_aba: str, chat_id: int):
    if chat_id not in USUARIOS:
        raise Exception("❌ Usuário não autorizado")

    planilha_nome = USUARIOS[chat_id]["planilha"]

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
    client = gspread.authorize(creds)

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
