import json
from pathlib import Path


# Cargar las opciones desde un archivo JSON
def cargar_opciones():
    # Asegurarse de que el archivo se encuentra en el directorio correcto
    p = Path(
        "/home/etec/InvertBot/opciones/opciones_de_acuerdo_al_perfil_del_inversor.json"
    )

    # Verifica si el archivo existe
    if not p.exists():
        raise FileNotFoundError(f"El archivo {p} no fue encontrado.")

    # Cargar y retornar el contenido del archivo JSON
    try:
        with open(p, "r") as f:
            opciones_json = json.load(f)
        return opciones_json
    except json.JSONDecodeError:
        raise ValueError(
            f"Error al leer el archivo JSON. Asegúrate de que el formato es correcto."
        )


# Función para obtener opciones de inversión basadas en el perfil
def obtener_opciones_por_perfil(perfil):
    try:
        opciones_json = cargar_opciones()  # Cargar las opciones desde el archivo JSON
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return []  # Devuelve una lista vacía si hay un error en la carga del archivo

    # Verificar que 'opciones_inversion' esté presente en el JSON cargado
    if "opciones_inversion" not in opciones_json:
        raise KeyError("El archivo JSON no contiene la clave 'opciones_inversion'.")

    # Filtrar las opciones basadas en el perfil
    opciones_filtradas = [
        opcion
        for opcion in opciones_json["opciones_inversion"]
        if opcion["perfil"] == perfil
    ]

    # Mostrar información detallada de cada opción filtrada
    return opciones_filtradas


# Ejemplo de uso
perfil = "Agresivo"  # Por ejemplo, "Conservador", "Moderado", "Agresivo"
opciones = obtener_opciones_por_perfil(perfil)
if opciones:
    print(f"Opciones de inversión para el perfil {perfil}:")
    for opcion in opciones:
        print(f"\nNombre: {opcion['nombre']}")
        print(f"Tipo de inversión: {opcion['tipo_inversion']}")
        print(f"Precio: {opcion['precio']}")
        print(f"Descripción: {opcion['descripcion']}")
        print("-" * 40)
else:
    print(f"No se encontraron opciones para el perfil {perfil}.")
