import os #modulo para manejar rutas de archivos y carpetas
import tkinter as tk
from PIL import Image, ImageTk

ventana = tk.Tk()
ventana.title("Inicio")
ventana.geometry("900x600")
ventana.attributes("-fullscreen", True)
ventana.resizable(True, True)

"BARRA PRINCIPAL DE LA VENTANA"
barra_tarea= tk.Frame(ventana, bg="lightgray" ,height=80)
barra_tarea.pack(side=tk.TOP, fill=tk.X)
"BARRA PRINCIPAL DE LA VENTANA- LOGO"
carpeta_script = os.path.dirname(os.path.abspath(__file__)) #Ruta dinámica a la imagen del logo
ruta_icono = os.path.join(carpeta_script, "ICONS", "ICON.png") #ruta completa y absoluta a la imagen, sin importar dónde esté el proyecto.

img = Image.open(ruta_icono)
img = img.resize((150, 60))
imagen_tk= ImageTk.PhotoImage(img) 


label_logo= tk.Label(barra_tarea, image=imagen_tk,bg="lightgray")
label_logo.place(relx=0,rely=0.0)
label_logo.image = imagen_tk
"BARRA PRINCIPAL DE LA VENTANA- TEXO"
label_texto= tk.Label(barra_tarea, text="HOTEL MANAGER | DASH BOARD", bg="lightgray", font=("Aldrich", 20, "bold"))
label_texto.place(relx=0.5,rely=0.5, anchor=tk.CENTER, x=-50, y=0)

"BARRA PRINCIPAL DE LA VENTANA- BOTON DE CERRAR"
def cerrar_ventana():
    ventana.destroy()

boton_cerrar= tk.Button(barra_tarea, text="x",bg="lightgray",relief=tk.FLAT,  font=("Aldrich", 20, "bold"),command=cerrar_ventana)
boton_cerrar.place(relx=1,rely=0.5, anchor=tk.CENTER, x=-50, y=0)



"CUERPO DEL PROGRAMA"

caja= tk.Frame(ventana, bg="red" ,height=820)
caja.pack(side=tk.TOP, fill=tk.X)
caja.pack_propagate(False) 
"MENU LATERAL"
menu_lateral= tk.Frame(caja, bg="gray" ,width=300)
menu_lateral.pack(side=tk.LEFT, fill=tk.Y)
menu_lateral.pack_propagate(False)
boton_1= tk.Button(menu_lateral, text="Inicio",bg="darkgray",relief=tk.FLAT,  font=("Aldrich", 12, "bold"),width=18, height=1)
boton_1.pack(pady=(70, 10))
boton_2= tk.Button(menu_lateral, text="Huespedes",bg="darkgray",relief=tk.FLAT,  font=("Aldrich", 12, "bold"),width=18, height=1)
boton_2.pack(pady=(10, 10))
boton_3= tk.Button(menu_lateral, text="Habitaciones",bg="darkgray",relief=tk.FLAT,  font=("Aldrich", 12, "bold"),width=18, height=1)
boton_3.pack(pady=(10, 10))
boton_4= tk.Button(menu_lateral, text="Reservas",bg="darkgray",relief=tk.FLAT,  font=("Aldrich", 12, "bold"),width=18, height=1)
boton_4.pack(pady=(10, 10))
boton_5= tk.Button(menu_lateral, text="Pagos y consumos",bg="darkgray",relief=tk.FLAT,  font=("Aldrich", 12, "bold"),width=18, height=1)
boton_5.pack(pady=(10, 10))
boton_6= tk.Button(menu_lateral, text="Consultas",bg="darkgray",relief=tk.FLAT,  font=("Aldrich", 12, "bold"),width=18, height=1)
boton_6.pack(pady=(10, 20))


"CUERPO DEL PROGRAMA = CONTENIDO"

cuerpo= tk.Frame(caja, bg="blue" ,height=820)
cuerpo.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
cuerpo.pack_propagate(False) 

"CUERPO DEL PROGRAMA =PRIMERAS ESTADISTICAS"
cajas= tk.Frame(cuerpo, bg="white" ,height=180,)
cajas.pack(side=tk.TOP, fill=tk.X)
cajas.pack_propagate(False) 
caja1= tk.Frame(cajas, bg="white" ,width=250, height=120,relief=tk.SOLID, bd=2)
caja1.pack(side=tk.LEFT, padx=(30, 10))
caja2= tk.Frame(cajas, bg="white" ,width=250, height=120,relief=tk.SOLID, bd=2)
caja2.pack(side=tk.LEFT, padx=(10, 10))
caja3= tk.Frame(cajas, bg="white" ,width=250, height=120,relief=tk.SOLID, bd=2)
caja3.pack(side=tk.LEFT, padx=(10, 10))
caja4= tk.Frame(cajas, bg="white" ,width=250, height=120,relief=tk.SOLID, bd=2)
caja4.pack(side=tk.LEFT, padx=(10, 10))
"CUERPO DEL PROGRAMA = SEGUNDAS ESTADISTICAS"

estats= tk.Frame(cuerpo, bg="white" ,height=350)
estats.pack(side=tk.TOP, fill=tk.X)
caja1= tk.Frame(estats, bg="white" ,width=520, height=320,relief=tk.SOLID, bd=2)
caja1.pack(side=tk.LEFT, padx=(30, 10),pady=(10, 10))
caja2= tk.Frame(estats, bg="white" ,width=520, height=320,relief=tk.SOLID, bd=2)
caja2.pack(side=tk.LEFT, padx=(10, 10),pady=(10, 10))
"CUERPO DEL PROGRAMA =  TERCERA ESTADISTICA"

estats2= tk.Frame(cuerpo, bg="white" ,height=350)
estats2.pack(side=tk.TOP, fill=tk.X)
caja1= tk.Frame(estats2, bg="white" ,width=520, height=320,relief=tk.SOLID, bd=2)
caja1.pack(side=tk.LEFT, padx=(30, 10),pady=(10, 10))

ventana.mainloop()



