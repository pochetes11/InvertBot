import discord
from discord.ext import commands

# Define los intents que el bot necesita
intents = discord.Intents.all()

# Crear el bot usando commands.Bot para manejar comandos
bot = commands.Bot(command_prefix='!', description="InvertBot", intents=intents)

# Simulación de una base de datos de acciones con información de dividendos
acciones = {
    'AAPL': {'nombre': 'Apple Inc.', 'precio': 150, 'dividendo': 0.62, 'yield': 0.69},
    'MSFT': {'nombre': 'Microsoft Corporation', 'precio': 300, 'dividendo': 2.24, 'yield': 0.86},
    'JNJ': {'nombre': 'Johnson & Johnson', 'precio': 170, 'dividendo': 1.06, 'yield': 2.63},
    'PG': {'nombre': 'Procter & Gamble Co.', 'precio': 120, 'dividendo': 0.87, 'yield': 2.53},
    'KO': {'nombre': 'The Coca-Cola Company', 'precio': 50, 'dividendo': 1.68, 'yield': 3.27}
}

# Máximo de inversión permitido
MAX_INVERSION = 1000

# Comando para buscar acciones por criterios de dividendos
@bot.command()
async def buscar(ctx, criterio: str):
    criterio = float(criterio)
    resultados = [accion for accion, info in acciones.items() if info['yield'] > criterio]
    
    if resultados:
        await ctx.send(f"Acciones con yield > {criterio}%: {', '.join(resultados)}")
    else:
        await ctx.send(f"No se encontraron acciones con yield > {criterio}%")

# Comando para obtener información detallada de una acción específica
@bot.command()
async def info(ctx, accion: str):
    if accion.upper() in acciones:
        info_accion = acciones[accion.upper()]
        mensaje = f"Información de {info_accion['nombre']}:\n"
        mensaje += f"Precio: ${info_accion['precio']} por acción\n"
        mensaje += f"Dividendo: ${info_accion['dividendo']} por acción\n"
        mensaje += f"Yield: {info_accion['yield']}%"
        await ctx.send(mensaje)
    else:
        await ctx.send(f"No se encontró información para la acción {accion}")

# Comando para configurar notificaciones de dividendos
@bot.command()
async def notificar(ctx):
    # Implementa la lógica para configurar notificaciones de dividendos
    await ctx.send("Notificaciones de dividendos configuradas")

# Comando para invertir en una acción
@bot.command()
async def invertir(ctx, accion: str, cantidad: int):
    if accion.upper() in acciones:
        precio_accion = acciones[accion.upper()]['precio']
        total_inversion = precio_accion * cantidad
        
        # Preguntar al usuario cuánto dinero tiene disponible para invertir
        await ctx.send(f"¿Cuánto dinero tienes disponible para invertir? (Máximo ${MAX_INVERSION})")
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()
        
        try:
            mensaje = await bot.wait_for('message', check=check, timeout=30)
            dinero_disponible = int(mensaje.content)
            
            if dinero_disponible > MAX_INVERSION:
                await ctx.send(f"No puedes invertir más de ${MAX_INVERSION}.")
            elif dinero_disponible < total_inversion:
                await ctx.send(f"No tienes suficiente dinero para invertir ${total_inversion}.")
            else:
                mensaje = f"Invertiste en {cantidad} acciones de {acciones[accion.upper()]['nombre']}.\n"
                mensaje += f"Costo total de la inversión: ${total_inversion}"
                await ctx.send(mensaje)
        except asyncio.TimeoutError:
            await ctx.send("Tiempo de espera agotado. Intenta de nuevo más tarde.")
    else:
        await ctx.send(f"No se encontró información para la acción {accion}")

# Evento al iniciar el bot usando discord.Client
@bot.event
async def on_ready():
    print(f'Bot iniciado como {bot.user.name}')

# Manejo de mensajes usando discord.Client
@bot.event
async def on_message(message):
    print("message-->", message.content)  # Imprimir el contenido del mensaje recibido

    if message.author == bot.user:
        return

    if message.content.startswith('hola'):
        await message.channel.send('Hola!')

    # Puedes seguir agregando más lógica de manejo de mensajes aquí

    await bot.process_commands(message)  # Importante para que los comandos funcionen correctamente
# Token de tu bot - recuerda mantenerlo seguro y no compartirlo públicamente
bot.run('MTI0NTg1NjQ5ODcyNzUxODI0OQ.GYbZ2A._C9eSow0XgiGyzrmoyyrG63ysstH8JULHxhNk4')