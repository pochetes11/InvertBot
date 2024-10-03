import discord
from discord.ext import commands

# Define los intents que el bot necesita
intents = discord.Intents.default()
intents.messages = True

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
    'Agresivo': {
        'tolerancia_riesgo': 'Alta',
        'objetivo': 'Crecimiento agresivo del capital',
        'horizonte': 'Largo plazo',
        'estrategia': 'Acciones de crecimiento, criptomonedas, inversiones en startups'
    }
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

        # Check for valid responses
        def check(m):
            return m.author == ctx.author and m.content.upper() in [opcion[0] for opcion in opciones]

        # Espera hasta que el usuario responda
        mensaje = await bot.wait_for('message', check=check)
        respuestas[pregunta] = mensaje.content.upper()
        await ctx.send(f"Respuesta registrada: {mensaje.content.upper()}")

    # Determinar el perfil basado en las respuestas
    perfil_sugerido = determinar_perfil(respuestas)
    await ctx.send(f"Tu perfil de inversor sugerido es: {perfil_sugerido}")
    await ctx.send(f"Estrategia recomendada: {perfiles[perfil_sugerido]['estrategia']}")

def determinar_perfil(respuestas):
    puntaje = 0

    # Evaluar respuestas para determinar puntaje
    puntaje += evaluar_tolerancia_riesgo(respuestas)
    puntaje += evaluar_horizonte_inversion(respuestas)
    # Añadir más evaluaciones de preguntas...

    # Determinar perfil basado en puntajes
    if puntaje < 0:
        return 'Conservador'
    elif puntaje < 2:
        return 'Moderado'
    else:
        return 'Agresivo'

def evaluar_tolerancia_riesgo(respuestas):
    """Evalúa la tolerancia al riesgo del inversor y ajusta el puntaje."""
    if respuestas.get("¿Cómo describiría su tolerancia al riesgo?", "").upper() == 'A':
        return -2
    elif respuestas.get("¿Cómo describiría su tolerancia al riesgo?", "").upper() == 'B':
        return -1
    elif respuestas.get("¿Cómo describiría su tolerancia al riesgo?", "").upper() == 'C':
        return 1
    return 0  # Valor predeterminado si no se encuentra respuesta

def evaluar_horizonte_inversion(respuestas):
    """Evalúa el horizonte de inversión del inversor y ajusta el puntaje."""
    if respuestas.get("¿Cuál es el horizonte temporal para sus inversiones?", "").upper() == 'D':
        return 2
    elif respuestas.get("¿Cuál es el horizonte temporal para sus inversiones?", "").upper() == 'C':
        return 1
    return 0  # Valor predeterminado si no se encuentra respuesta

# Evento al iniciar el bot
@bot.event
async def on_ready():
    print(f'Bot iniciado como {bot.user.name}')

# Token de tu bot - recuerda mantenerlo seguro y no compartirlo públicamente
bot.run('MTI0NTg1NjQ5ODcyNzUxODI0OQ.GYbZ2A._C9eSow0XgiGyzrmoyyrG63ysstH8JULHxhNk4')  # Cambia esto por tu token real

