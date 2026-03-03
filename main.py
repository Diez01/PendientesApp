from gui import AppGui

def main():
    # Inicializamos la aplicación
    app = AppGui()
    
    try:
        # Iniciamos el bucle principal de CustomTkinter
        app.mainloop()
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    finally:
        # Nos aseguramos de cerrar la conexión a la DB al salir
        # Esto evita que el archivo .db se corrompa
        if hasattr(app, 'db'):
            app.db.cerrar_conexion()
            print("Conexión a la base de datos cerrada correctamente.")

if __name__ == "__main__":
    main()