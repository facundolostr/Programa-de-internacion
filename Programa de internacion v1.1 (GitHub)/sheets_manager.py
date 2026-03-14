import gspread
from datetime import datetime
from gspread_formatting import set_frozen
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import locale
from config import SCOPES, CREDENTIALS_FILE, SPREADSHEET_ID, SHEETS_CONFIG


locale.setlocale(locale.LC_TIME, 'Spanish_Argentina.1252')

class GoogleSheetsManager:
   
    
    def __init__(self):
        self.client = None
        self.spreadsheet = None
        self._cache_hojas = {}
        self._ultima_conexion = None
        self._tiempo_expiracion_cache = 300  # 5 minutos
    
    def conectar(self):
        """Establece conexión con Google Sheets - OPTIMIZADO"""
        if self._es_conexion_valida():
            return True
            
        try:
            creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
            self.client = gspread.authorize(creds)
            self.spreadsheet = self.client.open_by_key(SPREADSHEET_ID)
            self._ultima_conexion = datetime.now()
            return True
        except Exception as e:
            raise Exception(f"Error al conectar con Google Sheets: {e}")
    
    def _es_conexion_valida(self):
        """Verifica si la conexión actual es válida - OPTIMIZADO"""
        if not self.client or not self.spreadsheet:
            return False
            
        if self._ultima_conexion:
            tiempo_transcurrido = (datetime.now() - self._ultima_conexion).total_seconds()
            if tiempo_transcurrido > self._tiempo_expiracion_cache:
                return False
                
        try:
            self.spreadsheet.title
            return True
        except:
            return False
    
    def obtener_hoja_mes(self, fecha_dt):
        """Obtiene o crea la hoja del mes correspondiente - OPTIMIZADO"""
        nombre_mes = fecha_dt.strftime("%B").capitalize()
        
        if nombre_mes in self._cache_hojas:
            hoja_cache = self._cache_hojas[nombre_mes]
            if self._es_hoja_cache_valida(hoja_cache):
                return hoja_cache
            else:
                del self._cache_hojas[nombre_mes]
        
        try:
            hoja = self.spreadsheet.worksheet(nombre_mes)
            if self._es_hoja_cache_valida(hoja):
                self._cache_hojas[nombre_mes] = hoja
            return hoja
        except gspread.exceptions.WorksheetNotFound:
            hoja = self._crear_hoja_mes(nombre_mes)
            if self._es_hoja_cache_valida(hoja):
                self._cache_hojas[nombre_mes] = hoja
            return hoja
        except Exception as e:
            if nombre_mes in self._cache_hojas:
                del self._cache_hojas[nombre_mes]
            raise Exception(f"Error al obtener hoja del mes {nombre_mes}: {e}")
    
    def _es_hoja_cache_valida(self, hoja):
        try:
            if not hoja or not hasattr(hoja, 'title'):
                return False
            hoja.title
            if not hasattr(hoja, '_properties') or 'sheetId' not in hoja._properties:
                return False
            return True
        except:
            return False
    
    def limpiar_cache(self):
        """Limpia el caché de hojas y datos - OPTIMIZADO"""
        for nombre_mes in list(self._cache_hojas.keys()):
            try:
                if not self._es_hoja_cache_valida(self._cache_hojas[nombre_mes]):
                    del self._cache_hojas[nombre_mes]
            except:
                del self._cache_hojas[nombre_mes]
        
        if hasattr(self, '_cache_datos_hoja'):
            self._cache_datos_hoja.clear()
        if hasattr(self, '_ultima_actualizacion_datos'):
            self._ultima_actualizacion_datos.clear()
        self._ultima_conexion = None
    
    def limpiar_cache_completo(self):
        self._cache_hojas.clear()
        if hasattr(self, '_cache_datos_hoja'):
            self._cache_datos_hoja.clear()
        if hasattr(self, '_ultima_actualizacion_datos'):
            self._ultima_actualizacion_datos.clear()
        self._ultima_conexion = None

    
    def recuperar_de_error(self):
        try:
            self.limpiar_cache_completo()
            
            self.client = None
            self.spreadsheet = None
            self._ultima_conexion = None
            
            return self.conectar()
        except Exception as e:
            return False
    
    def _crear_hoja_mes(self, nombre_mes):
        hoja = self.spreadsheet.add_worksheet(
            title=nombre_mes, 
            rows=str(SHEETS_CONFIG['filas_por_defecto']), 
            cols=str(SHEETS_CONFIG['columnas_por_defecto'])
        )
        
        self._configurar_encabezados(hoja)
        self._aplicar_formato(hoja)
        
        return hoja
    
    def _configurar_encabezados(self, hoja):
        fila1 = ["Apellido(s)", "Nombre(s)", "Fecha de ingreso", "Servicio",
                 "Pase 1", "", "Pase 2", "", "Pase 3", "", "Pase 4", "", "Pase 5", "",
                 "Causa egreso", "Fecha de egreso"]
        fila2 = ["", "", "", "",
                 "Fecha", "Servicio", "Fecha", "Servicio", "Fecha", "Servicio", "Fecha", "Servicio", "Fecha", "Servicio",
                 "", ""]
        
        hoja.update("A1:P1", [fila1])
        hoja.update("A2:P2", [fila2])
        
        hoja.merge_cells("A1:A2")  # Apellido(s)
        hoja.merge_cells("B1:B2")  # Nombre(s)
        hoja.merge_cells("C1:C2")  # Fecha de ingreso
        hoja.merge_cells("D1:D2")  # Servicio
        hoja.merge_cells("O1:O2")  # Causa egreso
        hoja.merge_cells("P1:P2")  # Fecha de egreso
        
        hoja.merge_cells("E1:F1")  # Pase 1
        hoja.merge_cells("G1:H1")  # Pase 2
        hoja.merge_cells("I1:J1")  # Pase 3
        hoja.merge_cells("K1:L1")  # Pase 4
        hoja.merge_cells("M1:N1")  # Pase 5
    
    def _aplicar_formato(self, hoja):
        hoja.format("A1:P2", {
            "textFormat": {"bold": True, "fontSize": 12},
            "horizontalAlignment": "CENTER",
            "verticalAlignment": "MIDDLE",
            "backgroundColor": {"red": 1, "green": 1, "blue": 0}
        })
        
        hoja.format("A3:P1000", {
            "horizontalAlignment": "CENTER",
            "verticalAlignment": "MIDDLE",
            "textFormat": {"fontSize": 10}
        })
        
        self._aplicar_formato_condicional(hoja)
        
        self._aplicar_bordes(hoja)
        
        self._configurar_ancho_columnas(hoja)
        
        set_frozen(hoja, rows=2)

    def _aplicar_formato_condicional(self, hoja):
        try:
            if not hasattr(hoja, '_properties') or 'sheetId' not in hoja._properties:
                return False
            
            sheet_id = hoja._properties['sheetId']
            
            request_body = {
                "requests": [
                    {
                        "addConditionalFormatRule": {
                            "rule": {
                                "ranges": [
                                    {
                                        "sheetId": sheet_id,
                                        "startRowIndex": 2,  # Desde fila 3 (índice 2)
                                        "endRowIndex": 1000,  # Hasta fila 1000
                                        "startColumnIndex": 0,  # Columna A
                                        "endColumnIndex": 16   # Columna P (índice 15)
                                    }
                                ],
                                "booleanRule": {
                                    "condition": {
                                        "type": "CUSTOM_FORMULA",
                                        "values": [
                                            {
                                                "userEnteredValue": "=Y($P3<>\"\";ESNUMERO(FECHANUMERO($P3));ESNUMERO(FECHANUMERO($C3));FECHANUMERO($P3)<FECHANUMERO($C3))"
                                            }
                                        ]
                                    },
                                    "format": {
                                        "backgroundColor": {
                                            "red": 1,
                                            "green": 0,
                                            "blue": 0
                                        }
                                    }
                                }
                            }
                        }
                    }
                ]
            }
            
            # Aplicar formato condicional
            hoja.spreadsheet.batch_update(request_body)
            return True
            
        except Exception as e:
            return False
    
    def _aplicar_bordes(self, hoja):
        """Aplica bordes a la fila de encabezado"""
        hoja.spreadsheet.batch_update({
            "requests": [
                {
                    "updateBorders": {
                        "range": {
                            "sheetId": hoja._properties['sheetId'],
                            "startRowIndex": 0,
                            "endRowIndex": 2,
                            "startColumnIndex": 0,
                            "endColumnIndex": SHEETS_CONFIG['columnas_totales']
                        },
                        "top": {"style": "SOLID"},
                        "bottom": {"style": "SOLID"},
                        "left": {"style": "SOLID"},
                        "right": {"style": "SOLID"},
                        "innerHorizontal": {"style": "SOLID"},
                        "innerVertical": {"style": "SOLID"}
                    }
                }
            ]
        })
    
    def _configurar_ancho_columnas(self, hoja):
        """Configura el ancho de las columnas"""
        hoja.spreadsheet.batch_update({
            "requests": [
                {
                    "updateDimensionProperties": {
                        "range": {
                            "sheetId": hoja._properties['sheetId'],
                            "dimension": "COLUMNS",
                            "startIndex": 0,
                            "endIndex": SHEETS_CONFIG['columnas_totales']
                        },
                        "properties": {
                            "pixelSize": SHEETS_CONFIG['ancho_columna']
                        },
                        "fields": "pixelSize"
                    }
                }
            ]
        })

class PacienteManager:    
    def __init__(self, sheets_manager):
        self.sheets_manager = sheets_manager
    
    def insertar_paciente_ordenado(self, datos_paciente):
        """Inserta un paciente en orden alfabético y cronológico"""
        try:
            if not self.sheets_manager._es_conexion_valida():
                self.sheets_manager.conectar()
            
            if not datos_paciente or len(datos_paciente) < 3:
                raise Exception("Datos del paciente incompletos")
            
            try:
                if isinstance(datos_paciente[2], datetime):
                    fecha_dt = datos_paciente[2]
                else:
                    fecha_dt = datetime.strptime(datos_paciente[2], "%d/%m/%Y")
            except ValueError:
                raise Exception(f"Formato de fecha inválido: {datos_paciente[2]}")
            
            if isinstance(datos_paciente[2], datetime):
                datos_paciente[2] = datos_paciente[2].strftime("%d/%m/%Y")
            
            hoja = self.sheets_manager.obtener_hoja_mes(fecha_dt)
            
            if not self.sheets_manager._es_hoja_cache_valida(hoja):
                raise Exception("La hoja del mes no es válida")
            
            posicion = self._encontrar_posicion_insercion(hoja, datos_paciente)
            
            if posicion < 3:
                posicion = 3
            
            hoja.insert_row(datos_paciente, posicion)
            
            
            self._aplicar_formato_asincrono(hoja, posicion)
            
            self._invalidar_cache_hoja(hoja.title)
            
            return True
            
        except Exception as e:
            if "APIERROR" in str(e) or "400" in str(e):
                self.sheets_manager.limpiar_cache_completo()
            raise Exception(f"Error al insertar paciente: {e}")
    
    def _aplicar_formato_asincrono(self, hoja, posicion):
        try:
            self._aplicar_formato_fila_centrada(hoja, posicion)
        except:
            pass

    def _invalidar_cache_hoja(self, nombre_hoja):
        if hasattr(self.sheets_manager, '_cache_datos_hoja'):
            if nombre_hoja in self.sheets_manager._cache_datos_hoja:
                del self.sheets_manager._cache_datos_hoja[nombre_hoja]
        if hasattr(self.sheets_manager, '_ultima_actualizacion_datos'):
            if nombre_hoja in self.sheets_manager._ultima_actualizacion_datos:
                del self.sheets_manager._ultima_actualizacion_datos[nombre_hoja]
    
    def _aplicar_formato_fila_centrada(self, hoja, numero_fila):
        try:
            rango = f"A{numero_fila}:P{numero_fila}"
            
            formato_optimizado = {
                "horizontalAlignment": "CENTER",
                "verticalAlignment": "MIDDLE"
            }
            
            hoja.format(rango, formato_optimizado)
            
        except Exception as e:
            pass
    
    def _encontrar_posicion_insercion(self, hoja, nueva_fila):
        if not hasattr(self, '_cache_datos_hoja') or not hasattr(self, '_ultima_actualizacion_datos'):
            self._cache_datos_hoja = {}
            self._ultima_actualizacion_datos = {}
        
        nombre_hoja = hoja.title
        tiempo_actual = datetime.now()
        
        if (nombre_hoja in self._cache_datos_hoja and 
            nombre_hoja in self._ultima_actualizacion_datos):
            tiempo_cache = self._ultima_actualizacion_datos[nombre_hoja]
            if (tiempo_actual - tiempo_cache).total_seconds() < 60:  # 1 minuto
                datos = self._cache_datos_hoja[nombre_hoja]
            else:
                datos = self._actualizar_cache_datos(hoja, nombre_hoja)
        else:
            datos = self._actualizar_cache_datos(hoja, nombre_hoja)
        
        fila_insertar = 3
        nuevo_apellido = nueva_fila[0].lower()
        
        try:
            if isinstance(nueva_fila[2], datetime):
                nueva_fecha = nueva_fila[2]
            else:
                nueva_fecha = datetime.strptime(nueva_fila[2], "%d/%m/%Y")
        except ValueError:
            raise Exception(f"Formato de fecha inválido: {nueva_fila[2]}")
        
        if isinstance(nueva_fila[2], datetime):
            nueva_fila[2] = nueva_fila[2].strftime("%d/%m/%Y")
        
        for i, fila in enumerate(datos):
            if not fila[0]:
                break
                
            apellido = fila[0].lower()
            
            if nuevo_apellido < apellido:
                break
            elif nuevo_apellido == apellido:
                try:
                    if isinstance(fila[2], datetime):
                        fecha = fila[2]
                    else:
                        fecha = datetime.strptime(fila[2], "%d/%m/%Y")
                    
                    if nueva_fecha < fecha:
                        break
                except ValueError:
                    continue
            
            fila_insertar += 1
        
        return fila_insertar
    
    def _actualizar_cache_datos(self, hoja, nombre_hoja):
        try:
            datos = hoja.get_all_values()[2:]
            self._cache_datos_hoja[nombre_hoja] = datos
            self._ultima_actualizacion_datos[nombre_hoja] = datetime.now()
            return datos
        except Exception as e:
            if nombre_hoja in self._cache_datos_hoja:
                del self._cache_datos_hoja[nombre_hoja]
            if nombre_hoja in self._ultima_actualizacion_datos:
                del self._ultima_actualizacion_datos[nombre_hoja]
            return hoja.get_all_values()[2:]

def conectar_google_sheets():
    manager = GoogleSheetsManager()
    manager.conectar()
    return manager.client

def generar_mes(fecha_dt):
    manager = GoogleSheetsManager()
    manager.conectar()
    return manager.obtener_hoja_mes(fecha_dt)

def insertar_ordenado(nueva_fila):
    sheets_manager = GoogleSheetsManager()
    paciente_manager = PacienteManager(sheets_manager)
    return paciente_manager.insertar_paciente_ordenado(nueva_fila) 