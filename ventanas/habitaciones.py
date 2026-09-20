"""Pantalla de Estado de Habitaciones."""
import tkinter as tk
def contenido_habitaciones(parent):
    
    contenedor = tk.Frame(parent, bg="white", width=680, height=47)
    contenedor.pack(anchor="w", padx=30, pady=(30, 0))
    contenedor.pack_propagate(False)
    
    titulo = tk.Label(
        contenedor,
        text="ESTADO DE HABITACIONES",
        font=("Aldrich", 24),
        fg="#434343",
        bg="white",
        anchor="w"
    )
    titulo.place(x=0, y=0, width=433, height=47)
    
    #Panel de filtro de busqueda
    panel_filtros = tk.Frame(parent, bg="#EBEBEB", width=680, height=82)
    panel_filtros.pack(anchor="w", padx=30, pady=(27, 0))
    panel_filtros.pack_propagate(False)
    
    # Etiquetas 
    tk.Label(
    panel_filtros,
    text="Tipo de Habitación",
    bg="#EBEBEB",
    fg="#434343",
    font=("Aldrich", 10)).place(x=41, y=15)
    
    tk.Label(
    panel_filtros,
    text="Estado",
    bg="#EBEBEB",
    fg="#434343",
    font=("Aldrich", 10)).place(x=266, y=15)
    
    # botón desplegable "Tipo de Habitación"
    var_tipo = tk.StringVar(value="Simple")
    menu_tipo = tk.OptionMenu(
    panel_filtros,
    var_tipo,
        "Simple", "Doble", "Suite", "Familiar")
    
    menu_tipo.config(
    bg="#434343",
    fg="white",
    font=("Aldrich", 10),
    relief=tk.FLAT,
    highlightthickness=0,
    anchor="w")

    menu_tipo["menu"].config(
    bg="#434343",
    fg="white",
    font=("Aldrich", 10))

    menu_tipo.place(x=41, y=38, width=167, height=23)
    
    # boton desplegable opciones
    var_estado = tk.StringVar(value="Disponible")
    menu_estado = tk.OptionMenu(
    panel_filtros,
    var_estado,
    "Disponible", "Ocupada", "Mantenimiento")
    menu_estado.config(bg="#434343",
    fg="white",
    font=("Aldrich", 10),
    relief=tk.FLAT,
    highlightthickness=0,
    anchor="w")
    menu_estado["menu"].config(bg="#434343",
    fg="white",
    font=("Aldrich", 10))
    menu_estado.place(x=266, y=38, width=167, height=23)
    
    #botón "Filtrar"
    boton_filtrar = tk.Button(panel_filtros,
    text="Filtrar",
    bg="#434343",
    fg="white",
    font=("Aldrich", 10),
    relief=tk.FLAT,
    cursor="hand2")
    boton_filtrar.place(x=535, y=38, width=103, height=23)

    #Contenedor de la tabla 
    contenedor_tabla = tk.Frame(parent, bg="white", width=680, height=268)
    contenedor_tabla.pack(anchor="w", padx=30, pady=(20, 0))
    contenedor_tabla.pack_propagate(False)
    
    # Encabezado 
    encabezado = tk.Frame(contenedor_tabla, bg="#D9D9D9", width=680, height=42)
    encabezado.pack(fill=tk.X)
    encabezado.pack_propagate(False)
    
    tk.Label(encabezado, 
    text="Nro. Hab.", 
    bg="#D9D9D9", 
    fg="#434343",
    font=("Aldrich", 10)).place(x=9, y=14)

    tk.Label(encabezado, 
    text="Tipo", 
    bg="#D9D9D9", 
    fg="#434343",
    font=("Aldrich", 10)).place(x=100, y=14)

    tk.Label(encabezado, 
    text="Capacidad", 
    bg="#D9D9D9", 
    fg="#434343",
    font=("Aldrich", 10)).place(x=187, y=14)
    tk.Label(encabezado, 
    text="Precio/Noche", 
    bg="#D9D9D9", 
    fg="#434343",
    font=("Aldrich", 10)).place(x=298, y=14)
    tk.Label(encabezado, 
    text="Estado", 
    bg="#D9D9D9", 
    fg="#434343",
    font=("Aldrich", 10)).place(x=439, y=14)
    tk.Label(encabezado, 
    text="Acción", 
    bg="#D9D9D9", 
    fg="#434343",
    font=("Aldrich", 10)).place(x=601, y=14)
    
    #datos falsos
    filas = [
        ("#12", "Doble", "2 Personas", "$45.000", "Disponible", "Editar"),
        ("#14", "Suite", "4 Personas", "$85.000", "Ocupada", "Editar"),
        ("#15", "Simple", "2 Personas", "$25.000", "Mantenimiento", "Editar"),
    ]
    
    for i, datos in enumerate(filas):
        y = 42 + (i * 47)
        dibujar_fila_habitacion(contenedor_tabla, y, datos)

"""Dibuja fila de la tabla de habitaciones."""
def dibujar_fila_habitacion(contenedor, y, datos):
    
    numero, tipo, capacidad, precio, estado, accion = datos
    
    tk.Label(contenedor, 
    text=numero, 
    bg="white", 
    fg="#434343",
    font=("Aldrich", 10), 
    anchor="w").place(x=11, y=y + 15)
    
    tk.Label(contenedor, 
    text=tipo, 
    bg="white", 
    fg="#434343",
    font=("Aldrich", 10), 
    anchor="w").place(x=100, y=y + 15)
    
    tk.Label(contenedor,
    text=capacidad,
    bg="white", 
    fg="#434343",
    font=("Aldrich", 10), anchor="w").place(x=187, y=y + 15)
    
    tk.Label(contenedor,
    text=precio, 
    bg="white", 
    fg="#434343",
    font=("Aldrich", 10), 
    anchor="w").place(x=298, y=y + 15)
    
    tk.Label(contenedor, 
    text=estado, 
    bg="white", 
    fg="#434343",
    font=("Aldrich", 10), 
    anchor="w").place(x=439, y=y + 15)
    
    # Botón "Editar"
    tk.Button(contenedor, text=accion, bg="#434343", fg="white",
              font=("Aldrich", 8), relief=tk.FLAT, cursor="hand2"
              ).place(x=601, y=y + 12, width=58, height=21)
    
    # Separador
    tk.Frame(contenedor, bg="#D9D9D9", height=1, width=648).place(x=16, y=y + 47)