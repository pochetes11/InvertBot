import discord
from discord.ext import commands
from db.db import inicializar_db, registrar_usuario, iniciar_sesion, obtener_perfil_usuario, guardar_perfil_usuario, actualizar_capital
from opciones.obtener_opciones_de_inversion_de_acuerdo_al_perfil_del_inversor import obtener_opciones_por_perfil
from opciones.obtener_opciones_inversion import obtener_opciones_inversion
from perfil_de_inversor.determinar_perfil_inversor import determinar_perfil, obtener_cuestionario_para_determinar_perfil_del_inversor

# Inicializar la base de datos
inicializar_db()

# Configuración del bot
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', description="InvertBot", intents=intents)

# Comando para iniciar sesión o registrarse
@bot.command()
async def iniciar_sesion(ctx):
    user_id = ctx.author.id

    # Preguntar si el usuario quiere registrarse o iniciar sesión
    await ctx.send(f"{ctx.author.name}, ¿quieres registrarte o iniciar sesión? Responde con 'registrar' o 'iniciar'.")

    def check(m):
        return m.author == ctx.author and m.content.lower() in ['registrar', 'iniciar']

    # Esperar la respuesta
    respuesta = await bot.wait_for('message', check=check)

    if respuesta.content.lower() == 'registrar':
        # Intentar registrar al usuario
        if registrar_usuario(user_id, ctx.author.name):
            await ctx.send(f"¡Bienvenido {ctx.author.name}! Te has registrado exitosamente.")
        else:
            await ctx.send(f"Lo siento {ctx.author.name}, ya estás registrado. Inicia sesión con tu cuenta.")
    elif respuesta.content.lower() == 'iniciar':
        # Intentar iniciar sesión
        if iniciar_sesion(user_id):
            await ctx.send(f"¡Bienvenido de nuevo {ctx.author.name}! Has iniciado sesión correctamente.")
        else:
            await ctx.send(f"Lo siento {ctx.author.name}, tu ID de Discord no está registrado. Usa `!iniciar_sesion` para registrarte primero.")

# Comando para obtener el perfil de inversión del usuario
@bot.command()
async def perfil(ctx):
    user_id = ctx.author.id
    perfil = obtener_perfil_usuario(user_id)

    if perfil:
        await ctx.send(f"Tu perfil de inversión es: {perfil}")
    else:
        await ctx.send("No se ha encontrado un perfil para ti. Por favor, completa la evaluación de perfil.")
        # Llamar a las preguntas para definir el perfil
        await definir_perfil(ctx)

# Función para definir el perfil de inversión a través de preguntas
async def definir_perfil(ctx):
    respuestas = {}
    preguntas = obtener_cuestionario_para_determinar_perfil_del_inversor()

    for pregunta, opciones in preguntas:
        opciones_formato = "\n".join(opciones)
        await ctx.send(f"{pregunta}\n{opciones_formato}")

        # Esperar respuesta válida del usuario
        def check(m):
            return m.author == ctx.author and m.content.upper() in [opcion[0] for opcion in opciones]
        
        mensaje = await bot.wait_for('message', check=check)
        respuestas[pregunta] = mensaje.content.upper()
        await ctx.send(f"Respuesta registrada: {mensaje.content.upper()}")
    
    perfil_sugerido = determinar_perfil(respuestas)
    await ctx.send(f"Tu perfil de inversor sugerido es: {perfil_sugerido}")
    guardar_perfil_usuario(ctx.author.id, perfil_sugerido)

# Comando para depositar dinero
@bot.command()
async def depositar(ctx, monto: float):
    user_id = ctx.author.id
    nuevo_capital = actualizar_capital(user_id, monto)
    await ctx.send(f"Has depositado ${monto}. Tu saldo actual es ${nuevo_capital}.")

# Comando para listar las opciones de inversión
@bot.command()
async def listado_de_opciones(ctx):
    user_id = ctx.author.id
    perfil = obtener_perfil_usuario(user_id)
    
    if perfil:
        opciones = obtener_opciones_por_perfil(perfil)
        opciones_str = "\n".join([f"{opcion['nombre']} - {opcion['tipo_inversion']}" for opcion in opciones])
        await ctx.send(f"Opciones de inversión disponibles:\n{opciones_str}")
    else:
        await ctx.send("No se puede mostrar las opciones de inversión. Primero, define tu perfil con el comando !perfil.")

# Evento cuando el bot está listo
@bot.event
async def on_ready():
    print(f'Bot iniciado como {bot.user.name}')

# Ejecutar el bot con el token
bot.run('tu_token_aqui')
