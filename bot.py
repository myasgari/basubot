import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = '8002485361:AAFHTiI8N6hhHGxw2KtRLCUFQ5Pzyq8UNVE'  # روی Render به عنوان Secret
WEBHOOK_URL = 'https://basubot.onrender.com'  # مثلا https://yourservice.onrender.com/
PORT = int(10000)

# سوالات و پاسخ‌های ثابت
QUESTIONS = {
    "q1": {"question": "چگونه می‌توانم در پایتون شروع به یادگیری کنم؟",
           "answer": "برای شروع یادگیری پایتون:\n1. ابتدا پایتون را نصب کنید\n2. منابع آنلاین یا کتاب‌ها را مطالعه کنید\n3. پروژه‌های کوچک بسازید و تمرین کنید\n4. در انجمن‌ها مشارکت کنید"},
    "q2": {"question": "تفاوت بین list و tuple در پایتون چیست؟",
           "answer": "List mutable است و Tuple immutable.\nList با [] و Tuple با () تعریف می‌شوند."},
    "q3": {"question": "چگونه یک بات تلگرام بسازم؟",
           "answer": "1. با @BotFather یک بات بسازید\n2. توکن را ذخیره کنید\n3. از python-telegram-bot استفاده کنید\n4. کد خود را اجرا کنید"},
    "q4": {"question": "چگونه در پایتون از API استفاده کنم؟",
           "answer": "1. requests نصب کنید\n2. درخواست HTTP ارسال کنید\n3. پاسخ JSON را پردازش کنید\n4. خطاها را مدیریت کنید"},
    "q5": {"question": "بهترین IDE برای پایتون چیست؟",
           "answer": "PyCharm، VS Code، Jupyter Notebook یا IDLE"}
}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(data["question"], callback_data=key)] for key, data in QUESTIONS.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"سلام {update.effective_user.first_name}! یکی از سوالات را انتخاب کنید:", reply_markup=reply_markup)

# Callback handler
# Callback handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    key = query.data

    if key in QUESTIONS:
        q = QUESTIONS[key]["question"]
        a = QUESTIONS[key]["answer"]
        await query.edit_message_text(f"❓ {q}\n\n💡 {a}")

        # دکمه برای بازگشت به لیست سوالات
        keyboard = [[InlineKeyboardButton("📋 مشاهده همه سوالات", callback_data="show_all")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="می‌خواهید سوال دیگری بپرسید؟",
            reply_markup=reply_markup
        )

    elif key == "show_all":
        # نمایش دوباره همه سوالات
        keyboard = [[InlineKeyboardButton(data["question"], callback_data=key)] for key, data in QUESTIONS.items()]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="لطفاً یکی از سوالات زیر را انتخاب کنید:",
            reply_markup=reply_markup
        )

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "/start - شروع\n/help - راهنما\n/questions - مشاهده سوالات\n/about - درباره بات"
    await update.message.reply_text(text)

# /questions
async def show_questions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(data["question"], callback_data=key)] for key, data in QUESTIONS.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("لطفاً یکی از سوالات زیر را انتخاب کنید:", reply_markup=reply_markup)

# /about
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🤖 FAQ Bot\nساخته شده با پایتون و python-telegram-bot"
    await update.message.reply_text(text)

# Main
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("questions", show_questions))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("✅ بات در حال اجراست (Webhook)...")

    # Webhook
    WEBHOOK_PATH = "/bot"
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"{WEBHOOK_URL}{WEBHOOK_PATH}",
        url_path=WEBHOOK_PATH
    )

if __name__ == "__main__":
    main()
