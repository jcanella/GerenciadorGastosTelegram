
import re
from datetime import datetime, timedelta

MESES = {
    "janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4,
    "maio": 5, "junho": 6, "julho": 7, "agosto": 8,
    "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12
}

def extrair_data(texto):
    hoje = datetime.now()
    t = texto.lower()

    if "ontem" in t:
        return hoje - timedelta(days=1)

    # 02/02
    match = re.search(r"\b(\d{1,2})/(\d{1,2})\b", t)
    if match:
        dia, mes = map(int, match.groups())
        return datetime(hoje.year, mes, dia)

    # Dia 03 de janeiro
    match = re.search(r"dia (\d{1,2}) de (\w+)", t)
    if match:
        dia = int(match.group(1))
        mes = MESES.get(match.group(2))
        if mes:
            return datetime(hoje.year, mes, dia)

    return hoje



def extrair_valor(texto):
    valores = re.findall(r"\d+[.,]?\d*", texto)
    if not valores:
        raise ValueError("Valor não encontrado")
    return float(valores[-1].replace(",", "."))


def limpar_texto(texto, valor):
    texto = texto.lower()
    texto = re.sub(r"\d{1,2}/\d{1,2}", "", texto)
    texto = texto.replace(str(valor), "").replace(str(valor).replace(".", ","), "")
    texto = texto.replace("ontem", "").replace("hoje", "")
    return texto.strip()

