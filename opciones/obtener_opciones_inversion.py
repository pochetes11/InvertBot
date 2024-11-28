import random

# Opciones de inversión predefinidas
def obtener_opciones_inversion():
    # Opciones de inversión definidas con perfiles específicos
    opciones_inversion_json = [
        {"nombre": "Bonos del gobierno", "tipo_inversion": "Bonos", "valor_perfil_inversor": 2, "perfil": "Conservador"},
        {"nombre": "Acciones de empresas consolidadas", "tipo_inversion": "Acciones", "valor_perfil_inversor": 4, "perfil": "Moderado"},
        {"nombre": "Fondos mutuos de renta fija", "tipo_inversion": "Fondos", "valor_perfil_inversor": 3, "perfil": "Conservador"},
        {"nombre": "Ethereum", "tipo_inversion": "Criptomonedas", "valor_perfil_inversor": 7, "perfil": "Agresivo"},
        {"nombre": "Bonos corporativos de alto rendimiento", "tipo_inversion": "Bonos", "valor_perfil_inversor": 6, "perfil": "Moderado"},
        {"nombre": "Acciones de startups tecnológicas", "tipo_inversion": "Acciones", "valor_perfil_inversor": 8, "perfil": "Agresivo"},
        {"nombre": "Inversión en bienes raíces", "tipo_inversion": "Bienes raíces", "valor_perfil_inversor": 5, "perfil": "Moderado"},
        {"nombre": "Oro y metales preciosos", "tipo_inversion": "Commodities", "valor_perfil_inversor": 3, "perfil": "Conservador"},
        {"nombre": "Acciones de tecnología emergente", "tipo_inversion": "Acciones", "valor_perfil_inversor": 9, "perfil": "Agresivo"}
    ]
    
    # Opciones predefinidas no asignadas a un perfil específico
    opciones_predefinidas = [
        "Bonos de empresa A", "Bonos de empresa B", "Acciones de empresa C", "Acciones de empresa D",
        "Ethereum (ETH)", "Bitcoin (BTC)", "Litecoin (LTC)", "Fondos de inversión en bienes raíces", 
        "Acciones de tecnología", "Acciones de energía renovable", "Criptomonedas emergentes", 
        "Bonos del gobierno", "Fondos de inversión diversificados", "Acciones de salud", "Acciones de consumo", 
        "Acciones de energía solar", "Acciones de telecomunicaciones", "Fondos cotizados (ETFs) de criptomonedas", 
        "Bonos de alto rendimiento", "Criptomonedas de bajo capital", "Acciones de aerolíneas", 
        "Bonos de infraestructura", "Acciones de viajes y turismo", "Acciones de servicios financieros", 
        "Bonos municipales", "Inversiones en startups", "Acciones de comercio electrónico", 
        "Bonos de empresas tecnológicas", "Criptomonedas estables", "Fondos de inversión en tecnología", 
        "Acciones de servicios públicos"
    ]

    # Combinar las opciones predefinidas con las opciones definidas por el perfil
    opciones_combinadas = opciones_inversion_json + [
        {"nombre": opcion, "tipo_inversion": "Variedad", "valor_perfil_inversor": random.randint(1, 10), "perfil": "Diversificado"} 
        for opcion in opciones_predefinidas
    ]

    # Eliminar duplicados basados en el nombre de la inversión
    opciones_combinadas_unicas = {opcion["nombre"]: opcion for opcion in opciones_combinadas}.values()

    # Convertir a lista y mezclar las opciones aleatoriamente
    opciones_combinadas_lista = list(opciones_combinadas_unicas)
    random.shuffle(opciones_combinadas_lista)

    return opciones_combinadas_lista
