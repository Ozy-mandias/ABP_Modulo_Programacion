import tkinter as tk 
def contenido_reserva(parent):  #dibuja el contenido de pantalla reservas
    contenedor = tk.Frame(parent, bg="white", width=680, height=47)
    contenedor.pack(anchor="w", padx=30, pady=(30, 0))
    contenedor.pack_propagate(False)

    titulo= tk.Label (contenedor, 
        text="RESERVACIONES", 
        font= ("Aldrich", 24),
        fg="#434343",
        bg="white",
        anchor="w")
    
    titulo.place(x=0, y=0, width=433, height=47)

    
    boton_agregar= tk.Button (contenedor,   # Botón "Agregar Nueva Reserva"
        text= "Agregar Nueva Reserva", 
        bg="#434343", 
        fg="white", 
        font=("Aldrich", 12),
        relief=tk.FLAT, #boton sin relieve
        cursor="hand2") #cursor mano
    boton_agregar.place(x=453, y=0, width=227, height=47)


##panel de filtros#
    panel_filtros = tk.Frame(parent, bg="#f0f0f0", width=680, height=147)
    panel_filtros.pack(anchor="w", padx=30, pady=(27, 0))
    panel_filtros.pack_propagate(False) #evita el encogimiento del frame
 #Fila 1 de panel de busqueda 
    tk.Label(             
        panel_filtros,
        text="Filtrar Busqueda",
        bg="#f0f0f0",
        fg="#434343",
        font=("Aldrich", 10)
    ).place(x=51, y=15)

    campo_busqueda = tk.Entry(
        panel_filtros,
        font=("Aldrich", 10),
        bg="#434343",
        fg="#9A9A9A",
        relief=tk.FLAT)
    
    campo_busqueda.place(x=51, y=45, width=243, height=25)
    campo_busqueda.insert(0, "Nombre de huésped / N°Confirmación #")
    campo_busqueda.config(fg="gray")
    
    tk.Label(
        panel_filtros,
        text="Rango Fecha",
        bg="#f0f0f0",
        fg="#434343",
        font=("Aldrich", 10)).place(x=329, y=15)

    fecha1 = tk.Entry(
        panel_filtros,
        font=("Aldrich", 10),
        fg="#9A9A9A",
        bg="#434343",
        relief=tk.FLAT)
    
    fecha1.place(x=329, y=45, width=122, height=25)
    fecha1.insert(0, "Rango Fecha")
    fecha1.config(fg="gray")
    tk.Label(
        panel_filtros,
        text="—",
        bg="#f0f0f0",
        fg="#434343",
        font=("Aldrich", 12)).place(x=455, y=45)

    fecha2 = tk.Entry(
        panel_filtros,
        font=("Aldrich", 10),
        bg="#434343",
        fg= "#9A9A9A",
        relief=tk.FLAT)
    
    fecha2.place(x=485, y=45, width=92, height=25)
    fecha2.insert(0, "Rango Fecha")
    fecha2.config(fg="gray")
    # Fila 2 del panel de busqueda

    tk.Label(
        panel_filtros,
        text="Tipo Habitación",
        bg="#f0f0f0",
        fg="#434343",
        font=("Aldrich", 10)).place(x=51, y=80)

    var_tipo = tk.StringVar(value="Tipo Habitación")
    menu_tipo = tk.OptionMenu(  #menú desplegable
        panel_filtros,
        var_tipo,
        "Simple", "Doble", "Suite", "Familiar")
    menu_tipo.config(
        bg="#434343",
        fg="#9A9A9A",
        font=("Aldrich", 10),
        relief=tk.FLAT,
        highlightthickness=0,
        anchor="w")
    
    menu_tipo["menu"].config(
        bg="#434343",
        fg="#9A9A9A",
        font=("Aldrich", 10)) 
    menu_tipo.place(x=51, y=103, width=227, height=23)

    tk.Label(
        panel_filtros,
        text="Estado de Reserva",
        bg="#f0f0f0",
        fg="#434343",
        font=("Aldrich", 10)).place(x=288, y=80)
    var_estado = tk.StringVar(value="Estado Reserva")
    menu_estado = tk.OptionMenu(
        panel_filtros,
        var_estado,
        "Confirmado", "Pendiente", "Cancelado")
    menu_estado.config(
        bg="#434343",
        fg="#9A9A9A",
        font=("Aldrich", 10),
        relief=tk.FLAT,
        highlightthickness=0,
        anchor="w")
    menu_estado["menu"].config(
        bg="#434343",
        fg="#9A9A9A",
        font=("Aldrich", 10))
    menu_estado.place(x=288, y=103, width=227, height=23)
#Botón de buscar
    boton_buscar = tk.Button(
        panel_filtros,
        text="Buscar",
        bg="#434343",
        fg="white",
        font=("Aldrich", 10),
        relief=tk.FLAT,
        cursor="hand2")
    boton_buscar.place(x=535, y=103, width=103, height=23)

    #Contenedor de la tabla de resultado de Busqueda
    contenedor_tabla = tk.Frame(parent, bg="white", width=680, height=388)
    contenedor_tabla.pack(anchor="w", padx=30, pady=(20, 0))
    contenedor_tabla.pack_propagate(False)

    # encabezado de la tabla 
    encabezado = tk.Frame(contenedor_tabla, bg="#D9D9D9", width=680, height=42)
    encabezado.pack(fill=tk.X)
    encabezado.pack_propagate(False)


    #Columnas de la tabla 
    filas = [
        ("#12345", "Juan Pérez", "#15", "07/10/2026", "07/11/2026", "Confirmado", "Eliminar / Editar"),
        ("#12344", "Juan Pérez", "#14", "08/10/2026", "15/10/2026", "Confirmado", "Eliminar / Editar"),
        ("#12343", "Juan Pérez", "#12", "07/10/2026", "07/11/2026", "Cancelado", "Eliminar / Editar"),
        ("#12342", "Juan Pérez", "#13", "17/09/2026", "22/10/2026", "Confirmado", "Eliminar / Editar"),
        ("#12341", "Juan Pérez", "#16", "17/10/2026", "07/11/2026", "Confirmado", "Eliminar / Editar"),
        ("#12340", "Juan Pérez", "#17", "07/10/2026", "12/11/2026", "Cancelado", "Eliminar / Editar"),
        ("#12339", "Juan Pérez", "#5", "09/12/2026", "23/12/2026", "Pendiente", "Eliminar / Editar"),
    ]
    
    for i, datos in enumerate(filas):
        y = 42 + (i * 47)
        dibujar_fila(contenedor_tabla, y, datos)

    tk.Label(
        encabezado,
        text="Confirmación -",
        bg="#D9D9D9",
        fg="#434343",
        font=("Aldrich", 10)).place(x=9, y=16)

    
    tk.Label(
        encabezado,
        text="Nombre Huésped -",
        bg="#D9D9D9",
        fg="#434343",
        font=("Aldrich", 10)).place(x=100, y=16)

    
    tk.Label(
        encabezado,
        text="Hab. # -",
        bg="#D9D9D9",
        fg="#434343",
        font=("Aldrich", 10)).place(x=237, y=16)

    
    tk.Label(
        encabezado,
        text="Fecha Check-In",
        bg="#D9D9D9",
        fg="#434343",
        font=("Aldrich", 10)).place(x=298, y=16)

    
    tk.Label(
        encabezado,
        text="/ Fecha Check-Out",
        bg="#D9D9D9",
        fg="#434343",
        font=("Aldrich", 10)).place(x=395, y=16)

    
    tk.Label(
        encabezado,
        text="- Estado -",
        bg="#D9D9D9",
        fg="#434343",
        font=("Aldrich", 10)).place(x=511, y=16)

    tk.Label(
        encabezado,
        text="Acción",
        bg="#D9D9D9",
        fg="#434343",
        font=("Aldrich", 10)).place(x=601, y=16)

def dibujar_fila(contenedor, y, datos):
    """Dibuja una fila de la tabla en la posición y con los datos dados."""
    confirmacion, nombre, habitacion, check_in, check_out, estado, accion = datos
    
    tk.Label(contenedor, text=confirmacion, bg="white", fg="#434343",
             font=("Aldrich", 10), anchor="w").place(x=11, y=y + 15)
    
    tk.Label(contenedor, text=nombre, bg="white", fg="#434343",
             font=("Aldrich", 10), anchor="w").place(x=100, y=y + 15)
    
    tk.Label(contenedor, text=habitacion, bg="white", fg="#434343",
             font=("Aldrich", 10), anchor="w").place(x=237, y=y + 15)
    
    tk.Label(contenedor, text=check_in, bg="white", fg="#434343",
             font=("Aldrich", 10), anchor="w").place(x=298, y=y + 15)
    
    tk.Label(contenedor, text=check_out, bg="white", fg="#434343",
             font=("Aldrich", 10), anchor="w").place(x=395, y=y + 15)
    
    tk.Label(contenedor, text=estado, bg="white", fg="#434343",
             font=("Aldrich", 10), anchor="w").place(x=511, y=y + 15)
    
    tk.Label(contenedor, text=accion, bg="white", fg="#434343",
             font=("Aldrich", 8), anchor="w").place(x=601, y=y + 19)
    
    tk.Frame(contenedor, bg="#D9D9D9", height=1, width=648).place(x=11, y=y + 47)