from tkinter import messagebox
from database import insertar_cliente
from base_app import BaseERPApp
from validaciones import Validaciones
from widgets import config_apariencia, crear_frame, crear_frame_izquierda, crear_frame_derecha, \
crear_campo_combo, crear_boton, crear_campo_entry

# Opciones para combobox plazo en cobros.
plazos_cobro = ["Seleccione un valor...", "Al contado", "Crédito 7 días", "Crédito 15 días",
    "Crédito 30 días", "Crédito 60 días", "Crédito 90 días"]

# Configurar apariencia.
config_apariencia("dark", "blue")

class ClienteApp(BaseERPApp):
    # (1) Método constructor
    def __init__(self):
        super().__init__(titulo_modulo="Ingreso de clientes")
        self._crear_seccion_cliente()
    
    # (2) Método para la creación de clientes (viene de constructor)
    def _crear_seccion_cliente(self):
        frame_cliente = crear_frame(self.main_frame, "x", 10, "Registrar nuevo cliente")

        # Contenedor para el frame izquierda/derecha.
        frame_izquierda = crear_frame_izquierda(frame_cliente)
        frame_derecha = crear_frame_derecha(frame_cliente)

        # Creación de los campos del módulo Clientes.
        self.entry_nombre = crear_campo_entry(frame_izquierda, "Nombre completo:", "Edwin Lee")
        self.entry_nit = crear_campo_entry(frame_izquierda, "NIT:", "12345678")
        self.entry_edad = crear_campo_entry(frame_izquierda, "Edad:", "18")
        self.entry_telefono = crear_campo_entry(frame_derecha, "Teléfono:", "7832-2925")
        self.entry_email = crear_campo_entry(frame_derecha, "Email:", "ejemplo@empresa.com")
        self.combo_pago = crear_campo_combo(frame_derecha, "Plazo cobro:", plazos_cobro)

        # Creación de botón 'Registro'.
        crear_boton(self.main_frame, "Registrar", self._registrar_cliente)
    
    # (3) Método para validar datos del cliente:
    def _validar_cliente(self, nombre, nit, edad, telefono, email, plazo_cobro):

        # Validación para campo Nombre.
        if not Validaciones.validar_campo_obligatorio(nombre, "nombre cliente"):
            return False
        
        # Validación para campo NIT.
        if not Validaciones.validar_campo_obligatorio(nit, "NIT"):
            return False
        
        # Validación para campo Edad.
        if not Validaciones.validar_edad(edad, "edad"):
            return False
        
        # Validación para campo Teléfono.
        if not Validaciones.validar_telefono(telefono, "teléfono"):
            return False
        
        # Validación para campo Email.
        if not Validaciones.validar_email(email, "email"):
            return False
        
        # Validación para campo Plazo de Cobro.
        if not Validaciones.validar_combobox(plazo_cobro, plazos_cobro, "plazo de cobro"):
            return False

        return True

    # (4) Método para limpiar campos.
    def _limpiar_campos(self):
        self.entry_nombre.delete(0, "end")
        self.entry_nit.delete(0, "end")
        self.entry_edad.delete(0, "end")
        self.entry_telefono.delete(0, "end")
        self.entry_email.delete(0, "end")
        self.combo_pago.set(plazos_cobro[0])

    # (5) Método para el registro de los clientes en BD.
    def _registrar_cliente(self):

        # Captura y depuración final de los datos.
        nombre = self.entry_nombre.get().strip()
        nit = self.entry_nit.get().strip()
        edad = self.entry_edad.get().strip()
        telefono = self.entry_telefono.get().strip()
        email = self.entry_email.get().strip().lower()
        plazo_cobro = self.combo_pago.get().strip()

        # Guarda de seguridad (early return).
        if not self._validar_cliente(nombre, nit, edad, telefono, email, plazo_cobro):
            return
        
        # Inserción de datos en BD y limpieza de campos en módulo.
        try:
            insertar_cliente(nombre, nit, edad, telefono, email, plazo_cobro)
            self._limpiar_campos()
            messagebox.showinfo("Éxito", "Cliente registrado correctamente")
        except Exception as error:
            messagebox.showerror("Error", f"No se puede realizar el registro: {str(error)}")

# Punto de entrada.
if __name__ == "__main__":
    app = ClienteApp()
    app.mainloop()