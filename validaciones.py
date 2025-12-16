from tkinter import messagebox
from datetime import datetime

class Validaciones:

    # Método para validar campos obligatorios.
    @staticmethod
    def validar_campo_obligatorio(valor, nombre_campo: str) -> bool:
        if not valor or len(valor.strip()) == 0:
            messagebox.showerror("Error", f"El campo: {nombre_campo} es obligatorio")
            return False 
        return True
    
    # Método para validar edades.
    @staticmethod
    def validar_edad(valor, nombre_campo: str) -> bool:
        if not valor or len(str(valor).strip()) == 0:
            messagebox.showerror("Error", f"El campo: {nombre_campo} es obligatorio")
            return False
        try:
            valor_num = int(valor)
            if valor_num < 0 or valor_num > 120:
                messagebox.showerror("Error", "La edad debe estar entre 0 y 120 años")
                return False
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un número entero")
            return False
        return True
    
    # Método para validar números de teléfono.
    @staticmethod
    def validar_telefono(valor, nombre_campo: str) -> bool:
        if not valor or len(valor.strip()) == 0:
            messagebox.showerror("Error", f"El campo: {nombre_campo} es obligatorio")
            return False
        if len(valor.strip()) != 9 or "-" not in valor:
            messagebox.showerror("Error", "Ingrese un número de teléfono válido")
            return False
        return True

   # Método para validar correos electrónicos. 
    @staticmethod
    def validar_email(valor, nombre_campo: str) -> bool:
        if not valor or len(valor.strip()) == 0:
            messagebox.showerror("Error", f"El campo: {nombre_campo} es obligatorio")
            return False
        if "@" not in valor:
            messagebox.showerror("Error", "Ingrese un email válido")
            return False
        usuario, _, dominio = valor.partition("@")
        if not usuario or "." not in dominio:
            messagebox.showerror("Error", "Ingrese un email válido")
            return False
        return True
    
    # Método para validar comboboxes.
    @staticmethod
    def validar_combobox(valor, lista_opciones, nombre_campo: str) -> bool:
        if not valor or len(valor.strip()) == 0:
            messagebox.showerror("Error", f"El campo: {nombre_campo} es obligatorio")
            return False
        if valor not in lista_opciones or valor == "Seleccione un valor...":
            messagebox.showerror("Error", "Ingrese un valor que sea válido")
            return False
        return True
    
    # Método para validar valores enteros.
    @staticmethod
    def validar_valores_enteros(valor, nombre_campo: str) -> bool:
        if not valor:
            messagebox.showerror("Error", f"El campo: {nombre_campo} es obligatorio")
            return False
        try:
            valor_num = int(valor)
            if valor_num < 0:
                messagebox.showerror("Error", f"El {nombre_campo} debe ser mayor a cero")
                return False
        except ValueError:
            messagebox.showerror("Error", f"El {nombre_campo} debe ser un número real")
            return False
        return True
    
    # Métodos para validar valores monetarios.
    @staticmethod
    def validar_valor_monetario(valor, nombre_campo: str) -> bool:
        if not valor:
            messagebox.showerror("Error", f"El campo: {nombre_campo} es obligatorio")
            return False
        try:
            valor_num = float(valor)
            if valor_num < 0:
                messagebox.showerror("Error", f"El {nombre_campo} debe ser mayor a cero")
                return False
        except ValueError:
            messagebox.showerror("Error", f"El {nombre_campo} debe ser un número real")
            return False
        return True
    
    # Método para comparar valores monetarios entre sí.
    @staticmethod
    def validar_valores(val1: float, val2:float, n1:str, n2:str) -> bool:
        try:
            num1 = float(val1)
            num2 = float(val2)
            if num1 > num2:
                messagebox.showerror("Error", f"El {n1} no puede ser mayor que {n2}")
                return False
            return True
        except ValueError:
            return False
    
    # Método para validar fechas.
    @staticmethod
    def validar_fecha(valor, nombre_campo: str) -> bool:
        if not valor or len(valor.strip()) == 0:
            messagebox.showerror("Error", f"El campo: {nombre_campo} es obligatorio")
            return False
        valor = valor.strip()
        try:
            datetime.strptime(valor, "%d/%m/%Y")
            return True
        except ValueError:
            messagebox.showerror("Error", "Ingrese una fecha válida")
            return False
    
    # Método para validación ID.
    @staticmethod
    def validar_id(lista_datos, nombre_buscado, entidad_tipo):
        for item in lista_datos:
            if item[1] == nombre_buscado:
                return item[0], None
        return None, f"{entidad_tipo.capitalize()}  {nombre_buscado} no encontrado"