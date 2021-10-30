import logging

import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.utils import executor

import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

aid = 0


@dp.message_handler(content_types=ContentType.all())
async def on_message(message: aiogram.types.Message):
    global aid

    if message.from_user.id == 777000:
        markup = types.InlineKeyboardMarkup(row_width=2)
        join_btn = types.InlineKeyboardButton(config.button_text, callback_data='join_to_chat', url=config.button_link)

        markup.add(join_btn)

        try:
            maid = int(message.media_group_id)
        except TypeError:
            maid = -1

        if maid != aid:
            await message.reply(config.message_text, reply_markup=markup)

        try:
            aid = int(message.media_group_id)
        except TypeError:
            aid = 0


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
