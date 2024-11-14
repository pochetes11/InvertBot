import discord
from discord.ext import commands
import random
from datetime import datetime
import json
import sqlite3

# Conectar a la base de datos usando 'with' para asegurar el cierre automático
with sqlite3.connect('./tablas.sql') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    results = cursor.fetchall()
    print(results)

def guardar_respuestas_en_bd(usuario_id, respuestas):
    # Conectar a la base de datos usando 'with' para asegurar el cierre automático
    with sqlite3.connect('tablas.sql') as conn:
        cursor = conn.cursor()

        # Insertar las respuestas del perfil en la tabla 'respuestas_perfil'
    cursor.execute("""
            INSERT OR REPLACE INTO respuestas_perfil (
                usuario_id, objetivo_inversion, horizonte_temporal, tiempo_mantener,
                nivel_experiencia, capital_inicial, ingreso_anual, nivel_deuda,
                porcentaje_ingresos_invertir, tolerancia_riesgo, inversiones_activas,
                ingresos_o_crecimiento, reaccion_perdida, productos_financieros,
                preferencias_sector, mercados_nacionales_o_internacionales, conocimiento_mercado,
                volatilidad_mercado, sostenibilidad, preocupaciones_inversiones, expectativa_rendimiento
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            usuario_id, respuestas.get("¿Cuál es su principal objetivo de inversión?", ""),
            respuestas.get("¿Cuál es su horizonte temporal para sus inversiones?", ""),
            respuestas.get("¿Cuánto tiempo está dispuesto a mantener sus inversiones sin necesidad de acceder a los fondos?", ""),
            respuestas.get("¿Cuál es su nivel de experiencia con inversiones?", ""),
            respuestas.get("¿Cuánto capital está dispuesto a invertir inicialmente?", ""),
            respuestas.get("¿Cuál es su ingreso anual aproximado?", ""),
            respuestas.get("¿Cuál es su nivel de deuda actual y cómo maneja sus obligaciones financieras?", ""),
            respuestas.get("¿Qué porcentaje de sus ingresos está dispuesto a invertir?", ""),
            respuestas.get("¿Cómo describiría su tolerancia al riesgo?", ""),
            respuestas.get("¿Cuáles son sus inversiones actuales?", ""),
            respuestas.get("¿Está buscando inversiones que generen ingresos regulares o crecimiento del capital a largo plazo?", ""),
            respuestas.get("¿Cómo reaccionaría si su inversión principal pierde un 10% de su valor en un corto período de tiempo?", ""),
            respuestas.get("¿Qué tipo de productos financieros prefiere o ha utilizado anteriormente?", ""),
            respuestas.get("¿Tiene alguna preferencia en cuanto a sectores o industrias en los que invertir?", ""),
            respuestas.get("¿Está dispuesto a invertir en mercados internacionales o prefiere limitarse a mercados nacionales?", ""),
            respuestas.get("¿Cuánto conocimiento tiene sobre las tendencias y movimientos del mercado financiero?", ""),
            respuestas.get("¿Cuál es su nivel de comodidad con la volatilidad del mercado?", ""),
            respuestas.get("¿Qué importancia le da a la sostenibilidad y a las inversiones socialmente responsables?", ""),
            respuestas.get("¿Tiene alguna preocupación específica respecto a sus inversiones?", ""),
            respuestas.get("¿Cuál es su expectativa de rendimiento anual para sus inversiones?", "")
        ))

conn.commit()

# Cargar las opciones de inversión desde el archivo JSON
with open('opciones.json', 'r') as f:
    opciones_json = json.load(f)

# Función para obtener opciones de inversión basadas en el perfil
def obtener_opciones_por_perfil(perfil):
    opciones_filtradas = [opcion for opcion in opciones_json['opciones_inversion'] if opcion['perfil'] == perfil]
    return opciones_filtradas

# Define los intents que el bot necesita
intents = discord.Intents.default()
intents.messages = True

# Crear el bot usando commands.Bot para manejar comandos
bot = commands.Bot(command_prefix='!', description="InvertBot", intents=intents)

# Conjunto de opciones de inversión predefinidas
opciones_predefinidas = [
    "Bonos de empresa A",
    "Bonos de empresa B",
    "Acciones de empresa C",
    "Acciones de empresa D",
    "Ethereum (ETH)",
    "Bitcoin (BTC)",
    "Litecoin (LTC)",
    "Fondos de inversión en bienes raíces",
    "Acciones de tecnología",
    "Acciones de energía renovable",
    "Criptomonedas emergentes",
    "Bonos del gobierno",
    "Fondos de inversión diversificados",
    "Acciones de salud",
    "Acciones de consumo",
    "Acciones de energía solar",
    "Acciones de telecomunicaciones",
    "Fondos cotizados (ETFs) de criptomonedas",
    "Bonos de alto rendimiento",
    "Criptomonedas de bajo capital",
    "Acciones de aerolíneas",
    "Bonos de infraestructura",
    "Acciones de viajes y turismo",
    "Acciones de servicios financieros",
    "Bonos municipales",
    "Inversiones en startups",
    "Acciones de comercio electrónico",
    "Bonos de empresas tecnológicas",
    "Criptomonedas estables",
    "Fondos de inversión en tecnología",
    "Acciones de servicios públicos",
]

# Opciones de inversión iniciales
listado_de_opciones = []

# Función para actualizar automáticamente las opciones de inversión
def actualizar_opciones():
    global listado_de_opciones
    random.seed(datetime.now().timestamp())
    listado_de_opciones = random.sample(opciones_predefinidas, 10)

# Comando para listar las opciones de inversión
@bot.command()
async def listado_de_opciones(ctx):
    if not listado_de_opciones:
        await ctx.send("Las opciones de inversión aún no han sido establecidas. Usa `!cambiar_opciones` para establecerlas.")
        return
    opciones_str = "\n".join(listado_de_opciones)
    await ctx.send(f"Opciones de inversión disponibles:\n{opciones_str}")

# Comando para cambiar las opciones de inversión automáticamente
@bot.command()
async def cambiar_opciones(ctx):
    actualizar_opciones()
    await ctx.send("Las opciones de inversión han sido actualizadas automáticamente. Usa `!listado_de_opciones` para ver las nuevas opciones.")

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
    await ctx.send(f"Estrategia recomendada: {perfil[perfil_sugerido]['estrategia']}")

    # Mostrar opciones de inversión recomendadas basadas en el perfil
    opciones_recomendadas = obtener_opciones_por_perfil(perfil_sugerido)
    opciones_str = "\n".join([f"{opcion['nombre']} - {opcion['tipo_inversion']}" for opcion in opciones_recomendadas])
    await ctx.send(f"Opciones de inversión recomendadas:\n{opciones_str}")

def evaluar_capital_inicial(respuestas):
    """Evalúa el capital inicial que el inversor está dispuesto a invertir."""
    if respuestas.get("¿Cuánto capital está dispuesto a invertir inicialmente?", "").upper() == 'A':
        return -2  # Menos de $1,000, perfil conservador
    elif respuestas.get("¿Cuánto capital está dispuesto a invertir inicialmente?", "").upper() == 'B':
        return 0   # $1,000 - $10,000, perfil moderado
    elif respuestas.get("¿Cuánto capital está dispuesto a invertir inicialmente?", "").upper() == 'C':
        return 2   # $10,000 - $50,000, perfil moderado
    elif respuestas.get("¿Cuánto capital está dispuesto a invertir inicialmente?", "").upper() == 'D':
        return 4   # Más de $50,000, perfil agresivo
    return 0


def evaluar_experiencia_inversion(respuestas):
    """Evalúa el nivel de experiencia del inversor."""
    if respuestas.get("¿Cuál es su nivel de experiencia con inversiones?", "").upper() == 'A':
        return -2  # Principiante, perfil conservador
    elif respuestas.get("¿Cuál es su nivel de experiencia con inversiones?", "").upper() == 'B':
        return 0   # Intermedio, perfil moderado
    elif respuestas.get("¿Cuál es su nivel de experiencia con inversiones?", "").upper() == 'C':
        return 2   # Avanzado, perfil agresivo
    return 0

def determinar_perfil(respuestas):
    puntaje = 0
    puntaje += evaluar_tolerancia_riesgo(respuestas)
    puntaje += evaluar_horizonte_inversion(respuestas)
    puntaje += evaluar_capital_inicial(respuestas)
    puntaje += evaluar_experiencia_inversion(respuestas)
    # Agregar más evaluaciones si es necesario...

    if puntaje < 0:
        return 'Conservador'
    elif puntaje < 5:
        return 'Moderado'
    else:
        return 'Agresivo'

def evaluar_tolerancia_riesgo(respuestas):
    """Evalúa la tolerancia al riesgo del inversor y ajusta el puntaje."""
    if respuestas.get("¿Cómo describiría su tolerancia al riesgo?", "").upper() == 'A':
        return -2
    elif respuestas.get("¿Cómo describiría su tolerancia al riesgo?", "").upper() == 'B':
        return 0
    elif respuestas.get("¿Cómo describiría su tolerancia al riesgo?", "").upper() == 'C':
        return 2
    return 0

def evaluar_horizonte_inversion(respuestas):
    """Evalúa el horizonte de inversión del inversor y ajusta el puntaje."""
    if respuestas.get("¿Cuál es su horizonte temporal para sus inversiones?", "").upper() == 'A':
        return -2
    elif respuestas.get("¿Cuál es su horizonte temporal para sus inversiones?", "").upper() == 'B':
        return 0
    elif respuestas.get("¿Cuál es su horizonte temporal para sus inversiones?", "").upper() == 'C':
        return 1
    elif respuestas.get("¿Cuál es su horizonte temporal para sus inversiones?", "").upper() == 'D':
        return 2
    return 0

# Evento al iniciar el bot
@bot.event
async def on_ready():
    print(f'Bot iniciado como {bot.user.name}')

# Token de tu bot - recuerda mantenerlo seguro y no compartirlo públicamente
bot.run('')


