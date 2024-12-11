import sqlite3
# Función para inicializar la base de datos
def inicializar_db():
    conn = sqlite3.connect('perfil_inversion.db')  # Crea o abre la base de datos
    c = conn.cursor()
    # Crear la tabla de usuarios si no existe
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id_discord TEXT PRIMARY KEY,
            nombre_usuario TEXT NOT NULL,
            fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
            capital REAL DEFAULT 0
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS respuestas_perfil (
            usuario_id TEXT PRIMARY KEY,
            objetivo_inversion TEXT,
            horizonte_temporal TEXT,
            tiempo_mantener TEXT,
            nivel_experiencia TEXT,
            capital_inicial TEXT,
            ingreso_anual TEXT,
            nivel_deuda TEXT,
            porcentaje_ingresos_invertir TEXT,
            tolerancia_riesgo TEXT,
            inversiones_activas TEXT,
            ingresos_o_crecimiento TEXT,
            reaccion_perdida TEXT,
            productos_financieros TEXT,
            preferencias_sector TEXT,
            mercados_nacionales_o_internacionales TEXT,
            conocimiento_mercado TEXT,
            volatilidad_mercado TEXT,
            sostenibilidad TEXT,
            preocupaciones_inversiones TEXT,
            expectativa_rendimiento TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id_discord)
        )
    ''')

    conn.commit()
    conn.close()

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

# Función para guardar el perfil de un usuario
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

# Función para obtener el capital de un usuario
def obtener_capital_usuario(usuario_id):
    conn = sqlite3.connect('perfil_inversion.db')
    c = conn.cursor()
    c.execute('SELECT capital FROM usuarios WHERE id_discord = ?', (usuario_id,))
    capital = c.fetchone()
    conn.close()
    if capital:
        return capital[0]
    return 0

# Función para actualizar el capital de un usuario
def actualizar_capital_usuario(usuario_id, cantidad):
    conn = sqlite3.connect('perfil_inversion.db')
    c = conn.cursor()
    c.execute('UPDATE usuarios SET capital = capital + ? WHERE id_discord = ?', (cantidad, usuario_id))
    conn.commit()
    conn.close()
