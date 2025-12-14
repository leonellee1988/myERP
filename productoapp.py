from tkinter import messagebox
from database import insertar_producto
from base_app import BaseERPApp
from validaciones import Validaciones
from widgets import config_apariencia, crear_frame, crear_frame_izquierda, crear_frame_derecha, \
crear_campo_combo, crear_boton, crear_campo_entry

# Configurar apariencia.
config_apariencia("dark", "blue")

# Opciones para combobox categorias.
categorias = ["Seleccione un valor...", "Laptop", "PC Escritorio", "Impresoras", "Audífonos", "Almacenamiento",
    "Teclados", "Mouse", "Celulares", "Consolas", "Cables", "Bocinas"]

# Opciones para combobox unidad de medida.
unidad_medida = ["Seleccione un valor...", "Unidad", "Par", "Metro (m)", "Centímetro (cm)", "Paquete",
    "Caja", "Resma", "Cartucho"]

class ProductoApp(BaseERPApp):
    # (1) Método constructor.
    def __init__(self):
        super().__init__(titulo_modulo="Ingreso de productos")
        self._crear_seccion_producto()
    
    # (2) Método para la creación de productos (viene de constructor)
    def _crear_seccion_producto(self):
        frame_producto = crear_frame(self.main_frame, "x", 10, "Registrar nuevo producto")

        # Contenedor para el frame izquierda/derecha.
        frame_izquierda = crear_frame_izquierda(frame_producto)
        frame_derecha = crear_frame_derecha(frame_producto)

        # Creación de los campos del módulo Productos.
        self.entry_nombre = crear_campo_entry(frame_izquierda, "Nombre del producto:", "Laptop Latitude 5540")
        self.entry_descripcion = crear_campo_entry(frame_izquierda, "Descripción:", "Dell procesador Core i5 8G Ram")
        self.combo_categoria = crear_campo_combo(frame_izquierda, "Categoría:", categorias)
        self.entry_costo = crear_campo_entry(frame_izquierda, "Costo:", "5000.00")
        self.entry_precio = crear_campo_entry(frame_derecha, "Precio:", "10000.00")
        self.entry_stock = crear_campo_entry(frame_derecha, "Stock actual:", "10")
        self.entry_stock_min = crear_campo_entry(frame_derecha, "Stock mínimo:", "5")
        self.combo_unidad = crear_campo_combo(frame_derecha, "Unidad medida:", unidad_medida)

        # Creación de botón 'Registro'.
        crear_boton(self.main_frame, "Registrar", self._registrar_producto)

    # (3) Método para validar datos del producto:
    def _validar_producto(self, nombre, descripcion, categoria, costo, precio, stock, stock_min, unidad):

        # Validación campo Nombre.
        if not Validaciones.validar_campo_obligatorio(nombre, "nombre producto"):
            return False
        
        # Validación campo Descripción.
        if not Validaciones.validar_campo_obligatorio(descripcion, "descripción"):
            return False
        
        # Validación campo Categoría.
        if not Validaciones.validar_combobox(categoria, categorias, "categoría"):
            return False
        
        # Validación campo Costo.
        if not Validaciones.validar_valor_monetario(costo, "costo"):
            return False
        
        # Validación campo Precio.
        if not Validaciones.validar_valor_monetario(precio, "precio"):
            return False
        
        # Validación campo Stock.
        if not Validaciones.validar_valor_monetario(stock, "stock"):
            return False
        
        # Validación campo Stock Mínimo:
        if not Validaciones.validar_valor_monetario(stock_min, "stock mínimo"):
            return False
        
        # Validación campo Unidad de Medida.
        if not Validaciones.validar_combobox(unidad, unidad_medida, "unidad de medida"):
            return False
        
        # Validación Costo vs Precio.
        if not Validaciones.validar_valores(costo, precio, "costo", "precio"):
            return False
        
        return True
    
    # (4) Método para limpiar campos.
    def _limpiar_campos(self):
        self.entry_nombre.delete(0, "end")
        self.entry_descripcion.delete(0, "end")
        self.combo_categoria.set(categorias[0])
        self.entry_costo.delete(0, "end")
        self.entry_precio.delete(0, "end")
        self.entry_stock.delete(0, "end")
        self.entry_stock_min.delete(0, "end")
        self.combo_unidad.set(unidad_medida[0])
    
    # (5) Método para el registro de productos en BD.
    def _registrar_producto(self):

        # Captura y depuración final de los datos.
        nombre = self.entry_nombre.get().strip()
        descripcion = self.entry_descripcion.get().strip()
        categoria = self.combo_categoria.get()
        costo = self.entry_costo.get().strip()
        precio = self.entry_precio.get().strip()
        stock = self.entry_stock.get().strip()
        stock_min = self.entry_stock_min.get().strip()
        unidad = self.combo_unidad.get()

        # Guarda de seguridad (early return).
        if not self._validar_producto(nombre, descripcion, categoria, costo, precio, stock, stock_min, unidad):
            return
        
        # Inserción de datos en BD y limpieza de campos en módulo.
        try:
            insertar_producto(nombre, descripcion, categoria, costo, precio, stock, stock_min, unidad)
            self._limpiar_campos()
            messagebox.showinfo("Éxito", "Producto registrado correctamente")
        except Exception as error:
            messagebox.showerror("Error", f"No se puede realizar el registro: {str(error)}")
 
# Punto de entrada.
if __name__ == "__main__":
    app = ProductoApp()
    app.mainloop()