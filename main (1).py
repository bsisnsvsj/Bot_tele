from keep_alive import keep_alive
keep_alive()

# --- هنا كود بوت التيليجرام عندك ---
# ... باقي كود البوت ...
# --- هنا كود بوت التيليجرام عندك ---
# ... باقي كود البوت ...




import json,requests
import os
from deep_translator import GoogleTranslator
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import pytz  # بدل zoneinfo
import os
import json
import random
import asyncio

from apscheduler.schedulers.background import BackgroundScheduler

# هذا التايمزون المطلوب
timezone = pytz.timezone("Asia/Baghdad")

# تعريف السكيجولر
scheduler = BackgroundScheduler(timezone=timezone)

FILE_NAME = "data.json"

def load_data():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_data(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()

# دالة start أصبحت async ولازم await للرد

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 مرحباً! أرسل لي رسالة وسأحاول الرد. إذا ماعرفت الجواب، تقدر تعلمني.")
    user_id = update.effective_chat.id
    users = []
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            users = json.load(f)
    if user_id not in users:
        users.append(user_id)
        with open("users.json", "w") as f:
            json.dump(users, f)

# دالة لمعالجة الرسائل (السؤال والجواب)
async def handle_learning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()

    # إذا بدأ بـ "answer:" معناه تعليم إجابة جديدة
    if user_text.lower().startswith("answer:"):
        answer = user_text[7:].strip()
        question = context.user_data.get("last_question")
        if question:
            data[question] = answer
            save_data(data)
            await update.message.reply_text("✅ شكراً! تعلمت إجابة جديدة.")
        else:
            await update.message.reply_text("⚠️ ماكو سؤال سابق مرتبط. رجاءً أرسل السؤال أولاً.")
    else:
        # نخزن السؤال الأخير
        context.user_data["last_question"] = user_text
        # نرد إذا موجود الجواب
        if user_text in data:
            await update.message.reply_text(data[user_text])
        else:
            await update.message.reply_text("🤖 ما أعرف الجواب، تقدر تعلمني؟ أرسل: answer: ردك هنا")



#Weather
API_KEY = "0f930cc25fe2d697574d396717377254"

# دالة تجيب الطقس
async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        city = " ".join(context.args)
        if not city:
            await update.message.reply_text("اكتب اسم المدينة >> مثال : /weather بغداد")
            return

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&lang=ar&units=metric"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            feels = data["main"]["feels_like"]

            msg = f"🌤️ الطقس في {city}:\nالحالة: {desc}\nدرجة الحرارة: {temp}°C\nيشعر بها كـ {feels}°C"
            await update.message.reply_text(msg)
        else:
            await update.message.reply_text("❌ ماكدر أجيب الطقس. تأكد من اسم المدينة.")
    except Exception as e:
        await update.message.reply_text(f"❌ صار خطأ: {e}")

# دالة البدء
#async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
 #   await update.message.reply_text("👋 أهلاً! أرسل /الطقس واسم مدينة حتى أرجعلك الطقس.\nمثال: /الطقس بغداد")

#Translator

async def translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        original_text = " ".join(context.args)
        translated = GoogleTranslator(source='auto', target='en').translate(original_text)
        await update.message.reply_text(f"✅ الترجمة:\n{translated}")
    else:
        await update.message.reply_text("❗ اكتب الجملة بعد الأمر\nمثال: /translate كيف حالك؟")
        
        
        
#اشعارات للمستخدمين
# رسائل عشوائية مضحكة باللهجة العراقية

async def send_random_message(application):
    if not os.path.exists("users.json"):
        return

    with open("users.json", "r") as f:
        users = json.load(f)
    MESSAGES = [
    "😂 لك قوم اشتغل، الكسل بعده ما صار إنجاز!",
    "😴 إذا نايم، تره الحلم ما يتحقق بالحلم... قوم!",
    "📱 كافي تفتر عالفيس، اشتغل شي يفيدك!",
    "🥲 راح اليوم؟ لا تخاف بعدك ما بلّشت بيه أصلاً!",
    "🤡 إذا تنتظر حظك، فتره هو نايم... إنت اشتغل.",
    "🧠 كل عقلك تقول 'ورا العيد أبلش'... أي عيد؟",
    "🕺 كاعد تنتظر المعجزة؟ المعجزة إنك تتحرك هسه.",
    "👊 قوم اشرب چاي وتعال نبلّش نشتغل، لا تسوي نفسك مشغول.",
    "🧹 الدنيا دوارة، بس إنت ثابت مثل طابوگة 😆",
    "📚 العلم نور... بس إنت مطفي اللمبة من الأساس."
]



    message = random.choice(MESSAGES)

    for user_id in users:
        try:
            await application.bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            print(f"❌ خطأ في الإرسال إلى {user_id}: {e}")



def main():
    TOKEN = "7810466393:AAGbJDkNKJP8odFbEeVgXCH58z5RfSFj5Ks"

    # نستخدم ApplicationBuilder بدلاً من Updater
    app = ApplicationBuilder().token(TOKEN).build()

    # إضافة الأوامر والرسائل مع async handlers
    app.add_handler(CommandHandler("start", start))
    
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_learning))
    app.add_handler(CommandHandler("Weather", weather_command))
    
    app.add_handler(CommandHandler("translate", translate_text))
    
    
# إعداد الجدولة
    scheduler = BackgroundScheduler()

    # جدولة مهمة ترسل كل يومين
    scheduler.add_job(lambda: asyncio.run(send_random_message(app)), 'interval', days=1)
    scheduler.start()


    # بدء البوت
    app.run_polling()

if __name__ == "__main__":
    main()
