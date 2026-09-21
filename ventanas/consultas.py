"""Pantalla de Consultas."""
import os
import tkinter as tk
from PIL import Image, ImageTk


def cargar_icono(nombre, ancho, alto):
    """Carga una imagen de la carpeta ICONS y la devuelve lista para usar."""
    carpeta_ventanas = os.path.dirname(os.path.abspath(__file__))
    carpeta_raiz = os.path.dirname(carpeta_ventanas)
    ruta = os.path.join(carpeta_raiz, "ICONS", nombre)

    img = Image.open(ruta).convert("RGBA")
    img = img.resize((ancho, alto))
    return ImageTk.PhotoImage(img)


def dibujar_fila_consulta(contenedor, y, datos):
    """Dibuja una fila de la tabla de consultas."""
    fecha, remitente, medio, asunto, estado = datos

    tk.Label(contenedor, text=fecha, bg="white", fg="#434343",
             font=("Aldrich", 10), anchor="w").place(x=16, y=y + 15)

    tk.Label(contenedor, text=remitente, bg="white", fg="#434343",
             font=("Aldrich", 10), anchor="w").place(x=100, y=y + 15)

    tk.Label(contenedor, text=medio, bg="white", fg="#434343",
             font=("Aldrich", 10), anchor="w").place(x=220, y=y + 15)

    # el asunto puede ocupar dos lineas, por eso se centra en la fila
    tk.Label(contenedor, text=asunto, bg="white", fg="#434343",
             font=("Aldrich", 10), anchor="w", justify="left",
             wraplength=155).place(x=305, y=y + 23, anchor="w")

    tk.Label(contenedor, text=estado, bg="white", fg="#434343",
             font=("Aldrich", 10), anchor="w").place(x=470, y=y + 15)

    # color del puntito segun el estado
    if estado == "Pendiente":
        color_punto = "#FFC400"
    elif estado == "Terminado":
        color_punto = "#3CA433"
    else:
        color_punto = "#AFAFAF"

    tk.Label(contenedor, text="●", bg="white", fg=color_punto,
             font=("Aldrich", 10)).place(x=550, y=y + 14)

    # ICONO responder (solo si esta pendiente)
    if estado == "Pendiente":
        img_responder = cargar_icono("compartir.png", 24, 24)
        boton_responder = tk.Button(contenedor, image=img_responder, bg="white",
                                    activebackground="white", relief=tk.FLAT,
                                    bd=0, highlightthickness=0, cursor="hand2")
        boton_responder.image = img_responder  # guarda la imagen para que no se borre
        boton_responder.place(x=590, y=y + 11, width=24, height=24)

    # ICONO ver
    img_ver = cargar_icono("ojo.png", 27, 27)
    boton_ver = tk.Button(contenedor, image=img_ver, bg="white",
                          activebackground="white", relief=tk.FLAT,
                          bd=0, highlightthickness=0, cursor="hand2")
    boton_ver.image = img_ver
    boton_ver.place(x=622, y=y + 10, width=27, height=27)

    # Separador
    tk.Frame(contenedor, bg="#D9D9D9", height=1, width=648).place(x=16, y=y + 47)


def contenido_consultas(parent):

    contenedor = tk.Frame(parent, bg="white", width=680, height=47)
    contenedor.pack(anchor="w", padx=30, pady=(30, 0))
    contenedor.pack_propagate(False)

    titulo = tk.Label(
        contenedor,
        text="CONSULTAS",
        font=("Aldrich", 24),
        fg="#434343",
        bg="white",
        anchor="w")
    titulo.place(x=0, y=0, width=433, height=47)

    boton_nueva = tk.Button(
        contenedor,
        text="+ NUEVA CONSULTA",
        bg="#000000",
        fg="white",
        font=("Aldrich", 9),
        relief=tk.FLAT,
        cursor="hand2")
    boton_nueva.place(x=541, y=7, width=139, height=34)

    # Panel de filtros
    panel_filtros = tk.Frame(parent, bg="#EBEBEB", width=680, height=82)
    panel_filtros.pack(anchor="w", padx=30, pady=(27, 0))
    panel_filtros.pack_propagate(False)

    # Etiquetas
    tk.Label(panel_filtros, text="Filtrar", bg="#EBEBEB", fg="#434343",
             font=("Aldrich", 10)).place(x=41, y=15)

    tk.Label(panel_filtros, text="Rango Fecha", bg="#EBEBEB", fg="#434343",
             font=("Aldrich", 10)).place(x=258, y=15)

    tk.Label(panel_filtros, text="Estado", bg="#EBEBEB", fg="#434343",
             font=("Aldrich", 10)).place(x=438, y=15)

    # campo de busqueda
    campo_busqueda = tk.Entry(
        panel_filtros,
        font=("Aldrich", 9),
        bg="#434343",
        fg="#9A9A9A",
        insertbackground="white",
        relief=tk.FLAT)
    campo_busqueda.place(x=41, y=38, width=200, height=23)
    campo_busqueda.insert(0, "Nombre, asunto o teléfono")

    # rango de fechas
    fecha_desde = tk.Entry(
        panel_filtros,
        font=("Aldrich", 9),
        bg="#434343",
        fg="#9A9A9A",
        insertbackground="white",
        relief=tk.FLAT)
    fecha_desde.place(x=258, y=38, width=72, height=23)
    fecha_desde.insert(0, "21/09/26")

    tk.Label(panel_filtros, text="-", bg="#EBEBEB", fg="#434343",
             font=("Aldrich", 10)).place(x=335, y=40)

    fecha_hasta = tk.Entry(
        panel_filtros,
        font=("Aldrich", 9),
        bg="#434343",
        fg="#9A9A9A",
        insertbackground="white",
        relief=tk.FLAT)
    fecha_hasta.place(x=348, y=38, width=72, height=23)
    fecha_hasta.insert(0, "21/10/26")

    # boton desplegable "Estado"
    var_estado = tk.StringVar(value="Pendiente")
    menu_estado = tk.OptionMenu(
        panel_filtros,
        var_estado,
        "Todos", "Pendiente", "Terminado", "Archivada")
    menu_estado.config(
        bg="#434343",
        fg="white",
        font=("Aldrich", 10),
        relief=tk.FLAT,
        highlightthickness=0,
        anchor="w")
    menu_estado["menu"].config(
        bg="#434343",
        fg="white",
        font=("Aldrich", 10))
    menu_estado.place(x=438, y=38, width=100, height=23)

    # boton "Buscar"
    boton_buscar = tk.Button(
        panel_filtros,
        text="BUSCAR",
        bg="#000000",
        fg="white",
        font=("Aldrich", 10),
        relief=tk.FLAT,
        cursor="hand2")
    boton_buscar.place(x=555, y=38, width=103, height=23)

    # Contenedor de la tabla
    contenedor_tabla = tk.Frame(parent, bg="white", width=680, height=230)
    contenedor_tabla.pack(anchor="w", padx=30, pady=(20, 0))
    contenedor_tabla.pack_propagate(False)

    # Encabezado
    encabezado = tk.Frame(contenedor_tabla, bg="#D9D9D9", width=680, height=42)
    encabezado.pack(fill=tk.X)
    encabezado.pack_propagate(False)

    tk.Label(encabezado, text="Fecha", bg="#D9D9D9", fg="#434343",
             font=("Aldrich", 10)).place(x=16, y=14)
    tk.Label(encabezado, text="Remitente", bg="#D9D9D9", fg="#434343",
             font=("Aldrich", 10)).place(x=100, y=14)
    tk.Label(encabezado, text="Medio", bg="#D9D9D9", fg="#434343",
             font=("Aldrich", 10)).place(x=220, y=14)
    tk.Label(encabezado, text="Asunto de consulta", bg="#D9D9D9", fg="#434343",
             font=("Aldrich", 10)).place(x=305, y=14)
    tk.Label(encabezado, text="Estado", bg="#D9D9D9", fg="#434343",
             font=("Aldrich", 10)).place(x=470, y=14)
    tk.Label(encabezado, text="Acción", bg="#D9D9D9", fg="#434343",
             font=("Aldrich", 10)).place(x=590, y=14)

    # datos falsos
    filas = [
        ("21/09/26", "Carlos Gomez", "WhatsApp", "Disponibilidad por fin de semana largo", "Pendiente"),
        ("21/09/26", "Maria Gimenez", "Web", "Consulta por hospedaje", "Pendiente"),
        ("20/09/26", "Juan Pérez", "Telefono", "Modificacion de fechas de reserva #12345", "Terminado"),
        ("19/09/26", "Valentin Nuñez", "Email", "Consulta de casa para 20 personas", "Archivada"),
    ]

    for i, datos in enumerate(filas):
        y = 42 + (i * 47)
        dibujar_fila_consulta(contenedor_tabla, y, datos)

    # Boton "Ver mas"
    fila_ver_mas = tk.Frame(parent, bg="white", width=680, height=30)
    fila_ver_mas.pack(anchor="w", padx=30, pady=(20, 0))
    fila_ver_mas.pack_propagate(False)

    boton_ver_mas = tk.Button(
        fila_ver_mas,
        text="VER MAS",
        bg="#000000",
        fg="white",
        font=("Aldrich", 12),
        relief=tk.FLAT,
        cursor="hand2")
    boton_ver_mas.place(x=285, y=0, width=110, height=30)

    # Contacto
    contacto = tk.Frame(parent, bg="#FAFAFA", width=680, height=85)
    contacto.pack(anchor="w", padx=30, pady=(16, 0))
    contacto.pack_propagate(False)

    # Email
    img_email = cargar_icono("email.webp", 26, 26)
    label_email = tk.Label(contacto, image=img_email, bg="#FAFAFA")
    label_email.image = img_email
    label_email.place(x=10, y=10, width=26, height=26)
    tk.Label(contacto, text="Email", bg="#FAFAFA", fg="#000000",
             font=("Aldrich", 12)).place(x=45, y=12)
    tk.Label(contacto, text="gestarho.soporte@gmail.com", bg="#FAFAFA", fg="#000000",
             font=("Aldrich", 10), anchor="w").place(x=10, y=48)

    # Telefono
    img_tel = cargar_icono("tel.png", 26, 26)
    label_tel = tk.Label(contacto, image=img_tel, bg="#FAFAFA")
    label_tel.image = img_tel
    label_tel.place(x=255, y=10, width=26, height=26)
    tk.Label(contacto, text="Telefono", bg="#FAFAFA", fg="#000000",
             font=("Aldrich", 12)).place(x=291, y=12)
    tk.Label(contacto, text="+54 351 875-5501\nAtencion de 7 a 18hs", bg="#FAFAFA", fg="#000000",
             font=("Aldrich", 10), anchor="w", justify="left").place(x=255, y=48)

    # Soporte presencial
    img_ubi = cargar_icono("ubi.webp", 26, 26)
    label_ubi = tk.Label(contacto, image=img_ubi, bg="#FAFAFA")
    label_ubi.image = img_ubi
    label_ubi.place(x=446, y=10, width=26, height=26)
    tk.Label(contacto, text="Soporte Presencial", bg="#FAFAFA", fg="#000000",
             font=("Aldrich", 12)).place(x=481, y=12)
    tk.Label(contacto, text="Av. Siempre Viva 123,\nBuenos Aires, Argentina", bg="#FAFAFA", fg="#000000",
             font=("Aldrich", 10), anchor="w", justify="left").place(x=475, y=48)