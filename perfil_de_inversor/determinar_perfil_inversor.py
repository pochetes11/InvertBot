from db.db import (
    obtener_perfil_usuario,
    guardar_perfil_usuario,
    obtener_progreso,
    guardar_progreso,
    eliminar_progreso,
)


def alguna_funcion():
    from db.db import obtener_perfil_usuario

    # Resto del código


# Función para obtener el cuestionario para determinar el perfil del inversor
def obtener_cuestionario_para_determinar_perfil_del_inversor():
    preguntas = [
        (
            "¿Cuál es su principal objetivo de inversión?",
            [
                "A) Crecimiento de capital",
                "B) Generación de ingresos regulares",
                "C) Preservación del capital",
                "D) Diversificación del patrimonio",
            ],
        ),
        (
            "¿Cuál es el horizonte temporal para sus inversiones?",
            ["A) Menos de 1 año", "B) 1-3 años", "C) 3-5 años", "D) Más de 5 años"],
        ),
        (
            "¿Cuánto tiempo está dispuesto a mantener sus inversiones sin necesidad de acceder a los fondos?",
            ["A) Menos de 6 meses", "B) 6-12 meses", "C) 1-3 años", "D) Más de 3 años"],
        ),
        (
            "¿Cuál es su nivel de experiencia con inversiones?",
            ["A) Principiante", "B) Intermedio", "C) Avanzado"],
        ),
        (
            "¿Cuánto capital está dispuesto a invertir inicialmente?",
            [
                "A) Menos de $1,000",
                "B) $1,000 - $10,000",
                "C) $10,000 - $50,000",
                "D) Más de $50,000",
            ],
        ),
        (
            "¿Cuál es su ingreso anual aproximado?",
            [
                "A) Menos de $20,000",
                "B) $20,000 - $50,000",
                "C) $50,000 - $100,000",
                "D) Más de $100,000",
            ],
        ),
        (
            "¿Cuál es su nivel de deuda actual y cómo maneja sus obligaciones financieras?",
            [
                "A) Alta deuda, dificultades para manejarla",
                "B) Deuda moderada, manejable",
                "C) Baja deuda, buen manejo",
                "D) Sin deuda",
            ],
        ),
        (
            "¿Qué porcentaje de sus ingresos está dispuesto a invertir?",
            ["A) Menos del 5%", "B) 5-10%", "C) 10-20%", "D) Más del 20%"],
        ),
        (
            "¿Cómo describiría su tolerancia al riesgo?",
            ["A) Baja", "B) Moderada", "C) Alta"],
        ),
        (
            "¿Cuáles son sus inversiones actuales?",
            [
                "A) Acciones",
                "B) Bonos",
                "C) Bienes raíces",
                "D) Fondos mutuos",
                "E) Otros",
            ],
        ),
        (
            "¿Está buscando inversiones que generen ingresos regulares o crecimiento del capital a largo plazo?",
            ["A) Ingresos regulares", "B) Crecimiento del capital", "C) Ambos"],
        ),
        (
            "¿Cómo reaccionaría si su inversión principal pierde un 10% de su valor en un corto período de tiempo?",
            [
                "A) Vendería todo",
                "B) Vendería parte",
                "C) Mantendría la inversión",
                "D) Invertiría más",
            ],
        ),
        (
            "¿Qué tipo de productos financieros prefiere o ha utilizado anteriormente?",
            [
                "A) Fondos de inversión",
                "B) Acciones",
                "C) Bonos",
                "D) Criptomonedas",
                "E) Otros",
            ],
        ),
        (
            "¿Tiene alguna preferencia en cuanto a sectores o industrias en los que invertir?",
            [
                "A) Tecnología",
                "B) Salud",
                "C) Energía",
                "D) Bienes de consumo",
                "E) No tengo preferencia",
            ],
        ),
        (
            "¿Está dispuesto a invertir en mercados internacionales o prefiere limitarse a mercados nacionales?",
            [
                "A) Solo nacionales",
                "B) Solo internacionales",
                "C) Ambos, sin preferencia",
            ],
        ),
        (
            "¿Cuánto conocimiento tiene sobre las tendencias y movimientos del mercado financiero?",
            ["A) Ninguno", "B) Básico", "C) Intermedio", "D) Avanzado"],
        ),
        (
            "¿Cuál es su nivel de comodidad con la volatilidad del mercado?",
            ["A) Muy incómodo", "B) Incómodo", "C) Cómodo", "D) Muy cómodo"],
        ),
        (
            "¿Qué importancia le da a la sostenibilidad y a las inversiones socialmente responsables?",
            [
                "A) Muy importante",
                "B) Importante",
                "C) Poco importante",
                "D) No importa",
            ],
        ),
        (
            "¿Tiene alguna preocupación específica respecto a sus inversiones?",
            [
                "A) Seguridad del capital",
                "B) Impacto fiscal",
                "C) Liquidez",
                "D) Ninguna preocupación específica",
            ],
        ),
        (
            "¿Cuál es su expectativa de rendimiento anual para sus inversiones?",
            ["A) Menos del 5%", "B) 5-10%", "C) 10-20%", "D) Más del 20%"],
        ),
    ]
    return preguntas


# Evaluación de respuestas
def evaluar_tolerancia_riesgo(respuestas):
    tolerancia = respuestas.get(
        "¿Cómo describiría su tolerancia al riesgo?", ""
    ).upper()
    return {"A": -2, "B": 0, "C": 2}.get(tolerancia, 0)


def evaluar_horizonte_inversion(respuestas):
    if (
        respuestas.get(
            "¿Cuál es el horizonte temporal para sus inversiones?", ""
        ).upper()
        == "A"
    ):
        return -2
    elif (
        respuestas.get(
            "¿Cuál es el horizonte temporal para sus inversiones?", ""
        ).upper()
        == "B"
    ):
        return 0
    elif (
        respuestas.get(
            "¿Cuál es el horizonte temporal para sus inversiones?", ""
        ).upper()
        == "C"
    ):
        return 1
    elif (
        respuestas.get(
            "¿Cuál es el horizonte temporal para sus inversiones?", ""
        ).upper()
        == "D"
    ):
        return 2
    return 0


def evaluar_capital_inicial(respuestas):
    if (
        respuestas.get(
            "¿Cuánto capital está dispuesto a invertir inicialmente?", ""
        ).upper()
        == "A"
    ):
        return -2
    elif (
        respuestas.get(
            "¿Cuánto capital está dispuesto a invertir inicialmente?", ""
        ).upper()
        == "B"
    ):
        return 0
    elif (
        respuestas.get(
            "¿Cuánto capital está dispuesto a invertir inicialmente?", ""
        ).upper()
        == "C"
    ):
        return 2
    elif (
        respuestas.get(
            "¿Cuánto capital está dispuesto a invertir inicialmente?", ""
        ).upper()
        == "D"
    ):
        return 4
    return 0


def evaluar_experiencia_inversion(respuestas):
    if (
        respuestas.get("¿Cuál es su nivel de experiencia con inversiones?", "").upper()
        == "A"
    ):
        return -2
    elif (
        respuestas.get("¿Cuál es su nivel de experiencia con inversiones?", "").upper()
        == "B"
    ):
        return 0
    elif (
        respuestas.get("¿Cuál es su nivel de experiencia con inversiones?", "").upper()
        == "C"
    ):
        return 2
    return 0


def determinar_perfil(respuestas):
    puntaje = 0
    puntaje += evaluar_tolerancia_riesgo(respuestas)
    puntaje += evaluar_horizonte_inversion(respuestas)
    puntaje += evaluar_capital_inicial(respuestas)
    puntaje += evaluar_experiencia_inversion(respuestas)

    LIMITE_CONSERVADOR = 0
    LIMITE_MODERADO = 5

    if puntaje < LIMITE_CONSERVADOR:
        return "Conservador"
    elif puntaje < LIMITE_MODERADO:
        return "Moderado"
    else:
        return "Agresivo"


# Modificar para que las importaciones no se realicen al principio del archivo
def obtener_perfil_usuario(user_id):
    from db.db import obtener_perfil_usuario  # Importación dentro de la función

    perfil = obtener_perfil_usuario(user_id)
    if perfil:
        return f"Tu perfil de inversión es: {perfil}"
    else:
        return "No se ha encontrado un perfil para ti. Por favor, completa la evaluación de perfil."
