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
        font=("Aldrich", 11),
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

    #Primera fila (Hardcodeada)
    
    fila1 = tk.Frame(contenedor_tabla, bg="white", width=680, height=47)
    fila1.pack(fill=tk.X)
    fila1.pack_propagate(False)

    tk.Label(
        fila1, text="#12345", 
        bg="white", 
        fg="#434343",
        font=("Aldrich", 10), 
        anchor="w").place(x=11, y=15)

    tk.Label(fila1, 
        text="Juan Pérez", 
        bg="white", 
        fg="#434343",
        font=("Aldrich", 10), 
        anchor="w").place(x=100, y=15)
    tk.Label(fila1, 
        text="#15", 
        bg="white",
          fg="#434343",
        font=("Aldrich", 10), 
        anchor="w").place(x=237, y=15)
    tk.Label(
        fila1, text="07/10/2026", 
        bg="white", 
        fg="#434343",
        font=("Aldrich", 10),
          anchor="w").place(x=298, y=15)
    tk.Label(
        fila1, text="07/11/2026", 
        bg="white", 
        fg="#434343",
        font=("Aldrich", 10), 
        anchor="w").place(x=395, y=15)
    tk.Label(
        fila1, 
        text="Confirmado", 
        bg="white", 
        fg="#434343",
        font=("Aldrich", 10), 
        anchor="w" ).place(x=511, y=15)
    tk.Label(fila1, 
        text="Eliminar / Editar", 
        bg="white", 
        fg="#434343",
        font=("Aldrich", 8), 
        anchor="w").place(x=600, y=15)
    # Separador
    tk.Frame(fila1, 
    bg="#D9D9D9",
    height=2, 
    width=648).place(x=11, y=45)

    
    
    