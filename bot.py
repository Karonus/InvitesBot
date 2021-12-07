import logging

import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.utils import executor
import requests

import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

aid = 0


@dp.message_handler(content_types=ContentType.all())
async def on_message(message: aiogram.types.Message):
    global aid

    if message.from_user.id == 777000 and message.forward_date:
        markup = types.InlineKeyboardMarkup(row_width=2)
        join_btn = types.InlineKeyboardButton(config.button_text, url=config.button_link)

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

    if message.from_user.id == 777000 and not message.forward_date and config.autoban_user_channels:
        await message.delete()

        params = {
            'chat_id': str(message.chat.id),
            'sender_chat_id': str(message.sender_chat.id)
        }

        requests.get(f"https://api.telegram.org/bot{config.TOKEN}/banChatSenderChat", params=params)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
