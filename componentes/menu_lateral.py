"""Menu lateral reutilizable con botones de navegación 
cada botón llama a un callback para cambiar de pantalla"""

import tkinter as tk

def crear_menu_lateral(parent, callback_cambio_pantalla):
    menu_lateral = tk.Frame(parent, bg="gray", width=300)
    menu_lateral.pack(side=tk.LEFT, fill=tk.Y)
    menu_lateral.pack_propagate(False)

    botones_info = [
    ("Inicio", "inicio"),
    ("Huéspedes", "huespedes"),
    ("Habitaciones", "habitaciones"),
    ("Reservas", "reservas"),
    ("Pagos y consumos", "pagos"),
    ("Consultas", "consultas"),]
    botones = {}

# crea a cada boton como un bucle en lugar de escribir 6 bloques tk.Button, escribimos los datos en una lista y un bucle los procesa.
    for i, (texto, nombre) in enumerate(botones_info):
        if i == 0:
            padding_top = 70
        else:
            padding_top = 10

        if i == len(botones_info) - 1:
            padding_bottom = 20
        else:
            padding_bottom = 10
        boton = tk.Button(
            menu_lateral,
            text=texto,
            bg="darkgray",
            relief=tk.FLAT,
            font=("Aldrich", 12, "bold"),
            width=18,
            height=1,
            cursor="hand2",
            # el lambda captura el nombre de la pantalla actual
            command=lambda n=nombre: callback_cambio_pantalla(n)) # n=nombre captura el valor en el momento de crear el lambda sino solo llama a consultas
        boton.pack(pady=(padding_top, padding_bottom))
        botones[nombre] = boton #guardo el dato para luego resaltar botón
    
    return menu_lateral, botones

# Resalta el botón activo y deja los demás normales.
def marcar_boton_activo(botones, nombre_activo):
    for nombre, boton in botones.items():
        if nombre == nombre_activo:
            # Botón activo: fondo más claro y hundido
            boton.config(bg="lightgray", relief=tk.SUNKEN)
        else:
            # Botones normales
            boton.config(bg="darkgray", relief=tk.FLAT)