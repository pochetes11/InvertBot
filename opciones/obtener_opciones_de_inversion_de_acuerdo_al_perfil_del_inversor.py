import json
from pathlib import Path


# Cargar las opciones desde un archivo JSON
def cargar_opciones():
    # Asegurarse de que el archivo se encuentra en el directorio correcto
    p = Path(
        "/home/etec/InvertBot/opciones/opciones_de_acuerdo_al_perfil_del_inversor.json"
    )
    p.resolve()
    # Verifica si el archivo existe
    if not p.exists():
        raise FileNotFoundError(f"El archivo {p} no fue encontrado.")

    with open(p, "r") as f:
        opciones_json = json.load(f)
    return opciones_json


# Función para obtener opciones de inversión basadas en el perfil
def obtener_opciones_por_perfil(perfil):
    try:
        opciones_json = (
            cargar_opciones()
        )  # Asegúrate de que opciones_json esté definido
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return []  # Devuelve una lista vacía si no se encuentra el archivo JSON

    # Filtrar las opciones basadas en el perfil
    opciones_filtradas = [
        opcion
        for opcion in opciones_json["opciones_inversion"]
        if opcion["perfil"] == perfil
    ]
    return opciones_filtradas
