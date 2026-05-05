from dotenv import load_dotenv # Для файла .env
import discord                 # Основная библиотека дискорда
import logging                 # Библиотека для логов
import traceback
import os

class MyBot(discord.Client):
    def __init__(self, *, intents, log_handler=None, log_level=None):
        super().__init__(intents=intents)
        self.log_handler = log_handler
        self.log_level = log_level
        with open('bot.log', 'a', encoding='utf-8') as f:
            f.write("\n" + "="*60 + "\n")
            f.write("БОТ ЗАПУЩЕН\n")
            f.write("="*60 + "\n")
        print("Бот запущен")

    async def on_ready(self):
        print(f'Бот {client.user} запущен')

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

if __name__ == '__main__':
    intents = discord.Intents.default()      # Набор стандартных намерений
    intents.message_content = True           # Намерение читать содержимое сообщений
    client = discord.Client(intents=intents) # Передаёт дискорду настроенные намерения

    # Настройка логов в файл. Создаёт файл bot.log с логами
    handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='a')

    bot = MyBot(intents=intents)

    # Пробуем запустить
    # Eсли запустить не получится, то в файл bot.log будет написана строка, на которой ошибка
    try:
        load_dotenv()   # загружает переменные из .env
        token = os.getenv('BOT_TOKEN')
        bot.run(token, log_handler=handler, log_level=logging.DEBUG)
    except Exception:
        with open('bot.log', 'a', encoding='utf-8') as f:
            f.write("\n" + "="*60 + "\n")
            f.write("БОТ УПАЛ:\n")
            f.write(traceback.format_exc())
            f.write("="*60 + "\n")
        print("Критическая ошибка. Смотрите bot.log")
        raise   # чтобы увидеть ошибку в терминале
