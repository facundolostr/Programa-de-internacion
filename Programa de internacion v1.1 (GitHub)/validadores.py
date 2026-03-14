import re
from datetime import datetime
from config import VALIDACION, MENSAJES_ERROR

def validar_nombre_apellido(texto):
    """
    Valida que el texto contenga solo letras, espacios y caracteres especiales comunes en nombres
    
    Args:
        texto (str): Texto a validar
        
    Returns:
        tuple: (bool, str) - (es_válido, mensaje_error)
    """
    if not texto.strip():
        return False, MENSAJES_ERROR['campo_vacio']
    
    if not re.match(VALIDACION['patron_nombre'], texto):
        return False, MENSAJES_ERROR['solo_letras']
    
    if not re.search(r'[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]', texto):
        return False, MENSAJES_ERROR['debe_contener_letra']
    
    return True, ""

def validar_fecha(fecha_str):
    """
    Valida el formato y lógica de la fecha
    
    Args:
        fecha_str (str): Fecha en formato DD/MM/AAAA
        
    Returns:
        tuple: (bool, str) - (es_válido, mensaje_error)
    """
    try:
        if isinstance(fecha_str, datetime):
            fecha = fecha_str
        else:
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
        
        if fecha > datetime.today():
            return False, MENSAJES_ERROR['fecha_futura']
        return True, ""
    except ValueError:
        return False, MENSAJES_ERROR['formato_fecha']

def validar_servicio_personalizado(servicio):
    """
    Valida el servicio personalizado
    
    Args:
        servicio (str): Nombre del servicio
        
    Returns:
        tuple: (bool, str) - (es_válido, mensaje_error)
    """
    if not servicio.strip():
        return False, MENSAJES_ERROR['servicio_vacio']
    
    if len(servicio.strip()) < VALIDACION['servicio_min_length']:
        return False, MENSAJES_ERROR['servicio_corto']
    
    if re.search(VALIDACION['caracteres_prohibidos'], servicio):
        return False, MENSAJES_ERROR['caracteres_especiales']
    
    return True, ""

def validar_datos_completos(apellido, nombre, fecha, servicio):
    """
    Valida que todos los campos requeridos estén completos
    
    Args:
        apellido (str): Apellido del paciente
        nombre (str): Nombre del paciente
        fecha (str): Fecha de ingreso
        servicio (str): Servicio
        
    Returns:
        tuple: (bool, str) - (es_válido, mensaje_error)
    """
    if not all([apellido, nombre, fecha, servicio]):
        return False, MENSAJES_ERROR['faltan_datos']
    return True, ""

def limpiar_texto(texto):
    """
    Limpia y formatea el texto (capitaliza palabras)
    
    Args:
        texto (str): Texto a limpiar
        
    Returns:
        str: Texto limpio y formateado
    """
    return ' '.join(p.capitalize() for p in texto.strip().split()) 