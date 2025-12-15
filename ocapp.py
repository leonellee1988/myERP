import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from database import obtener_proveedores, obtener_productos
from base_app import BaseERPApp
from validaciones import Validaciones
from widgets import WidgetsFactory

# Configurar apariencia.
WidgetsFactory.config_apariencia("dark", "blue")

class OrdenCompra(BaseERPApp):
    # (1) Método constructor.
    def __init__(self):
        super().__init__(titulo_modulo="Ingreso de orden de compra")
        self.proveedores_data = []
        self.productos_data = []
        self.lineas_detalle = []

        # Métodos de clase.
        self._crear_seccion_cabecera()
        self._cargar_proveedores()
        self._cargar_productos()
        self._crear_seccion_detalle()
    
    # (2) CREACIÓN DE CABECERA ORDEN DE COMPRA.

    # (2.1) Método para crear la sección de Cabecera.
    def _crear_seccion_cabecera(self):
        # Frame principal.
        frame_cabecera = WidgetsFactory.crear_frame(self.main_frame, "x", 10)

        # Contenedor para el frame izquierda/derecha.
        frame_izquierda = WidgetsFactory.crear_frame_izquierda(frame_cabecera)
        frame_derecha = WidgetsFactory.crear_frame_derecha(frame_cabecera)
        
        # Campos de la cabecera.
        self.entry_no_oc = WidgetsFactory.crear_campo_entry_auto(frame_izquierda, "No. OC:", "")
        self.combo_proveedor = WidgetsFactory.crear_campo_combo(frame_izquierda, "Proveedor:", ["Seleccione un valor..."])
        self.combo_proveedor.configure(command=self._proveedor_seleccionado)
        self.entry_nit = WidgetsFactory.crear_campo_entry_auto(frame_izquierda, "NIT:", "")
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")
        self.entry_fecha_emision = WidgetsFactory.crear_campo_entry_auto(frame_derecha, "Fecha emisión:", fecha_hoy)
        self.entry_fecha_entrega = WidgetsFactory.crear_campo_entry(frame_derecha, "Fecha entrega:", "dd/mm/YYYY")
        self.entry_plazo_pago = WidgetsFactory.crear_campo_entry_auto(frame_derecha, "Plazo de pago:", "")

    # (2.2) Método para cargar información de proveedores.
    def _cargar_proveedores(self):
        try:
            self.proveedores_data = obtener_proveedores()
            nombres_proveedores = [p[1] for p in self.proveedores_data]
            self.combo_proveedor.configure(values=nombres_proveedores)
            if len(self.proveedores_data) == 0:
                messagebox.showwarning("Advertencia", "No hay proveedores registrados")
        except Exception as error:
            messagebox.showerror("Error", f"No se pudieron cargar los proveedores {error}")
    
    # (2.3) Método para gestionar: nit y plazo de pago, en función a proveedor.
    def _proveedor_seleccionado(self, event=None):

        proveedor_seleccionado = self.combo_proveedor.get()
        if not proveedor_seleccionado or proveedor_seleccionado == "Seleccione un valor...":
            self.entry_nit.configure(state="normal")
            self.entry_nit.delete(0, "end")
            self.entry_nit.insert(0, "")
            self.entry_nit.configure(state="readonly")
            self.entry_plazo_pago.configure(state="normal")
            self.entry_plazo_pago.delete(0, "end")
            self.entry_plazo_pago.insert(0, "")
            self.entry_plazo_pago.configure(state="readonly")
            return
        for proveedor in self.proveedores_data:
            if proveedor[1] == proveedor_seleccionado:
                nit = proveedor[2] if proveedor[2] else "No registrado"
                plazo_pago = proveedor[3] if proveedor[3] else "No definido"
                self.entry_nit.configure(state="normal")
                self.entry_nit.delete(0, "end")
                self.entry_nit.insert(0, nit)
                self.entry_nit.configure(state="readonly")
                self.entry_plazo_pago.configure(state="normal")
                self.entry_plazo_pago.delete(0, "end")
                self.entry_plazo_pago.insert(0, plazo_pago)
                self.entry_plazo_pago.configure(state="readonly")
                return
        messagebox.showwarning("Advertencia", "Proveedor no encontrado en la base de datos")

    # (2.4) Método para validar datos de cabecera.
    def _validar_cabecera(self, proveedor, fecha_entrega):

        # Validación para campo Nombre.
        if not Validaciones.validar_campo_obligatorio(proveedor, "nombre proveedor"):
            return False
            
        # Validación para campo Fecha Entrega.
        if not Validaciones.validar_fecha(fecha_entrega, "fecha de entrega"):
            return False 
        return True
    
    # (3) CREACIÓN DE DETALLE ORDEN DE COMPRA.

    # (3.1) Método para crear la sección de Detalle.
    def _crear_seccion_detalle(self):
        # Frame principal.
        frame_detalle = WidgetsFactory.crear_frame(self.main_frame, "both", 10, "Detalle de productos", expand=True)

        # Controles (botón agregar).
        controles_widget = WidgetsFactory.crear_frame_controles(frame_detalle, "Agregar línea", self._agregar_linea_detalle)
        self.btn_agregar_linea = controles_widget["btn_agregar"]

        # Creción de encabezados de tabla.
        frame_encabezados = WidgetsFactory.crear_frame_encabezado(frame_detalle)
        config_encabezados = [("No.", 0, 40, (10, 5)), ("Producto", 1, 0, 5, "w", "w"), ("Cantidad", 2, 100, 5), ("Precio Unit.", 3, 120, 5),
        ("Subtotal", 4, 100, 5), ("Acciones", 5, 80, (5, 10))]
        encabezados_widget = WidgetsFactory.crear_encabezados_tabla(frame_encabezados, config_encabezados)
        self.frame_encabezados = encabezados_widget["frame"]

        # Frame para tabla de contenido.
        tabla_widgets = WidgetsFactory.crear_frame_tabla(frame_detalle, altura_maxima=200)
        self.frame_tabla_detalle = tabla_widgets["frame"]
        self.frame_contenido_tabla = tabla_widgets["frame_contenido"]

        # Mensaje cuando la tabla no tenga información.
        self.mensaje_tabla_vacia = WidgetsFactory.mensaje_tabla_vacia(self.frame_contenido_tabla)

        # Frame para creación de total de OC.
        total_widget = WidgetsFactory.crear_frame_total(frame_detalle)
        self.total_oc = total_widget["label"]

    # (3.2) Método para cargar información de productos.
    def _cargar_productos(self):
        try:
            self.productos_data = obtener_productos()
            nombres_productos = [p[1] for p in self.productos_data]
            if len(self.productos_data) == 0:
                messagebox.showwarning("Advertencia", "No hay productos registrados")
        except Exception as error:
            messagebox.showerror("Error", f"No se pudieron cargar los productos {error}")
            self.productos_data = []
    
    # (3.3) Método para agregar línea de detalle.
    def _agregar_linea_detalle(self):

        # Ocultar mensaje inicial de tabla vacía.
        if hasattr(self, "mensaje_tabla_vacia"):
            self.mensaje_tabla_vacia.pack_forget()
        
        # Preparar opciones de producto y crear línea.
        opciones_productos = ["Seleccione un valor..."]
        if hasattr(self, "productos_data") and self.productos_data:
            opciones_productos += [p[1] for p in self.productos_data]
        
        linea_data = WidgetsFactory.crear_linea_detalle(parent=self.frame_contenido_tabla, num_linea=len(self.lineas_detalle) + 1,
            productos_opciones=opciones_productos, on_delete=self._eliminar_linea_detalle, on_update=self._calcular_totales)
        if not hasattr(self, "lineas_detalle"):
            self.lineas_detalle = []
        self.lineas_detalle.append(linea_data)
    
        self._calcular_totales()
    
    # (3.4) Método para eliminar linea de detalle.
    def _eliminar_linea_detalle(self, linea_frame):
        
        # Buscar la línea asociada.
        for linea in self.lineas_detalle:
            if linea["frame"] == linea_frame:
                linea_frame.destroy()
                self.lineas_detalle.remove(linea)
                break
        
        for i, linea in enumerate(self.lineas_detalle, 1):
            linea["label_num"].configure(text=f"{i}.")

        if not self.lineas_detalle:
            self.mensaje_tabla_vacia.pack(pady=50)

        self._calcular_totales()    
    
    # (3.5) Método para calcular subtotales y total.
    def _calcular_totales(self):
        total = 0.0

        for linea in self.lineas_detalle:
            try:
                cantidad = float(linea["entry_cantidad"].get())
                precio = float(linea["entry_precio"].get())
                subtotal = cantidad * precio
            except ValueError:
                subtotal = 0.0
            
            linea["subtotal"] = subtotal
            linea["label_subtotal"].configure(text=f"GTQ {subtotal:,.2f}")
            total += subtotal
        
        self.total_oc.configure(text=f"Total: GTQ {total:,.2f}")

# Punto de entrada.
if __name__ == "__main__":
    app = OrdenCompra()
    app.mainloop()