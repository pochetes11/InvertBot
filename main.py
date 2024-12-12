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

    await ctx.send(
        f"{ctx.author.name}, ¿quieres registrarte o iniciar sesión? Responde con 'registrar'."
    )

    def check(m):
        return m.author == ctx.author and m.content.lower() == "registrar"

    try:
        await bot.wait_for("message", check=check, timeout=30)
        if registrar_usuario(usuario_id, ctx.author.name):
            await ctx.send(
                f"¡Bienvenido, {ctx.author.name}! Te has registrado con éxito."
            )
        else:
            await ctx.send("Ocurrió un problema al registrarte. Intenta nuevamente.")
    except TimeoutError:
        await ctx.send(
            "No respondiste a tiempo. Intenta de nuevo con `!iniciar_sesion`."
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
    respuestas = obtener_progreso(usuario_id)

    if respuestas:
        respuestas = json.loads(respuestas)
        await ctx.send("Continuando con tu evaluación de perfil.")
    else:
        respuestas = {}
        await ctx.send("Iniciando la evaluación de tu perfil de inversión.")

    preguntas = obtener_cuestionario_para_determinar_perfil_del_inversor()
    preguntas_pendientes = [(p, o) for p, o in preguntas if p.lower() not in respuestas]

    for pregunta, opciones in preguntas_pendientes:
        opciones_formato = "\n".join(opciones)
        await ctx.send(f"{pregunta}\n{opciones_formato}")

        def check(m):
            return m.author == ctx.author and m.content.upper() in [
                op[0] for op in opciones
            ]

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
    opciones = (
        obtener_opciones_inversion()
    )  # Asegúrate de que este código esté recuperando las opciones

    if not opciones:
        await ctx.send("No hay opciones de inversión disponibles.")
        return

    mensaje = "Opciones de inversión disponibles:\n\n"
    for idx, opcion in enumerate(opciones, start=1):
        mensaje += (
            f"{idx}. **{opcion.get('nombre', 'Nombre no disponible')}**\n"
            f"   - Precio: ${opcion.get('precio', 'Precio no disponible')}\n"
            f"   - Tipo: {opcion.get('tipo_inversion', 'Tipo no disponible')}\n"
        )

        # Verificar si el mensaje excede los 2000 caracteres y enviarlo en partes
        if len(mensaje) > 2000:
            await ctx.send(mensaje)  # Enviar la parte del mensaje
            mensaje = ""  # Restablecer el mensaje para la siguiente parte

    # Enviar la última parte si es necesario
    if mensaje:
        await ctx.send(mensaje)


@bot.command()
async def mas_info(ctx, opcion_numero: int):
    opciones = obtener_opciones_inversion()

    if not opciones:
        await ctx.send("No hay opciones de inversión disponibles.")
        return

    if opcion_numero < 1 or opcion_numero > len(opciones):
        await ctx.send("Opción inválida. Por favor, selecciona un número válido.")
        return

    opcion = opciones[opcion_numero - 1]  # Restar 1 para acceder al índice correcto

    descripcion = opcion.get("descripcion", "Descripción no disponible")
    link = opcion.get("link", "No hay más información disponible")

    await ctx.send(
        f"**{opcion['nombre']}** - Más información:\n"
        f"   - Descripción: {descripcion}\n"
        f"   - Más información: {link}\n"
    )


@bot.command()
async def invertir(ctx):
    usuario_id = ctx.author.id

    perfil = obtener_perfil_usuario(usuario_id)
    if not perfil:
        await ctx.send("Primero, define tu perfil con el comando !perfil.")
        return

    # Obtener las opciones de inversión desde la base de datos
    opciones = obtener_opciones_inversion()  # Aquí estamos obteniendo las opciones

    if not opciones:
        await ctx.send("No hay opciones disponibles para tu perfil.")
        return

    mensaje = "Opciones de inversión disponibles:\n\n"
    for idx, opcion in enumerate(opciones, start=1):
        mensaje += (
            f"{idx}. **{opcion['nombre']}**\n"
            f"   - Precio: ${opcion['precio']}\n"
            f"   - Tipo: {opcion['tipo_inversion']}\n"
            f"   - Descripción: {opcion['descripcion']}\n"
            f"   👉 Más información: {opcion['link']}\n\n"
        )
    mensaje += "\nResponde con el número de la opción en la que deseas invertir."

    await ctx.send(mensaje)

    def check(m):
        return m.author == ctx.author and m.content.isdigit()

    try:
        respuesta = await bot.wait_for("message", check=check, timeout=60)
        opcion_index = int(respuesta.content.strip()) - 1

        if opcion_index < 0 or opcion_index >= len(opciones):
            await ctx.send("Por favor, selecciona una opción válida.")
            return

        opcion_seleccionada = opciones[
            opcion_index
        ]  # Aquí se obtiene la opción seleccionada

        # Preguntar por la cantidad que desea invertir
        await ctx.send(
            f"Has seleccionado **{opcion_seleccionada['nombre']}**. ¿Cuánto dinero deseas invertir?"
        )

        def monto_check(m):
            return m.author == ctx.author and m.content.replace(".", "", 1).isdigit()

        monto_respuesta = await bot.wait_for("message", check=monto_check, timeout=60)
        monto = float(monto_respuesta.content.strip())

        if monto <= 0:
            await ctx.send("Por favor, ingresa un monto válido.")
            return

        precio = opcion_seleccionada["precio"]
        cantidad_maxima = int(monto // precio)
        total_invertido = cantidad_maxima * precio

        capital_actual = obtener_capital(usuario_id)
        if capital_actual < total_invertido:
            await ctx.send(
                f"No tienes suficiente dinero para invertir. Tu saldo actual es ${capital_actual:.2f}."
            )
            return

        realizar_inversion(
            usuario_id,
            opcion_seleccionada["nombre"],
            opcion_seleccionada["tipo_inversion"],
            cantidad_maxima,
            total_invertido,
        )

        # Mensaje de confirmación
        capital_restante = capital_actual - total_invertido
        await ctx.send(
            f"¡Inversión exitosa! Has invertido ${total_invertido:.2f} en {opcion_seleccionada['nombre']} "
            f"({cantidad_maxima} unidades). Tu saldo restante es ${capital_restante:.2f}."
        )

    except TimeoutError:
        await ctx.send("No respondiste a tiempo. Intenta nuevamente con `!invertir`.")


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
