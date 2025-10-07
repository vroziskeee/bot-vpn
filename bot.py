from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройки
BOT_TOKEN = "8328377123:AAEzccKhnKlWsBb0-BlLiHHc3-vve9bnb3c"
ADMIN_ID = 5406733841  # Ваш ID в Telegram

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_info = f"👤 {user.first_name} (@{user.username}) ID: {user.id}"
    
    await update.message.reply_text(
        "🔒 Привет! Я бот для продажи VPN подписок\n\n"
        "📨 Напишите сообщение, и я сразу свяжу вас с администратором\n"
        "Обычно отвечаем в течение 5-15 минут\n\n"
        "💬 Просто напишите, что вас интересует:"
    )
    
    # Уведомляем администратора
    await context.bot.send_message(
        ADMIN_ID,
        f"🆕 Новый пользователь в боте:\n{user_info}"
    )

# Пересылаем все сообщения администратору
async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message_text = update.message.text
    
    user_info = f"👤 {user.first_name} (@{user.username}) ID: {user.id}"
    
    # Пересылаем сообщение администратору
    await context.bot.send_message(
        ADMIN_ID,
        f"✉️ НОВОЕ СООБЩЕНИЕ ОТ:\n{user_info}\n\n"
        f"💬 Текст:\n{message_text}\n\n"
        f"➖➖➖➖➖➖➖➖➖➖\n"
        f"Чтобы ответить, напишите:\n"
        f"/reply {user.id} ваш_текст"
    )
    
    # Подтверждаем пользователю
    await update.message.reply_text(
        "✅ Ваше сообщение отправлено администратору!\n"
        "Скоро с вами свяжутся для оформления заказа."
    )

# Команда для ответа администратора
async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Доступ запрещен")
        return
    
    if len(context.args) < 2:
        await update.message.reply_text("Использование: /reply USER_ID текст")
        return
    
    user_id = int(context.args[0])
    reply_text = " ".join(context.args[1:])
    
    try:
        await context.bot.send_message(
            user_id,
            f"📨 Ответ от администратора:\n\n{reply_text}"
        )
        await update.message.reply_text("✅ Ответ отправлен!")
    except:
        await update.message.reply_text("❌ Ошибка отправки. Пользователь не найден.")

# Статистика
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    
    await update.message.reply_text(
        "📊 Бот работает в простом режиме\n"
        "Все сообщения пересылаются вам\n"
        "Для ответа используйте /reply USER_ID текст"
    )

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reply", admin_reply))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_admin))
    
    print("🤖 Бот запущен в простом режиме...")
    application.run_polling()

if __name__ == "__main__":
    main()