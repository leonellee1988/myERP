import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from widgets import crear_frame, crear_frame_izquierda, crear_frame_derecha, crear_campo_combo, \
crear_campo_entry, crear_campo_entry_auto, crear_encabezados_tabla, crear_linea_detalle
from scroll import crear_scroll_vertical
from database import obtener_proveedores, obtener_productos

# Configurar apariencia.
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class OrdenCompra(ctk.CTk):
    # (1) Método constructor.
    def __init__(self):
        super().__init__()

        # Configurar ventana principal.
        self.title("myERP")
        self.resizable(True, True)

        # Configurar frame principal.
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.label_titulo = ctk.CTkLabel(self.main_frame, text="Ingreso de Orden de Compra", font=("Arial", 20, "bold"))
        self.label_titulo.pack(pady=20)

        # Métodos de clase.
        self._crear_seccion_cabecera()
        self._cargar_proveedores()
        self._cargar_productos()
        self._crear_seccion_detalle()
    
    # (2) Método para crear la sección de Cabecera.
    def _crear_seccion_cabecera(self):
        # Frame principal.
        frame_cabecera = crear_frame(self.main_frame, "x", 10, "Cabecera Orden de Compra")

        # Contenedor para el frame izquierda/derecha.
        frame_izquierda = crear_frame_izquierda(frame_cabecera)
        frame_derecha = crear_frame_derecha(frame_cabecera)

        # Campo1: Número de Orden de Compra.
        self.entry_no_oc = crear_campo_entry_auto(frame_izquierda, "No. OC:", "")

        # Campo2: Proveedor.
        self.combo_proveedor = crear_campo_combo(frame_izquierda, "Proveedor:", ["Seleccionar proveedor..."])
        self.combo_proveedor.configure(command=self._proveedor_seleccionado)

        # Campo3: Número de Identificación Tributario (NIT).
        self.entry_nit = crear_campo_entry_auto(frame_izquierda, "NIT:", "")

        # Campo4: Fecha de emisión OC.
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")
        self.entry_fecha_emision = crear_campo_entry_auto(frame_derecha, "Fecha emisión:", fecha_hoy)

        # Campo5: Fecha estimada de entrega.
        self.entry_fecha_entrega = crear_campo_entry(frame_derecha, "Fecha entrega:", "dd/mm/YYYY")

        # Campo6: Plazo de pago.
        self.entry_plazo_pago = crear_campo_entry_auto(frame_derecha, "Plazo de pago:", "")
    
    # (3) Método para cargar proveedores.
    def _cargar_proveedores(self):
        try:
            self.proveedores_data = obtener_proveedores()
            nombres_proveedores = [p[1] for p in self.proveedores_data]
            self.combo_proveedor.configure(values=nombres_proveedores)
            if len(self.proveedores_data) == 0:
                messagebox.showwarning("Advertencia", "No hay proveedores registrados")
        except Exception as error:
            messagebox.showerror("Error", f"No se pudieron cargar los proveedores {error}")
    
    # (4) Método para cargar productos.
    def _cargar_productos(self):
        try:
            self.productos_data = obtener_productos()
            nombres_productos = [p[1] for p in self.productos_data]
            # La configuración del combobox se hará en el método 9.
            if len(self.productos_data) == 0:
                messagebox.showwarning("Advertencia", "No hay productos registrados")
        except Exception as error:
            messagebox.showerror("Error", f"No se pudieron cargar los productos {error}")
            self.productos_data = []
    
    # (5) Método para gestionar selección de proveedor.
    def _proveedor_seleccionado(self, event=None):
        # Captura del proveedor seleccionado.
        proveedor_seleccionado = self.combo_proveedor.get()

        # Si no hay selección válida, limpiar campos.
        if not proveedor_seleccionado or proveedor_seleccionado == "Seleccionar proveedor...":
            self.entry_nit.configure(state="normal")
            self.entry_nit.delete(0, "end")
            self.entry_nit.insert(0, "")
            self.entry_nit.configure(state="readonly")
            self.entry_plazo_pago.configure(state="normal")
            self.entry_plazo_pago.delete(0, "end")
            self.entry_plazo_pago.insert(0, "")
            self.entry_plazo_pago.configure(state="readonly")
            return
        
        # Busqueda de proveedor en objeto 'self.proveedores_data'.
        for proveedor in self.proveedores_data:
            if proveedor[1] == proveedor_seleccionado:
                nit = proveedor[2] if proveedor[2] else "No registrado"
                plazo_pago = proveedor[3] if proveedor[3] else "No definido"
                self.entry_nit.configure(state="normal")

                # Visualización del valor relacionado con proveedor.
                self.entry_nit.delete(0, "end")
                self.entry_nit.insert(0, nit)
                self.entry_nit.configure(state="readonly")
                self.entry_plazo_pago.configure(state="normal")
                self.entry_plazo_pago.delete(0, "end")
                self.entry_plazo_pago.insert(0, plazo_pago)
                self.entry_plazo_pago.configure(state="readonly")
                return
            
        messagebox.showwarning("Advertencia", "Proveedor no encontrado en la base de datos")
    
    # (6) Método para gestionar la selección de producto.
    def _producto_seleccionado(self, valor_seleccionado, linea_data):
        # Captura del producto seleccionado.
        producto_seleccionado = valor_seleccionado
        
        # Si no hay selección válida, limpiar campo de precio
        if not producto_seleccionado or producto_seleccionado == "Seleccionar producto...":
            linea_data["entry_precio"].delete(0, "end")
            linea_data["entry_precio"].insert(0, "")
            return
        
        # Búsqueda de producto.
        for producto in self.productos_data:
            if producto[1] == producto_seleccionado:
                print(f"Producto seleccionado: {producto_seleccionado}")
                return
        
        # Producto no encontrado.
        messagebox.showwarning("Advertencia", 
            f"Producto '{producto_seleccionado}' no encontrado")
    
    # (7) Método para crear la sección de Detalle.
    def _crear_seccion_detalle(self):
        # (a) Frame principal.
        frame_detalle = crear_frame(self.main_frame, "x", 10, "Detalle de productos")

        # (b) Frame para controles (botones).
        frame_controles = ctk.CTkFrame(frame_detalle)
        frame_controles.pack(fill="x", padx=20, pady=(0, 10))

        # Botón para agregar línea.
        self.btn_agregar_linea = ctk.CTkButton(frame_controles, text="Agregar producto", 
            command=self._agregar_linea_detalle, width=150, height=35, font=("Arial", 12))
        self.btn_agregar_linea.pack(side="left", padx=(0,10))
        
        # (c) Frame para la tabla de detalle.
        self.frame_tabla_detalle = ctk.CTkFrame(frame_detalle)
        self.frame_tabla_detalle.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        self._crear_encabezados_tabla()

        # (d) Frame para el contenido de la tabla (líneas de compra).
        scroll_data = crear_scroll_vertical(self.frame_tabla_detalle, altura_maxima=250)
        scroll_data['frame'].pack(fill="both", expand=True, padx=5, pady=5)
        self.frame_contenido_tabla = scroll_data['frame_interior']

        # Etiqueta temporal (será reemplazada por las líneas de compra).
        self.label_tabla_vacia = ctk.CTkLabel(self.frame_contenido_tabla, 
            text="No hay productos agregados. Haga clic en 'Agregar producto' para iniciar",
            font=("Arial", 12), text_color="gray")
        self.label_tabla_vacia.pack(pady=50)

        # Iniciar lista para almacenar líneas de detalle.
        self.lineas_detalle = []

        # (e) Frame para totales.
        self.frame_totales = ctk.CTkFrame(frame_detalle)
        self.frame_totales.pack(fill="x", padx=20, pady=10)

        # Label para mostrar totales.
        self.label_total = ctk.CTkLabel(self.frame_totales, text="Total OC: Q 0.00", font=("Arial", 16, "bold"),
            text_color="#4CC9F0")
        self.label_total.pack(anchor="e")

    # (8) Método para la creación de encabezados de la tabla.
    def _crear_encabezados_tabla(self):
        # Frame para los encabezados de la tabla.
        frame_encabezados = ctk.CTkFrame(self.frame_tabla_detalle)
        frame_encabezados.pack(fill="x", padx=5, pady=(5, 0))
        frame_encabezados.grid_columnconfigure(1, weight=1)

        # Configuraciones para cada columna del encabezado.    
        config_encabezados = [
            ("No.", 0, 40, (10, 5)),                    
            ("Producto", 1, 0, 5, "w", "w"),            
            ("Cantidad", 2, 100, 5),
            ("Precio Unit.", 3, 120, 5),
            ("Subtotal", 4, 100, 5),
            ("Acciones", 5, 80, (5, 10))
        ]
        
        self.encabezados_widgets = crear_encabezados_tabla(frame_encabezados, config_encabezados, pady=5)
        
    # (9) Método para agregar líneas de compra.
    def _agregar_linea_detalle(self):
        # Ocultar mensaje "No hay productos" si es la primera línea.
        if len(self.lineas_detalle) == 0:
            self.label_tabla_vacia.pack_forget()
        
        # Preparar opciones de productos.
        opciones_productos = ["Seleccionar producto..."]
        if hasattr(self, "productos_data") and self.productos_data:
            opciones_productos += [p[1] for p in self.productos_data]
        else:
            messagebox.showwarning("Advertencia", "No hay productos en la base de datos")
        
        # Crear línea de compra.
        linea_data = crear_linea_detalle(parent=self.frame_contenido_tabla, num_linea=len(self.lineas_detalle) + 1,
            productos_opciones=opciones_productos)
        combo_producto = linea_data["combo_producto"]
        combo_producto.configure(command=lambda valor, cp=combo_producto, 
            ld=linea_data:self._producto_seleccionado(valor, ld))
        
        # Configurar botón eliminar.
        linea_data["btn_eliminar"].configure(
            command=lambda frame=linea_data["frame"]: self._eliminar_linea(frame))
        
        self.lineas_detalle.append(linea_data)

    # (10) Método para eliminar líneas de detalle.
    def _eliminar_linea(self, linea_frame):
        # Buscar la línea en la lista.
        for i, linea_data in enumerate(self.lineas_detalle):
            if linea_data["frame"] == linea_frame:

                # Destruir todos los widgets de la línea
                linea_frame.destroy()
                
                # Eliminar de la lista
                self.lineas_detalle.pop(i)
                
                # Métodos para renumerar filas y recalcular total.
                #self._renumerar_lineas()
                #self._calcular_total()
                
                # Mostrar mensaje si no hay líneas
                if len(self.lineas_detalle) == 0:
                    self.label_tabla_vacia.pack(pady=50)
                return
        
        messagebox.showwarning("Advertencia", "No se pudo eliminar la línea. La línea ya no existe o hubo un error.")

# Punto de entrada.
if __name__ == "__main__":

    app = OrdenCompra()
    app.mainloop()