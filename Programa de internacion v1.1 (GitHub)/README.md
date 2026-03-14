## Sistema de Carga de Internaciones

Aplicación de escritorio en Python/Tkinter para registrar internaciones en una planilla de Google Sheets, con una interfaz moderna y validaciones de datos.

### Requisitos

- Python 3.9+
- Cuenta de servicio de Google Cloud con acceso a Google Sheets

### Instalación

1. Crear y activar un entorno virtual (opcional, pero recomendado):

```bash
python -m venv .venv
.venv\Scripts\activate  # En Windows
```

2. Instalar dependencias principales (ajústalo a tus necesidades):

```bash
pip install gspread gspread-formatting google-auth
```

### Configuración de credenciales y Google Sheets

1. Crea una cuenta de servicio en Google Cloud y descarga el archivo JSON de credenciales.
2. Guarda ese archivo **fuera del control de versiones** o con un nombre como `credenciales.json` (ya está ignorado en `.gitignore`).
3. Define estas variables de entorno en tu sistema o en un archivo `.env` (no lo subas a GitHub):

- `GOOGLE_SERVICE_ACCOUNT_FILE`: ruta al archivo JSON de la cuenta de servicio (por ejemplo, `credenciales.json`).
- `GOOGLE_SPREADSHEET_ID`: ID de la planilla de Google Sheets donde se guardarán los datos.

El alcance (`SCOPES`) está configurado por defecto a:

- `https://www.googleapis.com/auth/spreadsheets`

### Ejecución

Ejecuta la interfaz principal con:

```bash
python interfaz_optimizada.py
```


