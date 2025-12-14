import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.request import HTTPXRequest
import httpx
import requests
# تنظیمات لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# سوالات و پاسخ‌های ثابت
QUESTIONS = {
    "q1": {
        "question": "چگونه می‌توانم در پایتون شروع به یادگیری کنم؟",
        "answer": "برای شروع یادگیری پایتون:\n1. ابتدا پایتون را از python.org دانلود و نصب کنید\n2. از منابع آنلاین مانند Codecademy، Coursera یا کتاب‌های فارسی استفاده کنید\n3. پروژه‌های کوچک بسازید و تمرین کنید\n4. در انجمن‌های برنامه‌نویسی مشارکت کنید"
    },
    "q2": {
        "question": "تفاوت بین list و tuple در پایتون چیست؟",
        "answer": "تفاوت‌های اصلی:\n• لیست‌ها تغییرپذیر (mutable) هستند اما توپل‌ها تغییرناپذیر (immutable)\n• لیست‌ها با [] و توپل‌ها با () تعریف می‌شوند\n• لیست‌ها برای داده‌های پویا و توپل‌ها برای داده‌های ثابت مناسب‌ترند"
    },
    "q3": {
        "question": "چگونه یک بات تلگرام بسازم؟",
        "answer": "مراحل ساخت بات تلگرام:\n1. با @BotFather در تلگرام یک بات جدید ایجاد کنید\n2. توکن دریافتی را ذخیره کنید\n3. از کتابخانه python-telegram-bot استفاده کنید\n4. کد خود را بنویسید و روی سرور اجرا کنید"
    },
    "q4": {
        "question": "چگونه در پایتون از API استفاده کنم؟",
        "answer": "برای استفاده از API در پایتون:\n1. کتابخانه requests را نصب کنید (pip install requests)\n2. درخواست HTTP مناسب (GET, POST و ...) بفرستید\n3. پاسخ JSON را پردازش کنید\n4. خطاها را به درستی مدیریت کنید"
    },
    "q5": {
        "question": "بهترین IDE برای پایتون چیست؟",
        "answer": "انتخاب IDE بستگی به نیاز شما دارد:\n• PyCharm: حرفه‌ای و کامل\n• VS Code: سبک و قابل گسترش\n• Jupyter Notebook: مناسب برای تحلیل داده\n• IDLE: ساده و پیش‌فرض پایتون"
    }
}

# دستور شروع
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ارسال پیام خوشامدگویی و نمایش سوالات"""
    print("📩 /start received")
    user = update.effective_user
    welcome_message = f"سلام {user.first_name}! 👋\n\nبه بات سوالات متداول خوش آمدید.\nلطفاً یکی از سوالات زیر را انتخاب کنید:"
    
    # ایجاد دکمه‌های شیشه‌ای برای سوالات
    keyboard = []
    for key, data in QUESTIONS.items():
        keyboard.append([InlineKeyboardButton(data["question"], callback_data=key)])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# دستور کمک
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ارسال پیام راهنما"""
    help_text = """
دستورات موجود:
/start - شروع کار با بات و مشاهده سوالات
/help - نمایش این راهنما
/questions - مشاهده مجدد سوالات
/about - درباره بات
    """
    await update.message.reply_text(help_text)

# نمایش مجدد سوالات
async def show_questions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """نمایش مجدد سوالات"""
    keyboard = []
    for key, data in QUESTIONS.items():
        keyboard.append([InlineKeyboardButton(data["question"], callback_data=key)])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("لطفاً یکی از سوالات زیر را انتخاب کنید:", reply_markup=reply_markup)

# درباره بات
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """نمایش اطلاعات درباره بات"""
    about_text = """
🤖 بات سوالات متداول (FAQ Bot)

این بات به شما کمک می‌کند تا پاسخ سوالات متداول را به سرعت پیدا کنید.

ویژگی‌ها:
• مجموعه‌ای از سوالات و پاسخ‌های از پیش تعریف شده
• رابط کاربری ساده و سریع
• دسترسی آسان به اطلاعات

ساخته شده با پایتون و کتابخانه python-telegram-bot
    """
    await update.message.reply_text(about_text)

# پردازش انتخاب سوال
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """پردازش کلیک روی دکمه سوال"""
    query = update.callback_query
    await query.answer()
    
    # دریافت پاسخ بر اساس کلید سوال
    question_key = query.data
    if question_key in QUESTIONS:
        answer = QUESTIONS[question_key]["answer"]
        question_text = QUESTIONS[question_key]["question"]
        
        # ارسال پاسخ
        response = f"❓ سوال:\n{question_text}\n\n💡 پاسخ:\n{answer}\n\nبرای مشاهده سوالات دیگر از /questions استفاده کنید."
        await query.edit_message_text(text=response)
        
        # ایجاد دکمه بازگشت به سوالات
        keyboard = [[InlineKeyboardButton("📋 مشاهده همه سوالات", callback_data="show_all")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="آیا می‌خواهید سوال دیگری بپرسید؟",
            reply_markup=reply_markup
        )
    elif query.data == "show_all":
        # نمایش مجدد همه سوالات
        keyboard = []
        for key, data in QUESTIONS.items():
            keyboard.append([InlineKeyboardButton(data["question"], callback_data=key)])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="لطفاً یکی از سوالات زیر را انتخاب کنید:",
            reply_markup=reply_markup
        )

# تابع اصلی
def main() -> None:
    """اجرای اصلی بات"""
    # دریافت توکن بات
    TOKEN = "8002485361:AAFHTiI8N6hhHGxw2KtRLCUFQ5Pzyq8UNVE"  # توکن بات خود را اینجا قرار دهید
    
    # ایجاد برنامه
    application = (Application.builder().token(TOKEN).build())
    
    # ثبت دستورات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("questions", show_questions))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # شروع بات
    print("✅ بات در حال اجراست...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()