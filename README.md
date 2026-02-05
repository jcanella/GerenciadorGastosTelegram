# 🤖 Gerenciador de Gastos via Telegram

Bot pessoal de controle financeiro integrado ao Telegram e Google Sheets.  
Permite registrar gastos de forma natural (texto livre), consultar resumos mensais, analisar gastos por pessoa e obter insights financeiros com base no salário.

Projeto pessoal, simples, funcional e rodando 24/7 na nuvem.

---

## ✨ Funcionalidades

### 💸 Registro de gastos (mensagem livre)
Envie mensagens como:
120 mercado eu
ontem 45 almoço namorada
15/01 200 jantar


O bot automaticamente:
- Detecta data (hoje, ontem ou data informada)
- Extrai valor
- Identifica beneficiário
- Classifica categoria
- Registra no Google Sheets

---

### 📊 Comandos disponíveis

| Comando | Descrição |
|------|---------|
| `/start` | Inicia o bot |
| `/help` | Mostra ajuda e exemplos |
| `/resumo` | Total gasto no mês atual |
| `/quem nome` | Total gasto por beneficiário |
| `/insights` | Percentual do salário gasto |
| `/beneficiario nome` | Adiciona novo beneficiário |
| `/entrada valor` | Registra entradas no mês |

---

## 🧠 Arquitetura do Projeto
GerenciadorDeGastos/
│
├─ bot.py # Core do bot e handlers
├─ commands.py # Comandos (/help, /resumo, etc)
├─ sheets.py # Integração com Google Sheets
├─ parser.py # NLP simples (data, valor, texto)
├─ categories.py # Classificação automática
├─ beneficiarios.py # Gestão de beneficiários
├─ router.py # Separação de planilhas por usuário
├─ config.py # Configurações e constantes
├─ requirements.txt # Dependências
└─ README.md

---

## 📄 Estrutura da Planilha (Google Sheets)

### Aba `GASTOS`
| Coluna | Descrição |
|-----|----------|
| id | UUID do gasto |
| data | Data do gasto |
| valor | Valor numérico |
| categoria | Categoria automática |
| beneficiario | Quem foi beneficiado |
| descricao | Descrição livre |
| created_at | Timestamp |

### Aba `CONFIG`
- `B1`: Salário mensal

### Aba `BENEFICIARIOS`
- Lista dinâmica de beneficiários permitidos por usuário

---

## 🔐 Segurança
- Cada usuário possui **sua própria planilha**
- Dados isolados por `chat_id`
- Service Account do Google com acesso restrito
- Tokens e credenciais via variáveis de ambiente

---

## 🚀 Deploy (24/7 gratuito)

Recomendado: **Railway.app**

### Variáveis de ambiente necessárias
TELEGRAM_TOKEN=seu_token
USUARIO_AUTORIZADO=seu_chat_id
GOOGLE_CREDENTIALS={JSON do service account}

O bot roda via **polling**, sem webhook.

---

## 🛠️ Tecnologias usadas
- Python 3.10+
- python-telegram-bot
- Google Sheets API
- gspread
- OAuth2 Service Account

---

## 📌 Status do Projeto
✔️ Funcional  
✔️ Estável  
✔️ Uso pessoal  
✔️ Manutenção simples  

> “Se melhorar, estraga.” 😄

---

## 📜 Licença
Projeto pessoal para uso próprio.  
Sinta-se livre para estudar, adaptar e melhorar.

