import sqlite3
import json

# Función para inicializar la base de datos
def inicializar_db():
    conn = sqlite3.connect('perfil_inversion.db')
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id_discord TEXT PRIMARY KEY,
            nombre_usuario TEXT NOT NULL,
            capital REAL DEFAULT 0.0,
            fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS perfiles (
            user_id TEXT PRIMARY KEY,
            perfil TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES usuarios(id_discord)
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS inversiones (
            id_inversion INTEGER PRIMARY KEY AUTOINCREMENT,
            id_discord TEXT,
            nombre_inversion TEXT,
            tipo_inversion TEXT,
            valor_perfil_inversor INTEGER,
            FOREIGN KEY (id_discord) REFERENCES usuarios(id_discord)
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS capital (
            usuario_id TEXT PRIMARY KEY,
            capital REAL DEFAULT 0,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id_discord)
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS progreso (
            usuario_id TEXT PRIMARY KEY,
            respuestas JSON,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id_discord)
        )
    ''')

    conn.commit()
    conn.close()

# Función para registrar un nuevo usuario
def registrar_usuario(usuario_id, nombre_usuario):
    conn = sqlite3.connect('perfil_inversion.db')
    c = conn.cursor()

    # Verificar si el usuario ya existe
    c.execute("SELECT id_discord FROM usuarios WHERE id_discord = ?", (usuario_id,))
    if c.fetchone():
        conn.close()
        return False  # Usuario ya registrado
    
    # Si el usuario no está registrado, lo insertamos
    c.execute("INSERT INTO usuarios (id_discord, nombre_usuario) VALUES (?, ?)", 
              (usuario_id, nombre_usuario))
    conn.commit()
    conn.close()
    return True  # Usuario registrado exitosamente

# Función para verificar si un usuario ya está registrado
def verificar_usuario(usuario_id):
    conn = sqlite3.connect('perfil_inversion.db')
    c = conn.cursor()
    
    # Comprobamos si el usuario ya está registrado
    c.execute("SELECT id_discord FROM usuarios WHERE id_discord = ?", (usuario_id,))
    if c.fetchone():
        conn.close()
        return True  # Usuario ya registrado
    
    conn.close()
    return False  # Usuario no registrado

# Función para iniciar sesión con un usuario existente
def iniciar_sesion(usuario_id):
    if verificar_usuario(usuario_id):
        return True  # Sesión iniciada
    else:
        return False  # Usuario no registrado

# Función para obtener el perfil de un usuario
def obtener_perfil_usuario(usuario_id):
    conn = sqlite3.connect('perfil_inversion.db')
    c = conn.cursor()
    c.execute('SELECT perfil FROM perfiles WHERE user_id = ?', (usuario_id,))
    perfil = c.fetchone()
    conn.close()
    if perfil:
        return perfil[0]
    return None

# Función para guardar o actualizar el perfil de un usuario
def guardar_perfil_usuario(usuario_id, perfil):
    conn = sqlite3.connect('perfil_inversion.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO perfiles (user_id, perfil) 
        VALUES (?, ?) 
        ON CONFLICT(user_id) 
        DO UPDATE SET perfil = ?
    ''', (usuario_id, perfil, perfil))
    conn.commit()
    conn.close()

# Función para gestionar el capital del usuario (sumar o restar)
def gestionar_capital(usuario_id, cantidad, operacion):
    conn = sqlite3.connect('perfil_inversion.db')
    c = conn.cursor()
    
    # Verificar si el capital ya existe para el usuario
    c.execute("SELECT capital FROM capital WHERE usuario_id = ?", (usuario_id,))
    capital_actual = c.fetchone()

    if capital_actual:
        # Si el usuario ya tiene un capital registrado, actualizarlo
        if operacion == 'sumar':
            c.execute("UPDATE capital SET capital = capital + ? WHERE usuario_id = ?", (cantidad, usuario_id))
        elif operacion == 'restar':
            c.execute("UPDATE capital SET capital = capital - ? WHERE usuario_id = ?", (cantidad, usuario_id))
    else:
        # Si el usuario no tiene un capital registrado, se le asigna el valor inicial
        c.execute("INSERT INTO capital (usuario_id, capital) VALUES (?, ?)", (usuario_id, cantidad))

    conn.commit()
    conn.close()


# Función para obtener el capital actual de un usuario
def obtener_capital(usuario_id):
    conn = sqlite3.connect('perfil_inversion.db')
    c = conn.cursor()
    c.execute("SELECT capital FROM capital WHERE usuario_id = ?", (usuario_id,))
    capital = c.fetchone()
    conn.close()
    return capital[0] if capital else 0

# Función para obtener el capital actual de un usuario
def obtener_capital(usuario_id):
    conn = sqlite3.connect('perfil_inversion.db')
    c = conn.cursor()
    c.execute("SELECT capital FROM capital WHERE usuario_id = ?", (usuario_id,))
    capital = c.fetchone()
    conn.close()
    return capital[0] if capital else 0


# Función para actualizar el capital del usuario (agregar o restar dinero)
def actualizar_capital(usuario_id, monto):
    capital_actual = obtener_capital(usuario_id)

    # Actualizamos el capital (sumamos el monto)
    gestionar_capital(usuario_id, monto, 'sumar')

    # Retornamos el nuevo capital
    return capital_actual + monto

# Función para guardar el progreso de las respuestas
def guardar_progreso(usuario_id, respuestas_json):
    conn = sqlite3.connect('perfil_inversion.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO progreso_perfil (usuario_id, respuestas)
        VALUES (?, ?)
    ''', (usuario_id, respuestas_json))
    conn.commit()
    conn.close()

# Función para obtener el progreso guardado
def obtener_progreso(usuario_id):
    conn = sqlite3.connect('perfil_inversion.db')
    c = conn.cursor()
    c.execute('SELECT respuestas FROM progreso_perfil WHERE usuario_id = ?', (usuario_id,))
    progreso = c.fetchone()
    conn.close()
    if progreso:
        return progreso[0]
    return None

# Función para eliminar el progreso del perfil
def eliminar_progreso(usuario_id):
    conn = sqlite3.connect('perfil_inversion.db')
    c = conn.cursor()
    c.execute('DELETE FROM progreso_perfil WHERE usuario_id = ?', (usuario_id,))
    conn.commit()
    conn.close()
