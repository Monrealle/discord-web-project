from dotenv import load_dotenv 
from discord.ext import commands  # Для слеш команд
from discord import app_commands
import discord                    # Основная библиотека дискорда
import os

class SlashCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.author_name = os.getenv('AUTHOR_NAME', 'Monreale')
        self.author_id = int(os.getenv('AUTHOR_ID', 483920151494787072))
    
    # ---------- ПРЕФИКСНЫЕ КОМАНДЫ ----------

    # Префиксная команда hello
    @commands.command(name = 'hello')
    async def hello_prefix(self, ctx):
        await ctx.send(f'Привет, {ctx.author.name}!')

    # ---------- СЛЭШ-КОМАНДЫ ----------

    # Слеш-команда /hello
    @app_commands.command(name = 'hello', description = 'Бот поздоровается')
    async def hello_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Привет, {interaction.user.name}!')

    # Слеш-команда /info
    @app_commands.command(name = 'info', description = 'Информация о боте')
    async def info_slash(self, interaction: discord.Interaction):
        embed = discord.Embed(title = 'Мой бот', description='Сделан на Python')
        embed.add_field(name = 'Автор', value = self.author_name)
        await interaction.response.send_message(embed = embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(SlashCommands(bot))
