import json
from asyncio import TimeoutError
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
# Diccionario para almacenar las sesiones activas


# Diccionario para almacenar las sesiones activas
sesiones_activas = set()

# Decorador para verificar si un usuario tiene una sesión activa
def requiere_sesion_activa():
    def decorador(func):
        async def envoltura(ctx, *args, **kwargs):
            usuario_id = ctx.author.id
            if usuario_id not in sesiones_activas:
                await ctx.send("❌ Debes iniciar sesión primero usando `!iniciar_sesion`.")
                return
            return await func(ctx, *args, **kwargs)
        return envoltura
    return decorador

# Comando para iniciar sesión o registrarse
@bot.command()
async def iniciar_sesion(ctx):
    usuario_id = ctx.author.id

    # Verificar si el usuario ya tiene una sesión activa
    if usuario_id in sesiones_activas:
        await ctx.send(f"¡Ya tienes una sesión activa, {ctx.author.name}!")
        return

    # Verificar si el usuario ya está registrado en la base de datos
    if verificar_usuario(usuario_id):
        sesiones_activas.add(usuario_id)
        await ctx.send(f"¡Bienvenido de nuevo, {ctx.author.name}! Tu sesión está activa.")
    else:
        await ctx.send(f"{ctx.author.name}, ¿quieres registrarte o iniciar sesión? Responde con 'registrar'.")

        def check(m):
            return m.author == ctx.author and m.content.lower() == "registrar"

        try:
            # Esperar respuesta del usuario para proceder con el registro
            await bot.wait_for("message", check=check, timeout=30)
            if registrar_usuario(usuario_id, ctx.author.name):
                sesiones_activas.add(usuario_id)
                await ctx.send(f"¡Te has registrado exitosamente, {ctx.author.name}! Tu sesión está activa.")
            else:
                await ctx.send("Ocurrió un problema al registrarte. Intenta nuevamente.")
        except TimeoutError:
            await ctx.send("⏰ No respondiste a tiempo. Intenta de nuevo con `!iniciar_sesion`.")

# Comando para cerrar sesión
@bot.command()
async def chao(ctx):
    usuario_id = ctx.author.id
    if usuario_id in sesiones_activas:
        sesiones_activas.remove(usuario_id)
        await ctx.send(f"👋 ¡Adiós, {ctx.author.name}! Tu sesión ha sido cerrada.")
    else:
        await ctx.send("❌ No tienes una sesión activa.")

# Comando para manejar el perfil de inversión
@bot.command()
@requiere_sesion_activa()
async def perfil(ctx):
    usuario_id = ctx.author.id

    try:
        # Verificar si el usuario ya tiene un perfil
        perfil = obtener_perfil_usuario(usuario_id)

        if perfil:
            await ctx.send(f"✅ Tu perfil de inversión es: **{perfil}**")
            return

        # Si no hay perfil definido, iniciar evaluación
        await ctx.send("🔍 No se ha encontrado un perfil para ti. Iniciando la evaluación de tu perfil de inversión.")

        # Verificar si hay progreso previo
        respuestas = obtener_progreso(usuario_id)
        if respuestas:
            respuestas = json.loads(respuestas)
            await ctx.send("🔄 Continuando con tu evaluación anterior.")
        else:
            respuestas = {}
            await ctx.send("📝 Empezaremos desde el inicio.")

        # Obtener cuestionario
        preguntas = obtener_cuestionario_para_determinar_perfil_del_inversor()
        preguntas_pendientes = [(p, o) for p, o in preguntas if p.lower() not in respuestas]

        for pregunta, opciones in preguntas_pendientes:
            opciones_formato = "\n".join([f"{op[0]} - {op[1]}" for op in opciones])
            await ctx.send(f"**{pregunta}**\n{opciones_formato}")

            def check(m):
                return (
                    m.author == ctx.author
                    and m.content.upper() in [op[0].upper() for op in opciones]
                )

            try:
                mensaje = await bot.wait_for("message", check=check, timeout=60)
                respuestas[pregunta.lower()] = mensaje.content.upper()
                guardar_progreso(usuario_id, json.dumps(respuestas))
                await ctx.send(f"✅ Respuesta registrada: **{mensaje.content}**")
            except TimeoutError:
                await ctx.send("⏰ Se acabó el tiempo para responder. Vuelve a intentarlo con `!perfil`.")
                return

        # Determinar y guardar perfil sugerido
        perfil_sugerido = determinar_perfil(respuestas)
        guardar_perfil_usuario(usuario_id, perfil_sugerido)
        eliminar_progreso(usuario_id)

        await ctx.send(f"🎉 ¡Evaluación completada! Tu perfil de inversor sugerido es: **{perfil_sugerido}**")
    except Exception as e:
        await ctx.send("❌ Ha ocurrido un error inesperado. Inténtalo nuevamente.")
        print(f"Error en comando !perfil: {e}")

# Comando para listar todas las opciones de inversión (sin filtrar)
@bot.command()
@requiere_sesion_activa()
async def listado_de_opciones(ctx):
    opciones = obtener_opciones_inversion()

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

    await ctx.send(mensaje)

# Comando para listar las opciones de inversión filtradas por perfil
@bot.command()
@requiere_sesion_activa()
async def opciones_por_perfil(ctx):
    usuario_id = ctx.author.id
    perfil = obtener_perfil_usuario(usuario_id)

    if perfil:
        opciones = obtener_opciones_por_perfil(perfil)
        if opciones:
            opciones_str = "\n".join(
                [
                    f"{idx + 1}. **{opcion['nombre']}**\n"
                    f"   - Tipo: {opcion['tipo_inversion']}\n"
                    f"   - Precio: ${opcion['precio']}\n"
                    f"   - Descripción: {opcion.get('descripcion', 'No disponible')}\n"
                    for idx, opcion in enumerate(opciones)
                ]
            )
            await ctx.send(f"Opciones de inversión disponibles para tu perfil:\n\n{opciones_str}")
        else:
            await ctx.send(f"No hay opciones disponibles para tu perfil: {perfil}.")
    else:
        await ctx.send("❌ No tienes un perfil asociado. Usa `!perfil` para crearlo.")



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
