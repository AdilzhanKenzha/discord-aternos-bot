import discord
from discord.ext import tasks
from mcstatus import JavaServer
import asyncio

# --- НАСТРОЙКИ ---
TOKEN = 'MTUwMDI1MDMxMzk2MDE5NDE4MA.GqnX9A.WkB8AmblQA_a7-7blW1aX9d_u0FmOETaHArmnU' 
IP = 'smpfarsh.aternos.me'

class MyBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)

    async def setup_hook(self):
        self.check_server.start()

    async def on_ready(self):
        print(f'--- Бот {self.user} запущен! Всегда онлайн (зеленый) ---')

    @tasks.loop(seconds=30)
    async def check_server(self):
        if not self.is_ready():
            return

        # Теперь статус всегда "online" (зеленый кружок)
        presence = discord.Status.online
        status_text = "Сервер Оффлайн 🔴"

        try:
            server = await JavaServer.async_lookup(IP)
            status = await server.async_status()
            
            description = str(status.description).lower()
            
            offline_markers = ["this server is offline", "offline", "оффлайн", "get this server more ram"]
            is_offline_message = any(marker in description for marker in offline_markers)

            if not is_offline_message and (status.players.online > 0 or status.latency < 180):
                status_text = f"Online: {status.players.online} 🟢"
            else:
                status_text = "Сервер Оффлайн 🔴"
            
            print(f"DEBUG | Игроков: {status.players.online} | Статус: {status_text}")

        except Exception as e:
            status_text = "Сервер Оффлайн 🔴"
            if "WinError 64" not in str(e):
                print(f"DEBUG | Статус: Оффлайн (Сетевая ошибка)")

        # Принудительно ставим зеленый кружок при каждом обновлении
        try:
            await self.change_presence(status=presence, activity=discord.Game(name=status_text))
        except Exception as e:
            print(f"Ошибка статуса: {e}")

bot = MyBot()
bot.run(TOKEN)