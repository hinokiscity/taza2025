import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.token import TokenValidationError
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command


TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

if not TOKEN:
    raise TokenValidationError("❌ BOT_TOKEN topilmadi (Railway env)")

if not GROUP_ID:
    raise TokenValidationError("❌ GROUP_ID topilmadi (Railway env)")


bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher(storage=MemoryStorage())


class Form(StatesGroup):
    fio = State()
    phone = State()
    video = State()


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Salom! FIO kiriting:")
    await state.set_state(Form.fio)


@dp.message(Form.fio)
async def get_fio(message: types.Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await message.answer("Telefon raqamingizni kiriting:")
    await state.set_state(Form.phone)


@dp.message(Form.phone)
async def get_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Endi videoni yuboring:")
    await state.set_state(Form.video)


@dp.message(Form.video, F.video)
async def get_video(message: types.Message, state: FSMContext):
    data = await state.get_data()
    fio = data["fio"]
    phone = data["phone"]

    caption = (
        f"📌 <b>Yangi ishtirokchi!</b>\n"
        f"👤 F.I.O: {fio}\n"
        f"📞 Telefon: {phone}"
    )

    # Videoni guruhga yuborish
    await bot.send_video(
        chat_id=int(GROUP_ID),
        video=message.video.file_id,
        caption=caption
    )

    await message.answer("Video yuborildi! Rahmat!")
    await state.clear()


async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
