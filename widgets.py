import customtkinter as ctk
from tkcalendar import DateEntry
from datetime import datetime
from scroll import crear_scroll_vertical

class WidgetsFactory():

    # Método para configurar apariencia.
    @staticmethod
    def config_apariencia(color_apariencia, color_default):
        ctk.set_appearance_mode(color_apariencia)
        ctk.set_default_color_theme(color_default)

    # Método para la creación de frames.
    @staticmethod
    def crear_frame(parent, fill, pady, text=None, expand=False):
            frame = ctk.CTkFrame(parent)
            frame.pack(fill=fill, pady=pady, expand=expand)

            # Revisar si el frame lleva título.
            if text:
                label = ctk.CTkLabel(frame, text=text, font=("Arial", 16, "bold"))
                label.pack(pady=10)
            return frame

    # Método para la creación de botones.
    @staticmethod
    def crear_boton(frame, text, command):
        boton = ctk.CTkButton(frame, text=text, command=command, height=40, font=("Arial", 14, "bold"))
        boton.pack(pady=10)
        return boton

    # Método para la creación de campos (entry).
    @staticmethod
    def crear_campo_entry(frame, texto, placeholder):
        contenedor = ctk.CTkFrame(frame, fg_color="transparent")
        contenedor.pack(fill="x", padx=20, pady=8) 
        label = ctk.CTkLabel(contenedor, text=texto, width=120, anchor="w")
        label.pack(side="left", padx=(0, 10))
        entry = ctk.CTkEntry(contenedor, placeholder_text=placeholder)
        entry.pack(side="left", fill="x", expand=True)
        return entry
    
    # Método para la creación de campos automáticos (entry).
    @staticmethod
    def crear_campo_entry_auto(frame, texto, placeholder):
        contenedor = ctk.CTkFrame(frame, fg_color="transparent")
        contenedor.pack(fill="x", padx=20, pady=8) 
        label = ctk.CTkLabel(contenedor, text=texto, width=120, anchor="w")
        label.pack(side="left", padx=(0, 10))
        entry = ctk.CTkEntry(contenedor, placeholder_text=placeholder)
        entry.pack(side="left", fill="x", expand=True)
        entry.configure(state="readonly", fg_color="#1e1e1e", border_color="#4CC9F0", text_color="#4CC9F0")
        return entry

    # Método para la creación de campos (combobox).
    @staticmethod
    def crear_campo_combo(frame, texto, opciones, valor_default=None):
        contenedor = ctk.CTkFrame(frame, fg_color="transparent")
        contenedor.pack(fill="x", padx=20, pady=8) 
        label = ctk.CTkLabel(contenedor, text=texto, width=120, anchor="w")
        label.pack(side="left", padx=(0, 10))
        combobox = ctk.CTkComboBox(contenedor, values=opciones, state="readonly")
        combobox.pack(side="left", fill="x", expand=True)

        # Establecer valor combobox por default.
        if valor_default and valor_default in opciones:
            combobox.set(valor_default)
        elif opciones:
            combobox.set(opciones[0])
        return combobox

    # Método para frame izquierda.
    @staticmethod
    def crear_frame_izquierda(parent):
        frame = ctk.CTkFrame(parent)
        frame.pack(side="left", fill="both", expand=True, padx=(20, 10), pady=10)
        return frame
    
    # Método para frame derecha.
    @staticmethod
    def crear_frame_derecha(parent):
        frame = ctk.CTkFrame(parent)
        frame.pack(side="right", fill="both", expand=True, padx=(10, 20), pady=10)
        return frame
    
    # Método para frame de controles.
    @staticmethod
    def crear_frame_controles(parent, text_btn_agregar="Agregar", comando_agregar=None, text_btn_guardar="Guardar",
        comando_guardar=None):
        frame_controles = ctk.CTkFrame(parent)
        frame_controles.pack(fill="x", padx=20, pady=(0,10))

        btn_agregar = ctk.CTkButton(frame_controles, text=text_btn_agregar, command=comando_agregar, 
            width=150, height=35, font=("Arial", 12))
        btn_agregar.pack(side="left", padx=(0,10))
        btn_guardar = ctk.CTkButton(frame_controles, text=text_btn_guardar, command=comando_guardar,
            width=150, height=35, font=("Arial", 12))
        btn_guardar.pack(side="left", padx=(0, 10))

        return {
            "frame": frame_controles,
            "btn_agregar": btn_agregar,
            "btn_guardar": btn_guardar
        }
    
    # Método para frame de tabla.
    @staticmethod
    def crear_frame_tabla(parent, altura_maxima=250):
        frame_tabla = ctk.CTkFrame(parent)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=(0, 5))
        scroll_data = crear_scroll_vertical(frame_tabla, altura_maxima=altura_maxima)
        scroll_data['frame'].pack(fill="both", expand=True, padx=5, pady=5)
        return {
            "frame": frame_tabla,
            "frame_contenido": scroll_data['frame_interior']
        }

    # Método para frame para encabezado.
    @staticmethod
    def crear_frame_encabezado(parent):
        frame_encabezados = ctk.CTkFrame(parent)
        frame_encabezados.pack(fill="x", padx=20)
        return frame_encabezados
    
    # Método mensaje para tabla vacía.
    @staticmethod
    def mensaje_tabla_vacia(parent, texto="No hay productos agregados. Haga clic en 'Agregar línea' para comenzar"):
        mensaje = ctk.CTkLabel(parent, text=texto, font=("Arial", 12), text_color="gray", anchor="center", justify="center")
        mensaje.pack(pady=50)
        return mensaje
    
    # Método para encabezado de tabla.
    @staticmethod
    def crear_encabezados_tabla(parent, configuraciones, pady=5):

        # Frame para encabezado de tabla.
        frame_encabezados = ctk.CTkFrame(parent)
        frame_encabezados.pack(fill="x", padx=5, pady=(5, 0))
        frame_encabezados.grid_columnconfigure(1, weight=1)

        # Configuración de las columnas o encabezados.
        encabezados = []
        for config in configuraciones:
            texto = config[0]
            columna = config[1]
            ancho = config[2]
            padx = config[3]
            sticky = config[4] if len(config) > 4 else ""
            anchor = config[5] if len(config) > 5 else "center"
            label = ctk.CTkLabel(frame_encabezados, text=texto, font=("Arial", 12, "bold"), anchor=anchor, width=ancho if ancho > 0 else 0)
            label.grid(row=0, column=columna, padx=padx, pady= pady, sticky=sticky)
            encabezados.append(label)
        return {
            "frame":frame_encabezados,
            "labels":encabezados
        }
    
    # Método para la creación de línea de detalle.
    @staticmethod
    def crear_linea_detalle(parent, num_linea, productos_opciones, on_delete, on_update):

        # Frame para la línea de detalle.
        linea_frame = ctk.CTkFrame(parent)
        linea_frame.pack(fill="x", padx=5, pady=2)
        linea_frame.grid_columnconfigure(1, weight=1)
        
        # Número de línea.
        label_num = ctk.CTkLabel(linea_frame, text=f"{num_linea}.", width=40)
        label_num.grid(row=0, column=0, padx=(10, 5), pady=5)
        
        # Combobox de producto.
        combo_producto = ctk.CTkComboBox(linea_frame, values=productos_opciones, width=200)
        combo_producto.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        combo_producto.set("Seleccionar producto...")
        
        # Cantidad.
        entry_cantidad = ctk.CTkEntry(linea_frame, placeholder_text="Cant.", width=100)
        entry_cantidad.grid(row=0, column=2, padx=5, pady=5)
        entry_cantidad.bind("<KeyRelease>", lambda e: on_update())
        
        # Precio.
        entry_precio = ctk.CTkEntry(linea_frame, placeholder_text="Precio", width=120)
        entry_precio.grid(row=0, column=3, padx=5, pady=5)
        entry_precio.bind("<KeyRelease>", lambda e: on_update())
        
        # Subtotal.
        label_subtotal = ctk.CTkLabel(linea_frame, text="Q 0.00", width=100, font=("Arial", 11))
        label_subtotal.grid(row=0, column=4, padx=5, pady=5)
        
        # Botón eliminar.
        btn_eliminar = ctk.CTkButton(linea_frame, text="X", width=30, height=30, fg_color="transparent", text_color="red", 
            hover_color="#2b2b2b", command=lambda: on_delete(linea_frame))
        btn_eliminar.grid(row=0, column=5, padx=(5, 10), pady=5)
        
        return {
            "frame": linea_frame,
            "label_num": label_num,
            "combo_producto": combo_producto,
            "entry_cantidad": entry_cantidad,
            "entry_precio": entry_precio,
            "label_subtotal": label_subtotal,
            "btn_eliminar": btn_eliminar,
            "subtotal": 0.0
        }
    
    # Método para crear totales.
    @staticmethod
    def crear_frame_total(parent):
        frame_total = ctk.CTkFrame(parent)
        frame_total.pack(fill="x", padx=20, pady=5)
        label_total = ctk.CTkLabel(frame_total, text="Total: GTQ 0.00", font=("Arial", 14, "bold"), anchor="e")
        label_total.pack(fill="x", padx=10)
        return {
            "frame": frame_total,
            "label": label_total
        }