# Función para obtener opciones de inversión basadas en el perfil
def obtener_opciones_por_perfil(perfil):
    opciones_filtradas = [opcion for opcion in opciones_json['opciones_inversion'] if opcion['perfil'] == perfil]
    return opciones_filtradas
