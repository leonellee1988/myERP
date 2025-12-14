import customtkinter as ctk

# Clase constructor.
class BaseERPApp(ctk.CTk):
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