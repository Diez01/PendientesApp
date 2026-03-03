from datetime import datetime

class TaskLogic:
    @staticmethod
    def calcular_urgencia(fecha_limite_str):
        """
        Compara la fecha actual con la fecha límite y devuelve un nivel de urgencia.
        Formato esperado: 'YYYY-MM-DD'
        """
        try:
            fecha_limite = datetime.strptime(fecha_limite_str, "%Y-%m-%d").date()
            hoy = datetime.now().date()
            dias_restantes = (fecha_limite - hoy).days

            if dias_restantes < 0:
                return "VENCIDO", "#FF4444"  # Rojo brillante
            elif dias_restantes <= 1:
                return "URGENTE", "#FF8C00"  # Naranja oscuro
            elif dias_restantes <= 3:
                return "PRÓXIMO", "#FFD700"  # Dorado/Amarillo
            else:
                return "A TIEMPO", "#4CAF50" # Verde
        except ValueError:
            return "FECHA INVÁLIDA", "#808080"

    @staticmethod
    def formatear_prioridad(nivel):
        """Convierte el nivel numérico de la DB a texto para la interfaz."""
        prioridades = {
            1: "🔴 ALTA",
            2: "🟡 MEDIA",
            3: "🟢 BAJA"
        }
        return prioridades.get(nivel, "SIN PRIORIDAD")

    @staticmethod
    def validar_datos(tarea, fecha):
        """Valida que los campos no estén vacíos y la fecha sea correcta."""
        if not tarea.strip():
            return False, "La descripción de la tarea no puede estar vacía."
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            return False, "Formato de fecha incorrecto (debe ser AAAA-MM-DD)."
        
        return True, "OK"