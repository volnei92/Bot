import nest_asyncio
nest_asyncio.apply()

import asyncio
import random
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

# Seu Novo Token do Bot do Telegram
TOKEN = "7971766586:AAGvajmZb_VcZuXTcOuaM4U2dnz5l_Fcb4o"

# Nome do livro
nome_do_livro = "O Evangelho Segundo o Espiritismo"

# Textos do livro (365 trechos selecionados do Evangelho)
trechos_do_livro = [
    "Fé inabalável é somente aquela que pode encarar a razão face a face, em todas as épocas da humanidade.",
    "A verdadeira caridade é a que se faz sem ostentação.",
    "O homem é o artífice de seu próprio destino, e suas escolhas determinam seu futuro.",
    "A felicidade não consiste na posse de bens materiais, mas na paz de espírito.",
    "A vida é uma escola onde aprendemos a amar e a perdoar.",
    "O orgulho e o egoísmo são os maiores obstáculos ao progresso espiritual.",
    "A caridade é a alma do Espiritismo; é a prática do amor ao próximo.",
    "A vida é uma oportunidade de aprendizado e evolução.",
    "O perdão é uma liberação tanto para quem perdoa quanto para quem é perdoado.",
    "A verdadeira felicidade é encontrada na simplicidade e na dedicação ao próximo.",
    "O amor é a força que move o universo e que transforma a vida.",
    "Uma palavra de amor pode mudar o coração de um ser.",
    "Não se deve retribuir uma injustiça com outra.",
    "A reencarnação é uma oportunidade de corrigir erros do passado e buscar a evolução.",
    "O verdadeiro sentido da vida está em servir ao próximo.",
    "A prática do bem deve ser um hábito cotidiano.",
    "A luz do amor ilumina até os caminhos mais escuros.",
    "A transformação pessoal é a chave para a verdadeira mudança no mundo.",
    "A paz interior é a base para a paz no mundo.",
    "A vida é uma travessia onde aprendemos a amar.",
    "A doação sem esperar recompensa é a verdadeira caridade.",
    "Os Espíritos nos ensinam que devemos amar uns aos outros.",
    "O amor deve ser a motivação de todas as nossas ações.",
    "Cada evento em nossa vida tem um propósito maior.",
    "Cada um é responsável por suas escolhas e ações.",
    "A verdadeira amizade é um tesouro que devemos valorizar.",
    "O respeito ao próximo é a base de uma sociedade justa.",
    "A esperança é a luz que ilumina nosso caminho nas horas de escuridão.",
    "O egoísmo é uma barreira ao crescimento espiritual.",
    "O amor é a maior força do universo e pode transformar tudo.",
    "As dificuldades da vida são oportunidades para o crescimento espiritual.",
    "Cada ato de bondade é uma semente que germina no coração do outro.",
    "A sinceridade é fundamental para a construção de relacionamentos saudáveis.",
    "O conhecimento deve ser utilizado para o bem.",
    "A vida é feita de escolhas e cada escolha tem suas consequências.",
    "O amor é a essência da vida e deve ser cultivado constantemente.",
    "A verdade sempre prevalecerá, mesmo diante da adversidade.",
    "As lições que aprendemos são como degraus para a evolução.",
    "Nossas experiências são valiosas e devem ser compartilhadas.",
    "O amor é capaz de curar as feridas da alma.",
    "Cada ser humano é um reflexo do Criador.",
    "As pequenas coisas da vida devem ser apreciadas com gratidão.",
    "O conhecimento traz luz aos nossos caminhos.",
    "A caridade é a expressão mais pura do amor.",
    "O autoconhecimento é essencial para a transformação.",
    "Os laços de amor criados na Terra permanecem no além.",
    "A prática do bem gera frutos e recompensa.",
    "A atenção e a empatia são fundamentais nas relações.",
    "A felicidade é encontrada na entrega e no amor.",
    "Cada dia é uma nova oportunidade de recomeçar.",
    "O amor é uma linguagem que todos entendem.",
    "O tempo deve ser utilizado com sabedoria.",
    "A esperança é a âncora da nossa fé.",
    "Os Espíritos nos encorajam a viver com destemor.",
    "A compaixão nos ajuda a compreender o sofrimento do outro.",
    "Cuidar do próximo é uma forma de cuidar de si mesmo.",
    "A única força capaz de transformar o mundo é o amor.",
    "As dificuldades são momentos de aprendizado.",
    "A paciência é uma virtude que traz recompensas.",
    "Os seres humanos são todos interligados por laços invisíveis.",
    "A generosidade é uma prática que enriquece a alma.",
    "Cada escolha que fazemos é um passo em direção ao nosso destino.",
    "A vida é uma viagem repleta de aprendizado.",
    "A bondade traz alegria tanto para quem dá quanto para quem recebe.",
    "A luz da verdade é sempre libertadora.",
    "O amor deve ser cultivado todos os dias.",
    "Cada ser humano é digno de respeito e dignidade.",
    "A prática diária do bem transforma nosso caráter.",
    "Os laços de amor podem superar o tempo e a distância.",
    "O crescimento espiritual é uma jornada contínua.",
    "A caridade não deve ser apenas um ato, mas um modo de vida.",
    "O amor é a chave que abre todas as portas.",
    "A gratidão é uma ponte que nos conecta ao divino.",
    "Cada palavra de amor é um ato de criação.",
    "A vida é um reflexo do que somos por dentro.",
    "A empatia é fundamental para a convivência pacífica.",
    "O amor é o cimento que une a humanidade.",
    "Cada ato de bondade é uma semente de amor.",
    "As dificuldades da vida são oportunidades de aprendizado.",
    "A vida deve ser vivida com propósito e intenção.",
    "Os sentimentos nobres são essenciais para a paz.",
    "O amor é um presente que devemos cultivar.",
    "Cada novo dia traz novas possibilidades.",
    "A busca pela verdade é um caminho de libertação.",
    "A caridade deve ser uma prática diária.",
    "O amor é a energia que alimenta nossa alma.",
    "Cada pessoa é uma oportunidade de amar.",
    "A compaixão é a verdadeira essência da humanidade.",
    "O tempo é precioso e deve ser utilizado com sabedoria.",
    "A luz que emitimos deve ser cultivada.",
    "Cuidar do outro é um ato de amor genuíno.",
    "O amor é a força que une todos os seres.",
    "Cada pequena ação de bondade conta.",
    "Os desafios são testes que nos fortalecem.",
    "O amor verdadeiro não tem limites.",
    "A doação é uma forma de se conectar com o outro.",
    "A vida é uma experiência única que deve ser valorizada.",
    "Os laços criados pelo amor são eternos.",
    "A sabedoria é o resultado da reflexão e do aprendizado.",
    "O amor é a resposta para todas as perguntas da vida.",
    "Cada escolha reflete quem somos como indivíduos.",
    "O espírito é eternamente evolutivo.",
    "A comunhão com o próximo enriquece a alma.",
    "Cada ato de bondade gera um eco no universo.",
    "A presença da paz é um reflexo do amor que cultivamos.",
    "A prática da caridade traz luz à alma.",
    "A vida é uma dádiva que deve ser celebrada.",
    "O amor é o caminho que todos devemos seguir.",
    "A verdadeira felicidade é encontrada no amor ao próximo.",
    "O perdão é um presente que devemos dar a nós mesmos.",
    "Cada ato de amor deixa um legado.",
    "As lições da vida são ensinos do espírito.",
    "O amor é capaz de curar feridas profundas.",
    "Cada pequeno gesto importa e gera efeitos.",
    "A compaixão deve ser uma prática constante.",
    "A vida deve ser vivida com propósito e amor.",
    "Cada um é responsável por suas próprias ações.",
    "Os desafios são oportunidades de crescimento.",
    "O amor é a verdadeira essência da vida.",
    "A liberdade vem da prática do perdão.",
    "Os Espíritos superiores nos inspiram a amar.",
    "Cada erro é uma oportunidade de aprendizado.",
    "A prática diária da caridade traz luz à alma.",
    "A vida é um presente que deve ser aproveitado.",
    "O amor é um caminho que todos podemos trilhar.",
    "A união em torno de um propósito é fundamental.",
    "A felicidade é uma escolha diária.",
    "O amor é a luz que brilha em meio à escuridão.",
    "A sabedoria é o resultado da experiência.",
    "A vida é uma série de oportunidades para construir o bem.",
    "A verdade nos liberta.",
    "A vida é um reflexo da luz que cultivamos.",
    "Os laços de amor transcendem a morte.",
    "Cada ação gera uma reação; escolha o amor.",
    "A prática da gratidão transforma nossas vidas.",
    "O amor é a força que une todos os seres.",
    "Cada um de nós tem sua própria história para contar.",
    "A verdadeira amizade é um bem valioso.",
    "Os pensamentos positivos moldam a nossa realidade.",
    "A luz que emitimos influencia nosso entorno.",
    "Cuidar de si mesmo é um ato de amor.",
    "A força do amor pode mudar o mundo.",
    "A vida é uma viagem de aprendizado contínuo.",
    "O amor deve ser o motor de nossas vidas.",
    "A gratidão abre portas para novas bênçãos.",
    "Os desafios são oportunidades para aprender.",
    "A prática do amor transforma a sociedade.",
    "Cada pequeno gesto de bondade é significativo.",
    "O amor é a resposta para todos os males.",
    "Viver com amor e alegria é viver plenamente.",
    "As experiências vividas nos ensinam a amar mais.",
    "O caminho do amor é o caminho da paz.",
    "Celebrar a vida é reconhecer suas belezas.",
    "Buscar a verdade é um ato de amor ao próximo.",
    "A vida é uma oportunidade para amar e ser amado.",
    "A luz que brilha em nós deve ser compartilhada.",
    "O amor é a energia que nos move em direção ao bem.",
    "A prática da compaixão nos torna humanos.",
    "Cada escolha é uma oportunidade de fazer o bem.",
    "O amor é uma força que transforma o impossível em possível.",
    "As dificuldades são meios de encontrar a superação.",
    "A alegria de viver é uma benção que deve ser valorizada.",
]

# Dicionário para armazenar o estado do usuário (ex: qual capítulo ele está lendo)
user_states = {}

# Lista de emojis para adicionar a cada frase
emojis = [
    "🌟", "❤️", "✨", "👍", "🌈", "🙏", "💫", "🌹", "🌻", "🌼", "🌷", "🍀", "🍂", "🌏",
    "🔮", "🌙", "🌞", "🕊️", "💖", "💜", "💚", "💛", "🧡", "💙"
]

# Agendamento do horário para receber mensagens
user_schedule = {}

async def send_daily_message(application: Application, user_id: int) -> None:
    """Envia uma mensagem diária ao usuário especificado."""
    trecho_aleatorio = random.choice(trechos_do_livro)  # Mensagem aleatória
    emoji = random.choice(emojis)
    try:
        await application.bot.send_message(
            chat_id=user_id,
            text=f'🕊️📖✨ <b>"{nome_do_livro}"</b>\n{emoji} <b>{trecho_aleatorio}</b> {emoji} ✨📖🕊️',
            parse_mode='HTML'
        )
    except Exception as e:
        print(f"Não foi possível enviar mensagem para o usuário {user_id}: {e}")

async def schedule_messages(user_id: int):
    """Agendar a mensagem para o horário definido pelo usuário."""
    if user_id in user_schedule:
        schedule_time = user_schedule[user_id]
        hour, minute = map(int, schedule_time.split(':'))
        scheduler.add_job(send_daily_message, CronTrigger(hour=hour, minute=minute), args=[application, user_id], id=f"job_{user_id}")

async def send_daily_messages(application: Application) -> None:
    """Envia mensagens diárias programadas para todos os usuários com agendamento."""
    for user_id in user_schedule.keys():
        await send_daily_message(application, user_id)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia o primeiro trecho do livro quando o comando /start é usado."""
    user_id = update.effective_user.id
    current_index = 0  # Começa do primeiro trecho
    trecho_atual = random.choice(trechos_do_livro)  # Mensagem aleatória
    emoji = random.choice(emojis)

    # Armazena o estado do usuário
    user_states[user_id] = {
        "current_index": current_index,
        "total_trechos": len(trechos_do_livro)
    }

    keyboard = [
        [
            InlineKeyboardButton("Anterior", callback_data="anterior"),
            InlineKeyboardButton("Próximo", callback_data="proximo")
        ],
        [
            InlineKeyboardButton("Definir Horário", callback_data="set_horario"),
            InlineKeyboardButton("Apagar Agendamento", callback_data="delete_horario")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f'🕊️📖✨ <b>"{nome_do_livro}"</b>\n{emoji} <b>{trecho_atual}</b> {emoji} ✨📖🕊️',
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    if user_id not in user_states:
        await query.edit_message_text(text="Por favor, use /start para começar de novo.")
        return

    if query.data == "set_horario":
        await query.edit_message_text(text="Por favor, digite o horário desejado no formato HH:MM (24 horas).")
        return

    elif query.data == "delete_horario":
        if user_id in user_schedule:
            del user_schedule[user_id]
            await query.edit_message_text(text="Agendamento apagado com sucesso.")
        else:
            await query.edit_message_text(text="Nenhum agendamento encontrado para este usuário.")
        return

    user_data = user_states[user_id]
    current_index = user_data["current_index"]
    total_trechos = user_data["total_trechos"]

    if query.data == "proximo":
        current_index = (current_index + 1) % total_trechos
    elif query.data == "anterior":
        current_index = (current_index - 1 + total_trechos) % total_trechos

    user_data["current_index"] = current_index
    trecho_novo = random.choice(trechos_do_livro)  # Mensagem aleatória
    emoji = random.choice(emojis)

    keyboard = [
        [
            InlineKeyboardButton("Anterior", callback_data="anterior"),
            InlineKeyboardButton("Próximo", callback_data="proximo")
        ],
        [
            InlineKeyboardButton("Definir Horário", callback_data="set_horario"),
            InlineKeyboardButton("Apagar Agendamento", callback_data="delete_horario")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await query.edit_message_text(
            text=f'🕊️📖✨ <b>"{nome_do_livro}"</b>\n{emoji} <b>{trecho_novo}</b> {emoji} ✨📖🕊️',
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    except Exception as e:
        print(f"Erro ao editar mensagem para {user_id}: {e}")

async def set_horario(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    time_str = update.message.text  # O usuário irá digitar seu horário nesta parte.

    # Adicionar à programação
    user_schedule[user_id] = time_str
    await update.message.reply_text(f"Você definiu o horário: {time_str} para receber mensagens!")
    await schedule_messages(user_id)

async def main() -> None:
    """Inicia o bot e o mantém rodando."""
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, set_horario))

    # Inicia o agendador
    scheduler = AsyncIOScheduler()

    # Adiciona o envio de mensagens programadas para usuários que definiram um horário
    @scheduler.scheduled_job('cron', hour='*', minute='*/1')  # A cada minuto
    async def check_scheduled_messages():
        current_time = datetime.now().strftime("%H:%M")
        for user_id in user_schedule.keys():
            if user_schedule[user_id] == current_time:
                await send_daily_message(application, user_id)

    scheduler.start()

    # Inicia o bot de forma assíncrona
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    print("Bot iniciado. Ele permanecerá em execução até que o kernel seja interrompido.")

    # Mantém o bot rodando indefinidamente
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        await application.stop()
        scheduler.shutdown()
        print("Bot parado.")

# Executa a função main assíncrona
await main()

