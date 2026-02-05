from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
from sheets import get_sheet
from insights import obter_salario
from beneficiarios import adicionar_beneficiario

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bem-vindo ao Controle Financeiro!\n\n"
        "Digite `/help` para ver tudo que posso fazer 😉",
        parse_mode="Markdown"
    )


# =========================
# /help
# =========================
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Como usar o bot*\n\n"

        "💸 *Registrar gastos*\n"
        "Envie mensagens como:\n"
        "• `120 mercado namorada`\n"
        "• `ontem 45 almoço eu`\n"
        "• `15/01 200 jantar`\n\n"

        "📊 *Comandos disponíveis*\n"
        "• `/resumo` — gastos do mês atual\n"
        "• `/quem nome` — total gasto por pessoa\n"
        "• `/insights` — percentual do salário gasto\n"
        "• `/beneficiario nome` — adicionar beneficiário\n"
        "• `/entrada` — somar entradas ao salário\n"
        "• `/help` — mostrar ajuda\n\n"

        "💡 *Dica*\n"
        "Se não informar a data, o bot assume *hoje* automaticamente.",
        parse_mode="Markdown"
    )


# =========================
# /resumo
# =========================
async def resumo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    sheet = get_sheet("GASTOS", chat_id)

    registros = sheet.get_all_records()
    if not registros:
        await update.message.reply_text("📭 Nenhum gasto registrado neste mês.")
        return

    total = sum(float(r["valor"]) for r in registros if r["valor"])
    await update.message.reply_text(
        f"📊 Total gasto no mês: R$ {total:.2f}"
    )


# =========================
# /quem <pessoa>
# =========================
async def quem_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    sheet = get_sheet("GASTOS", chat_id)

    if not context.args:
        await update.message.reply_text("Use: /quem nome")
        return

    nome = context.args[0].lower()
    registros = sheet.get_all_records()

    total = sum(
        r["valor"] for r in registros
        if r["beneficiario"].lower() == nome
    )

    await update.message.reply_text(
        f"👤 Total gasto com {nome}: R$ {total:.2f}"
    )


# =========================
# /insights
# =========================
async def insights_cmd(update, context):
    chat_id = update.effective_chat.id

    sheet_gastos = get_sheet("GASTOS", chat_id)
    sheet_config = get_sheet("CONFIG", chat_id)

    salario = obter_salario(sheet_config)

    if not salario:
        await update.message.reply_text(
            "❌ Salário não configurado.\n"
            "Defina um valor na célula B1 da planilha CONFIG."
        )
        return

    registros = sheet_gastos.get_all_records()
    total = sum(float(r["valor"]) for r in registros if r["valor"])

    percentual = (total / salario) * 100
    Restante = salario - total
    await update.message.reply_text(
        f"📊 *Insights Financeiros*\n\n"
        f"💰 Salário: R$ {salario:.2f}\n"
        f"💸 Gastos: R$ {total:.2f}\n"
        f"📉 Percentual gasto: {percentual:.1f}%\n"
        f"💵 Restante do Salário: R$ {Restante:.1f}",
        parse_mode="Markdown"
    )



async def add_beneficiario_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if not context.args:
        await update.message.reply_text(
            "❌ Use assim:\n/add_beneficiario Nome"
        )
        return

    nome = " ".join(context.args)

    try:
        adicionar_beneficiario(nome, chat_id)
        await update.message.reply_text(
            f"✅ Beneficiário '{nome}' cadastrado com sucesso"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")


async def set_entrada_cmd(update, context):
    chat_id = update.effective_chat.id

    if not context.args:
        await update.message.reply_text("Use: /entrada 5000")
        return

    salario = float(context.args[0])
    sheet = get_sheet("CONFIG", chat_id)
    sheet.append_row([chat_id, salario])

    await update.message.reply_text("✅ Salário configurado com sucesso")
