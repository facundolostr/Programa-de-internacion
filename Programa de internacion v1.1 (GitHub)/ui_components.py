"""
Componentes de interfaz de usuario para el Sistema de Carga de Internaciones
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from config import COLORES, FUENTES, SERVICIOS_PREDEFINIDOS, SERVICIOS_DIFERENCIADOS, UI_CONFIG
    
class EstiloManager:
    
    @staticmethod
    def aplicar_estilo_error(widget, mensaje=""):
        if hasattr(widget, 'config'):
            try:
                widget.config(
                    bg=COLORES['error_bg'], 
                    relief="flat", 
                    bd=1,
                    highlightthickness=2,
                    highlightbackground=COLORES['error'],
                    highlightcolor=COLORES['error']
                )
                if UI_CONFIG['sombras']:
                    widget.config(bd=2, relief="solid")
                    
            except tk.TclError:
                pass

        if hasattr(widget, 'error_label'):
            widget.error_label.destroy()
        if mensaje:
            widget.error_label = tk.Label(
                widget.master, 
                text=f"⚠️ {mensaje}", 
                fg=COLORES['error'], 
                font=FUENTES['error'], 
                bg=COLORES['fondo']
            )
            widget.error_label.grid(
                row=widget.grid_info()['row']+1, 
                column=widget.grid_info()['column'], 
                sticky="w", 
                padx=20
            )

    @staticmethod
    def aplicar_estilo_normal(widget):
        if hasattr(widget, 'config'):
            try:
                widget.config(
                    bg=COLORES['entry_bg'], 
                    relief="flat", 
                    bd=1,
                    highlightthickness=2,  
                    highlightbackground=COLORES['entry_border'],
                    highlightcolor=COLORES['entry_border']
                )
                if UI_CONFIG['sombras']:
                    widget.config(bd=1, relief="solid")
                    
            except tk.TclError:
                pass
                
        if hasattr(widget, 'error_label'):
            widget.error_label.destroy()
            
    @staticmethod
    def aplicar_estilo_hover(widget):
        if not UI_CONFIG['efectos_hover']:
            return
            
        if hasattr(widget, 'config'):
            try:
                widget.config(
                    bg=COLORES['hover_suave'],
                    highlightthickness=2,
                    highlightbackground=COLORES['entry_focus']
                )
            except tk.TclError:
                pass
                
    @staticmethod
    def aplicar_estilo_focus(widget):
        """Aplica estilo de foco a un widget"""
        if hasattr(widget, 'config'):
            try:
                widget.config(
                    bg=COLORES['entry_bg'],
                    highlightthickness=2, 
                    highlightbackground=COLORES['entry_focus'],
                    highlightcolor=COLORES['entry_focus']
                )
            except tk.TclError:
                pass
                
    @staticmethod
    def crear_frame_con_sombra(parent, **kwargs):
        """Crea un frame con sombra moderna"""
        if UI_CONFIG['sombras']:
            frame_sombra = tk.Frame(
                parent, 
                bg=COLORES['sombra_suave'], 
                relief="flat", 
                bd=0
            )
            frame_sombra.pack(fill="both", padx=2, pady=2)
            
            frame_interno = tk.Frame(
                frame_sombra, 
                bg=COLORES['frame'], 
                relief="flat", 
                bd=0,
                **kwargs
            )
            frame_interno.pack(fill="both", padx=0, pady=0)
            
            return frame_interno
        else:
            return tk.Frame(parent, **kwargs)

class FormularioPaciente:    
    def __init__(self, parent):
        self.parent = parent
        self.widgets = {}
        self.servicios_recientes = []
        self._crear_formulario()
    
    def _crear_formulario(self):
        """Crea todos los elementos del formulario con diseño mejorado"""
        self.frame_formulario = EstiloManager.crear_frame_con_sombra(
            self.parent
        )
        self.frame_formulario.pack(fill="x", padx=15, pady=15)
    
        self.frame_formulario.columnconfigure(1, weight=1)
        
        self._crear_campo_apellido()
        self._crear_campo_nombre()
        self._crear_campo_fecha()
        self._crear_campo_servicio()
        self._crear_campo_servicio_personalizado()
        
        self._crear_servicios_recientes()
    
    def _crear_campo_apellido(self):
        label = tk.Label(
            self.frame_formulario, 
            text="👤 Apellido(s):", 
            font=FUENTES['etiqueta_campo'], 
            bg=COLORES['frame'], 
            fg=COLORES['label']
        )
        label.grid(row=0, column=0, sticky="e", padx=20, pady=(25, 8))
        
        self.widgets['apellido'] = tk.Entry(
            self.frame_formulario, 
            font=FUENTES['texto'], 
            relief="flat", 
            bd=1, 
            bg=COLORES['entry_bg'],
            highlightthickness=2, 
            highlightbackground=COLORES['entry_border'],
            highlightcolor=COLORES['entry_border'] 
        )
        self.widgets['apellido'].grid(row=0, column=1, sticky="we", padx=20, pady=(25, 8))
        
        self._configurar_eventos_campo(self.widgets['apellido'])
        
    
    def _crear_campo_nombre(self):

        label = tk.Label(
            self.frame_formulario, 
            text="👤 Nombre(s):", 
            font=FUENTES['etiqueta_campo'], 
            bg=COLORES['frame'], 
            fg=COLORES['label']
        )
        label.grid(row=1, column=0, sticky="e", padx=20, pady=8)

        self.widgets['nombre'] = tk.Entry(
            self.frame_formulario, 
            font=FUENTES['texto'], 
            relief="flat", 
            bd=1, 
            bg=COLORES['entry_bg'],
            highlightthickness=2, 
            highlightbackground=COLORES['entry_border'],
            highlightcolor=COLORES['entry_border']  
        )
        self.widgets['nombre'].grid(row=1, column=1, sticky="we", padx=20, pady=8)
        
        self._configurar_eventos_campo(self.widgets['nombre'])
        

    
    def _crear_campo_fecha(self):
        tk.Label(self.frame_formulario, text="Fecha de ingreso:", font=FUENTES['titulo'], 
                bg=COLORES['frame'], fg=COLORES['label']).grid(row=2, column=0, 
                                                             sticky="e", padx=20, pady=8)
        

        frame_fecha = tk.Frame(self.frame_formulario, bg=COLORES['frame'])
        frame_fecha.grid(row=2, column=1, sticky="we", padx=20, pady=8)

        self.widgets['fecha'] = tk.Entry(
            frame_fecha,
            font=FUENTES['texto'],
            relief="flat",
            bd=1,
            bg=COLORES['entry_bg'],
            highlightthickness=2,
            highlightbackground=COLORES['entry_border'],
            highlightcolor=COLORES['entry_border'],
            width=15
        )
        self.widgets['fecha'].pack(side="left", padx=(0, 10))
        
        self.boton_fecha = tk.Button(
            frame_fecha,
            text="📅",
            font=("Segoe UI", 12),
            bg=COLORES['boton_secundario'],
            fg="white",
            relief="flat",
            bd=0,
            padx=8,
            pady=4,
            cursor="hand2",
            command=self._abrir_selector_fecha
        )
        self.boton_fecha.pack(side="left")
        

        self._configurar_eventos_campo(self.widgets['fecha'])
        
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        self.widgets['fecha'].insert(0, fecha_actual)
        
        self.widgets['fecha'].bind('<KeyRelease>', self._validar_formato_fecha)
    
    def _abrir_selector_fecha(self):

        ventana_fecha = VentanaSelectorFecha(self.parent, self.widgets['fecha'])
    
    def _validar_formato_fecha(self, event=None):

        fecha_texto = self.widgets['fecha'].get()
        

        fecha_limpia = ''.join(c for c in fecha_texto if c.isdigit() or c == '/')
        
        # Aplicar formato automático dd/mm/yyyy
        if len(fecha_limpia) >= 2 and fecha_limpia[2] != '/':
            fecha_limpia = fecha_limpia[:2] + '/' + fecha_limpia[2:]
        if len(fecha_limpia) >= 5 and fecha_limpia[5] != '/':
            fecha_limpia = fecha_limpia[:5] + '/' + fecha_limpia[5:]
        
        # Limitar a 10 caracteres (dd/mm/yyyy)
        if len(fecha_limpia) > 10:
            fecha_limpia = fecha_limpia[:10]
        
        # Actualizar el campo si cambió
        if fecha_limpia != fecha_texto:
            self.widgets['fecha'].delete(0, tk.END)
            self.widgets['fecha'].insert(0, fecha_limpia)
    
    def _configurar_eventos_campo(self, widget):

        if not UI_CONFIG['efectos_hover']:
            return
            
        def on_enter(event):
            EstiloManager.aplicar_estilo_hover(widget)
            
        def on_leave(event):
            EstiloManager.aplicar_estilo_normal(widget)
            
        def on_focus_in(event):
            EstiloManager.aplicar_estilo_focus(widget)
            
        def on_focus_out(event):
            EstiloManager.aplicar_estilo_normal(widget)
            

        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
        widget.bind('<FocusIn>', on_focus_in)
        widget.bind('<FocusOut>', on_focus_out)
    
    def _crear_campo_servicio(self):

        # Etiqueta con icono
        label = tk.Label(
            self.frame_formulario, 
            text="🏥 Servicio:", 
            font=FUENTES['etiqueta_campo'], 
            bg=COLORES['frame'], 
            fg=COLORES['label']
        )
        label.grid(row=3, column=0, sticky="e", padx=20, pady=8)
        

        frame_servicio = tk.Frame(self.frame_formulario, bg=COLORES['frame'])
        frame_servicio.grid(row=3, column=1, sticky="we", padx=20, pady=8)
        

        self.widgets['servicio'] = ttk.Combobox(
            frame_servicio, 
            values=SERVICIOS_PREDEFINIDOS, 
            font=FUENTES['texto'], 
            state="readonly", 
            width=25
        )
        self.widgets['servicio'].pack(side="left")
        

        self._configurar_eventos_campo(self.widgets['servicio'])
        
        

        self.widgets['servicio'].bind('<<ComboboxSelected>>', self._manejar_cambio_servicio)

        self.frame_servicios_recientes = tk.Frame(self.frame_formulario, bg=COLORES['frame'])
        self.frame_servicios_recientes.grid(row=4, column=1, sticky="w", padx=20, pady=(15, 20))
        
    def _crear_servicios_recientes(self):
        """Crea la sección de servicios recientes con mejor diseño"""
        label_recientes = tk.Label(
            self.frame_servicios_recientes, 
            text="🕒 Servicios recientes:", 
            font=FUENTES['etiqueta_servicios'], 
            bg=COLORES['frame'], 
            fg=COLORES['separador']
        )
        label_recientes.pack(anchor="w", pady=(0, 8))
        

        self.frame_hipervinculos = tk.Frame(self.frame_servicios_recientes, bg=COLORES['frame'])
        self.frame_hipervinculos.pack(fill="x")
        

        self._actualizar_servicios_recientes()
        
    def _crear_campo_servicio_personalizado(self):

        self.frame_otro = tk.Frame(self.frame_formulario, bg=COLORES['frame'])
        self.frame_otro.grid(row=5, column=1, sticky="we", padx=20, pady=(5, 20))
        self.frame_otro.grid_remove()
        
        label_otro = tk.Label(
            self.frame_otro, 
            text="✏️ Servicio personalizado:", 
            font=FUENTES['etiqueta_campo'], 
            bg=COLORES['frame'], 
            fg=COLORES['label']
        )
        label_otro.pack(anchor="w", pady=(0, 5))
        
        self.widgets['otro'] = tk.Entry(
            self.frame_otro, 
            font=FUENTES['texto'], 
            relief="flat", 
            bd=1, 
            bg=COLORES['entry_bg'],
            highlightthickness=2,  
            highlightbackground=COLORES['entry_border'],
            highlightcolor=COLORES['entry_border']  
        )
        self.widgets['otro'].pack(fill="x", pady=(0, 5))

        self._configurar_eventos_campo(self.widgets['otro'])
        

    def _manejar_cambio_servicio(self, event):
        servicio_seleccionado = self.widgets['servicio'].get()

        if servicio_seleccionado in SERVICIOS_DIFERENCIADOS:

            from ui_components import VentanaServicioDiferenciado
            opciones = SERVICIOS_DIFERENCIADOS[servicio_seleccionado]
            ventana_servicio = VentanaServicioDiferenciado(self.parent, servicio_seleccionado, opciones)
            
            if ventana_servicio.resultado:
                servicio_completo = f"{servicio_seleccionado} {ventana_servicio.resultado}"
                self.widgets['servicio'].set(servicio_completo)
            else:
                self.widgets['servicio'].set('')
        
        es_otro = servicio_seleccionado == "Otro"
        self.mostrar_servicio_personalizado(es_otro)
    
    def _actualizar_servicios_recientes(self):
        if hasattr(self, '_ultimos_servicios') and self._ultimos_servicios == self.servicios_recientes:
            return
            
        self._ultimos_servicios = self.servicios_recientes.copy()
        
        for widget in self.frame_servicios_recientes.winfo_children():
            widget.destroy()
        
        if self.servicios_recientes:
            label_titulo = tk.Label(self.frame_servicios_recientes, 
                                   text="Servicios recientes:", 
                                   font=FUENTES['etiqueta_servicios'], 
                                   bg=COLORES['frame'], 
                                   fg=COLORES['label'])
            label_titulo.grid(row=0, column=0, sticky="w", padx=(0, 15), pady=(0, 8))
            
            # Crear hipervínculos organizados en filas de 2
            for i, servicio in enumerate(self.servicios_recientes):
                # Calcular fila y columna para layout de 2 por línea
                fila = (i // 2) + 1  # +1 porque la fila 0 es el título
                columna = (i % 2) * 2  # 0 o 2 (dejando espacio para separadores)
                
                hipervinculo = tk.Label(self.frame_servicios_recientes, 
                                       text=servicio, 
                                       font=FUENTES['hipervinculo'], 
                                       bg=COLORES['frame'], 
                                       fg=COLORES['hipervinculo'], 
                                       cursor="hand2",
                                       relief="flat",
                                       bd=0)
                
                hipervinculo.grid(row=fila, column=columna, sticky="w", padx=(0, 15), pady=3)
                
                hipervinculo.bind("<Enter>", lambda e, s=servicio: self._resaltar_hipervinculo(e, True))
                hipervinculo.bind("<Leave>", lambda e, s=servicio: self._resaltar_hipervinculo(e, False))
                hipervinculo.bind("<Button-1>", lambda e, s=servicio: self._seleccionar_servicio_reciente(s))
                
                if i < len(self.servicios_recientes) - 1:
                    separador = tk.Label(self.frame_servicios_recientes, 
                                       text="•", 
                                       font=FUENTES['etiqueta_servicios'], 
                                       bg=COLORES['frame'], 
                                       fg=COLORES['separador'])
                    
                    separador.grid(row=fila, column=columna + 1, sticky="w", padx=(0, 15), pady=3)
    
    def _resaltar_hipervinculo(self, event, resaltar):
        if resaltar:
            event.widget.config(fg=COLORES['hipervinculo_hover'], bg=COLORES['frame_sombra'])
        else:
            event.widget.config(fg=COLORES['hipervinculo'], bg=COLORES['frame'])
    
    def _seleccionar_servicio_reciente(self, servicio):
        self.widgets['servicio'].set(servicio)
        self.widgets['servicio'].event_generate('<<ComboboxSelected>>')
    
    def limpiar_campos(self):
        self.widgets['apellido'].delete(0, tk.END)
        self.widgets['nombre'].delete(0, tk.END)
        
        self.widgets['fecha'].delete(0, tk.END)
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        self.widgets['fecha'].insert(0, fecha_actual)
        
        self.widgets['servicio'].set('')
        self.widgets['otro'].delete(0, tk.END)
        self.frame_otro.grid_remove()
        
        for widget_name, widget in self.widgets.items():
            if isinstance(widget, tk.Entry):
                EstiloManager.aplicar_estilo_normal(widget)
        
        self.widgets['apellido'].focus()
    
    def mostrar_servicio_personalizado(self, mostrar=True):
        if mostrar:
            self.frame_otro.grid()
            self.widgets['otro'].focus()
        else:
            self.frame_otro.grid_remove()
    
    def configurar_eventos(self, eventos):
        for widget_name, event_func in eventos.items():
            if widget_name in self.widgets:
                self.widgets[widget_name].bind('<KeyRelease>', event_func)
    
    def obtener_datos(self):
        fecha_raw = self.widgets['fecha'].get()
        
        if fecha_raw:
            fecha_limpia = fecha_raw
            fecha_limpia = fecha_limpia.replace("'", "").replace('"', "").replace("'", "").replace("'", "")
            fecha_limpia = fecha_limpia.replace("'", "").replace("'", "").replace(""", "").replace(""", "")
            fecha_limpia = fecha_limpia.strip()
        else:
            fecha_limpia = ""
        
        datos_retorno = {
            'apellido': self.widgets['apellido'].get().strip(),
            'nombre': self.widgets['nombre'].get().strip(),
            'fecha': fecha_limpia,
            'servicio': self.widgets['servicio'].get(),
            'otro': self.widgets['otro'].get().strip()
        }
        
        return datos_retorno
    
    def registrar_servicio_utilizado(self, servicio):
        """Registra un servicio como utilizado en la memoria volátil - OPTIMIZADO"""
        if servicio and servicio.strip():
            servicio_limpio = servicio.strip()
            
            if servicio_limpio in self.servicios_recientes:
                self.servicios_recientes.remove(servicio_limpio)
            
            self.servicios_recientes.insert(0, servicio_limpio)
            
            if len(self.servicios_recientes) > 4:
                self.servicios_recientes = self.servicios_recientes[:4]
            
            self._actualizar_servicios_recientes()

class PanelBotones:
    
    def __init__(self, parent):
        self.parent = parent
        self.botones = {}
        self._crear_panel()
    
    def _crear_panel(self):
        self.frame_panel = EstiloManager.crear_frame_con_sombra(
            self.parent
        )
        self.frame_panel.pack(fill="x", padx=15, pady=15)
        
        frame_interno = tk.Frame(self.frame_panel, bg=COLORES['frame'])
        frame_interno.pack(expand=True, pady=20)
        
        frame_interno.columnconfigure(0, weight=1)
        frame_interno.columnconfigure(2, weight=1)
        
        self.botones['cargar'] = tk.Button(
            frame_interno,
            text="💾 Cargar Paciente",
            font=FUENTES['boton'],
            bg=COLORES['boton_primario'],
            fg="white",
            relief="flat",
            bd=0,
            padx=30,
            pady=15,
            width=20,
            height=1,
            activebackground=COLORES['boton_primario_hover'],
            activeforeground="white",
            cursor="hand2"
        )
        self.botones['cargar'].grid(row=0, column=1, padx=10)
        
        self.botones['limpiar'] = tk.Button(
            frame_interno,
            text="🧹 Limpiar",
            font=FUENTES['boton'],
            bg=COLORES['boton_secundario'],
            fg="white",
            relief="flat",
            bd=0,
            padx=30,
            pady=15,
            width=20,
            height=1,
            activebackground=COLORES['boton_secundario_hover'],
            activeforeground="white",
            cursor="hand2"
        )
        self.botones['limpiar'].grid(row=0, column=3, padx=10)
        
        self._configurar_efectos_botones()
    
    def _configurar_efectos_botones(self):
        if not UI_CONFIG['efectos_hover']:
            return
            
        for nombre, boton in self.botones.items():
            boton.bind('<Enter>', lambda e, b=boton: self._on_hover_enter(b))
            boton.bind('<Leave>', lambda e, b=boton: self._on_hover_leave(b))
            
            boton.bind('<Button-1>', lambda e, b=boton: self._on_click(b))
            boton.bind('<ButtonRelease-1>', lambda e, b=boton: self._on_release(b))
    
    def _on_hover_enter(self, boton):
        if boton.cget('text').startswith('💾'):
            boton.config(bg=COLORES['boton_primario_hover'])
        elif boton.cget('text').startswith('🧹'):
            boton.config(bg=COLORES['boton_secundario_hover'])
        else:
            boton.config(bg=COLORES['boton_primario_hover'])
    
    def _on_hover_leave(self, boton):
        if boton.cget('text').startswith('💾'):
            boton.config(bg=COLORES['boton_primario'])
        elif boton.cget('text').startswith('🧹'):
            boton.config(bg=COLORES['boton_secundario'])
        else:
            boton.config(bg=COLORES['estado_info'])
    
    def _on_click(self, boton):
        boton.config(relief="sunken", bd=1)
    
    def _on_release(self, boton):
        boton.config(relief="flat", bd=0)
    
    def cambiar_estado_cargar(self, cargando=False):
        if cargando:
            self.botones['cargar'].config(
                text="⏳ Cargando...",
                state="disabled",
                bg=COLORES['estado_cargando']
            )
        else:
            self.botones['cargar'].config(
                text="💾 Cargar Paciente",
                state="normal",
                bg=COLORES['boton_primario']
            )
    
    def obtener_boton(self, nombre):
        return self.botones.get(nombre)
    
    def configurar_comando(self, nombre, comando):
        if nombre in self.botones:
            self.botones[nombre].config(command=comando)

class VentanaServicioDiferenciado:
    
    def __init__(self, parent, servicio_principal, opciones):
        self.parent = parent
        self.servicio_principal = servicio_principal
        self.opciones = opciones
        self.resultado = None
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title(f"Seleccionar {servicio_principal}")
        self.ventana.configure(bg=COLORES['fondo'])
        
        self.ventana.geometry("600x500")
        self.ventana.resizable(False, False)
        self.ventana.transient(parent)
        self.ventana.grab_set()
        
        self.ventana.update_idletasks()
        x = (self.ventana.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (500 // 2)
        self.ventana.geometry(f"600x500+{x}+{y}")
        
        self._crear_interfaz()
        
        self.ventana.protocol("WM_DELETE_WINDOW", self._cerrar_sin_seleccion)
        
        self.ventana.wait_window()
    
    def _crear_interfaz(self):
        frame_principal = EstiloManager.crear_frame_con_sombra(
            self.ventana
        )
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        titulo = tk.Label(
            frame_principal, 
            text=f"🏥 {self.servicio_principal}", 
            font=FUENTES['titulo_grande'], 
            bg=COLORES['frame'], 
            fg=COLORES['label']
        )
        titulo.pack(pady=(30, 10))
        
        subtitulo = tk.Label(
            frame_principal, 
            text="Seleccione la opción correspondiente:", 
            font=FUENTES['subtitulo'], 
            bg=COLORES['frame'], 
            fg=COLORES['separador']
        )
        subtitulo.pack(pady=(0, 30))
        
        frame_botones = tk.Frame(frame_principal, bg=COLORES['frame'])
        frame_botones.pack(fill="x", padx=40)
        
        for i, opcion in enumerate(self.opciones):
            boton = tk.Button(
                frame_botones,
                text=f"🔹 {opcion}",
                font=FUENTES['boton'],
                bg=COLORES['boton_primario'],
                fg="white",
                relief="flat",
                bd=0,
                padx=30,
                pady=15,
                width=20,
                height=1,
                activebackground=COLORES['boton_primario_hover'],
                activeforeground="white",
                cursor="hand2",
                command=lambda o=opcion: self._seleccionar_opcion(o)
            )
            boton.pack(pady=10, fill="x")
            
            if UI_CONFIG['efectos_hover']:
                boton.bind('<Enter>', lambda e, b=boton: self._on_hover_enter(b))
                boton.bind('<Leave>', lambda e, b=boton: self._on_hover_leave(b))
                boton.bind('<Button-1>', lambda e, b=boton: self._on_click(b))
                boton.bind('<ButtonRelease-1>', lambda e, b=boton: self._on_release(b))
        
        boton_cancelar = tk.Button(
            frame_principal,
            text="❌ Cancelar",
            font=FUENTES['boton'],
            bg=COLORES['boton_secundario'],
            fg="white",
            relief="flat",
            bd=0,
            padx=30,
            pady=10,
            width=15,
            height=1,
            activebackground=COLORES['boton_secundario_hover'],
            activeforeground="white",
            cursor="hand2",
            command=self._cerrar_sin_seleccion
        )
        boton_cancelar.pack(pady=(20, 30))
        
        if UI_CONFIG['efectos_hover']:
            boton_cancelar.bind('<Enter>', lambda e, b=boton_cancelar: self._on_hover_enter_cancelar(b))
            boton_cancelar.bind('<Leave>', lambda e, b=boton_cancelar: self._on_hover_leave_cancelar(b))
    
    def _on_hover_enter(self, boton):
        boton.config(bg=COLORES['boton_primario_hover'])
    
    def _on_hover_leave(self, boton):
        boton.config(bg=COLORES['boton_primario'])
    
    def _on_click(self, boton):
        boton.config(relief="sunken", bd=1)
    
    def _on_release(self, boton):
        boton.config(relief="flat", bd=0)
    
    def _on_hover_enter_cancelar(self, boton):
        boton.config(bg=COLORES['boton_secundario_hover'])
    
    def _on_hover_leave_cancelar(self, boton):
        boton.config(bg=COLORES['boton_secundario'])
    
    def _seleccionar_opcion(self, opcion):
        self.resultado = opcion
        self.ventana.destroy()
    
    def _cerrar_sin_seleccion(self):
        self.resultado = None
        self.ventana.destroy()


class VentanaSelectorFecha:
    
    def __init__(self, parent, campo_fecha):
        self.parent = parent
        self.campo_fecha = campo_fecha
        self.fecha_seleccionada = None
        self.botones_dias = []
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("📅 Selector de Fecha")
        self.ventana.configure(bg=COLORES['fondo'])
        
        self.ventana.geometry("450x520")
        self.ventana.resizable(False, False)
        self.ventana.transient(parent)
        self.ventana.grab_set()
        
        self.ventana.update_idletasks()
        
        screen_width = self.ventana.winfo_screenwidth()
        screen_height = self.ventana.winfo_screenheight()
        
        x = (screen_width // 2) - (450 // 2)
        y = (screen_height // 2) - (520 // 2)
        
        x = max(0, min(x, screen_width - 450))
        y = max(0, min(y, screen_height - 520))
        
        self.ventana.geometry(f"450x520+{x}+{y}")
        
        self.ventana.update()
        self.ventana.lift()
        
        try:
            self.ventana.wm_attributes('-topmost', True)
        except:
            pass
            
        self._crear_interfaz()
        
        self.ventana.protocol("WM_DELETE_WINDOW", self._cerrar_sin_seleccion)
        
        self.ventana.bind('<Escape>', lambda e: self._cerrar_sin_seleccion())
        self.ventana.bind('<Return>', lambda e: self._seleccionar_hoy())
        
        self.ventana.focus_set()
        
        self.ventana.wait_window()
    
    def _crear_interfaz(self):
        frame_principal = EstiloManager.crear_frame_con_sombra(self.ventana)
        frame_principal.pack(fill="both", expand=True, padx=15, pady=15)
        
        self._crear_header(frame_principal)
        
        separador = tk.Frame(frame_principal, height=2, bg=COLORES['separador'])
        separador.pack(fill="x", pady=(10, 20))
        
        self._crear_header_dias(frame_principal)
        
        self.frame_calendario = tk.Frame(
            frame_principal, 
            bg=COLORES['frame'],
            relief="flat",
            bd=0
        )
        self.frame_calendario.pack(fill="both", expand=True, pady=10)
        
        self.fecha_actual = datetime.now()
        self._generar_calendario()
        
        self._crear_botones_accion(frame_principal)
    
    def _crear_header(self, parent):
        frame_header = tk.Frame(parent, bg=COLORES['frame'])
        frame_header.pack(fill="x", pady=(10, 0))
        
        titulo = tk.Label(
            frame_header,
            text="📅 Seleccionar Fecha de Ingreso",
            font=("Segoe UI", 16, "bold"),
            bg=COLORES['frame'],
            fg=COLORES['label']
        )
        titulo.pack(pady=(0, 15))
        
        frame_nav = tk.Frame(frame_header, bg=COLORES['frame'])
        frame_nav.pack(fill="x")
        
        frame_nav.columnconfigure(1, weight=1)
        
        self.boton_anterior = tk.Button(
            frame_nav,
            text="‹",
            font=("Segoe UI", 24, "bold"),
            bg=COLORES['entry_bg'],
            fg=COLORES['boton_primario'],
            relief="flat",
            bd=0,
            width=3,
            height=1,
            cursor="hand2",
            command=self._mes_anterior
        )
        self.boton_anterior.grid(row=0, column=0, padx=10)
        
        self.label_mes = tk.Label(
            frame_nav,
            text="",
            font=("Segoe UI", 18, "bold"),
            bg=COLORES['frame'],
            fg=COLORES['label']
        )
        self.label_mes.grid(row=0, column=1)
        
        self.boton_siguiente = tk.Button(
            frame_nav,
            text="›",
            font=("Segoe UI", 24, "bold"),
            bg=COLORES['entry_bg'],
            fg=COLORES['boton_primario'],
            relief="flat",
            bd=0,
            width=3,
            height=1,
            cursor="hand2",
            command=self._mes_siguiente
        )
        self.boton_siguiente.grid(row=0, column=2, padx=10)
        
        self._configurar_efectos_navegacion()
    
    def _crear_header_dias(self, parent):
        frame_dias = tk.Frame(parent, bg=COLORES['frame'])
        frame_dias.pack(fill="x", pady=(0, 5))
        
        dias_semana = ["LUN", "MAR", "MIÉ", "JUE", "VIE", "SÁB", "DOM"]
        colores_dias = [COLORES['label']] * 5 + [COLORES['error']] * 2
        
        for i, (dia, color) in enumerate(zip(dias_semana, colores_dias)):
            label = tk.Label(
                frame_dias,
                text=dia,
                font=("Segoe UI", 10, "bold"),
                bg=COLORES['frame'],
                fg=color,
                width=6,
                height=1
            )
            label.grid(row=0, column=i, padx=1)
    
    def _crear_botones_accion(self, parent):
        frame_botones = tk.Frame(parent, bg=COLORES['frame'])
        frame_botones.pack(fill="x", pady=(20, 10))
        
        frame_botones.columnconfigure(0, weight=1)
        frame_botones.columnconfigure(2, weight=1)
        
        boton_hoy = tk.Button(
            frame_botones,
            text="📅 Hoy",
            font=("Segoe UI", 11, "bold"),
            bg=COLORES['boton_primario'],
            fg="white",
            relief="flat",
            bd=0,
            padx=25,
            pady=12,
            cursor="hand2",
            command=self._seleccionar_hoy
        )
        boton_hoy.grid(row=0, column=1, padx=5)
        
        boton_cancelar = tk.Button(
            frame_botones,
            text="✕ Cancelar",
            font=("Segoe UI", 11),
            bg=COLORES['boton_secundario'],
            fg="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=12,
            cursor="hand2",
            command=self._cerrar_sin_seleccion
        )
        boton_cancelar.grid(row=0, column=2, padx=5, sticky="e")
        
        self._configurar_efectos_botones(boton_hoy, boton_cancelar)
    
    def _configurar_efectos_navegacion(self):
        def on_enter_nav(event, boton):
            boton.config(bg=COLORES['boton_primario_hover'], fg="white")
        
        def on_leave_nav(event, boton):
            boton.config(bg=COLORES['entry_bg'], fg=COLORES['boton_primario'])
        
        self.boton_anterior.bind('<Enter>', lambda e: on_enter_nav(e, self.boton_anterior))
        self.boton_anterior.bind('<Leave>', lambda e: on_leave_nav(e, self.boton_anterior))
        self.boton_siguiente.bind('<Enter>', lambda e: on_enter_nav(e, self.boton_siguiente))
        self.boton_siguiente.bind('<Leave>', lambda e: on_leave_nav(e, self.boton_siguiente))
    
    def _configurar_efectos_botones(self, *botones):
        def on_enter_primary(event, boton):
            if 'Hoy' in boton.cget('text'):
                boton.config(bg=COLORES['boton_primario_hover'])
            else:
                boton.config(bg=COLORES['boton_secundario_hover'])
        
        def on_leave_primary(event, boton):
            if 'Hoy' in boton.cget('text'):
                boton.config(bg=COLORES['boton_primario'])
            else:
                boton.config(bg=COLORES['boton_secundario'])
        
        for boton in botones:
            boton.bind('<Enter>', lambda e, b=boton: on_enter_primary(e, b))
            boton.bind('<Leave>', lambda e, b=boton: on_leave_primary(e, b))
    
    def _generar_calendario(self):
        for widget in self.frame_calendario.winfo_children():
            widget.destroy()
        
        self.botones_dias = []
        
        primer_dia = self.fecha_actual.replace(day=1)
        if self.fecha_actual.month == 12:
            ultimo_dia = self.fecha_actual.replace(year=self.fecha_actual.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            ultimo_dia = self.fecha_actual.replace(month=self.fecha_actual.month + 1, day=1) - timedelta(days=1)
        
        dia_semana = primer_dia.weekday()
        
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        self.label_mes.config(text=f"{meses[self.fecha_actual.month - 1]} {self.fecha_actual.year}")
        
        fila = 0
        
        for col in range(dia_semana):
            espaciador = tk.Frame(
                self.frame_calendario,
                bg=COLORES['frame'],
                width=50,
                height=40
            )
            espaciador.grid(row=fila, column=col, padx=3, pady=3)
            espaciador.grid_propagate(False)
        
        for dia in range(1, ultimo_dia.day + 1):
            col = (dia_semana + dia - 1) % 7
            if col == 0 and dia > 1:
                fila += 1
            
            fecha_boton = self.fecha_actual.replace(day=dia)
            es_hoy = (fecha_boton.date() == datetime.now().date())
            es_fin_semana = col >= 5  # Sábado (5) y Domingo (6)
            es_futuro = fecha_boton.date() > datetime.now().date()  # Comparar solo fechas, no horas
            

            
            if not es_futuro:
                from functools import partial
                boton_dia = tk.Button(
                    self.frame_calendario,
                    text=str(dia),
                    font=("Segoe UI", 11, "bold" if es_hoy else "normal"),
                    relief="flat",
                    bd=0,
                    width=6,
                    height=2,
                    cursor="hand2",
                    command=partial(self._seleccionar_fecha, dia)
                )
            else:
                boton_dia = tk.Button(
                    self.frame_calendario,
                    text=str(dia),
                    font=("Segoe UI", 11, "normal"),
                    relief="flat",
                    bd=0,
                    width=6,
                    height=2,
                    cursor="arrow",
                    command=None
                )
            

            
            if es_futuro:
                boton_dia.config(
                    bg=COLORES['sombra_suave'],
                    fg=COLORES['separador'],
                    state="disabled"
                )
            elif es_hoy:
                boton_dia.config(
                    bg=COLORES['boton_primario'],
                    fg="white",
                    relief="solid",
                    bd=1
                )
            elif es_fin_semana:
                boton_dia.config(
                    bg=COLORES['entry_bg'],
                    fg=COLORES['error'],
                    activebackground=COLORES['boton_secundario_hover'],
                    activeforeground="white"
                )
            else:
                boton_dia.config(
                    bg=COLORES['entry_bg'],
                    fg=COLORES['label'],
                    activebackground=COLORES['boton_primario_hover'],
                    activeforeground="white"
                )
            
            boton_dia.grid(row=fila, column=col, padx=3, pady=3, sticky="nsew")
            
            if not es_futuro:
                self._configurar_efecto_dia(boton_dia, es_hoy, es_fin_semana)
                self._agregar_efecto_clic(boton_dia)
            
            self.botones_dias.append(boton_dia)
        
        for i in range(7):
            self.frame_calendario.columnconfigure(i, weight=1)
        for i in range(fila + 1):
            self.frame_calendario.rowconfigure(i, weight=1)
    
    def _configurar_efecto_dia(self, boton, es_hoy, es_fin_semana):
        bg_original = boton.cget('bg')
        fg_original = boton.cget('fg')
        
        def on_enter(event):
            if es_hoy:
                boton.config(bg=COLORES['boton_primario_hover'])
            elif es_fin_semana:
                boton.config(bg=COLORES['error'], fg="white")
            else:
                boton.config(bg=COLORES['boton_primario'], fg="white")
        
        def on_leave(event):
            boton.config(bg=bg_original, fg=fg_original)
        
        boton.bind('<Enter>', on_enter)
        boton.bind('<Leave>', on_leave)
    
    def _agregar_efecto_clic(self, boton):
        def on_click_visual(event):
            relief_original = boton.cget('relief')
            boton.config(relief="sunken")
            boton.after(100, lambda: boton.config(relief=relief_original))
        
        boton.bind('<ButtonRelease-1>', on_click_visual)
    
    def _mes_anterior(self):
        if self.fecha_actual.month == 1:
            self.fecha_actual = self.fecha_actual.replace(year=self.fecha_actual.year - 1, month=12)
        else:
            self.fecha_actual = self.fecha_actual.replace(month=self.fecha_actual.month - 1)
        
        self._generar_calendario()
    
    def _mes_siguiente(self):
        if self.fecha_actual.month == 12:
            self.fecha_actual = self.fecha_actual.replace(year=self.fecha_actual.year + 1, month=1)
        else:
            self.fecha_actual = self.fecha_actual.replace(month=self.fecha_actual.month + 1)
        
        self._generar_calendario()
    
    def _seleccionar_fecha(self, dia):
        fecha_seleccionada = self.fecha_actual.replace(day=dia)
        fecha_formateada = fecha_seleccionada.strftime("%d/%m/%Y")
        
        self.campo_fecha.delete(0, tk.END)
        self.campo_fecha.insert(0, fecha_formateada)
        
        self.ventana.destroy()
    
    def _seleccionar_hoy(self):
        fecha_hoy = datetime.now()
        fecha_formateada = fecha_hoy.strftime("%d/%m/%Y")
        
        self.campo_fecha.delete(0, tk.END)
        self.campo_fecha.insert(0, fecha_formateada)
        
        self.ventana.destroy()
    
    def _cerrar_sin_seleccion(self):
        self.ventana.destroy()


 