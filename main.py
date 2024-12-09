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

    el_usuario_existe = verificar_usuario(usuario_id)

    if not el_usuario_existe:
        await ctx.send(
            f"{ctx.author.name}, ¿quieres registrarte o iniciar sesión? Responde con 'registrar' o 'iniciar'."
        )

        def check(m):
            return m.author == ctx.author and m.content.lower() in [
                "registrar",
                "iniciar",
            ]

        respuesta = await bot.wait_for("message", check=check)

        if respuesta.content.lower() == "registrar":
            pass
    # Verificar si el usuario está registrado
    if not el_usuario_existe:
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
    respuestas = obtener_progreso(usuario_id)  # Recuperar respuestas guardadas
    await ctx.send(
        "No se ha encontrado un perfil para ti. Por favor, completa la evaluación de perfil."
    )
    await definir_perfil(ctx)


# Función para definir el perfil de inversión a través de preguntas
async def definir_perfil(ctx):
    usuario_id = ctx.author.id
    respuestas = obtener_progreso(usuario_id)

    if respuestas:
        await ctx.send("Continuando con tu evaluación de perfil.")
        respuestas = json.loads(respuestas)
    else:
        respuestas = {}
        await ctx.send("Iniciando la evaluación de tu perfil de inversión.")

    preguntas = obtener_cuestionario_para_determinar_perfil_del_inversor()

    # Filtrar preguntas que faltan por responder
    preguntas_pendientes = [(p, o) for p, o in preguntas if p.lower() not in respuestas]

    for pregunta, opciones in preguntas_pendientes:
        opciones_formato = "\n".join(opciones)
        await ctx.send(f"{pregunta}\n{opciones_formato}")

        def check(m):
            return m.author == ctx.author and m.content.lower() in [
                opcion[0].lower() for opcion in opciones
            ]

            # mensaje = await bot.wait_for("message", check=check)
            # respuestas[pregunta.lower()] = mensaje.content.lower()

            # return m.author == ctx.author and m.content.upper() in [opcion[0] for opcion in opciones]

        mensaje = await bot.wait_for("message", check=check)
        respuestas[pregunta] = mensaje.content.upper()

        guardar_progreso(usuario_id, json.dumps(respuestas))
        await ctx.send(f"Respuesta registrada: {mensaje.content.lower()}")

    perfil_sugerido = determinar_perfil(respuestas)
    await ctx.send(f"Tu perfil de inversor sugerido es: {perfil_sugerido}")
    guardar_perfil_usuario(usuario_id, perfil_sugerido)
    eliminar_progreso(usuario_id)


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


# Comando para realizar una inversión
@bot.command()
async def invertir(ctx, opcion: str, cantidad: float):
    usuario_id = ctx.author.id
    perfil = obtener_perfil_usuario(usuario_id)

    if not perfil:
        await ctx.send("Primero, define tu perfil con el comando !perfil.")
        return

    # Buscar la opción seleccionada
    opciones = obtener_opciones_por_perfil(perfil)
    inversion = next(
        (opcion for opcion in opciones if opcion["nombre"].lower() == opcion.lower()),
        None,
    )

    if not inversion:
        await ctx.send("Opción de inversión no válida.")
        return

    precio = inversion["precio"]
    cantidad_maxima = int(
        cantidad / precio
    )  # Número de acciones que el usuario puede comprar
    total_invertido = cantidad_maxima * precio

    capital_actual = obtener_capital(usuario_id)

    if capital_actual < total_invertido:
        await ctx.send(
            f"No tienes suficiente dinero para realizar esta inversión. Tu saldo actual es ${capital_actual}."
        )
        return

    # Realizar inversión
    realizar_inversion(
        usuario_id,
        inversion["nombre"],
        inversion["tipo_inversion"],
        cantidad_maxima,
        total_invertido,
    )
    await ctx.send(f"Has invertido ${total_invertido} en {inversion['nombre']}.")


# Comando para depositar dinero
@bot.command()
async def depositar(ctx, monto: float):
    usuario_id = ctx.author.id
    if not verificar_usuario(usuario_id):
        await ctx.send("Debes iniciar sesión primero usando !iniciar_sesion.")
        return

    nuevo_capital = actualizar_capital(usuario_id, monto)
    await ctx.send(f"Has depositado ${monto}. Tu saldo actual es ${nuevo_capital}.")


# Comando para retirar dinero
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


# Comando para invertir en una opción específica
@bot.command()
async def invertir(ctx, opcion: str, monto: str):
    usuario_id = ctx.author.id
    if not verificar_usuario(usuario_id):
        await ctx.send("Debes iniciar sesión primero usando !iniciar_sesion.")
        return

    # Convertir el monto a minúsculas y manejar error de conversión
    try:
        monto = float(monto)
    except ValueError:
        await ctx.send(
            f"El monto '{monto}' no es válido. Por favor, ingresa un número."
        )
        return

    # Obtener la opción de inversión
    opciones = obtener_opciones_inversion()
    opcion_seleccionada = next(
        (op for op in opciones if op["nombre"].lower() == opcion.lower()), None
    )

    if not opcion_seleccionada:
        await ctx.send("Opción de inversión no encontrada.")
        return

    capital_usuario = obtener_capital(usuario_id)
    precio_opcion = opcion_seleccionada["precio"]
    cantidad_posible = monto // precio_opcion
    cantidad_invertida = cantidad_posible * precio_opcion

    if capital_usuario < cantidad_invertida:
        await ctx.send(
            f"No tienes suficiente capital. Tu saldo es ${capital_usuario}. Intentaste invertir ${monto}."
        )
        return

    realizar_inversion(
        usuario_id,
        opcion_seleccionada["nombre"],
        opcion_seleccionada["tipo_inversion"],
        cantidad_posible,
        cantidad_invertida,
    )
    await ctx.send(
        f"Has invertido ${cantidad_invertida} en {opcion_seleccionada['nombre']} ({cantidad_posible} unidades)."
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
bot.run("TU_TOKEN_AQUI")
