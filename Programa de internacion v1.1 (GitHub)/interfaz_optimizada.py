"""
Interfaz principal optimizada del Sistema de Carga de Internaciones

"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from config import UI_CONFIG


from config import VENTANA_CONFIG, COLORES, FUENTES, ATAJOS, SERVICIOS_DIFERENCIADOS
from validadores import (
    validar_nombre_apellido, validar_fecha, validar_servicio_personalizado,
    validar_datos_completos, limpiar_texto
)
from ui_components import FormularioPaciente, PanelBotones, EstiloManager
from sheets_manager import GoogleSheetsManager, PacienteManager

class ControladorAplicacion:
    """Controlador principal de la aplicación"""
    
    def __init__(self):
        self.ventana = None
        self.formulario = None
        self.panel_botones = None
        self.sheets_manager = GoogleSheetsManager()
        self.paciente_manager = PacienteManager(self.sheets_manager)
        
    def iniciar_aplicacion(self):
        self._crear_ventana()
        self._crear_componentes()
        self._configurar_eventos()
        self._configurar_atajos()
        self._inicializar_aplicacion()
        
    def _crear_ventana(self):
        self.ventana = tk.Tk()
        self.ventana.title(VENTANA_CONFIG['titulo'])
        self.ventana.configure(bg=COLORES['fondo'])
        
        # Configurar tamaño y posición - VENTANA REDIMENSIONABLE
        self._configurar_geometria()
        
        # Configurar cierre de ventana
        self.ventana.protocol("WM_DELETE_WINDOW", self._cerrar_aplicacion)
        
        # Actualizar título con información de redimensionamiento
        self._actualizar_titulo_ventana()
        
    def _configurar_geometria(self):
        """Configura la geometría de la ventana - REDIMENSIONABLE CON TAMAÑO MÍNIMO"""

        ancho_inicial = 701
        alto_inicial = 780
        

        ancho_minimo = 700  # Mínimo para evitar que se oculten los botones
        alto_minimo = 600   # Mínimo para el formulario y servicios recientes
        
        self.ventana.geometry(f"{ancho_inicial}x{alto_inicial}")
        
        self.ventana.resizable(True, True)
        
        self.ventana.minsize(ancho_minimo, alto_minimo)

        screen_width = self.ventana.winfo_screenwidth()
        screen_height = self.ventana.winfo_screenheight()
        x = int((screen_width/2) - (ancho_inicial/2))
        y = int((screen_height/2) - (alto_inicial/2))
        self.ventana.geometry(f"{ancho_inicial}x{alto_inicial}+{x}+{y}")
        
        self.ventana.bind('<Configure>', self._on_ventana_redimensionar)
        
    def _on_ventana_redimensionar(self, event):
        """Maneja el redimensionamiento de la ventana"""
        if event.widget == self.ventana:
            nuevo_ancho = event.width
            nuevo_alto = event.height
            
            if nuevo_ancho < 700 or nuevo_alto < 600:
                return
            
            if not hasattr(self, '_ultimo_tamaño'):
                self._ultimo_tamaño = (nuevo_ancho, nuevo_alto)
                self._actualizar_titulo_ventana()
            else:
                ultimo_ancho, ultimo_alto = self._ultimo_tamaño
                if abs(nuevo_ancho - ultimo_ancho) > 100 or abs(nuevo_alto - ultimo_alto) > 100:
                    self._ultimo_tamaño = (nuevo_ancho, nuevo_alto)
                    self._actualizar_titulo_ventana()
            # Solo actualizar estado si es significativo
            if not hasattr(self, '_estado_redimensionamiento'):
                self._estado_redimensionamiento = False
                
            if not self._estado_redimensionamiento:
                self._actualizar_estado(f"📐 Ventana redimensionada: {nuevo_ancho}x{nuevo_alto}", "info")
                self._estado_redimensionamiento = True
                self.ventana.after(2000, lambda: setattr(self, '_estado_redimensionamiento', False))
        
    def _actualizar_titulo_ventana(self):
        """Actualiza el título de la ventana con información del tamaño actual"""
        try:
            ancho_actual = self.ventana.winfo_width()
            alto_actual = self.ventana.winfo_height()
            titulo_base = VENTANA_CONFIG['titulo']
            self.ventana.title(f"{titulo_base} - {ancho_actual}x{alto_actual}")
        except:
            pass
        
    def _crear_componentes(self):
        frame_principal = tk.Frame(self.ventana, bg=COLORES['fondo'], padx=20, pady=20)
        frame_principal.pack(fill="both", expand=True)

        frame_titulo = tk.Frame(frame_principal, bg=COLORES['fondo'])
        frame_titulo.pack(fill="x", pady=(0, 25))

        titulo = tk.Label(
            frame_titulo, 
            text="🏥 Sistema de Carga de Internaciones", 
            font=FUENTES['titulo_grande'], 
            bg=COLORES['fondo'], 
            fg=COLORES['label']
        )
        titulo.pack(anchor="center")

        subtitulo = tk.Label(
            frame_titulo, 
            text="Complete los datos del paciente para registrar la internación", 
            font=FUENTES['subtitulo'], 
            bg=COLORES['fondo'], 
            fg=COLORES['separador']
        )
        subtitulo.pack(anchor="center", pady=(5, 0))

        separador = tk.Frame(frame_titulo, height=3, bg=COLORES['gradiente_primario'])
        separador.pack(fill="x", pady=(15, 0))
        
        frame_central = tk.Frame(frame_principal, bg=COLORES['fondo'])
        frame_central.pack(fill="both", expand=True, pady=(0, 20))

        self.formulario = FormularioPaciente(frame_central)
        self.panel_botones = PanelBotones(frame_central)
        self._crear_indicador_estado(frame_principal)
        self._configurar_menu_contextual_campos()
    
    def _crear_indicador_estado(self, parent):
        self.frame_estado = EstiloManager.crear_frame_con_sombra(
            parent
        )
        self.frame_estado.pack(fill="x", pady=(20, 0))
        
        frame_interno = tk.Frame(self.frame_estado, bg=COLORES['frame'])
        frame_interno.pack(fill="x", padx=20, pady=20)
        
        separador_superior = tk.Frame(frame_interno, height=2, bg=COLORES['gradiente_primario'])
        separador_superior.pack(fill="x", pady=(0, 15))
        
        self.label_estado = tk.Label(
            frame_interno, 
            text="✅ Aplicación lista", 
            font=FUENTES['estado'], 
            bg=COLORES['frame'], 
            fg=COLORES['success']
        )
        self.label_estado.pack()
        
        info_adicional = tk.Label(
            frame_interno, 
            text="⌨️ Use Ctrl+C, Ctrl+V, Ctrl+X para copiar, pegar y cortar • Ctrl+A para seleccionar todo", 
            font=FUENTES['placeholder'], 
            bg=COLORES['frame'], 
            fg=COLORES['separador']
        )
        info_adicional.pack(pady=(5, 0))
        
        info_redimensionamiento = tk.Label(
            frame_interno, 
            text="💡 La ventana es redimensionable • Tamaño mínimo: 700x600", 
            font=FUENTES['placeholder'], 
            bg=COLORES['frame'], 
            fg=COLORES['separador']
        )
        info_redimensionamiento.pack(pady=(5, 0))
    
    def _actualizar_estado(self, mensaje, tipo="info"):
        ESTADOS = {
            'info': {'icono': 'ℹ️', 'color': COLORES['estado_info']},
            'success': {'icono': '✅', 'color': COLORES['estado_exito']},
            'error': {'icono': '❌', 'color': COLORES['estado_error']},
            'warning': {'icono': '⚠️', 'color': COLORES['estado_cargando']},
            'loading': {'icono': '⏳', 'color': COLORES['estado_cargando']}
        }
        
        estado_config = ESTADOS.get(tipo, ESTADOS['info'])
        
        texto_completo = f"{estado_config['icono']} {mensaje}"
        self.label_estado.config(text=texto_completo, fg=estado_config['color'])
        
        if UI_CONFIG['estados_animados']:
            self._aplicar_animacion_estado()
    
    def _aplicar_animacion_estado(self):
        try:
            color_original = self.label_estado.cget('bg')
            self.label_estado.config(bg=COLORES['hover_suave'])
            
            self.ventana.after(200, lambda: self.label_estado.config(bg=color_original))
        except:
            pass

    def _configurar_menu_contextual_campos(self):
        campos = ['apellido', 'nombre', 'fecha', 'otro']
        for campo in campos:
            if campo in self.formulario.widgets:
                widget = self.formulario.widgets[campo]
    def _configurar_menu_contextual_campos(self):
        campos = ['apellido', 'nombre', 'fecha', 'otro']
        for campo in campos:
            if campo in self.formulario.widgets:
                widget = self.formulario.widgets[campo]
                self._crear_menu_contextual_widget(widget, campo)
                
    def _crear_menu_contextual_widget(self, widget, nombre_campo):
        menu = tk.Menu(widget, tearoff=0)
        
        COMANDOS_MENU = [
            ("Copiar (Ctrl+C)", 'copy'),
            ("Cortar (Ctrl+X)", 'cut'),
            ("Pegar (Ctrl+V)", 'paste'),
            ("Seleccionar todo (Ctrl+A)", 'select_all')
        ]
        
        for i, (etiqueta, comando) in enumerate(COMANDOS_MENU):
            if comando == 'select_all':
                menu.add_separator()
                menu.add_command(label=etiqueta, command=lambda: self._seleccionar_todo_widget(widget))
            else:
                menu.add_command(label=etiqueta, command=lambda c=comando: self._ejecutar_comando_widget(widget, c))
        
        widget.bind("<Button-3>", lambda e, m=menu, w=widget: self._mostrar_menu_contextual_widget(e, m, w))
        
    def _mostrar_menu_contextual_widget(self, event, menu, widget):
        try:
            self._seleccionar_todo_widget(widget)
            
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
            
    def _seleccionar_todo_widget(self, widget):
        try:
            if hasattr(widget, 'select_range'):
                widget.select_range(0, tk.END)
                widget.icursor(tk.END)
                widget.focus_set()
        except Exception as e:
            print(f"Error al seleccionar todo en {widget}: {e}")
            
    def _ejecutar_comando_widget(self, widget, comando):
        try:
            if comando == 'copy':
                widget.event_generate('<<Copy>>')
            elif comando == 'cut':
                widget.event_generate('<<Cut>>')
            elif comando == 'paste':
                widget.event_generate('<<Paste>>')
        except Exception as e:
            print(f"Error al ejecutar {comando} en {widget}: {e}")
    
    def _seleccionar_todo(self):
        try:
            widget_focus = self.ventana.focus_get()
            if hasattr(widget_focus, 'select_range'):
                widget_focus.select_range(0, tk.END)
                widget_focus.icursor(tk.END)
        except Exception as e:
            print(f"Error al seleccionar todo: {e}")
    
    def _configurar_eventos(self):
        self.panel_botones.configurar_comando('cargar', self._cargar_paciente)
        self.panel_botones.configurar_comando('limpiar', self._limpiar_formulario)
        
        self.ventana.bind('<Key>', self._manejar_atajos)
        
        self._configurar_menu_contextual_campos()
        
        self._configurar_validacion_campos()
        
        self._configurar_servicios_recientes()
    
    def _configurar_validacion_campos(self):
        campos_validacion = {
            'apellido': lambda: validar_nombre_apellido(self.formulario.widgets['apellido'].get()),
            'nombre': lambda: validar_nombre_apellido(self.formulario.widgets['nombre'].get()),
            'fecha': lambda: validar_fecha(self.formulario.widgets['fecha'].get()),
            'servicio': lambda: validar_servicio_personalizado(self.formulario.widgets['servicio'].get())
        }
        
        for nombre_campo, funcion_validacion in campos_validacion.items():
            if nombre_campo in self.formulario.widgets:
                widget = self.formulario.widgets[nombre_campo]
                widget.bind('<FocusOut>', lambda e, w=widget, f=funcion_validacion: self._validar_campo_al_perder_foco(w, f))
    
    def _configurar_servicios_recientes(self):
        pass
    
    def _configurar_atajos(self):
        self.ventana.bind('<Key>', self._manejar_atajos)
        
        self.ventana.bind('<Control-a>', self._seleccionar_todo)
        
    def _inicializar_aplicacion(self):
        self.formulario.widgets['apellido'].focus()
        
    def _validar_campo_al_perder_foco(self, widget, funcion_validacion):
        campo_nombre = self._identificar_campo_widget(widget)
        if not campo_nombre:
            return
            
        valor = widget.get().strip()
        
        VALIDACIONES = {
            'apellido': (validar_nombre_apellido, 'apellido'),
            'nombre': (validar_nombre_apellido, 'nombre'),
            'otro': (validar_servicio_personalizado, 'servicio personalizado')
        }
        
        if campo_nombre in VALIDACIONES:
            validador, nombre_campo = VALIDACIONES[campo_nombre]
            
            if valor or campo_nombre == 'otro':
                if campo_nombre == 'otro' and self.formulario.widgets['servicio'].get() != "Otro":
                    return
                    
                es_valido, mensaje = validador(valor)
                if not es_valido:
                    EstiloManager.aplicar_estilo_error(widget, mensaje)
                else:
                    EstiloManager.aplicar_estilo_normal(widget)
    
    def _identificar_campo_widget(self, widget):
        if not hasattr(self, '_widgets_inversos'):
            self._widgets_inversos = {w: nombre for nombre, w in self.formulario.widgets.items()}
        
        return self._widgets_inversos.get(widget)
                
    def _manejar_cambio_servicio(self, event):
        servicio = self.formulario.widgets['servicio'].get()
        
        if servicio in SERVICIOS_DIFERENCIADOS:
            from ui_components import VentanaServicioDiferenciado
            opciones = SERVICIOS_DIFERENCIADOS[servicio]
            ventana_servicio = VentanaServicioDiferenciado(self.ventana, servicio, opciones)
            
            if ventana_servicio.resultado:
                servicio_completo = f"{servicio} - {ventana_servicio.resultado}"
                self.formulario.widgets['servicio'].set(servicio_completo)
            else:
                self.formulario.widgets['servicio'].set('')
        
        self.formulario.mostrar_servicio_personalizado(servicio == "Otro")
        
    def _manejar_atajos(self, event):
        if event.keysym == ATAJOS['cargar']:
            self._cargar_paciente()
        elif event.keysym == ATAJOS['limpiar']:
            self._limpiar_formulario()
            
    def _cargar_paciente(self):
        self._actualizar_estado("⏳ Validando datos...", "loading")
        self.ventana.update()
        
        datos = self.formulario.obtener_datos()
        
        servicio_final = datos['servicio']
        if datos['servicio'] == "Otro":
            servicio_final = datos['otro']
        
        es_valido, mensaje = validar_datos_completos(
            datos['apellido'], datos['nombre'], datos['fecha'], servicio_final
        )
        if not es_valido:
            self._actualizar_estado(f"❌ {mensaje}", "error")
            messagebox.showwarning("Faltan datos", mensaje)
            return
        
        es_valido, mensaje = validar_nombre_apellido(datos['apellido'])
        if not es_valido:
            self._actualizar_estado(f"❌ Error en apellido: {mensaje}", "error")
            messagebox.showerror("Error en apellido", mensaje)
            self.formulario.widgets['apellido'].focus()
            return
        
        es_valido, mensaje = validar_nombre_apellido(datos['nombre'])
        if not es_valido:
            self._actualizar_estado(f"❌ Error en nombre: {mensaje}", "error")
            messagebox.showerror("Error en nombre", mensaje)
            self.formulario.widgets['nombre'].focus()
            return
        
        es_valido, mensaje = validar_fecha(datos['fecha'])
        if not es_valido:
            self._actualizar_estado(f"❌ Error en fecha: {mensaje}", "error")
            messagebox.showerror("Error en fecha", mensaje)
            self.formulario.widgets['fecha'].focus()
            return
        
        if datos['servicio'] == "Otro":
            es_valido, mensaje = validar_servicio_personalizado(servicio_final)
            if not es_valido:
                self._actualizar_estado(f"❌ Error en servicio: {mensaje}", "error")
                messagebox.showerror("Error en servicio", mensaje)
                self.formulario.widgets['otro'].focus()
                return
        
        apellido_limpio = limpiar_texto(datos['apellido'])
        nombre_limpio = limpiar_texto(datos['nombre'])
        servicio_limpio = limpiar_texto(servicio_final)
        
        try:
            if isinstance(datos['fecha'], datetime):
                fecha_dt = datos['fecha']
                fecha_str = fecha_dt.strftime("%d/%m/%Y")
            else:
                fecha_dt = datetime.strptime(datos['fecha'], "%d/%m/%Y")
                fecha_str = datos['fecha']
            
            nueva_fila = [apellido_limpio, nombre_limpio, fecha_str, servicio_limpio] + [""] * 11
            
        except (ValueError, TypeError) as e:
            nueva_fila = [apellido_limpio, nombre_limpio, datos['fecha'], servicio_limpio] + [""] * 11
        
        try:
            self._actualizar_estado("⏳ Insertando paciente en Google Sheets...", "loading")
            self.ventana.update()
            
            self.paciente_manager.insertar_paciente_ordenado(nueva_fila)
            
            self._actualizar_estado(f"✅ Paciente {apellido_limpio}, {nombre_limpio} agregado correctamente", "info")
            messagebox.showinfo("Éxito", f"Paciente {apellido_limpio}, {nombre_limpio} agregado correctamente.")
            
            self.formulario.registrar_servicio_utilizado(servicio_limpio)
            
            self._limpiar_formulario()
            
        except Exception as e:
            self._actualizar_estado(f"❌ Error al agregar paciente: {str(e)}", "error")
            messagebox.showerror("Error", f"No se pudo agregar el paciente: {e}")
            
    def _limpiar_formulario(self):
        self.formulario.limpiar_campos()
        self._actualizar_estado("✅ Formulario limpiado", "info")
        
    def _on_enter_boton(self, event, nombre_boton, color_hover):
        self.panel_botones.botones[nombre_boton].config(background=color_hover)
        
    def _on_leave_boton(self, event, nombre_boton, color_normal):
        self.panel_botones.botones[nombre_boton].config(background=color_normal)
        
    def _cerrar_aplicacion(self):
        self.ventana.destroy()
        
    def ejecutar(self):
        self.ventana.mainloop()

def main():
    try:
        print("Iniciando aplicación...")
        app = ControladorAplicacion()
        print("Aplicación creada, iniciando componentes...")
        app.iniciar_aplicacion()
        print("Componentes iniciados, ejecutando mainloop...")
        app.ejecutar()
    except Exception as e:
        print(f"Error en main: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
