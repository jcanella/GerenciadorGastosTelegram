
def obter_salario(sheet):
    try:
        salario = sheet.acell("B1").value
        if not salario:
            return None
        return float(salario.replace(",", "."))
    except:
        return None
