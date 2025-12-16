from tkinter import messagebox
from database import ConexionBD
from base_app import BaseERPApp
from validaciones import Validaciones
from widgets import WidgetsFactory
from datetime import datetime

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

        # Generar número de OC automático.
        numero_oc_generado = self._generar_numero_oc()
        
        # Campos de la cabecera.
        self.entry_no_oc = WidgetsFactory.crear_campo_entry_auto(frame_izquierda, "No. OC:", numero_oc_generado)
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
            self.proveedores_data = ConexionBD.obtener_proveedores()
            nombres_proveedores = [p[1] for p in self.proveedores_data]
            self.combo_proveedor.configure(values=nombres_proveedores)
            if len(self.proveedores_data) == 0:
                messagebox.showwarning("Advertencia", "No hay proveedores registrados")
        except Exception as error:
            messagebox.showerror("Error", f"No se pudieron cargar los pValidaciones.convertir_fecha_sqlroveedores {error}")
    
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

        nombres_proveedores = [p[1] for p in self.proveedores_data]

        # Validación para campo Nombre.
        if not Validaciones.validar_combobox(proveedor, nombres_proveedores, "nombre proveedor"):
            return False
            
        # Validación para campo Fecha Entrega.
        if not Validaciones.validar_fecha(fecha_entrega, "fecha de entrega"):
            return False 
        return True
    
    # (2.5) Método para generar número OC automático.
    def _generar_numero_oc(self):
        try:
            ultimo_numero = ConexionBD.obtener_ultimo_numero_oc()

            if ultimo_numero:
                partes = ultimo_numero.split("-")
                if len(partes) == 3:
                    try:
                        secuencia = int(partes[2])
                        nueva_secuencia = secuencia + 1
                    except ValueError:
                        nueva_secuencia = 1
                else:
                    nueva_secuencia = 1
            else:
                nueva_secuencia = 1
            anio_actual = datetime.now().year
            numero_oc = f"OC-{anio_actual}-{nueva_secuencia:03d}"
            return numero_oc
        except Exception as error:
            messagebox.showerror("Error", f"No se puede generar el número de OC: {error}")
            return None
    
    # (3) CREACIÓN DE DETALLE ORDEN DE COMPRA.

    # (3.1) Método para crear la sección de Detalle.
    def _crear_seccion_detalle(self):
        # Frame principal.
        frame_detalle = WidgetsFactory.crear_frame(self.main_frame, "both", 10, "Detalle de productos", expand=True)

        # Controles (botón agregar + guardar).
        controles_widget = WidgetsFactory.crear_frame_controles(frame_detalle, "Agregar línea", 
            self._agregar_linea_detalle, "Guardar", self._guardar_orden_compra)
        
        self.btn_agregar_linea = controles_widget["btn_agregar"]
        self.btn_guardar = controles_widget["btn_guardar"]

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
            self.productos_data = ConexionBD.obtener_productos()
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
    
    # (3.6) Método para validar datos de detalle.
    def _validar_detalle(self, producto, cantidad, precio):

        nombres_productos = [p[1] for p in self.productos_data]

        # Validación para campo producto.
        if not Validaciones.validar_combobox(producto, nombres_productos, "producto"):
            return False
        
        # Validación para campo cantidad.
        if not Validaciones.validar_valores_enteros(cantidad, "cantidad"):
            return False
        
        # Validación para campo precio.
        if not Validaciones.validar_valor_monetario(precio, "precio"):
            return False
        return True
    
    # (3.8) Método para guardar orden de compra. 
    def _guardar_orden_compra(self):
        numero_oc = self.entry_no_oc.cget("placeholder_text")
        
        try:
            proveedor = self.combo_proveedor.get()
            fecha_entrega = self.entry_fecha_entrega.get()
            if not self._validar_cabecera(proveedor, fecha_entrega):
                return 
            if len(self.lineas_detalle) == 0:
                messagebox.showerror("Error", "Debe agregar al menos un producto")
                return
            
            # Obtener datos de Cabecera.
            numero_oc = self.entry_no_oc.cget("placeholder_text")
            nit = self.entry_nit.get()
            plazo_pago = self.entry_plazo_pago.get()
            fecha_emision = datetime.now().strftime("%d/%m/%Y")
            total_text = self.total_oc.cget("text")
            total = float(total_text.replace("Total: GTQ", "").replace(",", "").strip())
            
            # Extracción de ID de Proveedor.
            proveedor_id, error_msg = Validaciones.validar_id(self.proveedores_data, proveedor, "proveedor")
            if error_msg:
                messagebox.showerror("Error", error_msg)
                return
            
            # Validación para datos de Detalle de OC.
            lineas_validas = []
            for i, linea in enumerate(self.lineas_detalle, 1):
                producto = linea["combo_producto"].get()
                cantidad = linea["entry_cantidad"].get()
                precio = linea["entry_precio"].get()
                subtotal = linea["subtotal"]
                if not self._validar_detalle(producto, cantidad, precio):
                    return
                
                # Extracción de ID de Producto.
                producto_id, error_msg = Validaciones.validar_id(self.productos_data, producto, "producto")
                if error_msg:
                    messagebox.showerror("Error", error_msg)
                    return
                
                lineas_validas.append({"no_item": i, "producto_id": producto_id, "producto_nombre": producto, "cantidad": float(cantidad),
                    "precio": float(precio), "subtotal": subtotal})
            
            # Método interno para gestión de fechas.
            fecha_emision_sql, error_msg = BaseERPApp.convertir_fecha_sql(fecha_emision)
            if error_msg:
                messagebox.showerror("Error", f"Fecha emisión: {error_msg}")
                return
            
            fecha_entrega_sql, error_msg = BaseERPApp.convertir_fecha_sql(fecha_entrega)
            if error_msg:
                messagebox.showerror("Error", f"Fecha entrega: {error_msg}")
                return 
            
            # Guardar registros de Cabecera.
            ConexionBD.insertar_orden_compra(numero_oc=numero_oc, proveedor_id=proveedor_id, proveedor_nombre=proveedor, nit=nit,
                fecha_emision=fecha_emision_sql, fecha_entrega=fecha_entrega_sql, plazo_pago=plazo_pago, total=total)
            
            # Guardar registros de Detalle OC.
            for linea in lineas_validas:
                ConexionBD.insertar_oc_detalle(no_item=linea["no_item"], numero_oc=numero_oc, producto_id=linea["producto_id"],
                    producto_nombre=linea["producto_nombre"], cantidad=linea["cantidad"], precio_unitario=linea["precio"], 
                    subtotal=linea["subtotal"])
            messagebox.showinfo("Éxito", f"Orden de Compra {numero_oc} guardada correctamente")
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo guardar la orden de compra: {str(error)}")
    
    # Método para limpiar formulario.

# Punto de entrada.
if __name__ == "__main__":
    app = OrdenCompra()
    app.mainloop()