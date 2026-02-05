from sheets import get_sheet

def listar_beneficiarios(chat_id):
    sheet = get_sheet("BENEFICIARIOS", chat_id)
    nomes = sheet.col_values(1)
    return [n.strip().lower() for n in nomes[1:]]


def beneficiario_valido(nome, chat_id):
    return nome.lower() in listar_beneficiarios(chat_id)


def adicionar_beneficiario(nome, chat_id):
    nome = nome.strip().lower()
    sheet = get_sheet("BENEFICIARIOS", chat_id)

    existentes = listar_beneficiarios(chat_id)
    if nome in existentes:
        raise Exception(f"Beneficiário '{nome}' já existe")

    sheet.append_row([nome])
