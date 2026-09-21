"""
Punto de entrada de la aplicación. prueba
Arma la ventana principal con barra superior, menú lateral y cuerpo navegable.
"""
import tkinter as tk

from componentes.barra_superior import crear_barra_superior
from componentes.menu_lateral import crear_menu_lateral , marcar_boton_activo
from ventanas.inicio import contenido_inicio
from ventanas.reserva import contenido_reserva
from ventanas.huespedes import contenido_huespedes
from ventanas.habitaciones import contenido_habitaciones
from ventanas.consultas import contenido_consultas

class App:
    def __init__(self):
        #Crear ventana principal 
        self.ventana = tk.Tk()
        self.ventana.title("Hotel Manager")
        self.ventana.geometry("900x600")
        self.ventana.geometry("1050x800")  
        self.ventana.resizable(True, True)
        
        crear_barra_superior(self.ventana)
        
        self.caja = tk.Frame(self.ventana, bg="white")
        self.caja.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        _,self.botones_menu = crear_menu_lateral(self.caja, self.cambiar_pantalla)
        
        # Cuerpo (donde cambia el contenido)
        self.cuerpo = tk.Frame(self.caja, bg="white")
        self.cuerpo.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.cambiar_pantalla("inicio")
    
    def cambiar_pantalla(self, nombre):
        """Limpia el cuerpo y carga la pantalla correspondiente."""
        marcar_boton_activo(self.botones_menu, nombre)
        for widget in self.cuerpo.winfo_children():
            widget.destroy()
        
        # 1. Destruir todo lo que hay en el cuerpo
        for widget in self.cuerpo.winfo_children():
            widget.destroy()
        
        # 2. Cargar la pantalla según el nombre
        if nombre == "inicio":
            contenido_inicio(self.cuerpo)
        elif nombre == "reservas":
            contenido_reserva(self.cuerpo)
        elif nombre == "huespedes":
            contenido_huespedes(self.cuerpo)
        elif nombre == "habitaciones":
            contenido_habitaciones(self.cuerpo)
        elif nombre == "consultas":
            contenido_consultas(self.cuerpo)
        else:
            # Placeholder para las pantallas que aún no están
            tk.Label(
                self.cuerpo,
                text=f"Pantalla: {nombre.capitalize()}",
                font=("Aldrich", 24, "bold"),
                bg="white",
                fg="#434343"
            ).pack(expand=True)
    
    def ejecutar(self):
        """Inicia el bucle de la aplicación."""
        self.ventana.mainloop()


if __name__ == "__main__":
    app = App()
    app.ejecutar()