### Barra superior reutilizable para todas las pantallas
### Contiene: logo, botón de cerrar y titulo

import os
import tkinter as tk
from PIL import Image, ImageTk

def crear_barra_superior(parent, titulo="HOTEL MANAGER | DASH BOARD"):

# Frame de la barra
    barra_tarea = tk.Frame(parent, bg="lightgray", height=80)
    barra_tarea.pack(side=tk.TOP, fill=tk.X)
    barra_tarea.pack_propagate(False)
#logo + Ruta dinamica 
    carpeta_componentes = os.path.dirname(os.path.abspath(__file__))
    carpeta_raiz = os.path.dirname(carpeta_componentes) #La ruta cambio a componentes
    ruta_icono = os.path.join(carpeta_raiz, "ICONS", "ICON.png")
    
    img = Image.open(ruta_icono)
    img = img.resize((150, 60))
    imagen_tk = ImageTk.PhotoImage(img)
    
    label_logo = tk.Label(barra_tarea, image=imagen_tk, bg="lightgray")
    label_logo.place(relx=0, rely=0.5, anchor="w")
    label_logo.image = imagen_tk  #importante, guarda la imagen como atributo del label 

#Titulo y botón 
    label_texto = tk.Label(
        barra_tarea,
        text=titulo,
        bg="lightgray",
        font=("Aldrich", 20, "bold"))
    label_texto.place(relx=0.5, rely=0.5, anchor=tk.CENTER, x=-50, y=0)

    def cerrar_ventana():
        parent.winfo_toplevel().destroy() 
    boton_cerrar = tk.Button(
        barra_tarea,
        text="x",
        bg="lightgray",
        relief=tk.FLAT,
        font=("Aldrich", 20, "bold"),
        cursor="hand2",
        command=cerrar_ventana
    )
    boton_cerrar.place(relx=1, rely=0.5, anchor=tk.CENTER, x=-50, y=0)
    
    return barra_tarea