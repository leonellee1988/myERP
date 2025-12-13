import customtkinter as ctk

def crear_scroll_vertical(parent, altura_maxima=300, fg_color="transparent"):
    # Frame contenedor.
    frame_contenedor = ctk.CTkFrame(parent, fg_color=fg_color)
    
    # Canvas.
    canvas = ctk.CTkCanvas(frame_contenedor, highlightthickness=0, height=altura_maxima, bg="#1e1e1e")
    
    # Scrollbar.
    scrollbar = ctk.CTkScrollbar(frame_contenedor, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Frame interior (del mismo color que el Canvas).
    frame_interior = ctk.CTkFrame(canvas, fg_color="#1e1e1e")
    canvas.create_window((0, 0), window=frame_interior, anchor="nw")
    
    # Empaquetar.
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    
    # Configurar eventos.
    def _actualizar_scroll(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    def _ajustar_ancho(event=None):
        canvas.itemconfig(1, width=event.width)
    
    frame_interior.bind("<Configure>", _actualizar_scroll)
    canvas.bind("<Configure>", _ajustar_ancho)
    
    return {
        'frame': frame_contenedor,
        'frame_interior': frame_interior
    }