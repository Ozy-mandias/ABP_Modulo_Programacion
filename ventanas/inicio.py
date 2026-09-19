#Pantalla de inicio (dashboard)
import tkinter as tk
def contenido_inicio(parent): #dibuja el contenido de los dashboard dentro del parent
    cajas = tk.Frame(parent, bg="white", height=180)
    cajas.pack(side=tk.TOP, fill=tk.X)
    cajas.pack_propagate(False)
#estadisticas superiores
    for i in range(4):
        caja = tk.Frame(cajas, bg="white", width=250, height=120,
                        relief=tk.SOLID, bd=2)
        padx_left = 30 if i == 0 else 10
        caja.pack(side=tk.LEFT, padx=(padx_left, 10))
# fila 2 de estadisticas 
    estats = tk.Frame(parent, bg="white", height=350)
    estats.pack(side=tk.TOP, fill=tk.X)
    for i in range(2):
        caja = tk.Frame(estats, bg="white", width=520, height=320,
                        relief=tk.SOLID, bd=2)
        padx_left = 30 if i == 0 else 10
        caja.pack(side=tk.LEFT, padx=(padx_left, 10), pady=(10, 10))
#fila 1 estadisticas grandes
    estats2 = tk.Frame(parent, bg="white", height=350)
    estats2.pack(side=tk.TOP, fill=tk.X)
    
    caja = tk.Frame(estats2, bg="white", width=520, height=320,
                    relief=tk.SOLID, bd=2)
    caja.pack(side=tk.LEFT, padx=(30, 10), pady=(10, 10))