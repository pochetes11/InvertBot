import discord
from discord.ext import commands
import json
from db.db import (
    inicializar_db,
    obtener_capital,
<<<<<<< HEAD
    obtener_usuario,
    registrar_usuario,
    iniciar_sesion,
=======
    realizar_inversion,
    registrar_usuario,
>>>>>>> refs/remotes/origin/main
    obtener_perfil_usuario,
    guardar_perfil_usuario,
    actualizar_capital,
    guardar_progreso,
    obtener_progreso,
    eliminar_progreso,
    verificar_usuario,
<<<<<<< HEAD
    realizar_inversion,
=======
>>>>>>> refs/remotes/origin/main
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
<<<<<<< HEAD
=======

>>>>>>> refs/remotes/origin/main

# Comando para iniciar sesión o registrarse
@bot.command()
async def iniciar_sesion(ctx):
    print("intentando iniciar sesion")
    usuario_id = ctx.author.id

    el_usuario_existe = verificar_usuario(usuario_id)

<<<<<<< HEAD
    if not el_usuario_existe:
        await ctx.send(f"{ctx.author.name}, ¿quieres registrarte o iniciar sesión? Responde con 'registrar' o 'iniciar'.")

        def check(m):
            return m.author == ctx.author and m.content.lower() in ["registrar", "iniciar"]

        respuesta = await bot.wait_for("message", check=check)

        if respuesta.content.lower() == "registrar":
=======
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
>>>>>>> refs/remotes/origin/main
            if registrar_usuario(usuario_id, ctx.author.name):
                await ctx.send(
                    f"¡Bienvenido {ctx.author.name}! Te has registrado exitosamente."
                )
            else:
<<<<<<< HEAD
                await ctx.send(f"Lo siento {ctx.author.name}, ya estás registrado. Inicia sesión con tu cuenta.")
        elif respuesta.content.lower() == "iniciar":
            await ctx.send(f"Lo siento {ctx.author.name}, tu ID de Discord no está registrado. Usa `!iniciar_sesion` para registrarte primero.")
=======
                await ctx.send(
                    f"Lo siento {ctx.author.name}, ya estás registrado. Inicia sesión con tu cuenta."
                )
        elif respuesta.content.lower() == "iniciar":
            await ctx.send(
                f"Lo siento {ctx.author.name}, tu ID de Discord no está registrado. Usa `!iniciar_sesion` para registrarte primero."
            )
>>>>>>> refs/remotes/origin/main
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
<<<<<<< HEAD
        await ctx.send("No se ha encontrado un perfil para ti. Por favor, completa la evaluación de perfil.")
        await definir_perfil(ctx)

# Función para definir el perfil de inversión
async def definir_perfil(ctx):
    usuario_id = ctx.author.id
    respuestas = obtener_progreso(usuario_id)  # Recuperar respuestas guardadas
=======
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
>>>>>>> refs/remotes/origin/main

    if respuestas:
        await ctx.send("Continuando con tu evaluación de perfil.")
        respuestas = json.loads(respuestas)  # Convertir de JSON a diccionario
    else:
        respuestas = {}
        await ctx.send("Iniciando la evaluación de tu perfil de inversión.")

    preguntas = obtener_cuestionario_para_determinar_perfil_del_inversor()

    preguntas_pendientes = [(p, o) for p, o in preguntas if p not in respuestas]

    for pregunta, opciones in preguntas_pendientes:
        opciones_formato = "\n".join(opciones)
        await ctx.send(f"{pregunta}\n{opciones_formato}")

        def check(m):
<<<<<<< HEAD
            return m.author == ctx.author and m.content.upper() in [opcion[0] for opcion in opciones]

        mensaje = await bot.wait_for('message', check=check)
=======
            return m.author == ctx.author and m.content.upper() in [
                opcion[0] for opcion in opciones
            ]

        mensaje = await bot.wait_for("message", check=check)
>>>>>>> refs/remotes/origin/main
        respuestas[pregunta] = mensaje.content.upper()

        guardar_progreso(usuario_id, json.dumps(respuestas))
        await ctx.send(f"Respuesta registrada: {mensaje.content.upper()}")

    perfil_sugerido = determinar_perfil(respuestas)
    await ctx.send(f"Tu perfil de inversor sugerido es: {perfil_sugerido}")
    guardar_perfil_usuario(usuario_id, perfil_sugerido)
    eliminar_progreso(usuario_id)

<<<<<<< HEAD
# Comando para listar las opciones de inversión
@bot.command()
async def listado_de_opciones(ctx):
    usuario_id = ctx.author.id
    perfil = obtener_perfil_usuario(usuario_id)

    if perfil:
        opciones = obtener_opciones_por_perfil(perfil)
        opciones_str = "\n".join([f"{opcion['nombre']} - {opcion['tipo_inversion']} - ${opcion['precio']}" for opcion in opciones])
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
    inversion = next((opcion for opcion in opciones if opcion["nombre"].lower() == opcion.lower()), None)

    if not inversion:
        await ctx.send("Opción de inversión no válida.")
        return

    precio = inversion['precio']
    cantidad_maxima = int(cantidad / precio)  # Número de acciones que el usuario puede comprar
    total_invertido = cantidad_maxima * precio

    capital_actual = obtener_capital(usuario_id)

    if capital_actual < total_invertido:
        await ctx.send(f"No tienes suficiente dinero para realizar esta inversión. Tu saldo actual es ${capital_actual}.")
        return

    # Realizar inversión
    realizar_inversion(usuario_id, inversion['nombre'], inversion['tipo_inversion'], cantidad_maxima, total_invertido)
    await ctx.send(f"Has invertido ${total_invertido} en {inversion['nombre']}.")
=======
>>>>>>> refs/remotes/origin/main

# Comando para depositar dinero
@bot.command()
async def depositar(ctx, monto: float):
    usuario_id = ctx.author.id
    nuevo_capital = actualizar_capital(usuario_id, monto)
    await ctx.send(f"Has depositado ${monto}. Tu saldo actual es ${nuevo_capital}.")

<<<<<<< HEAD
# Comando para retirar dinero
=======

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
>>>>>>> refs/remotes/origin/main
@bot.command()
async def retirar(ctx, monto: float):
    usuario_id = ctx.author.id
<<<<<<< HEAD
    capital_actual = obtener_capital(usuario_id)

    if capital_actual >= monto:
        nuevo_capital = actualizar_capital(usuario_id, -monto)
        await ctx.send(f"Has retirado ${monto}. Tu saldo actual es ${nuevo_capital}.")
    else:
        await ctx.send(f"No tienes suficiente dinero para retirar ${monto}. Tu saldo actual es ${capital_actual}.")
=======
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

>>>>>>> refs/remotes/origin/main

# Evento cuando el bot está listo
@bot.event
async def on_ready():
    print(f"Bot iniciado como {bot.user.name}")


# Ejecutar el bot con el token
bot.run("")  # No olvides reemplazarlo por tu token real
