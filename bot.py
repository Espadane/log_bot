import aioschedule
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from config import ADMIN_ID
from config import TOKEN
from config import CHECK_MINUTES
from file_parser import parse_log_files


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(msg: types.Message):
    await msg.answer('Ну если ты запустил этого бота, то ты и \
                    так знаешь что делать.\nА если нет, то удали, все равно\
                    ничего не сделаешь.')
    
async def send_logs() -> None:
    user = int(ADMIN_ID)
    logs = parse_log_files()
    for log in logs:
        await bot.send_message(user, log)
    
@dp.message_handler(Text)
async def answer(msg: types.message) -> None:
    await msg.answer('Тебе тут не рады, уходи!')
    
async def scheduler() -> None:
    aioschedule.every(CHECK_MINUTES).minutes.do(send_logs)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
        
async def on_startup(_) -> None:
    asyncio.create_task(scheduler())
    
if __name__=='__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)