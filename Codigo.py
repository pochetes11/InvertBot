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


import discord
from discord.ext import commands
import asyncio

# Define los intents que el bot necesita
intents = discord.Intents.all()

# Crear el bot usando commands.Bot para manejar comandos
bot = commands.Bot(command_prefix='!', description="InvertBot", intents=intents)

# Posibles perfiles de inversión
perfiles = {
    'Conservador': {
        'tolerancia_riesgo': 'Baja',
        'objetivo': 'Preservación del capital, ingresos estables',
        'horizonte': 'Corto a medio plazo',
        'estrategia': 'Bonos gubernamentales, depósitos a plazo fijo'
    },
    'Moderado': {
        'tolerancia_riesgo': 'Moderada',
        'objetivo': 'Crecimiento moderado del capital con ingresos adicionales',
        'horizonte': 'Medio a largo plazo',
        'estrategia': 'Bonos, acciones de dividendos, fondos de inversión'
    },
    # Añadir más perfiles según corresponda...
}

# Comando para determinar el perfil del inversor
@bot.command()
async def perfil(ctx):
    respuestas = {}

    # Preguntas para sacar el perfil del inversor con opciones múltiples
    preguntas = [
        ("¿Cuál es su principal objetivo de inversión?",
         ["A) Crecimiento de capital", "B) Generación de ingresos regulares", "C) Preservación del capital", "D) Diversificación del patrimonio"]),
        
        ("¿Cuál es el horizonte temporal para sus inversiones?",
         ["A) Menos de 1 año", "B) 1-3 años", "C) 3-5 años", "D) Más de 5 años"]),
        
        ("¿Cuánto tiempo está dispuesto a mantener sus inversiones sin necesidad de acceder a los fondos?",
         ["A) Menos de 6 meses", "B) 6-12 meses", "C) 1-3 años", "D) Más de 3 años"]),
        
        ("¿Cuál es su nivel de experiencia con inversiones?",
         ["A) Principiante", "B) Intermedio", "C) Avanzado"]),
        
        ("¿Cuánto capital está dispuesto a invertir inicialmente?",
         ["A) Menos de $1,000", "B) $1,000 - $10,000", "C) $10,000 - $50,000", "D) Más de $50,000"]),
        
        ("¿Cuál es su ingreso anual aproximado?",
         ["A) Menos de $20,000", "B) $20,000 - $50,000", "C) $50,000 - $100,000", "D) Más de $100,000"]),
        
        ("¿Cuál es su nivel de deuda actual y cómo maneja sus obligaciones financieras?",
         ["A) Alta deuda, dificultades para manejarla", "B) Deuda moderada, manejable", "C) Baja deuda, buen manejo", "D) Sin deuda"]),
        
        ("¿Qué porcentaje de sus ingresos está dispuesto a invertir?",
         ["A) Menos del 5%", "B) 5-10%", "C) 10-20%", "D) Más del 20%"]),
        
        ("¿Cómo describiría su tolerancia al riesgo?",
         ["A) Baja", "B) Moderada", "C) Alta"]),
        
        ("¿Cuáles son sus inversiones actuales?",
         ["A) Acciones", "B) Bonos", "C) Bienes raíces", "D) Fondos mutuos", "E) Otros"]),
        
        ("¿Está buscando inversiones que generen ingresos regulares o crecimiento del capital a largo plazo?",
         ["A) Ingresos regulares", "B) Crecimiento del capital", "C) Ambos"]),
        
        ("¿Cómo reaccionaría si su inversión principal pierde un 10% de su valor en un corto período de tiempo?",
         ["A) Vendería todo", "B) Vendería parte", "C) Mantendría la inversión", "D) Invertiría más"]),
        
        ("¿Qué tipo de productos financieros prefiere o ha utilizado anteriormente?",
         ["A) Fondos de inversión", "B) Acciones", "C) Bonos", "D) Criptomonedas", "E) Otros"]),
        
        ("¿Tiene alguna preferencia en cuanto a sectores o industrias en los que invertir?",
         ["A) Tecnología", "B) Salud", "C) Energía", "D) Bienes de consumo", "E) No tengo preferencia"]),
        
        ("¿Está dispuesto a invertir en mercados internacionales o prefiere limitarse a mercados nacionales?",
         ["A) Solo nacionales", "B) Solo internacionales", "C) Ambos, sin preferencia"]),
        
        ("¿Cuánto conocimiento tiene sobre las tendencias y movimientos del mercado financiero?",
         ["A) Ninguno", "B) Básico", "C) Intermedio", "D) Avanzado"]),
        
        ("¿Cuál es su nivel de comodidad con la volatilidad del mercado?",
         ["A) Muy incómodo", "B) Incómodo", "C) Cómodo", "D) Muy cómodo"]),
        
        ("¿Qué importancia le da a la sostenibilidad y a las inversiones socialmente responsables?",
         ["A) Muy importante", "B) Importante", "C) Poco importante", "D) No importa"]),
        
        ("¿Tiene alguna preocupación específica respecto a sus inversiones?",
         ["A) Seguridad del capital", "B) Impacto fiscal", "C) Liquidez", "D) Ninguna preocupación específica"]),
        
        ("¿Cuál es su expectativa de rendimiento anual para sus inversiones?",
         ["A) Menos del 5%", "B) 5-10%", "C) 10-20%", "D) Más del 20%"]),
    ]

    for pregunta, opciones in preguntas:
        opciones_formato = "\n".join(opciones)
        await ctx.send(f"{pregunta}\n{opciones_formato}")

        def check(m):
            return m.author == ctx.author and m.content.upper() in [opcion[0] for opcion in opciones]

        try:
            mensaje = await bot.wait_for('message', check=check, timeout=60.0)
            respuestas[pregunta] = mensaje.content.upper()
            await ctx.send(f"Respuesta registrada: {mensaje.content.upper()}")
        except asyncio.TimeoutError:
            await ctx.send("Se agotó el tiempo para responder. Por favor, intenta nuevamente.")
            return

    # Determinar el perfil basado en las respuestas
    perfil_sugerido = determinar_perfil(respuestas)  # Función para determinar el perfil basado en respuestas
    await ctx.send(f"Tu perfil de inversor sugerido es: {perfil_sugerido}")
    await ctx.send(f"Estrategia recomendada: {perfiles[perfil_sugerido]['estrategia']}")

def determinar_perfil(respuestas):
    # Lógica simplificada para determinar el perfil basado en las respuestas
    # Ejemplo básico: perfil conservador si la tolerancia al riesgo es baja
    if respuestas.get("¿Cómo describiría su tolerancia al riesgo?", "").upper() == 'A':
        return 'Conservador'
    # Añadir más lógica para determinar otros perfiles
    return 'Moderado'  # Perfil por defecto si no se cumple ninguna condición específica

# Evento al iniciar el bot
@bot.event
async def on_ready():
    print(f'Bot iniciado como {bot.user.name}')

# Token de tu bot - recuerda mantenerlo seguro y no compartirlo públicamente
bot.run('MTI0NTg1NjQ5ODcyNzUxODI0OQ.GYbZ2A._C9eSow0XgiGyzrmoyyrG63ysstH8JULHxhNk4')