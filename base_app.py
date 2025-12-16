import customtkinter as ctk

class BaseERPApp(ctk.CTk):

    # Método constructor master.
    def __init__(self, titulo_modulo: str):
        super().__init__()

        # Configurar ventana principal.
        self.title("myERP")
        self.resizable(True, True)

        # Configurar frame principal.
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Configurar título.
        self.label_titulo = ctk.CTkLabel(self.main_frame, text=titulo_modulo, font=("Arial", 20, "bold"))
        self.label_titulo.pack(pady=20)

    # Método para convertir datos a fecha_sql.
    @staticmethod
    def convertir_fecha_sql(fecha_str):
        try:
            partes = fecha_str.split("/")
            if len(partes) !=3:
                return None, f"Fecha {fecha_str} no tiene formato dd/mm/YYYY"
            dia, mes, anio = partes
            dia_int, mes_int, anio_int = int(dia), int(mes), int(anio)
            if not (1 <= dia_int <= 31):
                return None, f"Día '{dia}' inválido"
            if not (1 <= mes_int <= 12):
                return None, f"Mes '{mes}' inválido"
            if len(anio) != 4:
                return None, f"Año '{anio}' debe tener 4 dígitos"
            return f"{anio}-{mes}-{dia}", None
        except ValueError:
            return None, f"Fecha {fecha_str} contiene valores no numéricos"
        except Exception as e:
            return None, f"Error al convertir fecha: {str(e)}"          