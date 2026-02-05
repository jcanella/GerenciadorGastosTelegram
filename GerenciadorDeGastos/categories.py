CATEGORIAS = {
    "alimentacao": ["jantar", "almoço", "almoco", "sorvete","padaria","comida","pizza" ,"lanche","mercado"],
    "transporte": ["uber", "99", "gasolina","metro","estacionamento"],
    "lazer": ["cinema", "bar", "show"],
    "contas": ["luz", "agua", "internet","psicologa","telefone","barbeiro","sobrancelha", "Stream","Academia"],
    "streaming": ["Netflix", "Apple ", "Prime", "HBO", "Youtube",]
}

def classificar(descricao):
    desc = descricao.lower()
    for categoria, palavras in CATEGORIAS.items():
        if any(p in desc for p in palavras):
            return categoria
    return "outros"
