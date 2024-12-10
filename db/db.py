import sqlite3
from perfil_de_inversor.determinar_perfil_inversor import determinar_perfil


def inicializar_db():
    conn = sqlite3.connect("perfil_inversion.db")
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id_discord TEXT PRIMARY KEY,
            nombre_usuario TEXT NOT NULL,
            capital REAL DEFAULT 0.0,
            fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
        )"""
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS perfiles (
            user_id TEXT PRIMARY KEY,
            perfil TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES usuarios(id_discord)
        )"""
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS inversiones (
            id_inversion INTEGER PRIMARY KEY AUTOINCREMENT,
            id_discord TEXT,
            nombre_inversion TEXT,
            tipo_inversion TEXT,
            cantidad_invertida REAL,
            valor_invertido REAL,
            fecha_inversion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_discord) REFERENCES usuarios(id_discord)
        )"""
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS capital (
            usuario_id TEXT PRIMARY KEY,
            capital REAL DEFAULT 0,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id_discord)
        )"""
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS progreso (
            usuario_id TEXT PRIMARY KEY,
            respuestas JSON,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id_discord)
        )"""
    )
    conn.commit()
    conn.close()


def registrar_usuario(usuario_id, nombre_usuario):
    conn = sqlite3.connect("perfil_inversion.db")
    c = conn.cursor()
    c.execute("SELECT id_discord FROM usuarios WHERE id_discord = ?", (usuario_id,))
    if c.fetchone():
        conn.close()
        return False
    c.execute(
        "INSERT INTO usuarios (id_discord, nombre_usuario) VALUES (?, ?)",
        (usuario_id, nombre_usuario),
    )
    conn.commit()
    conn.close()
    return True


def obtener_perfil_usuario(usuario_id):
    conn = sqlite3.connect("perfil_inversion.db")
    c = conn.cursor()
    c.execute("SELECT perfil FROM perfiles WHERE user_id = ?", (usuario_id,))
    perfil = c.fetchone()
    conn.close()
    return perfil[0] if perfil else None


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


def eliminar_perfil_usuario(usuario_id):
    conn = sqlite3.connect("perfil_inversion.db")
    c = conn.cursor()
    c.execute("SELECT 1 FROM perfiles WHERE user_id = ?", (usuario_id,))
    if not c.fetchone():
        conn.close()
        return "El usuario no tiene un perfil para eliminar."
    c.execute("DELETE FROM perfiles WHERE user_id = ?", (usuario_id,))
    conn.commit()
    conn.close()
    return f"El perfil de {usuario_id} ha sido eliminado."


def realizar_inversion(
    usuario_id, nombre_inversion, tipo_inversion, cantidad_invertida, valor_invertido
):
    conn = sqlite3.connect("perfil_inversion.db")
    c = conn.cursor()
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
    gestionar_capital(usuario_id, valor_invertido, "restar")
    conn.commit()
    conn.close()


def gestionar_capital(usuario_id, cantidad, operacion):
    conn = sqlite3.connect("perfil_inversion.db")
    c = conn.cursor()
    c.execute("SELECT capital FROM capital WHERE usuario_id = ?", (usuario_id,))
    capital_actual = c.fetchone()
    if capital_actual:
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
        c.execute(
            "INSERT INTO capital (usuario_id, capital) VALUES (?, ?)",
            (usuario_id, cantidad),
        )
    conn.commit()
    conn.close()


def obtener_capital(usuario_id):
    conn = sqlite3.connect("perfil_inversion.db")
    c = conn.cursor()
    c.execute("SELECT capital FROM capital WHERE usuario_id = ?", (usuario_id,))
    capital = c.fetchone()
    conn.close()
    return capital[0] if capital else 0
