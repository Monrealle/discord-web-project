from dotenv import load_dotenv    # Для файла .env
from discord.ext import commands  # Для слеш команд
import discord                    # Основная библиотека дискорда
import logging                    # Библиотека для логов
import traceback                  # Библиотека для вывода ошибок
import os

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()        # Набор стандартных намерений
        intents.message_content = True             # Намерение читать содержимое сообщений

        super().__init__(command_prefix='!', intents = intents)
        self.author_name = os.getenv('AUTHOR_NAME', 'Monreale')
        self.author_id = int(os.getenv('AUTHOR_ID', 483920151494787072))

        with open('bot.log', 'a', encoding = 'utf-8') as f:
            f.write("\n" + "="*60 + "\n")
            f.write("БОТ ЗАПУЩЕН\n")
            f.write("="*60 + "\n")

    async def setup_hook(self):
        await self.load_extension('commands') # Загружаем расширение из файла commands.py
        await self.tree.sync()                # Синхронизация команд с Discord
        print(f'Синхронизировано {len(self.tree.get_commands())} слеш-команд')

    async def on_ready(self):
        print(f'Бот {self.user.name} запущен. (ID: {self.user.id})')
        print(f'Автор бота: {self.author_name}. (ID: {self.author_id}) \n')

if __name__ == '__main__':
    load_dotenv()   # загружает переменные из .env
    token = os.getenv('BOT_TOKEN')

    bot = MyBot()

    # Логирование
    handler = logging.FileHandler(filename = 'bot.log', encoding = 'utf-8', mode = 'a')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

    # Пробуем запустить. Настройки бота на https://discord.com/developers/applications
    # Eсли запустить не получится, то в файл bot.log будет написана строка, на которой ошибка
    try:
        bot.run(token, log_handler = handler, log_level = logging.DEBUG)
    except Exception:
        with open('bot.log', 'a', encoding = 'utf-8') as f:
            f.write("\n" + "="*60 + "\n")
            f.write("БОТ УПАЛ:\n")
            f.write(traceback.format_exc())
            f.write("="*60 + "\n")
        print("Критическая ошибка. Смотрите bot.log")
        raise   # чтобы увидеть ошибку в терминале
