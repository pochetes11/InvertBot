import json

# Cargar las opciones desde un archivo JSON
def cargar_opciones():  
    with open('opciones_de_acuerdo_al_perfil_del_inversor.json', 'r') as f:
        opciones_json = json.load(f)
    return opciones_json

# Función para obtener opciones de inversión basadas en el perfil
def obtener_opciones_por_perfil(perfil):
    opciones_json = cargar_opciones()  # Asegúrate de que opciones_json esté definido

    opciones_filtradas = [opcion for opcion in opciones_json['opciones_inversion'] if opcion['perfil'] == perfil]
    return opciones_filtradas