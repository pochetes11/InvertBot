import discord
from discord.ext import commands
import time

# Define los intents que el bot necesita
intents = discord.Intents.default()
intents.messages = True

# Crear el bot usando commands.Bot para manejar comandos
bot = commands.Bot(command_prefix='!', description="InvertBot", intents=intents)

# Aquí iría tu lógica y comandos del bot...

@bot.event
async def on_ready():
    print(f'Bot iniciado como {bot.user.name}')

# Función principal para ejecutar el bot
def run_bot():
    while True:
        try:
            bot.run('MTI0NTg1NjQ5ODcyNzUxODI0OQ.GYbZ2A._C9eSow0XgiGyzrmoyyrG63ysstH8JULHxhNk4')
        except Exception as e:
            print(f"Error: {e}, reiniciando en 5 segundos...")
            time.sleep(5)  # Esperar 5 segundos antes de reiniciar

if __name__ == "__main__":
    run_bot()
