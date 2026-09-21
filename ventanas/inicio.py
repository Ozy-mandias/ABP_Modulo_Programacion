#Pantalla de inicio (dashboard)
import tkinter as tk

def contenido_inicio(parent): #dibuja el contenido de los dashboard dentro del parent
    cajas = tk.Frame(parent, bg="white", height=180)
    cajas.pack(side=tk.TOP, fill=tk.X)
    cajas.pack_propagate(False)
    
    #estadisticas superiores
    titulos = ["Tasa de ocupación:", "Check-Ins Hoy:", "Check-Outs Hoy:", "Ganancias Totales:"]
    valores = ["60%", "1", "2", "$1,245K"]
    
    for i in range(4):
        caja = tk.Frame(cajas, bg="white", width=165, height=120,
                        relief=tk.SOLID, bd=2)
        padx_left = 30 if i == 0 else 10
        caja.pack(side=tk.LEFT, padx=(padx_left, 10), pady=(30, 0))
        caja.pack_propagate(False)
        
        # Rellenar cada caja con su texto
        tk.Label(caja, text=titulos[i], bg="white", font=("Aldrich", 10)).pack(pady=(20, 5))
        tk.Label(caja, text=valores[i], bg="white", font=("Aldrich", 18, "bold")).pack()

    # fila 2 estadisticas
    estats = tk.Frame(parent, bg="white", height=350)
    estats.pack(side=tk.TOP, fill=tk.X)
    estats.pack_propagate(False)
    
    cajas_medio = []
    for i in range(2):
        # Ajustamos width a 340 para que entren las 2 cajas perfectamente
        caja = tk.Frame(estats, bg="white", width=340, height=320,
                        relief=tk.SOLID, bd=2)
        padx_left = 30 if i == 0 else 10
        caja.pack(side=tk.LEFT, padx=(padx_left, 10), pady=(10, 10))
        caja.pack_propagate(False)
        cajas_medio.append(caja) # Guardamos para llenarlas abajo
        
    #caja izquierda (Resumen)
    tk.Label(cajas_medio[0], text="Resumen Semanal", bg="white", font=("Aldrich", 12, "bold")).pack(pady=(15, 10))
    dias = [("Lunes", 17), ("Martes", 9), ("Miércoles", 3), ("Jueves", 10), ("Viernes", 18), ("Sábado", 3), ("Domingo", 15)]
    for dia, cant in dias:
        fila = tk.Frame(cajas_medio[0], bg="white")
        fila.pack(fill=tk.X, padx=50, pady=2)
        tk.Label(fila, text=f"{dia}:", bg="white", font=("Aldrich", 10)).pack(side=tk.LEFT)
        tk.Label(fila, text=str(cant), bg="white", font=("Aldrich", 10, "bold")).pack(side=tk.RIGHT)

    # caja derecha (Porcentajes)
    tk.Label(cajas_medio[1], text="Reservas:", bg="white", font=("Aldrich", 12, "bold")).pack(pady=(15, 10))
    reservas = [("Check-Ins Hoy:", "+10%"), ("Check-Outs Hoy:", "+60%"), ("Ganancias Totales:", "+50%")]
    for tit, val in reservas:
        fila = tk.Frame(cajas_medio[1], bg="white")
        fila.pack(fill=tk.X, padx=30, pady=10)
        tk.Label(fila, text=tit, bg="white", font=("Aldrich", 10, "bold")).pack(side=tk.LEFT)
        tk.Label(fila, text=val, bg="white", font=("Aldrich", 14, "bold")).pack(side=tk.RIGHT)
        tk.Frame(cajas_medio[1], bg="#D9D9D9", height=2).pack(fill=tk.X, padx=30)

    #fila 1 estadisticas grandes
    estats2 = tk.Frame(parent, bg="white", height=350)
    estats2.pack(side=tk.TOP, fill=tk.X)
    estats2.pack_propagate(False)
    
    caja_inferior = tk.Frame(estats2, bg="white", width=710, height=320,
                    relief=tk.SOLID, bd=2)
    caja_inferior.pack(side=tk.LEFT, padx=(30, 10), pady=(10, 10))
    caja_inferior.pack_propagate(False)
    
    tk.Label(caja_inferior, text="Actividad Reciente", bg="white", font=("Aldrich", 12, "bold")).pack(pady=(10, 10))
    
    encabezado_act = tk.Frame(caja_inferior, bg="#D9D9D9", height=25)
    encabezado_act.pack(fill=tk.X)
    tk.Label(encabezado_act, text="Reserva reciente", bg="#D9D9D9", font=("Aldrich", 9)).pack(side=tk.LEFT, padx=20)
    tk.Label(encabezado_act, text="Hab. #", bg="#D9D9D9", font=("Aldrich", 9)).pack(side=tk.RIGHT, padx=20)

    for hab in ["#14", "#17", "#34", "#12", "#16"]:
        f = tk.Frame(caja_inferior, bg="white")
        f.pack(fill=tk.X, pady=4)
        tk.Label(f, text="Nombre del huésped", bg="white", font=("Aldrich", 9)).pack(side=tk.LEFT, padx=20)
        tk.Label(f, text=hab, bg="white", font=("Aldrich", 9, "bold")).pack(side=tk.RIGHT, padx=20)
        tk.Frame(caja_inferior, bg="#E0E0E0", height=1).pack(fill=tk.X, padx=10)