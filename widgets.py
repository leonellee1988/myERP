import customtkinter as ctk
from tkcalendar import DateEntry
from datetime import datetime

# (1) Método para la creación de frames.
def crear_frame(parent, fill, pady, text):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill=fill, pady=pady)
        label = ctk.CTkLabel(frame, text=text, font=("Arial", 16, "bold"))
        label.pack(pady=10)
        return frame

# (2) Método para la creación de botones.
def crear_boton(frame, text, command):
    boton = ctk.CTkButton(frame, text=text, command=command, height=40, font=("Arial", 14, "bold"))
    boton.pack(pady=10)
    return boton

# (3) Método para la creación de campos (entry).
def crear_campo_entry(frame, texto, placeholder):
    # Frame interno para objeto.
    contenedor = ctk.CTkFrame(frame, fg_color="transparent")
    contenedor.pack(fill="x", padx=20, pady=8) 

    # Label descriptivo.
    label = ctk.CTkLabel(contenedor, text=texto, width=120, anchor="w")
    label.pack(side="left", padx=(0, 10))

    # Objeto entry para campo.
    entry = ctk.CTkEntry(contenedor, placeholder_text=placeholder)
    entry.pack(side="left", fill="x", expand=True)
    return entry

# (4) Método para la creación de campos (combobox).
def crear_campo_combo(frame, texto, opciones, valor_default=None):
    # Frame interno para objeto.
    contenedor = ctk.CTkFrame(frame, fg_color="transparent")
    contenedor.pack(fill="x", padx=20, pady=8) 

    # Label descritivo.
    label = ctk.CTkLabel(contenedor, text=texto, width=120, anchor="w")
    label.pack(side="left", padx=(0, 10))

    # Objeto entry para campo.
    combobox = ctk.CTkComboBox(contenedor, values=opciones, state="readonly")
    combobox.pack(side="left", fill="x", expand=True)

    # Establecer valor combobox por default.
    if valor_default and valor_default in opciones:
        combobox.set(valor_default)
    elif opciones:
         combobox.set(opciones[0])
    return combobox

# (5) Método para frame izquierda.
def crear_frame_izquierda(parent):
     frame = ctk.CTkFrame(parent)
     frame.pack(side="left", fill="both", expand=True, padx=(20, 10), pady=10)
     return frame

# (6) Método para frame derecha.
def crear_frame_derecha(parent):
     frame = ctk.CTkFrame(parent)
     frame.pack(side="right", fill="both", expand=True, padx=(10, 20), pady=10)
     return frame

# (7) Método para la creación de campos automáticos (entry).
def crear_campo_entry_auto(frame, texto, placeholder):
    # Frame interno para objeto.
    contenedor = ctk.CTkFrame(frame, fg_color="transparent")
    contenedor.pack(fill="x", padx=20, pady=8) 

    # Label descriptivo.
    label = ctk.CTkLabel(contenedor, text=texto, width=120, anchor="w")
    label.pack(side="left", padx=(0, 10))

    # Objeto entry para campo.
    entry = ctk.CTkEntry(contenedor, placeholder_text=placeholder)
    entry.pack(side="left", fill="x", expand=True)
    entry.configure(state="readonly", fg_color="#1e1e1e", border_color="#4CC9F0", text_color="#4CC9F0")
    return entry

# (8) Método para crear encabezados de tabla.
def crear_encabezados_tabla(parent, configuraciones, pady=5):
    # Lista de encabezados.
    encabezados = []
    
    # Configuraciones para cada columna del encabezado. 
    for config in configuraciones:
        texto = config[0]
        columna = config[1]
        ancho = config[2]
        padx = config[3]
        sticky = config[4] if len(config) > 4 else ""
        anchor = config[5] if len(config) > 5 else "center"
        label = ctk.CTkLabel(parent, text=texto, font=("Arial", 12, "bold"), anchor=anchor,
            width=ancho if ancho > 0 else 0)
        label.grid(row=0, column=columna, padx=padx, pady=pady, sticky=sticky)
        encabezados.append(label)
    return encabezados

# (9) Método para crear líneas de compra.
def crear_linea_detalle(parent, num_linea, productos_opciones, grid_columnconfigure=True):
    # Frame para esta línea.
    linea_frame = ctk.CTkFrame(parent)
    linea_frame.pack(fill="x", padx=5, pady=2)
    
    if grid_columnconfigure:
        linea_frame.grid_columnconfigure(1, weight=1)
    
    # (A) Número de línea.
    label_num = ctk.CTkLabel(linea_frame, text=f"{num_linea}.", width=40)
    label_num.grid(row=0, column=0, padx=(10, 5), pady=5)
    
    # (B) Combobox para producto.
    combo_producto = ctk.CTkComboBox(linea_frame, values=productos_opciones, width=200)
    combo_producto.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    combo_producto.set("Seleccionar producto...")
    
    # (C) Entry para cantidad.
    entry_cantidad = ctk.CTkEntry(linea_frame, placeholder_text="Cant.", width=100)
    entry_cantidad.grid(row=0, column=2, padx=5, pady=5)
    
    # (D) Entry para precio.
    entry_precio = ctk.CTkEntry(linea_frame, placeholder_text="Precio", width=120)
    entry_precio.grid(row=0, column=3, padx=5, pady=5)
    
    # (E) Label para subtotal.
    label_subtotal = ctk.CTkLabel(linea_frame, text="Q 0.00", width=100, font=("Arial", 11))
    label_subtotal.grid(row=0, column=4, padx=5, pady=5)
    
    # (F) Botón eliminar.
    btn_eliminar = ctk.CTkButton(linea_frame, text="✕", width=30, height=30, fg_color="transparent", 
        text_color="red", hover_color="#2b2b2b")
    btn_eliminar.grid(row=0, column=5, padx=(5, 10), pady=5)
    
    # Retornar diccionario con todos los widgets.
    return {
        "frame": linea_frame,
        "label_num": label_num,
        "combo_producto": combo_producto,
        "entry_cantidad": entry_cantidad,
        "entry_precio": entry_precio,
        "label_subtotal": label_subtotal,
        "btn_eliminar": btn_eliminar
    }