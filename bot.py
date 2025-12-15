import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

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

    "q1": {
        "question": "سامانه‌های درس‌افزار دانشگاه چیست و هر دانشکده از کدام استفاده می‌کند؟",
        "answer": (
            "سامانه‌های درس‌افزار دانشگاه بوعلی سینا:\n\n"
            "📘 درس‌افزار 1 (CW1): https://cw1.basu.ac.ir\n"
            "مخصوص دانشکده‌های علوم انسانی و مهندسی\n\n"
            "📗 درس‌افزار 2 (CW2): https://cw2.basu.ac.ir\n"
            "مخصوص علوم پایه، کشاورزی، هنر و معماری و اقماری نهاوند\n\n"
            "📙 درس‌افزار 3 (CW3): https://cw3.basu.ac.ir\n"
            "مخصوص علوم اقتصادی و اجتماعی، شیمی، دامپزشکی، علوم ورزشی، "
            "اقماری تویسرکان، بهار، رزن، کبودرآهنگ و کلیه دروس عمومی\n\n"
            "🌍 درس‌افزار بین‌الملل: https://cw.basu.ac.ir\n"
            "مخصوص دانشجویان بین‌الملل"
        )
    },

    "q2": {
        "question": "نحوه ورود اساتید به سامانه درس‌افزار چگونه است؟",
        "answer": (
            "👨‍🏫 نام کاربری: کد استادی\n"
            "🔑 رمز عبور: کد ملی + حرف m\n"
            "مثال: 1234567890m"
        )
    },

    "q3": {
        "question": "نحوه ورود دانشجویان به سامانه درس‌افزار چگونه است؟",
        "answer": (
            "🎓 ورودی‌های 1403 و 1404:\n"
            "نام کاربری = شماره دانشجویی\n"
            "رمز عبور = شماره دانشجویی\n\n"
            "🎓 ورودی‌های قبل از 1403:\n"
            "نام کاربری = شماره دانشجویی\n"
            "رمز عبور = کد ملی"
        )
    },

    "q4": {
        "question": "چگونه سامانه درس‌افزار دانشکده خود را پیدا کنیم؟",
        "answer": (
            "فهرست کامل سامانه‌های هر دانشکده در لینک زیر موجود است:\n"
            "https://elearning.basu.ac.ir/cw\n\n"
            "دانشجو باید طبق دانشکده خود وارد CW1، CW2 یا CW3 شود."
        )
    },

    "q5": {
        "question": "چرا دروس عمومی در درس‌افزار دانشکده نمایش داده نمی‌شود؟",
        "answer": (
            "تمامی دروس عمومی فقط در سامانه CW3 ارائه می‌شوند.\n\n"
            "راه‌حل:\n"
            "ورود به https://cw3.basu.ac.ir با همان نام کاربری و رمز قبلی.\n"
            "نیازی به ساخت حساب جدید نیست."
        )
    },

    "q6": {
        "question": "آیا اساتید برای دروس عمومی باید از CW3 استفاده کنند؟",
        "answer": (
            "بله ✅\n"
            "اساتیدی که دروس عمومی دارند باید وارد CW3 شوند "
            "و از همان کد استادی و رمز (کد ملی + m) استفاده کنند."
        )
    },

    "q7": {
        "question": "اگر درس عمومی در CW3 نمایش داده نشد چه باید کرد؟",
        "answer": (
            "دلایل ممکن:\n"
            "• استاد درس را فعال نکرده\n"
            "• برنامه آموزشی ثبت نشده\n"
            "• مشکل در تخصیص درس\n\n"
            "راه‌حل:\n"
            "تماس با آموزش دانشکده یا پشتیبانی فنی"
        )
    },

    "q8": {
        "question": "نحوه ورود اساتید به کلاس Adobe Connect چگونه است؟",
        "answer": (
            "🎥 لینک اختصاصی استاد:\n"
            "http://vc.basu.ac.ir/basuxxxxxx\n\n"
            "نام کاربری: کد استادی\n"
            "رمز عبور: کد ملی + v\n"
            "مثال: 1234567890v\n\n"
            "اگر وارد نشد:\n"
            "فقط کد ملی را امتحان کنید."
        )
    },

    "q9": {
        "question": "نحوه ورود دانشجویان به کلاس Adobe Connect چگونه است؟",
        "answer": (
            "دانشجویان نام کاربری ندارند.\n\n"
            "مراحل ورود:\n"
            "1️⃣ کلیک روی لینک کلاس\n"
            "2️⃣ انتخاب «ورود به عنوان مهمان (Guest)»\n"
            "3️⃣ وارد کردن نام و نام خانوادگی کامل"
        )
    },

    "q10": {
        "question": "لینک کلاس آنلاین کجاست؟",
        "answer": (
            "تمام لینک‌های کلاس آنلاین داخل سامانه درس‌افزار (CW)\n"
            "و در صفحه همان درس قرار دارد."
        )
    },

    "q11": {
        "question": "اگر استاد با لینک دانشجویی وارد شود و Host نباشد چه کند؟",
        "answer": (
            "1️⃣ خروج از کلاس\n"
            "2️⃣ بستن کامل مرورگر یا Adobe Connect\n"
            "3️⃣ ورود مجدد از لینک اختصاصی استاد\n"
            "4️⃣ وارد کردن اطلاعات صحیح"
        )
    },

    "q12": {
        "question": "چرا دانشجویان نمی‌توانند جلسات ضبط‌شده را ببینند؟",
        "answer": (
            "زیرا استاد وضعیت ضبط جلسه را Public نکرده است.\n\n"
            "راه‌حل:\n"
            "استاد باید وضعیت ضبط را روی «عمومی (Public)» قرار دهد."
        )
    },

    "q13": {
        "question": "پروتکل امنیتی Adobe Connect دانشگاه چیست؟",
        "answer": (
            "پروتکل امن HTTPS\n"
            "آدرس رسمی:\n"
            "https://vc.basu.ac.ir/"
        )
    },

    "q14": {
        "question": "تفاوت اصلی درس‌افزار (CW) و Adobe Connect چیست؟",
        "answer": (
            "📚 درس‌افزار (CW):\n"
            "مدیریت آموزش، فایل‌ها، آزمون، تکلیف، نمره\n\n"
            "🎥 Adobe Connect:\n"
            "برگزاری کلاس آنلاین زنده و ضبط جلسه"
        )
    },

    "q15": {
        "question": "اگر استاد یا دانشجو نتوانست وارد کلاس شود چه کار کند؟",
        "answer": (
            "• پاک کردن کش مرورگر\n"
            "• بررسی اینترنت\n"
            "• بررسی اطلاعات ورود\n\n"
            "اساتید: تماس با پشتیبانی فنی\n"
            "دانشجویان: ورود به صورت Guest"
        )
    }
}



# منوی پایین ثابت (ReplyKeyboardMarkup)
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        ["🏠 شروع", "❓ کمک"],
        ["📋 سوالات", "ℹ️ درباره ربات"]
    ],
    resize_keyboard=True
)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(data["question"], callback_data=key)] for key, data in QUESTIONS.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"سلام {update.effective_user.first_name}! یکی از سوالات را انتخاب کنید:",
        reply_markup=reply_markup
    )

# Callback handler برای سوالات
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
    await update.message.reply_text(
        "/start - شروع\n/help - راهنما\n/questions - مشاهده سوالات\n/about - درباره بات",
        reply_markup=main_menu
    )

# /questions
async def show_questions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(data["question"], callback_data=key)] for key, data in QUESTIONS.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📋 لطفاً یکی از سوالات زیر را انتخاب کنید:", reply_markup=reply_markup)

# /about
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ℹ️ این بات FAQ است، ساخته شده با پایتون و python-telegram-bot", reply_markup=main_menu)

# handler برای دکمه‌های ReplyKeyboardMarkup
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🏠 شروع":
        await start(update, context)
    elif text == "❓ کمک":
        await help_command(update, context)
    elif text == "📋 سوالات":
        await show_questions(update, context)
    elif text == "ℹ️ درباره ربات":
        await about(update, context)
    else:
        await update.message.reply_text("لطفاً یکی از دکمه‌ها را انتخاب کنید.", reply_markup=main_menu)

# Main
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("questions", show_questions))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

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
