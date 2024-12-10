from fastapi import FastAPI
from pydantic import BaseModel
import random
import time
from datetime import datetime
import threading

# Carga de las opciones de inversión desde el archivo JSON y datos adicionales
opciones_inversion = [
    {
        "id": 1,
        "nombre": "Bonos del gobierno",
        "tipo_inversion": "Bonos",
        "valor_perfil_inversor": 2,
        "perfil": "Conservador",
        "precio": 1000,
    },
    {
        "id": 2,
        "nombre": "Acciones de empresas consolidadas",
        "tipo_inversion": "Acciones",
        "valor_perfil_inversor": 4,
        "perfil": "Moderado",
        "precio": 50,
    },
    {
        "id": 3,
        "nombre": "Fondos mutuos de renta fija",
        "tipo_inversion": "Fondos",
        "valor_perfil_inversor": 3,
        "perfil": "Conservador",
        "precio": 500,
    },
    {
        "id": 4,
        "nombre": "Ethereum",
        "tipo_inversion": "Criptomonedas",
        "valor_perfil_inversor": 7,
        "perfil": "Agresivo",
        "precio": 1800,
    },
    {
        "id": 5,
        "nombre": "Bonos corporativos de alto rendimiento",
        "tipo_inversion": "Bonos",
        "valor_perfil_inversor": 6,
        "perfil": "Moderado",
        "precio": 2000,
    },
    {
        "id": 6,
        "nombre": "Acciones de startups tecnológicas",
        "tipo_inversion": "Acciones",
        "valor_perfil_inversor": 8,
        "perfil": "Agresivo",
        "precio": 20,
    },
    {
        "id": 7,
        "nombre": "Inversión en bienes raíces",
        "tipo_inversion": "Bienes raíces",
        "valor_perfil_inversor": 5,
        "perfil": "Moderado",
        "precio": 15000,
    },
    {
        "id": 8,
        "nombre": "Oro y metales preciosos",
        "tipo_inversion": "Commodities",
        "valor_perfil_inversor": 3,
        "perfil": "Conservador",
        "precio": 1800,
    },
    {
        "id": 9,
        "nombre": "Acciones de tecnología emergente",
        "tipo_inversion": "Acciones",
        "valor_perfil_inversor": 9,
        "perfil": "Agresivo",
        "precio": 100,
    },
    {
        "id": 10,
        "nombre": "Bitcoin (BTC)",
        "tipo_inversion": "Criptomonedas",
        "valor_perfil_inversor": 8,
        "perfil": "Agresivo",
        "precio": 25000,
    },
    {
        "id": 11,
        "nombre": "Acciones de energía renovable",
        "tipo_inversion": "Acciones",
        "valor_perfil_inversor": 5,
        "perfil": "Moderado",
        "precio": 120,
    },
    {
        "id": 12,
        "nombre": "Bonos municipales",
        "tipo_inversion": "Bonos",
        "valor_perfil_inversor": 3,
        "perfil": "Conservador",
        "precio": 900,
    },
    {
        "id": 13,
        "nombre": "Fondos de inversión diversificados",
        "tipo_inversion": "Fondos",
        "valor_perfil_inversor": 4,
        "perfil": "Moderado",
        "precio": 800,
    },
]

# Creación de la aplicación FastAPI
app = FastAPI()


# Actualización de precios cada hora
def actualizar_precios():
    while True:
        for opcion in opciones_inversion:
            cambio_porcentaje = random.uniform(-2, 2)  # Variación de -2% a 2%
            nuevo_precio = opcion["precio"] * (1 + cambio_porcentaje / 100)
            # Aseguramos que los precios sean realistas (no negativos)
            opcion["precio"] = max(1, round(nuevo_precio, 2))
        time.sleep(3600)  # Espera de una hora


# Iniciar la actualización de precios en un hilo
threading.Thread(target=actualizar_precios, daemon=True).start()


# Modelo de respuesta para las opciones de inversión
class OpcionInversion(BaseModel):
    id: int
    nombre: str
    tipo_inversion: str
    valor_perfil_inversor: int
    perfil: str
    precio: float


@app.get("/opciones", response_model=list[OpcionInversion])
def obtener_opciones():
    """Retorna todas las opciones de inversión con sus precios actuales."""
    return opciones_inversion


@app.get("/opciones/{opcion_id}", response_model=OpcionInversion)
def obtener_opcion(opcion_id: int):
    """Retorna una opción de inversión específica por su ID."""
    opcion = next((op for op in opciones_inversion if op["id"] == opcion_id), None)
    if opcion is None:
        return {"error": "Opción no encontrada"}
    return opcion


# Rutas adicionales para facilitar el monitoreo
@app.get("/ultimo_actualizado")
def obtener_hora_actualizacion():
    """Retorna la última hora de actualización."""
    return {"ultima_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


# Instrucción para ejecutar el servidor
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
