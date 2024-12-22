import asyncio
import os

from aiogram import Bot, Dispatcher
from apscheduler.triggers.interval import IntervalTrigger
from dotenv import load_dotenv

from db.sql.connect import init_db
from routers import start_router, join_router, way_router, forward_router, wfp_data_remove_router, support_router
from routers.dismiss_routers import dismiss_router
from routers.lang_routers import lang_router
from tasks.scheduler import scheduler
from tasks.tasks import DistributedTask

load_dotenv()
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()
routers = [
    start_router.router,
    join_router.router,
    dismiss_router.router,
    way_router.router,
    forward_router.router,
    wfp_data_remove_router.router,
    support_router.router,
    lang_router.router,
]
tasks = [
    {"executor": DistributedTask, "args": [bot]},
]


@dp.startup()
async def startup():
    print("Starting up bot!")


async def main():
    for task in tasks:
        scheduler.add_job(task["executor"](*task['args']).task, IntervalTrigger(minutes=1))
    scheduler.start()
    await init_db()
    dp.include_routers(*routers)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Interrupted")
