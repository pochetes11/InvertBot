import sqlite3
import json


# Función para inicializar la base de datos
def inicializar_db():
    conn = sqlite3.connect("perfil_inversion.db")
    c = conn.cursor()

<<<<<<< HEAD
    # Crear tabla de usuarios
    c.execute('''
=======
    c.execute(
        """
>>>>>>> refs/remotes/origin/main
        CREATE TABLE IF NOT EXISTS usuarios (
            id_discord TEXT PRIMARY KEY,
            nombre_usuario TEXT NOT NULL,
            capital REAL DEFAULT 0.0,
            fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
<<<<<<< HEAD
    ''')

    # Crear tabla de perfiles
    c.execute('''
=======
    """
    )

    c.execute(
        """
>>>>>>> refs/remotes/origin/main
        CREATE TABLE IF NOT EXISTS perfiles (
            user_id TEXT PRIMARY KEY,
            perfil TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES usuarios(id_discord)
        )
<<<<<<< HEAD
    ''')

    # Crear tabla de inversiones
    c.execute('''
=======
    """
    )

    # Tabla de inversiones (común para todas las inversiones)
    c.execute(
        """
>>>>>>> refs/remotes/origin/main
        CREATE TABLE IF NOT EXISTS inversiones (
            id_inversion INTEGER PRIMARY KEY AUTOINCREMENT,
            id_discord TEXT,
            nombre_inversion TEXT,
            tipo_inversion TEXT,
            cantidad_invertida REAL,
            valor_invertido REAL,
            fecha_inversion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_discord) REFERENCES usuarios(id_discord)
        )
<<<<<<< HEAD
    ''')

    # Crear tabla de capital (billetera virtual)
    c.execute('''
=======
    """
    )

    c.execute(
        """
>>>>>>> refs/remotes/origin/main
        CREATE TABLE IF NOT EXISTS capital (
            usuario_id TEXT PRIMARY KEY,
            capital REAL DEFAULT 0,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id_discord)
        )
<<<<<<< HEAD
    ''')

    # Crear tabla de progreso de perfil
    c.execute('''
=======
    """
    )

    c.execute(
        """
>>>>>>> refs/remotes/origin/main
        CREATE TABLE IF NOT EXISTS progreso (
            usuario_id TEXT PRIMARY KEY,
            respuestas JSON,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id_discord)
        )
    """
    )

    conn.commit()
    conn.close()

<<<<<<< HEAD
# Función para iniciar sesión con un usuario existente
def iniciar_sesion(usuario_id):
    conn = sqlite3.connect('perfil_inversion.db')
    c = conn.cursor()

    # Comprobamos si el usuario existe
    c.execute("SELECT id_discord FROM usuarios WHERE id_discord = ?", (usuario_id,))
    usuario = c.fetchone()
    conn.close()

    if usuario:
        return True  # Usuario encontrado, sesión iniciada
    else:
        return False  # Usuario no encontrado, sesión no iniciada
=======
>>>>>>> refs/remotes/origin/main

# Función para registrar un nuevo usuario
def registrar_usuario(usuario_id, nombre_usuario):
    conn = sqlite3.connect("perfil_inversion.db")
    c = conn.cursor()

    # Verificar si el usuario ya existe
    c.execute("SELECT id_discord FROM usuarios WHERE id_discord = ?", (usuario_id,))
    if c.fetchone():
        conn.close()
        return False  # Usuario ya registrado

    # Si el usuario no está registrado, lo insertamos
    c.execute(
        "INSERT INTO usuarios (id_discord, nombre_usuario) VALUES (?, ?)",
        (usuario_id, nombre_usuario),
    )
    conn.commit()
    conn.close()
    return True  # Usuario registrado exitosamente


# Función para verificar si un usuario ya está registrado
def verificar_usuario(usuario_id):
    conn = sqlite3.connect("perfil_inversion.db")
    c = conn.cursor()

    # Comprobamos si el usuario ya está registrado
    c.execute("SELECT id_discord FROM usuarios WHERE id_discord = ?", (usuario_id,))
    if c.fetchone():
        conn.close()
        return True  # Usuario ya registrado

    conn.close()
    return False  # Usuario no registrado

<<<<<<< HEAD
# Función para obtener un usuario por ID
def obtener_usuario(usuario_id):
    conn = sqlite3.connect('perfil_inversion.db')
    c = conn.cursor()
    c.execute('SELECT nombre_usuario FROM usuarios WHERE id_discord = ?', (usuario_id,))
    usuario = c.fetchone()
    conn.close()
    if usuario:
        return usuario[0]  # Retorna el nombre del usuario
    return None  # Si el usuario no existe, retorna None

=======

# Función para iniciar sesión con un usuario existente
def iniciar_sesion(usuario_id):
    if verificar_usuario(usuario_id):
        return True  # Sesión iniciada
    else:
        return False  # Usuario no registrado
>>>>>>> refs/remotes/origin/main


# Función para obtener el perfil de un usuario
def obtener_perfil_usuario(usuario_id):
    conn = sqlite3.connect("perfil_inversion.db")
    c = conn.cursor()
    c.execute("SELECT perfil FROM perfiles WHERE user_id = ?", (usuario_id,))
    perfil = c.fetchone()
    conn.close()
    if perfil:
        return perfil[0]
    return None


<<<<<<< HEAD
# Función para obtener el capital del usuario
def obtener_capital(usuario_id):
    conn = sqlite3.connect('perfil_inversion.db')
    c = conn.cursor()
    c.execute('SELECT capital FROM capital WHERE usuario_id = ?', (usuario_id,))
    capital = c.fetchone()
    conn.close()
    return capital[0] if capital else 0


# Función para actualizar el capital del usuario
def actualizar_capital(usuario_id, monto):
    conn = sqlite3.connect('perfil_inversion.db')
    c = conn.cursor()

    # Obtener el saldo actual del usuario
    c.execute('SELECT capital FROM capital WHERE usuario_id = ?', (usuario_id,))
    capital_actual = c.fetchone()

    if capital_actual:
        # Si el usuario ya tiene un capital, actualizamos el saldo
        new_capital = capital_actual[0] + monto
        c.execute(
            'UPDATE capital SET capital = ? WHERE usuario_id = ?',
            (new_capital, usuario_id),
        )
    else:
        # Si el usuario no tiene un capital, lo insertamos
        c.execute(
            'INSERT INTO capital (usuario_id, capital) VALUES (?, ?)',
            (usuario_id, monto),
        )

    conn.commit()
    conn.close()
    return new_capital  # Retorna el nuevo saldo después de la actualización


# Función para realizar una inversión
def realizar_inversion(usuario_id, nombre_inversion, tipo_inversion, cantidad_invertida, valor_invertido):
    conn = sqlite3.connect('perfil_inversion.db')
    c = conn.cursor()

    # Insertar la inversión en la tabla de inversiones
    c.execute('''
        INSERT INTO inversiones (id_discord, nombre_inversion, tipo_inversion, cantidad_invertida, valor_invertido)
        VALUES (?, ?, ?, ?, ?)
    ''', (usuario_id, nombre_inversion, tipo_inversion, cantidad_invertida, valor_invertido))

    # Actualizar el capital del usuario
    actualizar_capital(usuario_id, -valor_invertido)  # Restar el monto invertido

    conn.commit()
    conn.close()

=======
def obtener_usuario(usuario_id):
    conn = sqlite3.connect("perfil_inversion.db")
    c = conn.cursor()
    c.execute("SELECT usuario FROM usuarios WHERE usuario_id = ?", (usuario_id,))
    usuario = c.fetchone()
    conn.close()
    if usuario:
        return usuario[0]
    return None


>>>>>>> refs/remotes/origin/main
# Función para guardar o actualizar el perfil de un usuario
def guardar_perfil_usuario(usuario_id, perfil):
    conn = sqlite3.connect("perfil_inversion.db")
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO perfiles (user_id, perfil) 
        VALUES (?, ?) 
        ON CONFLICT(user_id) 
        DO UPDATE SET perfil = ?
    """,
        (usuario_id, perfil, perfil),
    )
    conn.commit()
    conn.close()

<<<<<<< HEAD
=======

# Función para gestionar el capital del usuario (sumar o restar)
def gestionar_capital(usuario_id, cantidad, operacion):
    conn = sqlite3.connect("perfil_inversion.db")
    c = conn.cursor()

    # Verificar si el capital ya existe para el usuario
    c.execute("SELECT capital FROM capital WHERE usuario_id = ?", (usuario_id,))
    capital_actual = c.fetchone()

    if capital_actual:
        # Si el usuario ya tiene un capital registrado, actualizarlo
        if operacion == "sumar":
            c.execute(
                "UPDATE capital SET capital = capital + ? WHERE usuario_id = ?",
                (cantidad, usuario_id),
            )
        elif operacion == "restar":
            c.execute(
                "UPDATE capital SET capital = capital - ? WHERE usuario_id = ?",
                (cantidad, usuario_id),
            )
    else:
        # Si el usuario no tiene un capital registrado, se le asigna el valor inicial
        c.execute(
            "INSERT INTO capital (usuario_id, capital) VALUES (?, ?)",
            (usuario_id, cantidad),
        )

    conn.commit()
    conn.close()


# Función para obtener el capital actual de un usuario
def obtener_capital(usuario_id):
    conn = sqlite3.connect("perfil_inversion.db")
    c = conn.cursor()
    c.execute("SELECT capital FROM capital WHERE usuario_id = ?", (usuario_id,))
    capital = c.fetchone()
    conn.close()
    return capital[0] if capital else 0


# Función para actualizar el capital de un usuario
def actualizar_capital(usuario_id, monto):
    conn = sqlite3.connect("perfil_inversion.db")
    c = conn.cursor()

    # Obtener el saldo actual del usuario
    c.execute("SELECT capital FROM capital WHERE usuario_id = ?", (usuario_id,))
    capital_actual = c.fetchone()

    if capital_actual:
        # Si el usuario ya tiene un capital, actualizamos el saldo
        new_capital = capital_actual[0] + monto
        c.execute(
            "UPDATE capital SET capital = ? WHERE usuario_id = ?",
            (new_capital, usuario_id),
        )
    else:
        # Si el usuario no tiene un capital, lo insertamos
        c.execute(
            "INSERT INTO capital (usuario_id, capital) VALUES (?, ?)",
            (usuario_id, monto),
        )

    conn.commit()
    conn.close()
    return new_capital  # Retorna el nuevo saldo después de la actualización


>>>>>>> refs/remotes/origin/main
# Función para guardar el progreso de las respuestas
def guardar_progreso(usuario_id, respuestas_json):
    conn = sqlite3.connect("perfil_inversion.db")
    c = conn.cursor()
<<<<<<< HEAD
    c.execute('''
=======
    c.execute(
        """
>>>>>>> refs/remotes/origin/main
        INSERT OR REPLACE INTO progreso (usuario_id, respuestas)
        VALUES (?, ?)
    """,
        (usuario_id, respuestas_json),
    )
    conn.commit()
    conn.close()


# Función para obtener el progreso guardado
def obtener_progreso(usuario_id):
    conn = sqlite3.connect("perfil_inversion.db")
    c = conn.cursor()
<<<<<<< HEAD
    c.execute('SELECT respuestas FROM progreso WHERE usuario_id = ?', (usuario_id,))
=======
    c.execute("SELECT respuestas FROM progreso WHERE usuario_id = ?", (usuario_id,))
>>>>>>> refs/remotes/origin/main
    progreso = c.fetchone()
    conn.close()
    if progreso:
        return progreso[0]
    return None


# Función para eliminar el progreso del perfil
def eliminar_progreso(usuario_id):
    conn = sqlite3.connect("perfil_inversion.db")
    c = conn.cursor()
<<<<<<< HEAD
    c.execute('DELETE FROM progreso WHERE usuario_id = ?', (usuario_id,))
=======
    c.execute("DELETE FROM progreso WHERE usuario_id = ?", (usuario_id,))
    conn.commit()
    conn.close()


# Función para realizar una inversión
def realizar_inversion(
    usuario_id, nombre_inversion, tipo_inversion, cantidad_invertida, valor_invertido
):
    conn = sqlite3.connect("perfil_inversion.db")
    c = conn.cursor()

    # Insertar la inversión en la tabla de inversiones
    c.execute(
        """
        INSERT INTO inversiones (id_discord, nombre_inversion, tipo_inversion, cantidad_invertida, valor_invertido)
        VALUES (?, ?, ?, ?, ?)
    """,
        (
            usuario_id,
            nombre_inversion,
            tipo_inversion,
            cantidad_invertida,
            valor_invertido,
        ),
    )

    # Actualizar el capital del usuario
    actualizar_capital(usuario_id, -valor_invertido)  # Restar el monto invertido

>>>>>>> refs/remotes/origin/main
    conn.commit()
    conn.close()
