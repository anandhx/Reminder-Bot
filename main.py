import json
import asyncio
from datetime import datetime
from telegram import Bot
import schedule
import time
import pytz

from datetime import timedelta


TELEGRAM_BOT_TOKEN = " "
TELEGRAM_CHAT_ID = " "
INDIAN_TIMEZONE = "Asia/Kolkata"
UTC_TIMEZONE = "UTC"

def get_current_indian_time():
    indian_timezone = pytz.timezone(INDIAN_TIMEZONE)
    current_time = datetime.now(indian_timezone)
    return current_time.strftime("%Y-%m-%d %H:%M:%S %Z")

def load_reminders():
    # Function to load reminders from a JSON file
    try:
        with open('reminders.json') as f:
            reminders = json.load(f)
    except FileNotFoundError:
        reminders = []
    return reminders

async def send_telegram_message(message):
    # Async function to send a message to Telegram
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as e:
        # Catch any exceptions that may occur during message sending
        print(f"Error sending Telegram message: {str(e)}")


def send_reminders():
    # Function to check and send reminders
    print("Checking and sending reminders...")
    reminders = load_reminders()
    try:
        asyncio.run(check_and_send_daily_reminder(reminders))
    except Exception as e:
        # Catch any exceptions that may occur during reminder sending
        error_message = f"Error in send_reminders: {str(e)}"
        asyncio.run(send_telegram_message(error_message))

def send_activities():
    # Function to check and send daily activities reminders
    print("Checking and sending activities...")
    try:
        asyncio.run(send_daily_activities_reminder())
    except Exception as e:
        # Catch any exceptions that may occur during activities sending
        error_message = f"Error in send_activities: {str(e)}"
        asyncio.run(send_telegram_message(error_message))


async def send_daily_activities_reminder():
    # Async function to send daily activities reminders
    try:
        utc_timezone = pytz.timezone(UTC_TIMEZONE)
        current_utc_time = datetime.now(utc_timezone).time()

        # Define personalized messages for specific activities
        messages = {
            "morning": f"☀️ Good morning, Anandhu! It's time to start your day.",
            "night": f"🌙 Good night, Anandhu! Have a restful sleep.",
            "water": f"🥤 Don't forget to drink water!",
            "breakfast": f"🍳 Enjoy a nutritious breakfast!",
            "lunch": f"🍲 Lunchtime! Fuel up for the afternoon.",
            "dinner": f"🍽 Dinner time! Refuel after a productive day.",
            "gym": f"💪 Gym time! Break a sweat and stay active.",
            "college": f"📚 College time! Head to your classes at 04:00 UTC.",
            "study": f"📖 Study time! Take a break and review your notes.",
            "homework": f"📓 Check and complete your homework assignments.",
            "class": f"📖 Get ready for your upcoming classes!",
            "socialize": f"🤝 Socialize with friends and peers!",
            "creative": f"✨ Explore your creative side today!",
            "mindfulness": f"🧘 Practice mindfulness for a few minutes!",
            "coding": f"💻 Work on coding projects or practice coding exercises!",
            "reading": f"📖 Take some time to read a book or articles!",
            "music": f"🎵 Listen to your favorite music or discover new tunes!",
            "self-reflection": f"🌟 Reflect on your goals and achievements!",
            "career": f"🚀 Explore career opportunities and update your resume!",
            "afternoon_tea": f"☕ Enjoy a cup of tea in the afternoon!",
            "nap": f"😴 Take a short nap for rejuvenation!",
            "evening_walk": f"🚶‍♂️ Take a walk in the evening!",
            "review_day": f"📆 Review your day and plan for tomorrow!",
            # Add more activities and messages as needed
        }

        # Determine the appropriate message based on the current time
        if current_utc_time == datetime.strptime("02:00", "%H:%M").time():
            activity = "morning"
        elif current_utc_time == datetime.strptime("17:30", "%H:%M").time():
            activity = "gym"
        elif current_utc_time == datetime.strptime("09:30", "%H:%M").time():
            activity = "college"
        elif current_utc_time == datetime.strptime("12:30", "%H:%M").time():
            activity = "lunch"
        elif current_utc_time == datetime.strptime("21:30", "%H:%M").time():
            activity = "dinner"
        elif current_utc_time == datetime.strptime("15:00", "%H:%M").time():
            activity = "afternoon_tea"
        elif current_utc_time == datetime.strptime("14:00", "%H:%M").time():
            activity = "nap"
        elif current_utc_time == datetime.strptime("18:00", "%H:%M").time():
            activity = "evening_walk"
        elif current_utc_time == datetime.strptime("20:00", "%H:%M").time():
            activity = "review_day"
        elif current_utc_time == datetime.strptime("22:30", "%H:%M").time():
            activity = "night"
        else:
            activity = "water"  # Default to water reminder if no specific activity

        # Send the appropriate message
        await send_telegram_message(messages.get(activity, "🌟 Hi there! Here's your daily reminder:\n\n"))

    except Exception as e:
        # Catch any exceptions that may occur during the reminder sending process
        error_message = f"Error in send_daily_activities_reminder: {str(e)}"
        await send_telegram_message(error_message)

        


async def check_and_send_daily_reminder(reminders):
    indian_timezone = pytz.timezone(INDIAN_TIMEZONE)
    
    # Calculate the date for today and tomorrow
    today_indian = datetime.now(indian_timezone).date()
    tomorrow_indian = today_indian + timedelta(days=1)

    # Check if there are any reminders for today and tomorrow in Indian time
    today_reminders = [r for r in reminders if datetime.strptime(r['date'], '%Y-%m-%d').date() == today_indian]
    tomorrow_reminders = [r for r in reminders if datetime.strptime(r['date'], '%Y-%m-%d').date() == tomorrow_indian]

    # Prepare the message with today's and tomorrow's reminders
    message = f"🌟 Hi Anandh!\n\n"

    if today_reminders:
        message += f"📅 Today's adventures:\n"
        message += '\n'.join([f"• {r['name']} - {r['date']}" for r in today_reminders])
        message += "\n\n"

    if tomorrow_reminders:
        message += f"🚀 Tomorrow's plans:\n"
        message += '\n'.join([f"• {r['name']} - {r['date']}" for r in tomorrow_reminders])

    if not today_reminders and not tomorrow_reminders:
        message = f"🌈 Hi {your_name}, smooth sailing today! No reminders for today and tomorrow."

    await send_telegram_message(message)


if __name__ == '__main__':
    # Set up the Telegram bot and chat
    # TODO: Replace this line with your actual code to set up the Telegram bot

    print("Checking reminders...")
    current_indian_time = get_current_indian_time()
    print(f"Current Indian Time: {current_indian_time}")

    # Schedule the job based on specified times
    schedule.every().day.at("09:47").do(send_activities)
    schedule.every().day.at("09:48").do(send_reminders)
    schedule.every().day.at("02:00").do(lambda: asyncio.run(send_daily_activities_reminder()))
    schedule.every().day.at("17:30").do(lambda: asyncio.run(send_daily_activities_reminder()))
    schedule.every().day.at("09:30").do(lambda: asyncio.run(send_daily_activities_reminder()))
    schedule.every().day.at("12:30").do(lambda: asyncio.run(send_daily_activities_reminder()))
    schedule.every().day.at("21:30").do(lambda: asyncio.run(send_daily_activities_reminder()))
    schedule.every().day.at("15:00").do(lambda: asyncio.run(send_daily_activities_reminder()))
    schedule.every().day.at("14:00").do(lambda: asyncio.run(send_daily_activities_reminder()))
    schedule.every().day.at("18:00").do(lambda: asyncio.run(send_daily_activities_reminder()))
    schedule.every().day.at("20:00").do(lambda: asyncio.run(send_daily_activities_reminder()))
    schedule.every().day.at("22:30").do(lambda: asyncio.run(send_daily_activities_reminder()))

    # Add other schedule times...

    while True:
        schedule.run_pending()
        time.sleep(1)
