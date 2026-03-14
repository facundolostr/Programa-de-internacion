"""
Archivo de configuración centralizada para el Sistema de Carga de Internaciones.
"""

import os

# Configuración de Google Sheets (valores sensibles se obtienen de variables de entorno)
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDENTIALS_FILE = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE', 'credenciales.json')
SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID', '')

# Configuración de la interfaz
VENTANA_CONFIG = {
    'titulo': 'Sistema de Carga de Internaciones',
    'ancho': 600,
    'alto': 500,
    'redimensionable': False
}

UI_CONFIG = {
    'animaciones': True,
    'efectos_hover': True,
    'sombras': True,
    'gradientes': True,
    'bordes_redondeados': True,
    'transiciones': True,
    'feedback_visual': True,
    'iconos': True,
    'estados_animados': True
}



FUENTES = {
    'texto': ("Segoe UI", 10),
    'titulo': ("Segoe UI", 11, "bold"),
    'boton': ("Segoe UI", 10, "bold"),
    'titulo_principal': ("Segoe UI", 16, "bold"),
    'error': ("Segoe UI", 8),
    'hipervinculo': ("Segoe UI", 9, "underline"),
    'etiqueta_servicios': ("Segoe UI", 9, "italic"),
    

    'titulo_grande': ("Segoe UI", 20, "bold"),
    'subtitulo': ("Segoe UI", 12, "normal"),
    'etiqueta_campo': ("Segoe UI", 10, "bold"),
    'placeholder': ("Segoe UI", 9, "italic"),
    'estado': ("Segoe UI", 9, "normal"),
    'icono': ("Segoe UI", 14, "normal")
}


COLORES = {
    'fondo': "#f8fafc",  # Azul muy claro, 
    'frame': "#ffffff",  # Blanco puro
    'frame_sombra': "#e2e8f0",  # Gris muy claro para sombras
    'boton_primario': "#3b82f6",  # Azul moderno
    'boton_primario_hover': "#2563eb",  # Azul más oscuro para hover
    'boton_secundario': "#64748b",  # Gris azulado moderno
    'boton_secundario_hover': "#475569",  # Gris más oscuro para hover
    'label': "#334155",  # Gris oscuro para texto
    'entry_bg': "#ffffff",  # Blanco para entradas
    'entry_border': "#cbd5e1",  # Gris claro para bordes
    'entry_focus': "#93c5fd",  # Azul claro para foco
    'error': "#ef4444",  # Rojo moderno
    'success': "#10b981",  # Verde moderno
    'error_bg': "#fef2f2",  # Rojo muy claro para fondo de error
    'hipervinculo': "#2563eb",  # Azul para hipervínculos
    'hipervinculo_hover': "#1d4ed8",  # Azul más oscuro para hover
    'separador': "#94a3b8",  # Gris medio para separadores
    
    'gradiente_primario': "#3b82f6",  # Azul para gradientes
    'gradiente_secundario': "#1d4ed8",  # Azul oscuro para gradientes
    'sombra_suave': "#e2e8f0",  # Sombra muy sutil (gris claro)
    'sombra_media': "#cbd5e1",  # Sombra media (gris medio)
    'sombra_fuerte': "#94a3b8",  # Sombra más fuerte (gris oscuro)
    'estado_cargando': "#f59e0b",  # Amarillo para estado de carga
    'estado_exito': "#10b981",  # Verde para éxito
    'estado_error': "#ef4444",  # Rojo para error
    'estado_info': "#3b82f6",  # Azul para información
    'hover_suave': "#f1f5f9",  # Color de hover muy sutil
    'borde_redondeado': "#e2e8f0",  # Color para bordes redondeados
}


SERVICIOS_PREDEFINIDOS = [
    "Cardiología", "Clínica médica", "Cirugía", "Cirugia Plástica", "Endoscopía", 
    "Ginecología", "Guardia", "Neurocirugía", "Obstetricia", "Oftalmología", 
    "Oncología", "Pediatría", "Reumatología", "Salud Mental", 
    "Traumatología", "UCO", "Urología", "UTI", "Otro"
]


SERVICIOS_DIFERENCIADOS = {
    "Clínica médica": ["A", "B"],
    "Cirugía": ["Hombres", "Mujeres"],
    "Salud Mental": ["Hombres", "Mujeres"],
    "UTI": ["A", "B"]
}


VALIDACION = {
    'nombre_min_length': 1,
    'servicio_min_length': 2,
    'caracteres_prohibidos': r'[<>:"/\\|?*]',
    'patron_nombre': r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\'-]+$'
}


SHEETS_CONFIG = {
    'columnas_totales': 16,  
    'filas_por_defecto': 10000,
    'columnas_por_defecto': 16, 
    'ancho_columna': 140
}


MENSAJES_ERROR = {
    'campo_vacio': "El campo no puede estar vacío",
    'solo_letras': "Solo se permiten letras, espacios, guiones (-) y apóstrofes (')",
    'debe_contener_letra': "Debe contener al menos una letra",
    'fecha_futura': "La fecha no puede ser futura",
    'formato_fecha': "Formato de fecha inválido (DD/MM/AAAA)",
    'servicio_vacio': "Debe especificar el servicio",
    'servicio_corto': "El servicio debe tener al menos 2 caracteres",
    'caracteres_especiales': "El servicio no puede contener caracteres especiales",
    'faltan_datos': "Por favor complete todos los campos"
}


ATAJOS = {
    'cargar': 'Return',
    'limpiar': 'Escape',
    'copiar': 'c',
    'pegar': 'v',
    'seleccionar_todo': 'a'
} 