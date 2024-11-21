import sqlite3

# Función para inicializar la base de datos
def inicializar_db():
    conn = sqlite3.connect('perfil_inversion.db')  # Crea o abre la base de datos
    c = conn.cursor()
    # Crear la tabla de perfiles si no existe
    c.execute('''
        CREATE TABLE IF NOT EXISTS perfiles (
            user_id INTEGER PRIMARY KEY,
            perfil TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Función para obtener el perfil de un usuario
def obtener_perfil_usuario(user_id):
    conn = sqlite3.connect('perfil_inversion.db')
    c = conn.cursor()
    c.execute('SELECT perfil FROM perfiles WHERE user_id = ?', (user_id,))
    perfil = c.fetchone()  # Obtener el perfil
    conn.close()
    if perfil:
        return perfil[0]
    raise Exception("No encontramos el perfil.")

# Función para guardar el perfil de un usuario
def guardar_perfil_usuario(user_id, perfil):
    conn = sqlite3.connect('perfil_inversion.db')
    c = conn.cursor()
    # Si el perfil ya existe, actualízalo; de lo contrario, insértalo
    c.execute('''
        INSERT INTO perfiles (user_id, perfil) 
        VALUES (?, ?) 
        ON CONFLICT(user_id) 
        DO UPDATE SET perfil = ?
    ''', (user_id, perfil, perfil))
    conn.commit()
    conn.close()
