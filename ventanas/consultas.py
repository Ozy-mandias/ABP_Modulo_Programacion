"""Pantalla de Consultas con CRUD completo, filtros y formulario embebido."""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
from PIL import Image, ImageTk

from acceso_datos import (
    listar_consultas, obtener_consulta_por_id,
    insertar_consulta, actualizar_consulta, eliminar_consulta
)
from validaciones import validar_consulta

# ------------------------------------------------------------
# Paleta y fuentes (misma que el resto de la app)
# ------------------------------------------------------------
COLOR_FONDO = "white"
COLOR_PANEL = "#EBEBEB"
COLOR_TEXTO = "#434343"
COLOR_BOTON_OSCURO = "#434343"
COLOR_BOTON_CLARO = "#999999"
COLOR_BORDE = "#000000"          # bordes negros
COLOR_ENCABEZADO = "#D9D9D9"

FUENTE_TITULO = ("Aldrich", 24)
FUENTE_SUBTITULO = ("Aldrich", 18)
FUENTE_TEXTO = ("Aldrich", 10)
FUENTE_TEXTO_BOLD = ("Aldrich", 10, "bold")
FUENTE_CHICA = ("Aldrich", 8)

# OJO: en la BD el medio es "Telefono" (sin tilde) por el CHECK
MEDIOS = ["WhatsApp", "Web", "Telefono", "Email"]
# OJO: el estado es "Archivado" (masculino), no "Archivada"
ESTADOS = ["Pendiente", "Terminado", "Archivado"]
PASSWORD_ADMIN = "Admin2026!"


# ------------------------------------------------------------
# Utilidades
# ------------------------------------------------------------
def cargar_icono(nombre, ancho, alto):
    carpeta_ventanas = os.path.dirname(os.path.abspath(__file__))
    carpeta_raiz = os.path.dirname(carpeta_ventanas)
    ruta = os.path.join(carpeta_raiz, "ICONS", nombre)
    img = Image.open(ruta).convert("RGBA").resize((ancho, alto))
    return ImageTk.PhotoImage(img)


def fecha_a_texto(fecha):
    """date de MySQL → dd/mm/aaaa."""
    if hasattr(fecha, "strftime"):
        return fecha.strftime("%d/%m/%Y")
    if isinstance(fecha, str) and len(fecha) >= 10:
        try:
            return datetime.strptime(fecha[:10], "%Y-%m-%d").strftime("%d/%m/%Y")
        except ValueError:
            return fecha
    return str(fecha)


def color_estado(estado):
    e = estado.lower()
    if e == "pendiente":
        return "#FFC400"
    if e == "terminado":
        return "#3CA433"
    return "#AFAFAF"   # archivado


# ------------------------------------------------------------
# FILA DE TABLA
# ------------------------------------------------------------
def dibujar_medios_comunicacion(parent):
    """Dibuja el panel de medios de comunicación debajo de los filtros."""
    marco = tk.Frame(parent, bg="#FAFAFA",
                     highlightbackground=COLOR_BORDE, highlightthickness=1,
                     width=680, height=95)
    marco.pack_propagate(False)

    tk.Label(marco, text="NUESTROS MEDIOS DE COMUNICACIÓN",
             bg="#FAFAFA", fg=COLOR_TEXTO, font=FUENTE_TEXTO_BOLD,
             anchor="w").place(x=15, y=8)

    # --- Email ---
    try:
        img_email = cargar_icono("email.webp", 22, 22)
        lbl = tk.Label(marco, image=img_email, bg="#FAFAFA")
        lbl.image = img_email
        lbl.place(x=15, y=32, width=22, height=22)
    except Exception:
        pass
    tk.Label(marco, text="Email", bg="#FAFAFA", fg=COLOR_TEXTO,
             font=FUENTE_TEXTO_BOLD).place(x=45, y=32)
    tk.Label(marco, text="gestarho.soporte@gmail.com", bg="#FAFAFA",
             fg=COLOR_TEXTO, font=FUENTE_CHICA,
             anchor="w").place(x=15, y=58)

    # --- WhatsApp / Teléfono ---
    try:
        img_tel = cargar_icono("tel.png", 22, 22)
        lbl = tk.Label(marco, image=img_tel, bg="#FAFAFA")
        lbl.image = img_tel
        lbl.place(x=250, y=32, width=22, height=22)
    except Exception:
        pass
    tk.Label(marco, text="WhatsApp / Teléfono", bg="#FAFAFA", fg=COLOR_TEXTO,
             font=FUENTE_TEXTO_BOLD).place(x=280, y=32)
    tk.Label(marco, text="+54 351 875-5501  ·  Atención 7 a 18hs",
             bg="#FAFAFA", fg=COLOR_TEXTO, font=FUENTE_CHICA,
             anchor="w").place(x=250, y=58)

    # --- Soporte presencial ---
    try:
        img_ubi = cargar_icono("ubi.webp", 22, 22)
        lbl = tk.Label(marco, image=img_ubi, bg="#FAFAFA")
        lbl.image = img_ubi
        lbl.place(x=470, y=32, width=22, height=22)
    except Exception:
        pass
    tk.Label(marco, text="Soporte Presencial", bg="#FAFAFA", fg=COLOR_TEXTO,
             font=FUENTE_TEXTO_BOLD).place(x=500, y=32)
    tk.Label(marco, text="Av. Siempre Viva 123, Buenos Aires",
             bg="#FAFAFA", fg=COLOR_TEXTO, font=FUENTE_CHICA,
             anchor="w").place(x=470, y=58)
def dibujar_fila_consulta(contenedor, y, datos, al_ver, al_responder, al_editar, al_eliminar):
    id_consulta = datos['id_consulta']
    fecha = fecha_a_texto(datos['fecha'])
    remitente = datos['remitente']
    medio = datos['medio']
    asunto = datos['asunto']
    estado = datos['estado']

    tk.Label(contenedor, text=fecha, bg=COLOR_FONDO, fg=COLOR_TEXTO,
             font=FUENTE_TEXTO, anchor="w").place(x=16, y=y + 15)
    tk.Label(contenedor, text=remitente, bg=COLOR_FONDO, fg=COLOR_TEXTO,
             font=FUENTE_TEXTO, anchor="w").place(x=100, y=y + 15)
    tk.Label(contenedor, text=medio, bg=COLOR_FONDO, fg=COLOR_TEXTO,
             font=FUENTE_TEXTO, anchor="w").place(x=220, y=y + 15)
    tk.Label(contenedor, text=asunto, bg=COLOR_FONDO, fg=COLOR_TEXTO,
             font=FUENTE_TEXTO, anchor="w", justify="left",
             wraplength=150).place(x=305, y=y + 8, anchor="nw", width=150)
    tk.Label(contenedor, text=estado, bg=COLOR_FONDO, fg=COLOR_TEXTO,
             font=FUENTE_TEXTO, anchor="w").place(x=460, y=y + 15)

    tk.Label(contenedor, text="●", bg=COLOR_FONDO, fg=color_estado(estado),
             font=FUENTE_TEXTO).place(x=540, y=y + 14)

    # Botones con bordes negros
    tk.Button(contenedor, text="Ver", bg=COLOR_FONDO, fg=COLOR_TEXTO,
              font=FUENTE_CHICA, relief=tk.SOLID, bd=1,
              highlightbackground=COLOR_BORDE, cursor="hand2",
              command=lambda: al_ver(id_consulta)
              ).place(x=555, y=y + 12, width=34, height=22)

    if estado == "Pendiente":
        tk.Button(contenedor, text="Resp.", bg=COLOR_BOTON_OSCURO, fg="white",
                  font=FUENTE_CHICA, relief=tk.SOLID, bd=1,
                  highlightbackground=COLOR_BORDE, cursor="hand2",
                  command=lambda: al_responder(id_consulta)
                  ).place(x=592, y=y + 12, width=38, height=22)

    tk.Button(contenedor, text="Editar", bg="#5b9bd5", fg="white",
              font=FUENTE_CHICA, relief=tk.SOLID, bd=1,
              highlightbackground=COLOR_BORDE, cursor="hand2",
              command=lambda: al_editar(id_consulta)
              ).place(x=633, y=y + 12, width=50, height=22)

    tk.Button(contenedor, text="X", bg="#c0392b", fg="white",
              font=FUENTE_CHICA, relief=tk.SOLID, bd=1,
              highlightbackground=COLOR_BORDE, cursor="hand2",
              command=lambda: al_eliminar(id_consulta)
              ).place(x=686, y=y + 12, width=24, height=22)

    tk.Frame(contenedor, bg=COLOR_ENCABEZADO, height=1, width=694).place(x=16, y=y + 47)


# ------------------------------------------------------------
# FORMULARIO EMBEBIDO (alta / edición)
# ------------------------------------------------------------
def abrir_formulario(frame_formulario, frame_lista, refrescar, id_consulta=None):
    datos = None
    if id_consulta is not None:
        datos = obtener_consulta_por_id(id_consulta)
        if not datos:
            messagebox.showerror("Error", "No se encontró la consulta.")
            return

    for w in frame_formulario.winfo_children():
        w.destroy()

    def volver():
        frame_formulario.grid_remove()
        frame_lista.grid()

    # Header
    header = tk.Frame(frame_formulario, bg=COLOR_FONDO)
    header.pack(fill=tk.X, padx=30, pady=(15, 0))

    titulo = "CONSULTAS | Cargar" if datos is None else f"CONSULTAS | Editar #{datos['id_consulta']}"
    tk.Label(header, text=titulo, font=FUENTE_SUBTITULO,
             fg=COLOR_TEXTO, bg=COLOR_FONDO).pack(side="left")

    tk.Button(header, text="Volver", bg=COLOR_BOTON_OSCURO, fg="white",
              font=FUENTE_TEXTO, relief=tk.FLAT, command=volver
              ).pack(side="right")

    # Panel con borde negro
    panel = tk.Frame(frame_formulario, bg=COLOR_PANEL,
                     highlightbackground=COLOR_BORDE, highlightthickness=1,
                     width=680, height=210)
    panel.pack(padx=30, pady=(10, 15), anchor="w")
    panel.pack_propagate(False)

    def etiqueta(texto, x, y):
        tk.Label(panel, text=texto, bg=COLOR_PANEL, fg=COLOR_TEXTO,
                 font=FUENTE_TEXTO).place(x=x, y=y)

    def entry(x, y, ancho=190):
        e = tk.Entry(panel, font=FUENTE_TEXTO, relief=tk.SOLID, bd=1,
                     highlightbackground=COLOR_BORDE, highlightcolor=COLOR_BORDE)
        e.place(x=x, y=y, width=ancho, height=25)
        return e

    # Fila 1
    etiqueta("Fecha (AAAA-MM-DD)", 30, 20)
    entrada_fecha = entry(30, 42)

    etiqueta("Remitente", 250, 20)
    entrada_remitente = entry(250, 42)

    etiqueta("Medio", 470, 20)
    var_medio = tk.StringVar(value=datos['medio'] if datos else MEDIOS[0])
    menu_medio = tk.OptionMenu(panel, var_medio, *MEDIOS)
    menu_medio.config(bg=COLOR_BOTON_OSCURO, fg="white", font=FUENTE_TEXTO,
                      relief=tk.SOLID, bd=1, highlightthickness=1,
                      highlightbackground=COLOR_BORDE, anchor="w")
    menu_medio["menu"].config(bg=COLOR_BOTON_OSCURO, fg="white", font=FUENTE_TEXTO)
    menu_medio.place(x=470, y=42, width=170, height=25)

    # Fila 2
    etiqueta("Asunto", 30, 90)
    entrada_asunto = tk.Entry(panel, font=FUENTE_TEXTO, relief=tk.SOLID, bd=1,
                              highlightbackground=COLOR_BORDE, highlightcolor=COLOR_BORDE)
    entrada_asunto.place(x=30, y=112, width=420, height=25)

    etiqueta("Estado", 470, 90)
    var_estado = tk.StringVar(value=datos['estado'] if datos else ESTADOS[0])
    menu_estado = tk.OptionMenu(panel, var_estado, *ESTADOS)
    menu_estado.config(bg=COLOR_BOTON_OSCURO, fg="white", font=FUENTE_TEXTO,
                       relief=tk.SOLID, bd=1, highlightthickness=1,
                       highlightbackground=COLOR_BORDE, anchor="w")
    menu_estado["menu"].config(bg=COLOR_BOTON_OSCURO, fg="white", font=FUENTE_TEXTO)
    menu_estado.place(x=470, y=112, width=170, height=25)

    # Precarga
    if datos:
        entrada_fecha.insert(0, datos['fecha'].strftime('%Y-%m-%d'))
        entrada_remitente.insert(0, datos['remitente'])
        entrada_asunto.insert(0, datos['asunto'])
    else:
        entrada_fecha.insert(0, datetime.today().strftime('%Y-%m-%d'))

    def limpiar():
        entrada_fecha.delete(0, tk.END)
        entrada_remitente.delete(0, tk.END)
        entrada_asunto.delete(0, tk.END)
        var_medio.set(MEDIOS[0])
        var_estado.set(ESTADOS[0])
        entrada_fecha.insert(0, datetime.today().strftime('%Y-%m-%d'))

    def guardar():
        datos_validar = {
            'fecha': entrada_fecha.get().strip(),
            'remitente': entrada_remitente.get().strip(),
            'medio': var_medio.get(),
            'asunto': entrada_asunto.get().strip(),
            'estado': var_estado.get(),
        }
        es_valido, errores = validar_consulta(datos_validar)
        if not es_valido:
            messagebox.showwarning(
                "Datos inválidos",
                "Corrija los siguientes errores:\n\n" +
                "\n".join(f"• {e}" for e in errores)
            )
            return

        if datos is None:
            exito, mensaje = insertar_consulta(
                datos_validar['fecha'], datos_validar['remitente'],
                datos_validar['medio'], datos_validar['asunto'],
                datos_validar['estado']
            )
        else:
            exito, mensaje = actualizar_consulta(
                datos['id_consulta'], datos_validar['fecha'],
                datos_validar['remitente'], datos_validar['medio'],
                datos_validar['asunto'], datos_validar['estado'],
                datos.get('id_reserva'), datos.get('id_usuario_asignado')
            )

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            refrescar()
        else:
            messagebox.showerror("Error al guardar", mensaje)

    def borrar():
        if not messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Está SEGURO de eliminar la consulta #{datos['id_consulta']}?\n"
                "Esta acción NO se puede deshacer."):
            return
        password = simpledialog.askstring(
            "Seguridad",
            "Ingrese la contraseña de administrador para continuar:",
            show='*')
        if password != PASSWORD_ADMIN:
            messagebox.showerror("Acceso Denegado",
                                 "Contraseña incorrecta o cancelada.")
            return
        exito, mensaje = eliminar_consulta(datos['id_consulta'])
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            refrescar()
        else:
            messagebox.showerror("No se pudo eliminar", mensaje)

    # Botones
    botones = tk.Frame(panel, bg=COLOR_PANEL)
    botones.place(x=130, y=165)

    tk.Button(botones, text="Cancelar", bg=COLOR_BOTON_CLARO, fg="white",
              font=FUENTE_TEXTO, relief=tk.FLAT, command=volver
              ).pack(side="left", padx=5)
    tk.Button(botones, text="Limpiar", bg=COLOR_BOTON_CLARO, fg="white",
              font=FUENTE_TEXTO, relief=tk.FLAT, command=limpiar
              ).pack(side="left", padx=5)
    tk.Button(botones, text="Registrar" if datos is None else "Actualizar",
              bg="#333333", fg="white", font=FUENTE_TEXTO,
              relief=tk.FLAT, command=guardar
              ).pack(side="left", padx=5)

    if datos is None:
        tk.Button(botones, text="Borrar", state=tk.DISABLED,
                  bg=COLOR_PANEL, fg="#C8C8C8", disabledforeground="#C8C8C8",
                  font=FUENTE_TEXTO, relief=tk.FLAT
                  ).pack(side="left", padx=5)
    else:
        tk.Button(botones, text="Borrar", bg="#E57373", fg="white",
                  activebackground="#D9534F", activeforeground="white",
                  font=FUENTE_TEXTO, relief=tk.FLAT, cursor="hand2",
                  command=borrar).pack(side="left", padx=5)

    frame_lista.grid_remove()
    frame_formulario.grid()


# ------------------------------------------------------------
# PANTALLA PRINCIPAL
# ------------------------------------------------------------
def contenido_consultas(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    parent.grid_columnconfigure(0, weight=1)
    parent.grid_rowconfigure(0, weight=0)
    parent.grid_rowconfigure(1, weight=1)

    def refrescar():
        contenido_consultas(parent)

    # Formulario oculto arriba
    frame_formulario = tk.Frame(parent, bg=COLOR_FONDO)
    frame_formulario.grid(row=0, column=0, sticky="ew")
    frame_formulario.grid_remove()

    # Lista abajo
    frame_lista = tk.Frame(parent, bg=COLOR_FONDO)
    frame_lista.grid(row=1, column=0, sticky="nsew")
    frame_lista.grid_columnconfigure(0, weight=1)
    frame_lista.grid_rowconfigure(3, weight=0)   # medios (altura fija)
    frame_lista.grid_rowconfigure(4, weight=1) 

    # ----- Título + botón -----
    contenedor = tk.Frame(frame_lista, bg=COLOR_FONDO, width=680, height=47)
    contenedor.grid(row=0, column=0, sticky="w", padx=30, pady=(20, 0))
    contenedor.grid_propagate(False)

    tk.Label(contenedor, text="CONSULTAS", font=FUENTE_TITULO,
             fg=COLOR_TEXTO, bg=COLOR_FONDO, anchor="w"
             ).place(x=0, y=0, width=433, height=47)

    boton_nueva = tk.Button(contenedor, text="+ NUEVA CONSULTA",
                            bg=COLOR_BOTON_OSCURO, fg="white", font=("Aldrich", 12),
                            relief=tk.FLAT, cursor="hand2")
    boton_nueva.place(x=541, y=7, width=139, height=34)

    # ----- Panel de filtros (con borde negro) -----
    panel_filtros = tk.Frame(frame_lista, bg=COLOR_PANEL,
                             highlightbackground=COLOR_BORDE, highlightthickness=1,
                             width=680, height=95)
    panel_filtros.grid(row=1, column=0, sticky="w", padx=30, pady=(15, 0))
    panel_filtros.grid_propagate(False)

    tk.Label(panel_filtros, text="Filtrar (remitente o asunto)", bg=COLOR_PANEL,
             fg=COLOR_TEXTO, font=FUENTE_TEXTO).place(x=30, y=10)
    campo_busqueda = tk.Entry(panel_filtros, font=FUENTE_TEXTO,
                              relief=tk.SOLID, bd=1,
                              highlightbackground=COLOR_BORDE,
                              highlightcolor=COLOR_BORDE)
    campo_busqueda.place(x=30, y=32, width=220, height=25)

    tk.Label(panel_filtros, text="Rango Fecha (AAAA-MM-DD)", bg=COLOR_PANEL,
             fg=COLOR_TEXTO, font=FUENTE_TEXTO).place(x=270, y=10)
    fecha_desde = tk.Entry(panel_filtros, font=FUENTE_TEXTO, relief=tk.SOLID, bd=1,
                           highlightbackground=COLOR_BORDE, highlightcolor=COLOR_BORDE)
    fecha_desde.place(x=270, y=32, width=100, height=25)

    tk.Label(panel_filtros, text="—", bg=COLOR_PANEL, fg=COLOR_TEXTO,
             font=FUENTE_TEXTO).place(x=376, y=36)

    fecha_hasta = tk.Entry(panel_filtros, font=FUENTE_TEXTO, relief=tk.SOLID, bd=1,
                           highlightbackground=COLOR_BORDE, highlightcolor=COLOR_BORDE)
    fecha_hasta.place(x=390, y=32, width=100, height=25)

    tk.Label(panel_filtros, text="Estado", bg=COLOR_PANEL, fg=COLOR_TEXTO,
             font=FUENTE_TEXTO).place(x=510, y=10)
    var_estado_filtro = tk.StringVar(value="Todos")
    menu_estado_filtro = tk.OptionMenu(panel_filtros, var_estado_filtro,
                                       "Todos", *ESTADOS)
    menu_estado_filtro.config(bg=COLOR_BOTON_OSCURO, fg="white", font=FUENTE_TEXTO,
                              relief=tk.SOLID, bd=1, highlightthickness=1,
                              highlightbackground=COLOR_BORDE, anchor="w")
    menu_estado_filtro["menu"].config(bg=COLOR_BOTON_OSCURO, fg="white", font=FUENTE_TEXTO)
    menu_estado_filtro.place(x=510, y=32, width=140, height=25)

   # ----- Medios de comunicación (fila 3) -----
    medios_frame = tk.Frame(frame_lista, bg=COLOR_FONDO)
    medios_frame.grid(row=3, column=0, sticky="w", padx=30, pady=(15, 0))
    dibujar_medios_comunicacion(medios_frame)

    # ----- Contenedor de la tabla con scroll (fila 4) -----
    contenedor_tabla = tk.Frame(frame_lista, bg=COLOR_FONDO,
                                highlightbackground=COLOR_BORDE, highlightthickness=1,
                                width=680, height=300)
    contenedor_tabla.grid(row=4, column=0, sticky="nsew", padx=30, pady=(15, 20))

    encabezado = tk.Frame(contenedor_tabla, bg=COLOR_ENCABEZADO, width=680, height=42)
    encabezado.pack(fill=tk.X)
    encabezado.pack_propagate(False)

    for texto, x in [("Fecha", 16), ("Remitente", 100), ("Medio", 220),
                     ("Asunto de consulta", 305), ("Estado", 460),
                     ("Acción", 555)]:
        tk.Label(encabezado, text=texto, bg=COLOR_ENCABEZADO, fg=COLOR_TEXTO,
                 font=FUENTE_TEXTO).place(x=x, y=14)

    frame_scroll = tk.Frame(contenedor_tabla, bg=COLOR_FONDO)
    frame_scroll.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(frame_scroll, bg=COLOR_FONDO, highlightthickness=0)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(frame_scroll, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    area_filas = tk.Frame(canvas, bg=COLOR_FONDO, width=680, height=300)
    canvas.create_window((0, 0), window=area_filas, anchor="nw")

    area_filas.bind("<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    def mostrar_tabla(lista):
        for w in area_filas.winfo_children():
            w.destroy()

        if not lista:
            tk.Label(area_filas, text="No hay consultas para mostrar.",
                     bg=COLOR_FONDO, fg="gray",
                     font=("Aldrich", 12)).place(x=16, y=20)
            area_filas.configure(width=680, height=100)
        else:
            for i, c in enumerate(lista):
                dibujar_fila_consulta(area_filas, i * 47, c,
                                      al_ver, al_responder, al_editar, al_eliminar)
            area_filas.configure(width=680, height=len(lista) * 47 + 20)

        area_filas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    # ----- Acciones -----
    def al_editar(id_consulta):
        abrir_formulario(frame_formulario, frame_lista, refrescar, id_consulta=id_consulta)

    def al_ver(id_consulta):
        c = obtener_consulta_por_id(id_consulta)
        if not c:
            return
        msg = (f"Fecha: {fecha_a_texto(c['fecha'])}\n"
               f"Remitente: {c['remitente']}\n"
               f"Medio: {c['medio']}\n"
               f"Estado: {c['estado']}\n\n"
               f"Asunto:\n{c['asunto']}")
        messagebox.showinfo(f"Consulta #{id_consulta}", msg)

    def al_responder(id_consulta):
        c = obtener_consulta_por_id(id_consulta)
        if not c:
            return
        if not messagebox.askyesno(
                f"Responder consulta #{id_consulta}",
                f"Remitente: {c['remitente']}\nAsunto: {c['asunto']}\n\n"
                "¿Marcar esta consulta como Terminada?"):
            return
        exito, mensaje = actualizar_consulta(
            id_consulta, c['fecha'].strftime('%Y-%m-%d'),
            c['remitente'], c['medio'], c['asunto'], 'Terminado',
            c.get('id_reserva'), c.get('id_usuario_asignado')
        )
        if exito:
            messagebox.showinfo("Éxito", "Consulta marcada como Terminada.")
            mostrar_tabla(listar_consultas())
        else:
            messagebox.showerror("Error", mensaje)

    def al_eliminar(id_consulta):
        if not messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Está SEGURO de eliminar la consulta #{id_consulta}?"):
            return
        password = simpledialog.askstring(
            "Seguridad",
            "Ingrese la contraseña de administrador para continuar:",
            show='*')
        if password != PASSWORD_ADMIN:
            messagebox.showerror("Acceso Denegado",
                                 "Contraseña incorrecta o cancelada.")
            return
        exito, mensaje = eliminar_consulta(id_consulta)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            mostrar_tabla(listar_consultas())
        else:
            messagebox.showerror("No se pudo eliminar", mensaje)

    # ----- Filtros -----
    def filtrar():
        criterio = campo_busqueda.get().strip() or None
        estado = None if var_estado_filtro.get() == "Todos" else var_estado_filtro.get()
        desde = fecha_desde.get().strip() or None
        hasta = fecha_hasta.get().strip() or None
        mostrar_tabla(listar_consultas(criterio, estado, desde, hasta))

    def quitar_filtros():
        campo_busqueda.delete(0, tk.END)
        fecha_desde.delete(0, tk.END)
        fecha_hasta.delete(0, tk.END)
        var_estado_filtro.set("Todos")
        mostrar_tabla(listar_consultas())

    tk.Button(panel_filtros, text="Buscar", bg=COLOR_BOTON_OSCURO, fg="white",
              font=FUENTE_TEXTO, relief=tk.SOLID, bd=1,
              highlightbackground=COLOR_BORDE, cursor="hand2",
              command=filtrar).place(x=510, y=63, width=70, height=23)

    tk.Button(panel_filtros, text="Quitar", bg=COLOR_BOTON_CLARO, fg="white",
              font=FUENTE_TEXTO, relief=tk.SOLID, bd=1,
              highlightbackground=COLOR_BORDE, cursor="hand2",
              command=quitar_filtros).place(x=590, y=63, width=70, height=23)

    # Conectar botón nueva consulta
    boton_nueva.configure(
        command=lambda: abrir_formulario(frame_formulario, frame_lista, refrescar)
    )

    # Carga inicial
    mostrar_tabla(listar_consultas())