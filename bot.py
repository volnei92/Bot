import nest_asyncio
nest_asyncio.apply()

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Seu Token do Bot do Telegram (substitua pelo seu token)
TOKEN = "SEU_TOKEN_AQUI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia uma mensagem quando o comando /start é emitido."""
    await update.message.reply_text('Olá! Eu sou um bot simples. Como posso ajudá-lo?')

async def main() -> None:
    """Inicia o bot."""
    application = Application.builder().token(TOKEN).build()

    # Adiciona o manipulador do comando /start
    application.add_handler(CommandHandler("start", start))

    # Inicia o bot de forma assíncrona
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    print("Bot iniciado. Ele permanecerá em execução até que o kernel seja interrompido.")

    # Mantém o bot rodando indefinidamente
    try:
        await application.idle()
    except (KeyboardInterrupt, SystemExit):
        await application.stop()
        print("Bot parado.")

# Executa a função main assíncrona
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
