from dotenv import load_dotenv 
from discord.ext import commands  # Для слеш команд
from discord import app_commands
import discord                    # Основная библиотека дискорда
import os
import httpx

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

    # Слеш-команда /registration
    @app_commands.command(name = 'registration', description = 'Привязать osu! профиль')
    @app_commands.describe(link = "Ссылка на ваш профиль")
    async def registration_slash(self, interaction: discord.Interaction, link: str):
        payload = {
        "discord_id": str(interaction.user.id),
        "discord_name": interaction.user.name,
        "profile_link": link
        }

        api_url = "http://localhost:8000/api/users/register"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(api_url, json=payload, timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    await interaction.response.send_message(
                        f"Ты успешно зарегистрирован! Твой ID: {data['user_id']}"
                    )
                elif response.status_code == 400:
                    detail = response.json().get("detail", "Ошибка регистрации")
                    await interaction.response.send_message(f"❌ {detail}", ephemeral=True)
                else:
                    await interaction.response.send_message(
                        "Сервер временно недоступен. Попробуй позже.", ephemeral=True
                    )
            except httpx.RequestError:
                await interaction.response.send_message(
                    "Бэкенд не отвечает. Попробуйте позже.", ephemeral=True
                )

async def setup(bot: commands.Bot):
    await bot.add_cog(SlashCommands(bot))
