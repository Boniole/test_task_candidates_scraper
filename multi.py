import asyncio
import os
import sys
from multiprocessing import Process

import uvicorn

from app.telegram_bot import start_telegram_bot

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
host = os.getenv("HOST")
port = int(os.getenv("PORT"))


def run_telegram_bot():
    """
    Wrapper to run the asynchronous Telegram bot in a separate process.
    """
    asyncio.run(start_telegram_bot())


if __name__ == '__main__':
    # Start FastAPI-app by multiprocessing
    proc_scrapper = Process(target=uvicorn.run,
                            kwargs={"app": "app.main:app", "host": host, "port": port})

    proc_telegram_bot = Process(target=run_telegram_bot)

    proc_scrapper.start()
    proc_telegram_bot.start()

    proc_scrapper.join()
    proc_telegram_bot.join()
