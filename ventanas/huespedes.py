
"""Pantalla de Huéspedes."""
import tkinter as tk

def dibujar_fila_huesped(contenedor, y, datos):
    """Dibuja una fila de la tabla de huéspedes."""
    dni, nombre, apellido, telefono, email, accion = datos
    
    tk.Label(contenedor, text=dni, bg="white", fg="#434343",
             font=("Aldrich", 10), anchor="w").place(x=16, y=y + 15)
    
    tk.Label(contenedor, text=nombre, bg="white", fg="#434343",
             font=("Aldrich", 10), anchor="w").place(x=112, y=y + 15)
    
    tk.Label(contenedor, text=apellido, bg="white", fg="#434343",
             font=("Aldrich", 10), anchor="w").place(x=209, y=y + 15)
    
    tk.Label(contenedor, text=telefono, bg="white", fg="#434343",
             font=("Aldrich", 10), anchor="w").place(x=327, y=y + 15)
    
    tk.Label(contenedor, text=email, bg="white", fg="#434343",
             font=("Aldrich", 10), anchor="w").place(x=432, y=y + 15)
    
    tk.Label(contenedor, text=accion, bg="white", fg="#434343",
             font=("Aldrich", 8), anchor="w").place(x=601, y=y + 19)
    
    # Separador
    tk.Frame(contenedor, bg="#D9D9D9", height=1, width=648).place(x=16, y=y + 47)


def contenido_huespedes(parent):
    contenedor = tk.Frame(parent, bg="white", width=680, height=47)
    contenedor.pack(anchor="w", padx=30, pady=(30, 0))
    contenedor.pack_propagate(False)

    titulo = tk.Label(
        contenedor,
        text="HUÉSPEDES",
        font=("Aldrich", 24),
        fg="#434343",
        bg="white",
        anchor="w")
    titulo.place(x=0, y=0, width=433, height=47)

    boton_agregar = tk.Button(
        contenedor,
        text="Agregar Nuevo Huésped",
        bg="#434343",
        fg="white",
        font=("Aldrich", 12),
        relief=tk.FLAT,
        cursor="hand2")
    boton_agregar.place(x=453, y=0, width=227, height=47)

    #panel de busqueda
    panel_busqueda = tk.Frame(parent, bg="#EBEBEB", width=680, height=82)
    panel_busqueda.pack(anchor="w", padx=30, pady=(27, 0))
    panel_busqueda.pack_propagate(False)

    tk.Label(
        panel_busqueda,
        text="Buscar Huéspedes",
        bg="#EBEBEB",
        fg="#434343",
        font=("Aldrich", 12)).place(x=41, y=10)

    campo_busqueda = tk.Entry(
        panel_busqueda,
        font=("Aldrich", 10),
        bg="white",
        fg="gray",
        relief=tk.FLAT)
    campo_busqueda.place(x=41, y=42, width=335, height=23)
    campo_busqueda.insert(0, "Buscar por DNI o Apellido")

    boton_buscar = tk.Button(
        panel_busqueda,
        text="Buscar",
        bg="#434343",
        fg="white",
        font=("Aldrich", 10),
        relief=tk.FLAT,
        cursor="hand2")
    boton_buscar.place(x=494, y=42, width=103, height=23)

#contenedor de la tabla 
    contenedor_tabla = tk.Frame(parent, bg="white", width=680, height=265)
    contenedor_tabla.pack(anchor="w", padx=30, pady=(20, 0))
    contenedor_tabla.pack_propagate(False)

    encabezado = tk.Frame(contenedor_tabla, bg="#D9D9D9", width=680, height=42)
    encabezado.pack(fill=tk.X)
    encabezado.pack_propagate(False)

    tk.Label(encabezado, text="DNI-", bg="#D9D9D9", fg="#434343",
             font=("Aldrich", 10)).place(x=16, y=16)
    tk.Label(encabezado, text="Nombre-", bg="#D9D9D9", fg="#434343",
             font=("Aldrich", 10)).place(x=112, y=16)
    tk.Label(encabezado, text="Apellido-", bg="#D9D9D9", fg="#434343",
             font=("Aldrich", 10)).place(x=209, y=16)
    tk.Label(encabezado, text="Teléfono-", bg="#D9D9D9", fg="#434343",
             font=("Aldrich", 10)).place(x=327, y=16)
    tk.Label(encabezado, text="Email-", bg="#D9D9D9", fg="#434343",
             font=("Aldrich", 10)).place(x=432, y=16)
    tk.Label(encabezado, text="-Acción", bg="#D9D9D9", fg="#434343",
             font=("Aldrich", 10)).place(x=601, y=16)

    filas = [("38.456.789", "Carlos", "Fernández", "351-1234567", "fernandez@mail.com", "Eliminar / Editar"),
        ("35.476.789", "Carlos", "Gómez", "751-1234567", "cgomez@mail.com", "Eliminar / Editar"),
        ("39.123.856", "Lucia", "Fernández", "755-1234567", "luciafer@mail.com", "Eliminar / Editar"),
        ("48.416.735", "Carlos", "Frachez", "526-1234567", "cfrachez@mail.com", "Eliminar / Editar"),]
    for i, datos in enumerate(filas):
        y = 42 + (i * 47)
        dibujar_fila_huesped(contenedor_tabla, y, datos)