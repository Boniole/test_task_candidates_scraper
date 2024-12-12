import os

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from app.services import fetch_resumes_with_evaluation

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


# Command to start the bot
@dp.message(F.text == "/start")
async def start_command(message: Message):
    await message.answer("Hello! Send me a job title, and I'll fetch resumes for you.")


# Command to fetch resumes
@dp.message()
async def fetch_resumes(message: Message):
    position = message.text.strip()
    await message.reply(f"🔍 <b>Fetching resumes for:</b> {position}", parse_mode="HTML")

    try:
        # Call the existing FastAPI service
        resumes = await fetch_resumes_with_evaluation(position)

        if resumes:
            for resume in resumes[:5]:  # Limit to 5 resumes for readability
                # Формуємо основну інформацію
                resume_text = (
                    f"📄 <b>Title:</b> {resume.title}\n"
                    f"👤 <b>Name:</b> {resume.name}\n"
                    f"🎂 <b>Age:</b> {resume.age if resume.age else 'Not specified'}\n"
                    f"📍 <b>Location:</b> {resume.location if resume.location else 'Not specified'}\n"
                    f"🔗 <b>Link:</b> <a href='{resume.link}'>View Resume</a>\n"
                    f"🎓 <b>Education:</b> {resume.education if resume.education else 'Not specified'}\n"
                    f"📅 <b>Last Update:</b> {resume.last_update if resume.last_update else 'Not specified'}\n"
                    f"⭐ <b>Average Score:</b> <b>{resume.average_score if resume.average_score else 'N/A'}</b>\n"
                )

                # Формуємо таблицю оцінок Evaluation
                if resume.evaluation:
                    evaluation = resume.evaluation
                    evaluation_text = (
                        "<b>📊 Evaluation Scores:</b>\n"
                        f"  - Hard Skills: <b>{evaluation.hard_skills}</b>\n"
                        f"  - Soft Skills: <b>{evaluation.soft_skills}</b>\n"
                        f"  - Education: <b>{evaluation.education}</b>\n"
                        f"  - Languages: <b>{evaluation.languages}</b>\n"
                        f"  - Work Experience: <b>{evaluation.work_experience}</b>\n"
                        f"  - Projects & Certificates: <b>{evaluation.projects_and_certificates}</b>\n"
                        f"  - Overall Structure: <b>{evaluation.overall_structure}</b>\n"
                    )
                else:
                    evaluation_text = "<b>📊 Evaluation Scores:</b> Not available\n"

                # Формуємо рекомендації
                recommendations_text = (
                    "<b>💡 Recommendations:</b>\n" +
                    "\n".join([f"  - {rec}" for rec in resume.evaluation.recommendations]) if resume.evaluation and resume.evaluation.recommendations else "Not available"
                )

                # Повідомлення
                full_text = f"{resume_text}\n{evaluation_text}\n{recommendations_text}"
                await message.reply(full_text, parse_mode="HTML", disable_web_page_preview=True)
        else:
            await message.reply("⚠️ <b>No resumes found for the given position.</b>", parse_mode="HTML")
    except Exception as e:
        await message.reply(f"❌ <b>An error occurred:</b> {str(e)}", parse_mode="HTML")


# Run the bot
async def start_telegram_bot():
    await dp.start_polling(bot)
