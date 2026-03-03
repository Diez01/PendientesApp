import customtkinter as ctk
from database import Database
from logic import TaskLogic

class TareaCard(ctk.CTkFrame):
    """Clase para representar cada tarea como una 'tarjeta' individual."""
    def __init__(self, master, id_tarea, titulo, prioridad, fecha, color_urgencia, al_completar):
        super().__init__(master, border_width=2, border_color=color_urgencia)
        
        self.columnconfigure(0, weight=1)
        
        # Información de la tarea
        self.lbl_titulo = ctk.CTkLabel(self, text=titulo, font=("Arial", 14, "bold"), anchor="w")
        self.lbl_titulo.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="ew")
        
        # Prioridad y Fecha
        texto_info = f"{TaskLogic.formatear_prioridad(prioridad)} | Vence: {fecha}"
        self.lbl_info = ctk.CTkLabel(self, text=texto_info, font=("Arial", 11))
        self.lbl_info.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        # Botón para completar
        self.btn_done = ctk.CTkButton(self, text="✓", width=30, fg_color="#2FA572", 
                                      command=lambda: al_completar(id_tarea))
        self.btn_done.grid(row=0, column=1, rowspan=2, padx=10)

class AppGui(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.db = Database()
        self.title("Admin de Pendientes")
        self.geometry("700x500")

        # Configuración de Grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- FRAME IZQUIERDO (Formulario) ---
        self.form_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.form_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        ctk.CTkLabel(self.form_frame, text="Registrar Tarea", font=("Arial", 20, "bold")).pack(pady=20)
        
        self.entry_tarea = ctk.CTkEntry(self.form_frame, placeholder_text="¿Qué hay que hacer?")
        self.entry_tarea.pack(fill="x", padx=20, pady=10)

        self.combo_prioridad = ctk.CTkOptionMenu(self.form_frame, values=["1 - Alta", "2 - Media", "3 - Baja"])
        self.combo_prioridad.pack(fill="x", padx=20, pady=10)

        self.entry_fecha = ctk.CTkEntry(self.form_frame, placeholder_text="AAAA-MM-DD")
        self.entry_fecha.pack(fill="x", padx=20, pady=10)

        self.btn_guardar = ctk.CTkButton(self.form_frame, text="Guardar Pendiente", command=self.agregar_tarea)
        self.btn_guardar.pack(fill="x", padx=20, pady=20)

        # --- FRAME DERECHO (Lista de Tareas) ---
        self.list_frame = ctk.CTkScrollableFrame(self, label_text="Trabajos pendientes")
        self.list_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.actualizar_lista()

    def agregar_tarea(self):
        tarea = self.entry_tarea.get()
        prioridad_str = self.combo_prioridad.get()
        prioridad = int(prioridad_str[0]) # Extrae el número
        fecha = self.entry_fecha.get()

        valido, mensaje = TaskLogic.validar_datos(tarea, fecha)
        if valido:
            self.db.insertar_tarea(tarea, prioridad, fecha)
            self.entry_tarea.delete(0, 'end')
            self.entry_fecha.delete(0, 'end')
            self.actualizar_lista()
        else:
            print(f"Error: {mensaje}") # Aquí podrías usar un CTkMessagebox

    def actualizar_lista(self):
        # Limpiar lista actual
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        # Cargar desde DB
        tareas = self.db.obtener_tareas()
        for t in tareas:
            # t[0]=id, t[1]=descripcion, t[2]=prioridad, t[3]=fecha
            estado_urgencia, color = TaskLogic.calcular_urgencia(t[3])
            
            card = TareaCard(self.list_frame, t[0], t[1], t[2], t[3], color, self.completar_tarea)
            card.pack(fill="x", padx=5, pady=5)

    def completar_tarea(self, id_tarea):
        self.db.marcar_completada(id_tarea)
        self.actualizar_lista()