"""Pantalla de Reservas con formulario embebido, desplegables y validaciones RN."""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import messagebox, simpledialog
from acceso_datos import (
    insertar_reserva, listar_reservas, obtener_reserva_por_id,
    actualizar_reserva, eliminar_reserva,
    listar_huespedes_para_combo, listar_habitaciones_para_combo,
    obtener_habitacion_por_id
)
from validaciones import validar_reserva

COLOR_FONDO = "white"
COLOR_PANEL = "#EBEBEB"
COLOR_TEXTO = "#434343"
COLOR_BOTON_OSCURO = "#434343"
COLOR_BOTON_CLARO = "#999999"
FUENTE_TITULO = ("Aldrich", 24)
FUENTE_SUBTITULO = ("Aldrich", 18)
FUENTE_TEXTO = ("Aldrich", 10)

ESTADOS_RESERVA = ["Pendiente", "Confirmado", "Cancelado"]
PASSWORD_ADMIN = "Admin2026!"


def formato_fecha(fecha):
    """Convierte date de MySQL a dd/mm/aaaa."""
    if hasattr(fecha, 'strftime'):
        return fecha.strftime('%d/%m/%Y')
    return str(fecha)


# ============================================================
# PANTALLA PRINCIPAL
# ============================================================
def contenido_reserva(parent):
    """Dibuja la pantalla de reservas dentro del parent."""

    for widget in parent.winfo_children():
        widget.destroy()

    parent.grid_columnconfigure(0, weight=1)
    parent.grid_rowconfigure(0, weight=1)

    frame_principal = tk.Frame(parent, bg=COLOR_FONDO)
    frame_principal.grid(row=0, column=0, sticky="nsew")
    frame_principal.grid_columnconfigure(0, weight=1)
    frame_principal.grid_rowconfigure(0, weight=0)
    frame_principal.grid_rowconfigure(1, weight=0)
    frame_principal.grid_rowconfigure(2, weight=1)

    def refrescar():
        contenido_reserva(parent)

    # ----- Título + botón agregar -----
    contenedor_titulo = tk.Frame(frame_principal, bg=COLOR_FONDO, width=680, height=47)
    contenedor_titulo.grid(row=0, column=0, sticky="w", padx=30, pady=(20, 0))
    contenedor_titulo.grid_propagate(False)

    tk.Label(contenedor_titulo, text="RESERVACIONES", font=FUENTE_TITULO,
             fg=COLOR_TEXTO, bg=COLOR_FONDO, anchor="w"
             ).place(x=0, y=0, width=433, height=47)

    boton_agregar = tk.Button(contenedor_titulo, text="Agregar Nueva Reserva",
                              bg=COLOR_BOTON_OSCURO, fg="white", font=("Aldrich", 12),
                              relief=tk.FLAT, cursor="hand2")
    boton_agregar.place(x=453, y=0, width=227, height=47)

    # ----- Contenedor de la zona filtros/formulario -----
    zona_superior = tk.Frame(frame_principal, bg=COLOR_FONDO)
    zona_superior.grid(row=1, column=0, sticky="ew")
    # ----- Panel de filtros (estilo Figma) -----
    panel_filtros = tk.Frame(zona_superior, bg=COLOR_PANEL, width=680, height=147)
    panel_filtros.pack(fill=tk.X, padx=30, pady=(15, 0))
    panel_filtros.pack_propagate(False)
    # Fila 1
    tk.Label(panel_filtros, text="Filtrar", bg=COLOR_PANEL, fg=COLOR_TEXTO,
             font=FUENTE_TEXTO).place(x=51, y=15)
    campo_busqueda = tk.Entry(panel_filtros, font=FUENTE_TEXTO,
                              bg=COLOR_BOTON_OSCURO, fg="white",
                              insertbackground="white", relief=tk.FLAT)
    campo_busqueda.place(x=51, y=38, width=243, height=25)
    campo_busqueda.insert(0, "Buscar por nombre huésped / Confirmación #")
    campo_busqueda.config(fg="gray")

    def limpiar_placeholder_busqueda(event):
        if campo_busqueda.get() == "Buscar por nombre huésped / Confirmación #":
            campo_busqueda.delete(0, tk.END)
            campo_busqueda.config(fg="white")

    campo_busqueda.bind("<FocusIn>", limpiar_placeholder_busqueda)

    tk.Label(panel_filtros, text="Rango Fecha", bg=COLOR_PANEL,
             fg=COLOR_TEXTO, font=FUENTE_TEXTO).place(x=329, y=15)
    fecha1 = tk.Entry(panel_filtros, font=FUENTE_TEXTO, bg=COLOR_BOTON_OSCURO,
                      fg="white", insertbackground="white", relief=tk.FLAT)
    fecha1.place(x=329, y=38, width=122, height=25)
    fecha1.insert(0, "Rango Fecha")
    fecha1.config(fg="gray")

    def limpiar_placeholder_f1(event):
        if fecha1.get() == "Rango Fecha":
            fecha1.delete(0, tk.END)
            fecha1.config(fg="white")
    fecha1.bind("<FocusIn>", limpiar_placeholder_f1)

    tk.Label(panel_filtros, text="—", bg=COLOR_PANEL, fg=COLOR_TEXTO,
             font=FUENTE_TEXTO).place(x=455, y=40)

    fecha2 = tk.Entry(panel_filtros, font=FUENTE_TEXTO, bg=COLOR_BOTON_OSCURO,
                      fg="white", insertbackground="white", relief=tk.FLAT)
    fecha2.place(x=485, y=38, width=92, height=25)
    fecha2.insert(0, "Rango Fecha")
    fecha2.config(fg="gray")

    def limpiar_placeholder_f2(event):
        if fecha2.get() == "Rango Fecha":
            fecha2.delete(0, tk.END)
            fecha2.config(fg="white")
    fecha2.bind("<FocusIn>", limpiar_placeholder_f2)

    # Fila 2
    tk.Label(panel_filtros, text="Tipo Habitación", bg=COLOR_PANEL,
             fg=COLOR_TEXTO, font=FUENTE_TEXTO).place(x=51, y=80)
    var_tipo_filtro = tk.StringVar(value="Tipo Habitación")
    menu_tipo = tk.OptionMenu(panel_filtros, var_tipo_filtro,
                               "Tipo Habitación", "Simple", "Doble", "Suite", "Familiar")
    menu_tipo.config(bg=COLOR_BOTON_OSCURO, fg="white", font=FUENTE_TEXTO,
                     relief=tk.FLAT, highlightthickness=0, anchor="w")
    menu_tipo["menu"].config(bg=COLOR_BOTON_OSCURO, fg="white", font=FUENTE_TEXTO)
    menu_tipo.place(x=51, y=103, width=227, height=23)

    tk.Label(panel_filtros, text="Estado de Reserva", bg=COLOR_PANEL,
             fg=COLOR_TEXTO, font=FUENTE_TEXTO).place(x=288, y=80)
    var_estado_filtro = tk.StringVar(value="Estado Reserva")
    menu_estado = tk.OptionMenu(panel_filtros, var_estado_filtro,
                                 "Estado Reserva", "Pendiente", "Confirmado", "Cancelado")
    menu_estado.config(bg=COLOR_BOTON_OSCURO, fg="white", font=FUENTE_TEXTO,
                       relief=tk.FLAT, highlightthickness=0, anchor="w")
    menu_estado["menu"].config(bg=COLOR_BOTON_OSCURO, fg="white", font=FUENTE_TEXTO)
    menu_estado.place(x=288, y=103, width=227, height=23)

    # ----- Frame del formulario (oculto por defecto) -----
    frame_formulario = tk.Frame(zona_superior, bg=COLOR_FONDO)
    frame_formulario.pack(fill=tk.X)
    frame_formulario.pack_forget()

    # ----- Contenedor de la tabla con scroll -----
    contenedor_tabla = tk.Frame(frame_principal, bg=COLOR_FONDO, width=680, height=300)
    contenedor_tabla.grid(row=2, column=0, sticky="nsew", padx=30, pady=(15, 20))
    contenedor_tabla.grid_propagate(False)

    encabezado = tk.Frame(contenedor_tabla, bg="#D9D9D9", width=680, height=42)
    encabezado.pack(fill=tk.X)
    encabezado.pack_propagate(False)

    columnas = [
        ("N°", 10), ("Huésped", 70), ("Hab.", 220),
        ("Check-In", 280), ("Check-Out", 370),
        ("Estado", 470), ("Acción", 580)
    ]
    for texto, x in columnas:
        tk.Label(encabezado, text=texto, bg="#D9D9D9", fg=COLOR_TEXTO,
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

    # ----- Dibujo de filas -----
    def dibujar_fila_reserva(contenedor, y, r, al_editar):
        id_reserva = r['id_reserva']
        nombre = f"{r['nombre_huesped']} {r['apellido_huesped']}"
        habitacion = f"#{r['id_habitacion']}"
        check_in = formato_fecha(r['fecha_ingreso'])
        check_out = formato_fecha(r['fecha_salida'])
        estado = r['estado_reserva'].capitalize()

        tk.Label(contenedor, text=f"#{id_reserva}", bg=COLOR_FONDO, fg=COLOR_TEXTO,
                 font=FUENTE_TEXTO, anchor="w").place(x=10, y=y + 15)
        tk.Label(contenedor, text=nombre, bg=COLOR_FONDO, fg=COLOR_TEXTO,
                 font=FUENTE_TEXTO, anchor="w").place(x=70, y=y + 15)
        tk.Label(contenedor, text=habitacion, bg=COLOR_FONDO, fg=COLOR_TEXTO,
                 font=FUENTE_TEXTO, anchor="w").place(x=220, y=y + 15)
        tk.Label(contenedor, text=check_in, bg=COLOR_FONDO, fg=COLOR_TEXTO,
                 font=FUENTE_TEXTO, anchor="w").place(x=280, y=y + 15)
        tk.Label(contenedor, text=check_out, bg=COLOR_FONDO, fg=COLOR_TEXTO,
                 font=FUENTE_TEXTO, anchor="w").place(x=370, y=y + 15)
        tk.Label(contenedor, text=estado, bg=COLOR_FONDO, fg=COLOR_TEXTO,
                 font=FUENTE_TEXTO, anchor="w").place(x=470, y=y + 15)

        tk.Button(contenedor, text="Editar", bg=COLOR_BOTON_OSCURO, fg="white",
                  font=("Aldrich", 8), relief=tk.FLAT, cursor="hand2",
                  command=lambda: al_editar(id_reserva)
                  ).place(x=580, y=y + 12, width=60, height=21)

        tk.Frame(contenedor, bg="#D9D9D9", height=1, width=648).place(x=16, y=y + 47)

    def mostrar_tabla(lista):
        for widget in area_filas.winfo_children():
            widget.destroy()

        if not lista:
            tk.Label(area_filas, text="No hay reservas para mostrar.",
                     bg=COLOR_FONDO, fg="gray",
                     font=("Aldrich", 12)).place(x=16, y=20)
            area_filas.configure(width=680, height=100)
        else:
            for i, r in enumerate(lista):
                dibujar_fila_reserva(area_filas, i * 47, r, al_editar)
            area_filas.configure(width=680, height=len(lista) * 47 + 20)

        area_filas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    # ----- Alternar filtros ↔ formulario -----
    def mostrar_formulario(id_reserva=None):
        panel_filtros.pack_forget()
        for w in frame_formulario.winfo_children():
            w.destroy()
        frame_formulario.pack(fill=tk.X, padx=30, pady=(15, 0))
        _crear_formulario(frame_formulario, refrescar, volver_a_filtros, id_reserva=id_reserva)
    def volver_a_filtros():
        for w in frame_formulario.winfo_children():
            w.destroy()
        frame_formulario.pack_forget()
        # Volver a mostrar el panel con los MISMOS argumentos con los que se creó
        panel_filtros.pack(fill=tk.X, padx=30, pady=(15, 0))

    def al_editar(id_reserva):
        mostrar_formulario(id_reserva=id_reserva)

    def al_agregar():
        mostrar_formulario(id_reserva=None)

    # ----- Filtros -----
    def filtrar():
        criterio = campo_busqueda.get().strip()
        if criterio == "Buscar por nombre huésped / Confirmación #":
            criterio = ""
        estado = None
        if var_estado_filtro.get() != "Estado Reserva":
            estado = var_estado_filtro.get().lower()
        resultados = listar_reservas(
            filtro_texto=criterio if criterio else None,
            estado=estado
        )
        mostrar_tabla(resultados)

    def quitar_filtros():
        campo_busqueda.delete(0, tk.END)
        campo_busqueda.insert(0, "Buscar por nombre huésped / Confirmación #")
        campo_busqueda.config(fg="gray")
        fecha1.delete(0, tk.END)
        fecha1.insert(0, "Rango Fecha")
        fecha1.config(fg="gray")
        fecha2.delete(0, tk.END)
        fecha2.insert(0, "Rango Fecha")
        fecha2.config(fg="gray")
        var_tipo_filtro.set("Tipo Habitación")
        var_estado_filtro.set("Estado Reserva")
        mostrar_tabla(listar_reservas())

    tk.Button(panel_filtros, text="Buscar", bg=COLOR_BOTON_OSCURO,
              fg="white", font=FUENTE_TEXTO, relief=tk.FLAT, cursor="hand2",
              command=filtrar).place(x=535, y=103, width=103, height=23)


    # Conectar botón agregar
    boton_agregar.configure(command=al_agregar)

    # Carga inicial
    mostrar_tabla(listar_reservas())


# ============================================================
# FUNCIÓN AUXILIAR: crear el formulario
# ============================================================
def _crear_formulario(frame_formulario, refrescar, volver_a_filtros, id_reserva=None):
    """Crea el formulario dentro de frame_formulario."""

    datos = None
    if id_reserva is not None:
        datos = obtener_reserva_por_id(id_reserva)
        if not datos:
            messagebox.showerror("Error", "No se encontró la reserva.")
            volver_a_filtros()
            return

    def volver():
        volver_a_filtros()

    # Header
    header = tk.Frame(frame_formulario, bg=COLOR_FONDO)
    header.pack(fill=tk.X, padx=0, pady=(15, 0))

    titulo_form = "RESERVAS | Cargar" if datos is None else f"RESERVAS | Editar #{datos['id_reserva']}"
    tk.Label(header, text=titulo_form, font=FUENTE_SUBTITULO,
             fg=COLOR_TEXTO, bg=COLOR_FONDO).pack(side="left")

    tk.Button(header, text="Volver", bg=COLOR_BOTON_OSCURO, fg="white",
              font=FUENTE_TEXTO, relief=tk.FLAT, command=volver
              ).pack(side="right")

    # Panel de campos
    panel = tk.Frame(frame_formulario, bg=COLOR_PANEL, width=680, height=260)
    panel.pack(padx=0, pady=(10, 15), anchor="w")
    panel.pack_propagate(False)

    # --------- Fila 1: Huésped + Fechas ---------
    tk.Label(panel, text="Huésped", bg=COLOR_PANEL, fg=COLOR_TEXTO,
             font=FUENTE_TEXTO).place(x=30, y=20)

    huespedes = listar_huespedes_para_combo()
    opciones_huespedes = {}
    for h in huespedes:
        etiqueta = f"{h['id_huesped']} - {h['apellido']}, {h['nombre']} (DNI {h['dni']})"
        opciones_huespedes[etiqueta] = h['id_huesped']

    if datos:
        etiqueta_actual = None
        for etiq, id_h in opciones_huespedes.items():
            if id_h == datos['id_huesped']:
                etiqueta_actual = etiq
                break
        var_huesped = tk.StringVar(value=etiqueta_actual if etiqueta_actual else "Seleccione un huésped")
    else:
        var_huesped = tk.StringVar(value="Seleccione un huésped")

    if opciones_huespedes:
        menu_huesped = tk.OptionMenu(panel, var_huesped, *opciones_huespedes.keys())
        menu_huesped.config(bg=COLOR_BOTON_OSCURO, fg="white", font=FUENTE_TEXTO,
                            relief=tk.FLAT, highlightthickness=0, anchor="w")
        menu_huesped["menu"].config(bg=COLOR_BOTON_OSCURO, fg="white", font=FUENTE_TEXTO)
        menu_huesped.place(x=30, y=42, width=280, height=25)
    else:
        tk.Label(panel, text="No hay huéspedes cargados",
                 bg=COLOR_PANEL, fg="red", font=FUENTE_TEXTO,
                 anchor="w").place(x=30, y=42, width=280, height=25)

    tk.Label(panel, text="Fecha Ingreso / Salida (AAAA-MM-DD)", bg=COLOR_PANEL,
             fg=COLOR_TEXTO, font=FUENTE_TEXTO).place(x=330, y=20)
    entrada_fecha_ingreso = tk.Entry(panel, font=FUENTE_TEXTO, relief=tk.FLAT)
    entrada_fecha_ingreso.place(x=330, y=42, width=120, height=25)
    tk.Label(panel, text="—", bg=COLOR_PANEL, fg=COLOR_TEXTO,
             font=FUENTE_TEXTO).place(x=455, y=42)
    entrada_fecha_salida = tk.Entry(panel, font=FUENTE_TEXTO, relief=tk.FLAT)
    entrada_fecha_salida.place(x=470, y=42, width=120, height=25)

    # --------- Fila 2: Habitación + Precio + Nro Personas ---------
    tk.Label(panel, text="Habitación", bg=COLOR_PANEL, fg=COLOR_TEXTO,
             font=FUENTE_TEXTO).place(x=30, y=90)

    habitaciones = listar_habitaciones_para_combo()
    opciones_habitaciones = {}
    for h in habitaciones:
        etiqueta = (f"#{h['id_habitacion']} - {h['tipo_habitacion'].capitalize()} "
                    f"({h['capacidad']} pers.) ${h['precio_noche']:.0f}")
        opciones_habitaciones[etiqueta] = h['id_habitacion']

    if datos:
        etiqueta_hab_actual = None
        for etiq, id_h in opciones_habitaciones.items():
            if id_h == datos['id_habitacion']:
                etiqueta_hab_actual = etiq
                break
        # Si la habitación de la reserva está en mantenimiento, no está en opciones.
        # La agregamos manualmente para poder mostrarla en modo edición.
        if etiqueta_hab_actual is None:
            etiqueta_hab_actual = (f"#{datos['id_habitacion']} - "
                                    f"{datos['tipo_habitacion'].capitalize()} "
                                    f"({datos['capacidad']} pers.) [MANTENIMIENTO]")
            opciones_habitaciones[etiqueta_hab_actual] = datos['id_habitacion']
        var_habitacion = tk.StringVar(value=etiqueta_hab_actual)
    else:
        var_habitacion = tk.StringVar(value="Seleccione una habitación")

    if opciones_habitaciones:
        menu_habitacion = tk.OptionMenu(panel, var_habitacion, *opciones_habitaciones.keys())
        menu_habitacion.config(bg=COLOR_BOTON_OSCURO, fg="white", font=FUENTE_TEXTO,
                                relief=tk.FLAT, highlightthickness=0, anchor="w")
        menu_habitacion["menu"].config(bg=COLOR_BOTON_OSCURO, fg="white", font=FUENTE_TEXTO)
        menu_habitacion.place(x=30, y=112, width=190, height=25)
    else:
        tk.Label(panel, text="No hay habitaciones disponibles",
                 bg=COLOR_PANEL, fg="red", font=FUENTE_TEXTO,
                 anchor="w").place(x=30, y=112, width=190, height=25)

    tk.Label(panel, text="Precio por noche", bg=COLOR_PANEL, fg=COLOR_TEXTO,
             font=FUENTE_TEXTO).place(x=250, y=90)
    entrada_precio = tk.Entry(panel, font=FUENTE_TEXTO, relief=tk.FLAT,
                               state="readonly", readonlybackground="#F5F5F5")
    entrada_precio.place(x=250, y=112, width=190, height=25)

    # Callback autocompletar precio (solo en modo crear)
    def actualizar_precio(*args):
        etiqueta = var_habitacion.get()
        if etiqueta in opciones_habitaciones:
            id_hab = opciones_habitaciones[etiqueta]
            hab_data = obtener_habitacion_por_id(id_hab)
            if hab_data:
                entrada_precio.config(state="normal")
                entrada_precio.delete(0, tk.END)
                entrada_precio.insert(0, f"{hab_data['precio_noche']:.2f}")
                entrada_precio.config(state="readonly")

    tk.Label(panel, text="Nro Personas", bg=COLOR_PANEL, fg=COLOR_TEXTO,
             font=FUENTE_TEXTO).place(x=470, y=90)
    entrada_personas = tk.Entry(panel, font=FUENTE_TEXTO, relief=tk.FLAT)
    entrada_personas.place(x=470, y=112, width=120, height=25)

    # Precarga de precio / registro del trace
    if datos:
        entrada_precio.config(state="normal")
        entrada_precio.delete(0, tk.END)
        entrada_precio.insert(0, f"{datos['precio_noche_acordado']:.2f}")
        entrada_precio.config(state="readonly")
    else:
        var_habitacion.trace_add("write", actualizar_precio)

    # --------- Fila 3: Estado ---------
    tk.Label(panel, text="Estado de la reserva", bg=COLOR_PANEL, fg=COLOR_TEXTO,
             font=FUENTE_TEXTO).place(x=30, y=160)
    var_estado = tk.StringVar(value=datos['estado_reserva'].capitalize() if datos else ESTADOS_RESERVA[0])
    menu_estado_form = tk.OptionMenu(panel, var_estado, *ESTADOS_RESERVA)
    menu_estado_form.config(bg=COLOR_BOTON_OSCURO, fg="white", font=FUENTE_TEXTO,
                             relief=tk.FLAT, highlightthickness=0, anchor="w")
    menu_estado_form["menu"].config(bg=COLOR_BOTON_OSCURO, fg="white", font=FUENTE_TEXTO)
    menu_estado_form.place(x=30, y=182, width=190, height=25)

    # --------- Rellenar fechas y personas en modo edición ---------
    if datos:
        entrada_fecha_ingreso.insert(0, datos['fecha_ingreso'].strftime('%Y-%m-%d'))
        entrada_fecha_salida.insert(0, datos['fecha_salida'].strftime('%Y-%m-%d'))
        entrada_personas.insert(0, str(datos['nro_personas']))

    # --------- Limpiar ---------
    def limpiar():
        entrada_fecha_ingreso.delete(0, tk.END)
        entrada_fecha_salida.delete(0, tk.END)
        entrada_personas.delete(0, tk.END)
        var_estado.set(ESTADOS_RESERVA[0])
        var_huesped.set("Seleccione un huésped")
        var_habitacion.set("Seleccione una habitación")
        entrada_precio.config(state="normal")
        entrada_precio.delete(0, tk.END)
        entrada_precio.config(state="readonly")

    # --------- Guardar ---------
    def guardar():
        datos_validar = {
            'huesped': var_huesped.get().strip(),
            'fecha_ingreso': entrada_fecha_ingreso.get().strip(),
            'fecha_salida': entrada_fecha_salida.get().strip(),
            'habitacion': var_habitacion.get().strip(),
            'precio_noche': entrada_precio.get().strip(),
            'nro_personas': entrada_personas.get().strip(),
            'estado': var_estado.get().lower()
        }
        es_valido, errores = validar_reserva(datos_validar)
        if not es_valido:
            messagebox.showwarning(
                "Datos inválidos",
                "Corrija los siguientes errores:\n\n" +
                "\n".join(f"• {e}" for e in errores)
            )
            return

        # Resolver huésped
        etiqueta_huesped = var_huesped.get()
        if etiqueta_huesped not in opciones_huespedes:
            messagebox.showwarning("Huésped no seleccionado",
                                   "Por favor, seleccione un huésped de la lista.")
            return
        id_huesped = opciones_huespedes[etiqueta_huesped]

        # Resolver habitación
        etiqueta_habitacion = var_habitacion.get()
        if etiqueta_habitacion not in opciones_habitaciones:
            messagebox.showwarning("Habitación no seleccionada",
                                   "Por favor, seleccione una habitación de la lista.")
            return
        id_habitacion = opciones_habitaciones[etiqueta_habitacion]

        # RN-09 / CB-07: no reservar en mantenimiento
        hab_data = obtener_habitacion_por_id(id_habitacion)
        if not hab_data:
            messagebox.showerror("Error", "No se encontró la habitación seleccionada.")
            return
        if hab_data['estado_habitacion'] == 'mantenimiento':
            messagebox.showerror(
                "Habitación en mantenimiento",
                "La habitación seleccionada está en mantenimiento y no puede reservarse."
            )
            return

        # RN-08 / CB-06: capacidad
        nro_personas = int(datos_validar['nro_personas'])
        if nro_personas > hab_data['capacidad']:
            messagebox.showerror(
                "Capacidad excedida",
                f"La habitación #{id_habitacion} ({hab_data['tipo_habitacion']}) "
                f"tiene capacidad para {hab_data['capacidad']} personas.\n"
                f"Usted intentó reservar para {nro_personas} personas."
            )
            return

        precio = datos_validar['precio_noche'].replace(",", ".")

        if datos is None:
            exito, mensaje = insertar_reserva(
                id_huesped, id_habitacion,
                datos_validar['fecha_ingreso'], datos_validar['fecha_salida'],
                precio, nro_personas, datos_validar['estado']
            )
        else:
            exito, mensaje = actualizar_reserva(
                datos['id_reserva'], id_huesped, id_habitacion,
                datos_validar['fecha_ingreso'], datos_validar['fecha_salida'],
                precio, nro_personas, datos_validar['estado']
            )

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            refrescar()
        else:
            messagebox.showerror("Error al guardar", mensaje)

    # --------- Borrar ---------
    def borrar():
        if not messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Está SEGURO de eliminar la reserva #{datos['id_reserva']}?\n"
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
        exito, mensaje = eliminar_reserva(datos['id_reserva'])
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            refrescar()
        else:
            messagebox.showerror("No se pudo eliminar", mensaje)

    # Botones
    botones = tk.Frame(panel, bg=COLOR_PANEL)
    botones.place(x=130, y=215)

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
# El pack lo hace mostrar_formulario() cuando corresponde.
# No usar grid acá porque zona_superior ya usa pack para panel_filtros y sino borra al  apretar boton volver.
    frame_formulario.update_idletasks()