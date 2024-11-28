from db import obtener_perfil_usuario

async def intentar_obtener_el_perfil_del_inversor(id:str)->str: 
    try:
        perfil = obtener_perfil_usuario(id)   # Obtener perfil desde la base de datos
        return f"Tu perfil de inversión es: {perfil}"
    except:   
        return "No se ha encontrado un perfil para ti. Por favor, completa la evaluación de perfil."
    