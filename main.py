import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from aiogram.enums import ParseMode

BOT_TOKEN = '6969343979:AAHWyix4smbWl_kwje_m7PE_3k-tmtdBvPc'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Словарь для хранения идентификаторов последних отправленных сообщений ботом по чатам
previous_messages = {}

# Обработчик для удаления предыдущего сообщения бота
async def delete_previous_bot_message(chat_id):
    if chat_id in previous_messages and 'bot' in previous_messages[chat_id]:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=previous_messages[chat_id]['bot'])
        except Exception as e:
            logging.error(f"Ошибка при удалении предыдущего сообщения бота: {e}")

async def on_startup(dp):
    logging.warning('Bot has been started, press Ctrl+C to stop')
    print("Bot has been started")

# Обработчик команды /start
@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text='Завтрак')],
        [types.KeyboardButton(text='Обед')],
        [types.KeyboardButton(text='Ужин')],
        [types.KeyboardButton(text='Перекус')]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Выберите нужный раздел'
    )
    await message.answer(
        f'Здравствуй {message.from_user.full_name}\n\nДобро пожаловать в наш сборник рецептов 📝\nВыберите нужный вам раздел рецептов 👀',
        reply_markup=keyboard)


# Обработчики для разделов рецептов
@dp.message(F.text.lower() == 'завтрак')
async def r_breakfast(message: types.Message):
    await delete_previous_bot_message(message.chat.id)  # Удаление предыдущего сообщения бота
    sent_message = await message.answer("[Завтрак 🥞](https://telegra.ph/Testovyj-recept-02-19)", parse_mode=ParseMode.MARKDOWN_V2)
    previous_messages[message.chat.id] = {'bot': sent_message.message_id}  # Сохранение идентификатора текущего сообщения бота


@dp.message(F.text.lower() == 'обед')
async def r_lunch(message: types.Message):
    await delete_previous_bot_message(message.chat.id)
    sent_message = await message.answer("[Обед](https://telegra.ph/Stranica-s-receptami-na-obed-02-22)", parse_mode=ParseMode.MARKDOWN_V2)
    previous_messages[message.chat.id] = {'bot': sent_message.message_id}


@dp.message(F.text.lower() == 'ужин')
async def r_dinner(message: types.Message):
    await delete_previous_bot_message(message.chat.id)
    sent_message = await message.answer("[Ужин](https://telegra.ph/Uzhin-02-22)", parse_mode=ParseMode.MARKDOWN_V2)
    previous_messages[message.chat.id] = {'bot': sent_message.message_id}

@dp.message(F.text.lower() == 'перекус')
async def r_snack(message: types.Message):
    await delete_previous_bot_message(message.chat.id)
    sent_message = await message.answer("[Перекус](https://telegra.ph/Perekus-02-22)", parse_mode=ParseMode.MARKDOWN_V2)
    previous_messages[message.chat.id] = {'bot': sent_message.message_id}


# Обработчик команды /offer
@dp.message(Command('offer'))
async def cmd_offer(message: types.Message):
    await delete_previous_bot_message(message.chat.id)
    sent_message = await message.answer('Для предложения своего рецепта напишите *@Glymm*',
                                       parse_mode=ParseMode.MARKDOWN_V2)
    previous_messages[message.chat.id] = {'bot': sent_message.message_id}

# Основная функция
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

