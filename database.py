import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="pendientes.db"):
        self.conexion = sqlite3.connect(db_name)
        self.cursor = self.conexion.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        # Usamos un formato de fecha YYYY-MM-DD para que SQL pueda ordenarlos correctamente
        query = '''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tarea TEXT NOT NULL,
            prioridad INTEGER NOT NULL, -- 1: Alta, 2: Media, 3: Baja
            fecha_limite TEXT NOT NULL,
            estado TEXT DEFAULT 'Pendiente'
        )
        '''
        self.cursor.execute(query)
        self.conexion.commit()

    def insertar_tarea(self, tarea, prioridad, fecha):
        query = "INSERT INTO tareas (tarea, prioridad, fecha_limite) VALUES (?, ?, ?)"
        self.cursor.execute(query, (tarea, prioridad, fecha))
        self.conexion.commit()

    def obtener_tareas(self):
        # Ordenamos primero por prioridad (1 es mas importante) y luego por fecha mas cercana
        query = "SELECT * FROM tareas WHERE estado != 'Completado' ORDER BY prioridad ASC, fecha_limite ASC"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def marcar_completada(self, id_tarea):
        query = "UPDATE tareas SET estado = 'Completado' WHERE id = ?"
        self.cursor.execute(query, (id_tarea,))
        self.conexion.commit()

    def eliminar_tarea(self, id_tarea):
        query = "DELETE FROM tareas WHERE id = ?"
        self.cursor.execute(query, (id_tarea,))
        self.conexion.commit()

    def cerrar_conexion(self):
        self.conexion.close()