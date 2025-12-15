from tkinter import messagebox
from database import insertar_proveedor
from base_app import BaseERPApp
from validaciones import Validaciones
from widgets import WidgetsFactory

# Opciones para combobox plazo en pagos.
plazos_pago = ["Seleccione un valor...", "Al contado", "Crédito 7 días", "Crédito 15 días",
    "Crédito 30 días", "Crédito 60 días", "Crédito 90 días"]

# Configurar apariencia.
WidgetsFactory.config_apariencia("dark", "blue")

class ProveedorApp(BaseERPApp):
    # (1) Método constructor.
    def __init__(self):
        super().__init__(titulo_modulo="Ingreso de proveedores")
        self._crear_seccion_proveedor()
    
    # (2) Método para la creación de proveedores (viene de constructor)
    def _crear_seccion_proveedor(self):
        frame_proveedor = WidgetsFactory.crear_frame(self.main_frame, "x", 10, "Registrar nuevo proveedor")

        # Contenedor para el frame izquierda.
        frame_izquierda = WidgetsFactory.crear_frame_izquierda(frame_proveedor)
        frame_derecha = WidgetsFactory.crear_frame_derecha(frame_proveedor)

        # Creación de los campos del módulo Proveedores.
        self.entry_nombre = WidgetsFactory.crear_campo_entry(frame_izquierda, "Razón Social:", "Consultoría en Datos, S.A.")
        self.entry_nit = WidgetsFactory.crear_campo_entry(frame_izquierda, "NIT:", "12345678")
        self.entry_contacto = WidgetsFactory.crear_campo_entry(frame_izquierda, "Nombre contacto:", "Noemí Hernández")
        self.entry_telefono = WidgetsFactory.crear_campo_entry(frame_derecha, "Teléfono:", "7832-2925")
        self.entry_email = WidgetsFactory.crear_campo_entry(frame_derecha, "Email:", "ejemplo@empresa.com")
        self.combo_pago = WidgetsFactory.crear_campo_combo(frame_derecha, "Plazo pago:", plazos_pago)

        # # Creación de botón 'Registro'.
        WidgetsFactory.crear_boton(self.main_frame, "Registrar", self._registrar_proveedor)
    
    # (3) Método para validar datos del proveedor:
    def _validar_proveedor(self, nombre, nit, contacto, telefono, email, plazo_pago):

        # Validación para campo Nombre.
        if not Validaciones.validar_campo_obligatorio(nombre, "nombre proveedor"):
            return False
        
        # Validación para campo NIT.
        if not Validaciones.validar_campo_obligatorio(nit, "NIT"):
            return False
        
        # Validación para campo Contacto.
        if not Validaciones.validar_campo_obligatorio(contacto, "contacto"):
            return False
        
        # Validación para campo Teléfono.
        if not Validaciones.validar_telefono(telefono, "teléfono"):
            return False
        
        # Validación para campo Email.
        if not Validaciones.validar_email(email, "email"):
            return False
        
        # Validación para campo Plazo de Pago.
        if not Validaciones.validar_combobox(plazo_pago, plazos_pago, "plazo de pago"):
            return False
        
        return True

    # (4) Método para limpiar campos.
    def _limpiar_campos(self):
        self.entry_nombre.delete(0, "end")
        self.entry_nit.delete(0, "end")
        self.entry_contacto.delete(0, "end")
        self.entry_telefono.delete(0, "end")
        self.entry_email.delete(0, "end")
        self.combo_pago.set(plazos_pago[0])

    # (5) Método para el registro de los proveedor en BD.
    def _registrar_proveedor(self):

        # Captura y depuración final de los datos.
        nombre = self.entry_nombre.get().strip()
        nit = self.entry_nit.get().strip()
        contacto = self.entry_contacto.get().strip()
        telefono = self.entry_telefono.get().strip()
        email = self.entry_email.get().strip().lower()
        plazo_pago = self.combo_pago.get().strip()

        # Guarda de seguridad (early return).
        if not self._validar_proveedor(nombre, nit, contacto, telefono, email, plazo_pago):
            return
        
        # Inserción de datos en BD y limpieza de campos en módulo.
        try:
            insertar_proveedor(nombre, nit, contacto, telefono, email, plazo_pago)
            self._limpiar_campos()
            messagebox.showinfo("Éxito", "Proveedor registrado correctamente")
        except Exception as error:
            messagebox.showerror("Error", f"No se puede realizar el registro: {str(error)}")

# Punto de entrada.
if __name__ == "__main__":
    app = ProveedorApp()
    app.mainloop()