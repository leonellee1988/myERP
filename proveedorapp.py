from tkinter import messagebox
from database import insertar_proveedor
from base_app import BaseERPApp
from widgets import config_apariencia, crear_frame, crear_frame_izquierda, crear_frame_derecha, \
crear_campo_combo, crear_boton, crear_campo_entry

# Opciones para combobox plazo en pagos.
plazos_pago = ["Seleccione el plazo de pago...", "Al contado", "Crédito 7 días", "Crédito 15 días",
    "Crédito 30 días", "Crédito 60 días", "Crédito 90 días"]

# Configurar apariencia.
config_apariencia("dark", "blue")

class ProveedorApp(BaseERPApp):
    # (1) Método constructor.
    def __init__(self):
        super().__init__(titulo_modulo="Ingreso de proveedores")
        self._crear_seccion_proveedor()
    
    # (2) Método para la creación de proveedores (viene de constructor)
    def _crear_seccion_proveedor(self):
        frame_proveedor = crear_frame(self.main_frame, "x", 10, "Registrar nuevo proveedor")

        # Contenedor para el frame izquierda.
        frame_izquierda = crear_frame_izquierda(frame_proveedor)
        frame_derecha = crear_frame_derecha(frame_proveedor)

        # Creación de los campos del módulo Proveedores.
        self.entry_nombre = crear_campo_entry(frame_izquierda, "Razón Social:", "Consultoría en Datos, S.A.")
        self.entry_nit = crear_campo_entry(frame_izquierda, "NIT:", "12345678")
        self.entry_contacto = crear_campo_entry(frame_izquierda, "Nombre contacto:", "Noemí Hernández")
        self.entry_telefono = crear_campo_entry(frame_derecha, "Teléfono:", "7832-2925")
        self.entry_email = crear_campo_entry(frame_derecha, "Email:", "ejemplo@empresa.com")
        self.combo_pago = crear_campo_combo(frame_derecha, "Plazo pago:", plazos_pago)

        # # Creación de botón 'Registro'.
        crear_boton(self.main_frame, "Registrar", self._registrar_proveedor)
    
    # (3) Método para validar datos del proveedor:
    def _validar_proveedor(self, nombre, nit, contacto, telefono, email, plazo_pago):

        # Validación para campo Nombre.
        if not nombre or len(nombre.strip()) == 0:
            messagebox.showerror("Error", "El campo nombre es obligatorio")
            return False
        
        # Validación para campo NIT.
        if not nit or len(nit.strip()) == 0:
            messagebox.showerror("Error", "El campo NIT es obligatorio")
            return False
        
        # Validación para campo Contacto.
        if not contacto or len(contacto.strip()) == 0:
            messagebox.showerror("Error", "El campo contacto es obligatorio")
            return False
        
        # Validación para campo Teléfono.
        if not telefono or len(telefono.strip()) == 0:
            messagebox.showerror("Error", "El campo teléfono es obligatorio")
            return False
        if len(telefono.strip()) != 9 or "-" not in telefono:
            messagebox.showerror("Error", "Ingrese un número de teléfono válido")
            return False
        
        # Validación para campo Email.
        if not email or len(email.strip()) == 0:
            messagebox.showerror("Error", "El campo email es obligatorio")
            return False
        if "@" not in email:
            messagebox.showerror("Error", "Ingrese un email válido")
            return False
        usuario, _, dominio = email.partition("@")
        if not usuario or "." not in dominio:
            messagebox.showerror("Error", "Ingrese un email válido")
            return False
        
        # Validación para campo Plazo de Pago.
        if not plazo_pago or len(plazo_pago.strip()) == 0:
            messagebox.showerror("Error", "El campo plazo pago es obligatorio")
            return False
        if plazo_pago not in plazos_pago:
            messagebox.showerror("Error", "Ingrese un plazo de pago válido")
            return False
        if plazo_pago == "Seleccione el plazo de pago...":
            messagebox.showerror("Error", "Ingrese un plazo de pago válido")
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