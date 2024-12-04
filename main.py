import discord
from discord.ext import commands
import json
from db.db import (
    inicializar_db,
    obtener_capital,
    obtener_usuario,
    realizar_inversion,
    registrar_usuario,
    iniciar_sesion,
    obtener_perfil_usuario,
    guardar_perfil_usuario,
    actualizar_capital,
    guardar_progreso,
    obtener_progreso,
    eliminar_progreso,
    verificar_usuario,
)
from opciones.obtener_opciones_de_inversion_de_acuerdo_al_perfil_del_inversor import (
    obtener_opciones_por_perfil,
)
from opciones.obtener_opciones_inversion import obtener_opciones_inversion
from perfil_de_inversor.determinar_perfil_inversor import (
    determinar_perfil,
    obtener_cuestionario_para_determinar_perfil_del_inversor,
)

# Inicializar la base de datos
inicializar_db()

# Configuración del bot
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", description="InvertBot", intents=intents)


# Comando para iniciar sesión o registrarse
@bot.command()
async def iniciar_sesion(ctx):
    print("intentando iniciar sesion")
    usuario_id = ctx.author.id

    el_usuario_existe = verificar_usuario(usuario_id)

    # Verificar si el usuario está registrado
    if not el_usuario_existe:
        # Preguntar si el usuario quiere registrarse o iniciar sesión
        await ctx.send(
            f"{ctx.author.name}, ¿quieres registrarte o iniciar sesión? Responde con 'registrar' o 'iniciar'."
        )

        def check(m):
            return m.author == ctx.author and m.content.lower() in [
                "registrar",
                "iniciar",
            ]

        # Esperar la respuesta
        respuesta = await bot.wait_for("message", check=check)

        if respuesta.content.lower() == "registrar":
            # Intentar registrar al usuario
            if registrar_usuario(usuario_id, ctx.author.name):
                await ctx.send(
                    f"¡Bienvenido {ctx.author.name}! Te has registrado exitosamente."
                )
            else:
                await ctx.send(
                    f"Lo siento {ctx.author.name}, ya estás registrado. Inicia sesión con tu cuenta."
                )
        elif respuesta.content.lower() == "iniciar":
            await ctx.send(
                f"Lo siento {ctx.author.name}, tu ID de Discord no está registrado. Usa `!iniciar_sesion` para registrarte primero."
            )
    else:
        await ctx.send(
            f"¡Bienvenido de nuevo {ctx.author.name}! Has iniciado sesión correctamente."
        )


# Comando para obtener el perfil de inversión del usuario
@bot.command()
async def perfil(ctx):
    user_id = ctx.author.id
    perfil = obtener_perfil_usuario(user_id)

    # Si el perfil ya existe, mostrarlo
    if perfil:
        await ctx.send(f"Tu perfil de inversión es: {perfil}")
    else:
        await ctx.send(
            "No se ha encontrado un perfil para ti. Por favor, completa la evaluación de perfil."
        )
        # Llamar a las preguntas para definir el perfil
        await definir_perfil(ctx)


# Función para definir el perfil de inversión a través de preguntas
async def definir_perfil(ctx):
    usuario_id = ctx.author.id
    respuestas = obtener_progreso(
        usuario_id
    )  # Recuperar respuestas guardadas, si existen

    if respuestas:
        await ctx.send("Continuando con tu evaluación de perfil.")
        respuestas = json.loads(respuestas)  # Convertir de JSON a diccionario
    else:
        respuestas = {}
        await ctx.send("Iniciando la evaluación de tu perfil de inversión.")

    preguntas = obtener_cuestionario_para_determinar_perfil_del_inversor()

    # Filtrar preguntas que faltan por responder
    preguntas_pendientes = [(p, o) for p, o in preguntas if p not in respuestas]

    for pregunta, opciones in preguntas_pendientes:
        opciones_formato = "\n".join(opciones)
        await ctx.send(f"{pregunta}\n{opciones_formato}")

        # Validar respuesta del usuario
        def check(m):
            return m.author == ctx.author and m.content.upper() in [
                opcion[0] for opcion in opciones
            ]

        mensaje = await bot.wait_for("message", check=check)
        respuestas[pregunta] = mensaje.content.upper()

        # Guardar el progreso parcial
        guardar_progreso(usuario_id, json.dumps(respuestas))
        await ctx.send(f"Respuesta registrada: {mensaje.content.upper()}")

    # Determinar el perfil basado en todas las respuestas
    perfil_sugerido = determinar_perfil(respuestas)
    await ctx.send(f"Tu perfil de inversor sugerido es: {perfil_sugerido}")

    # Guardar el perfil definitivo y eliminar el progreso temporal
    guardar_perfil_usuario(usuario_id, perfil_sugerido)
    eliminar_progreso(usuario_id)


# Comando para depositar dinero
@bot.command()
async def depositar(ctx, monto: float):
    usuario_id = ctx.author.id
    nuevo_capital = actualizar_capital(usuario_id, monto)
    await ctx.send(f"Has depositado ${monto}. Tu saldo actual es ${nuevo_capital}.")


# Comando para retirar dinero
@bot.command()
async def retirar(ctx, monto: float):
    user_id = ctx.author.id
    capital_actual = obtener_capital(user_id)

    if capital_actual >= monto:
        nuevo_capital = actualizar_capital(user_id, -monto)
        await ctx.send(f"Has retirado ${monto}. Tu saldo actual es ${nuevo_capital}.")
    else:
        await ctx.send(
            f"No tienes suficiente dinero para retirar ${monto}. Tu saldo actual es ${capital_actual}."
        )


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
        await ctx.send(
            "No se puede mostrar las opciones de inversión. Primero, define tu perfil con el comando !perfil."
        )


# Comando para invertir en una opción específica
@bot.command()
async def invertir(ctx, opcion: str, cantidad: float):
    usuario_id = ctx.author.id
    opciones = obtener_opciones_inversion()
    opcion_seleccionada = next(
        (op for op in opciones if op["nombre"].lower() == opcion.lower()), None
    )

    if not opcion_seleccionada:
        await ctx.send("Opción de inversión no encontrada.")
        return

    capital_usuario = obtener_capital(usuario_id)
    precio_opcion = opcion_seleccionada["precio"]
    cantidad_invertida = precio_opcion * cantidad

    if capital_usuario < cantidad_invertida:
        await ctx.send(
            f"No tienes suficiente capital. Tu saldo es ${capital_usuario}. Intentaste invertir ${cantidad_invertida}."
        )
        return

    # Realizar la inversión
    realizar_inversion(
        usuario_id,
        opcion_seleccionada["nombre"],
        opcion_seleccionada["tipo_inversion"],
        cantidad,
        cantidad_invertida,
    )
    await ctx.send(
        f"Has invertido ${cantidad_invertida} en {opcion_seleccionada['nombre']}."
    )


# Evento cuando el bot está listo
@bot.event
async def on_ready():
    print(f"Bot iniciado como {bot.user.name}")


# Ejecutar el bot con el token
bot.run("")  # No olvides reemplazarlo por tu token real
