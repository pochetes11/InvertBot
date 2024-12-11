import discord
from discord.ext import commands
import json
from db.db import (
    inicializar_db,
    obtener_capital,
    obtener_usuario,
    registrar_usuario,
    iniciar_sesion,
    obtener_perfil_usuario,
    guardar_perfil_usuario,
    actualizar_capital,
    guardar_progreso,
    obtener_progreso,
    eliminar_progreso,
    verificar_usuario,
    realizar_inversion,
)
from opciones.obtener_opciones_de_inversion_de_acuerdo_al_perfil_del_inversor import (
    obtener_opciones_por_perfil,
)
from opciones.obtener_opciones_inversion import obtener_opciones_inversion
from perfil_de_inversor.determinar_perfil_inversor import (
    determinar_perfil,
    obtener_cuestionario_para_determinar_perfil_del_inversor,
)

intents = discord.Intents.default()
intents.message_content = True

# Inicializar la base de datos
inicializar_db()

# Configuración del bot
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", description="InvertBot", intents=intents)


# Comando para iniciar sesión o registrarse
@bot.command()
async def iniciar_sesion(ctx):
    usuario_id = ctx.author.id
    if verificar_usuario(usuario_id):
        await ctx.send(f"¡Bienvenido de nuevo, {ctx.author.name}!")
        return

    await ctx.send(f"{ctx.author.name}, ¿quieres registrarte o iniciar sesión? Responde con 'registrar'.")

    def check(m):
        return m.author == ctx.author and m.content.lower() == "registrar"

    try:
        await bot.wait_for("message", check=check, timeout=30)
        if registrar_usuario(usuario_id, ctx.author.name):
            await ctx.send(f"¡Bienvenido, {ctx.author.name}! Te has registrado con éxito.")
        else:
            await ctx.send("Ocurrió un problema al registrarte. Intenta nuevamente.")
    except TimeoutError:
        await ctx.send("No respondiste a tiempo. Intenta de nuevo con `!iniciar_sesion`.")


# Comando para obtener el perfil de inversión del usuario
@bot.command()
async def perfil(ctx):
    user_id = ctx.author.id
    perfil = obtener_perfil_usuario(user_id)

    if perfil:
        await ctx.send(f"Tu perfil de inversión es: {perfil}")
    else:
        await ctx.send(
            "No se ha encontrado un perfil para ti. Por favor, completa la evaluación de perfil."
        )
        await definir_perfil(ctx)


# Función para definir el perfil de inversión
async def definir_perfil(ctx):
    usuario_id = ctx.author.id
    respuestas = obtener_progreso(usuario_id)

    if respuestas:
        respuestas = json.loads(respuestas)
        await ctx.send("Continuando con tu evaluación de perfil.")
    else:
        respuestas = {}
        await ctx.send("Iniciando la evaluación de tu perfil de inversión.")

    preguntas = obtener_cuestionario_para_determinar_perfil_del_inversor()
    preguntas_pendientes = [
        (p, o) for p, o in preguntas if p.lower() not in respuestas
    ]

    for pregunta, opciones in preguntas_pendientes:
        opciones_formato = "\n".join(opciones)
        await ctx.send(f"{pregunta}\n{opciones_formato}")

        def check(m):
            return (
                m.author == ctx.author
                and m.content.upper() in [op[0] for op in opciones]
            )

        mensaje = await bot.wait_for("message", check=check)
        respuestas[pregunta.lower()] = mensaje.content.upper()
        guardar_progreso(usuario_id, json.dumps(respuestas))
        await ctx.send(f"Respuesta registrada: {mensaje.content.upper()}")

    perfil_sugerido = determinar_perfil(respuestas)
    guardar_perfil_usuario(usuario_id, perfil_sugerido)
    eliminar_progreso(usuario_id)

    await ctx.send(f"Tu perfil de inversor sugerido es: {perfil_sugerido}")



# Comando para listar las opciones de inversión
@bot.command()
async def listado_de_opciones(ctx):
    usuario_id = ctx.author.id
    perfil = obtener_perfil_usuario(usuario_id)

    if perfil:
        opciones = obtener_opciones_por_perfil(perfil)
        opciones_str = "\n".join(
            [
                f"{opcion['nombre']} - {opcion['tipo_inversion']} - ${opcion['precio']}"
                for opcion in opciones
            ]
        )
        await ctx.send(f"Opciones de inversión disponibles:\n{opciones_str}")
    else:
        await ctx.send("Primero, define tu perfil con el comando !perfil.")


@bot.command()
async def invertir(ctx, bonos):
    usuario_id = ctx.author.id

    # Verificar si el usuario tiene un perfil definido
    perfil = obtener_perfil_usuario(usuario_id)
    if not perfil:
        await ctx.send("Primero, define tu perfil con el comando !perfil.")
        return

    # Obtener las opciones disponibles para el perfil del usuario
    opciones = obtener_opciones_por_perfil(perfil)
    if not opciones:
        await ctx.send("No hay opciones disponibles para tu perfil.")
        return

    # Buscar la opción seleccionada
    inversion = next(
        (op for op in opciones if op["nombre"].lower() == opcion.lower()),
        None
    )
    if not inversion:
        await ctx.send(f"La opción de inversión '{opcion}' no está disponible.")
        return

    # Calcular el precio total de la inversión
    precio = inversion["precio"]
    cantidad_maxima = int(cantidad / precio)  # Cantidad de unidades que puede comprar
    total_invertido = cantidad_maxima * precio

    # Verificar el capital del usuario
    capital_actual = obtener_capital(usuario_id)
    if capital_actual < total_invertido:
        await ctx.send(
            f"No tienes suficiente dinero para invertir. Tu saldo actual es ${capital_actual:.2f}."
        )
        return

    # Realizar la inversión y actualizar el capital
    realizar_inversion(
        usuario_id,
        inversion["nombre"],
        inversion["tipo_inversion"],
        cantidad_maxima,
        total_invertido,
    )

    # Mensaje de confirmación
    capital_restante = capital_actual - total_invertido
    await ctx.send(
        f"¡Inversión exitosa! Has invertido ${total_invertido:.2f} en {inversion['nombre']} "
        f"({cantidad_maxima} unidades). Tu saldo restante es ${capital_restante:.2f}."
    )

# Comando para depositar dinero
@bot.command()
async def depositar(ctx, monto: float):
    usuario_id = ctx.author.id
    if not verificar_usuario(usuario_id):
        await ctx.send("Debes iniciar sesión primero usando !iniciar_sesion.")
        return

    nuevo_capital = actualizar_capital(usuario_id, monto)
    await ctx.send(f"Has depositado ${monto}. Tu saldo actual es ${nuevo_capital}.")


# Comando para listar las opciones de inversión
@bot.command()
async def retirar(ctx, monto: float):
    usuario_id = ctx.author.id
    if not verificar_usuario(usuario_id):
        await ctx.send("Debes iniciar sesión primero usando !iniciar_sesion.")
        return

    capital_actual = obtener_capital(usuario_id)

    if capital_actual >= monto:
        nuevo_capital = actualizar_capital(usuario_id, -monto)
        await ctx.send(f"Has retirado ${monto}. Tu saldo actual es ${nuevo_capital}.")
    else:
        await ctx.send(
            f"No tienes suficiente dinero para retirar ${monto}. Tu saldo actual es ${capital_actual}."
        )
    perfil = obtener_perfil_usuario(usuario_id)

    if perfil:
        # Filtrar opciones de acuerdo al perfil
        opciones = obtener_opciones_por_perfil(perfil)
        if opciones:
            opciones_str = "\n".join(
                [
                    f"{opcion['nombre']} - {opcion['tipo_inversion']} - ${opcion['precio']}"
                    for opcion in opciones
                ]
            )
            await ctx.send(f"Opciones de inversión disponibles:\n{opciones_str}")
        else:
            await ctx.send("No hay opciones de inversión disponibles para tu perfil.")
    else:
        await ctx.send(
            "No se puede mostrar las opciones de inversión. Primero, define tu perfil con el comando !perfil."
        )



# Comando para listar las opciones de inversión
@bot.command()
async def opciones_inversion(ctx):
    usuario_id = ctx.author.id
    if not verificar_usuario(usuario_id):
        await ctx.send("Debes iniciar sesión primero usando !iniciar_sesion.")
        return

    perfil = obtener_perfil_usuario(usuario_id)

    if perfil:
        # Filtrar opciones de acuerdo al perfil
        opciones = obtener_opciones_por_perfil(perfil)
        if opciones:
            opciones_str = "\n".join(
                [
                    f"{opcion['nombre']} - {opcion['tipo_inversion']} - ${opcion['precio']}"
                    for opcion in opciones
                ]
            )
            await ctx.send(f"Opciones de inversión disponibles:\n{opciones_str}")
        else:
            await ctx.send("No hay opciones de inversión disponibles para tu perfil.")
    else:
        await ctx.send(
            "No se puede mostrar las opciones de inversión. Primero, define tu perfil con el comando !perfil."
        )

# Comando para verificar el saldo actual
@bot.command()
async def saldo(ctx):
    usuario_id = ctx.author.id
    if not verificar_usuario(usuario_id):
        await ctx.send("Debes iniciar sesión primero usando !iniciar_sesion.")
        return

    capital_actual = obtener_capital(usuario_id)
    await ctx.send(f"Tu saldo actual es ${capital_actual}.")


# Evento cuando el bot está listo
@bot.event
async def on_ready():
    print(f"Bot iniciado como {bot.user.name}")


# Ejecutar el bot con el token
bot.run("")
