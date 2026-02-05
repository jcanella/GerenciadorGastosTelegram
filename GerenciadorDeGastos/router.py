from config import USUARIOS
from sheets import get_sheet

def get_user_sheet(user_id, aba="GASTOS"):
    if user_id not in USUARIOS:
        raise PermissionError("Usuário não autorizado")

    spreadsheet = USUARIOS[user_id]["spreadsheet"]
    return get_sheet(aba, spreadsheet)
