from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
from commands import help_cmd, resumo_cmd, quem_cmd, insights_cmd , add_beneficiario_cmd, set_entrada_cmd, start_cmd
from config import TELEGRAM_TOKEN
from router import get_user_sheet
from parser import extrair_data, extrair_valor, limpar_texto
from categories import classificar
import uuid
from datetime import datetime
from beneficiarios import listar_beneficiarios, beneficiario_valido
from sheets import get_sheet

async def handler(update, context):
    texto = update.message.text.strip()
    chat_id = update.effective_user.id

    if texto.startswith("/"):
        return

    try:
        data = extrair_data(texto)
        valor = extrair_valor(texto)
        texto_limpo = limpar_texto(texto, valor)

        palavras = texto_limpo.lower().split()
        beneficiarios = listar_beneficiarios(chat_id)

        beneficiario = "eu"
        descricao_palavras = []

        for p in palavras:
            if p in beneficiarios:
                beneficiario = p
            else:
                descricao_palavras.append(p)

        descricao = " ".join(descricao_palavras)

        if not beneficiario_valido(beneficiario, chat_id):
            raise Exception(f"Beneficiário '{beneficiario}' não cadastrado")


        categoria = classificar(descricao)

        chat_id = update.effective_chat.id
        sheet = get_sheet("GASTOS", chat_id)
        
        sheet.append_row([
            str(uuid.uuid4()),
            data.strftime("%Y-%m-%d"),
            valor,
            categoria,
            beneficiario,
            descricao,
            datetime.now().isoformat()
        ])

        await update.message.reply_text(
            f"✅ Gasto registrado com sucesso!\n"
            f"📅 {data.strftime('%d/%m')}\n"
            f"💰 R$ {valor:.2f}\n"
            f"👤 {beneficiario}\n"
            f"🏷️ {categoria}\n"
            f"📝 {descricao}"
        )


    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao interpretar: {e}")


app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))
app.add_handler(CommandHandler("start", start_cmd))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("resumo", resumo_cmd))
app.add_handler(CommandHandler("quem", quem_cmd))
app.add_handler(CommandHandler("insights", insights_cmd))
app.add_handler(CommandHandler("beneficiario", add_beneficiario_cmd))
app.add_handler(CommandHandler("entrada", set_entrada_cmd))

app.run_polling()
