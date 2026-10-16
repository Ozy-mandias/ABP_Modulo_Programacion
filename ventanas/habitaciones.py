"""Pantalla de Estado de Habitaciones: listado, filtro, alta y edición."""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import messagebox, simpledialog
from acceso_datos import (
    insertar_habitacion, listar_habitaciones, obtener_habitacion_por_id,
    actualizar_habitacion, listar_reservas_habitacion, eliminar_habitacion
)
from validaciones import validar_habitacion

TIPOS = ["Simple", "Doble", "Suite", "Familiar"]
ESTADOS = ["Disponible", "Ocupada", "Mantenimiento"]


def formato_precio(precio):
    """45000.00 -> $45.000"""
    return f"${precio:,.0f}".replace(",", ".")


def estilo_menu(menu):
    """Aplica el estilo oscuro de la app a un OptionMenu."""
    menu.config(bg="#434343", fg="white", font=("Aldrich", 10),
                relief=tk.FLAT, highlightthickness=0, anchor="w")
    menu["menu"].config(bg="#434343", fg="white", font=("Aldrich", 10))


# ============================================================
# FILA DE TABLA
# ============================================================
def dibujar_fila_habitacion(contenedor, y, datos, al_editar, al_ver_reservas):
    """Dibuja una fila de la tabla de habitaciones."""
    id_hab = datos['id_habitacion']
    columnas = [
        (f"#{id_hab}", 16),
        (datos['tipo_habitacion'].capitalize(), 90),
        (f"{datos['capacidad']} Personas", 170),
        (formato_precio(datos['precio_noche']), 285),
        (datos['estado_habitacion'].capitalize(), 400),
    ]
    for texto, x in columnas:
        tk.Label(contenedor, text=texto, bg="white", fg="#434343",
                 font=("Aldrich", 10), anchor="w").place(x=x, y=y + 15)

    tk.Button(contenedor, text="Editar", bg="#434343", fg="white",
              font=("Aldrich", 8), relief=tk.FLAT, cursor="hand2",
              command=lambda: al_editar(id_hab)
              ).place(x=535, y=y + 12, width=55, height=21)

    tk.Button(contenedor, text="Reservas", bg="#5b9bd5", fg="white",
              font=("Aldrich", 8), relief=tk.FLAT, cursor="hand2",
              command=lambda: al_ver_reservas(id_hab)
              ).place(x=597, y=y + 12, width=65, height=21)

    tk.Frame(contenedor, bg="#D9D9D9", height=1, width=648).place(x=16, y=y + 47)


# ============================================================
# FORMULARIO (agregar / editar)
# ============================================================
def abrir_formulario(frame_formulario, frame_lista, refrescar, id_habitacion=None):
    """Muestra el formulario embebido para agregar o editar una habitación."""

    datos = None
    if id_habitacion is not None:
        datos = obtener_habitacion_por_id(id_habitacion)
        if not datos:
            messagebox.showerror("Error", "No se encontró la habitación.")
            return

    for w in frame_formulario.winfo_children():
        w.destroy()

    def volver():
        frame_formulario.grid_remove()

    # Encabezado
    header = tk.Frame(frame_formulario, bg="white")
    header.pack(fill=tk.X, padx=30, pady=(15, 0))

    if datos is None:
        titulo_form = "HABITACIONES | Cargar"
    else:
        titulo_form = f"HABITACIONES | Editar #{datos['id_habitacion']}"
    tk.Label(header, text=titulo_form, font=("Aldrich", 20),
             fg="#434343", bg="white").pack(side="left")

    tk.Button(header, text="Volver", bg="#434343", fg="white",
              font=("Aldrich", 10), relief=tk.FLAT, command=volver
              ).pack(side="right")

    # Panel de campos
    panel = tk.Frame(frame_formulario, bg="#EBEBEB", width=680, height=200)
    panel.pack(padx=30, pady=(10, 15), anchor="w")
    panel.pack_propagate(False)

    tk.Label(panel, text="Tipo de habitación", bg="#EBEBEB", fg="#434343",
             font=("Aldrich", 10)).place(x=30, y=20)
    var_tipo = tk.StringVar(value=datos['tipo_habitacion'].capitalize() if datos else TIPOS[0])
    menu_tipo = tk.OptionMenu(panel, var_tipo, *TIPOS)
    estilo_menu(menu_tipo)
    menu_tipo.place(x=30, y=42, width=190, height=25)

    tk.Label(panel, text="Capacidad (personas)", bg="#EBEBEB", fg="#434343",
             font=("Aldrich", 10)).place(x=250, y=20)
    entrada_capacidad = tk.Entry(panel, font=("Aldrich", 10), relief=tk.FLAT)
    entrada_capacidad.place(x=250, y=42, width=190, height=25)

    tk.Label(panel, text="Precio por noche ($)", bg="#EBEBEB", fg="#434343",
             font=("Aldrich", 10)).place(x=470, y=20)
    entrada_precio = tk.Entry(panel, font=("Aldrich", 10), relief=tk.FLAT)
    entrada_precio.place(x=470, y=42, width=170, height=25)

    tk.Label(panel, text="Estado", bg="#EBEBEB", fg="#434343",
             font=("Aldrich", 10)).place(x=30, y=90)
    var_estado = tk.StringVar(value=datos['estado_habitacion'].capitalize() if datos else ESTADOS[0])
    menu_estado = tk.OptionMenu(panel, var_estado, *ESTADOS)
    estilo_menu(menu_estado)
    menu_estado.place(x=30, y=112, width=190, height=25)

    if datos:
        entrada_capacidad.insert(0, str(datos['capacidad']))
        entrada_precio.insert(0, f"{datos['precio_noche']:.2f}")

    def limpiar():
        var_tipo.set(TIPOS[0])
        var_estado.set(ESTADOS[0])
        entrada_capacidad.delete(0, tk.END)
        entrada_precio.delete(0, tk.END)

    def guardar():
        datos_validar = {
            'tipo': var_tipo.get().lower(),
            'capacidad': entrada_capacidad.get().strip(),
            'precio_noche': entrada_precio.get().strip(),
            'estado': var_estado.get().lower(),
        }
        es_valido, errores = validar_habitacion(datos_validar)
        if not es_valido:
            messagebox.showwarning(
                "Datos inválidos",
                "Corrija los siguientes errores:\n\n" +
                "\n".join(f"• {e}" for e in errores)
            )
            return

        tipo = datos_validar['tipo']
        capacidad = int(datos_validar['capacidad'])
        precio = datos_validar['precio_noche'].replace(",", ".")
        estado = datos_validar['estado']

        if datos is None:
            exito, mensaje = insertar_habitacion(tipo, capacidad, precio, estado)
        else:
            exito, mensaje = actualizar_habitacion(
                datos['id_habitacion'], tipo, capacidad, precio, estado
            )

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            refrescar()
        else:
            messagebox.showerror("Error al guardar", mensaje)

    def borrar():
        if not messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Está SEGURO de eliminar la habitación #{datos['id_habitacion']}?\n"
                "Esta acción NO se puede deshacer."):
            return
        password = simpledialog.askstring(
            "Seguridad",
            "Ingrese la contraseña de administrador para continuar:",
            show='*')
        if password != "Admin2026!":
            messagebox.showerror("Acceso Denegado",
                                 "Contraseña incorrecta o cancelada. Operación abortada.")
            return
        exito, mensaje = eliminar_habitacion(datos['id_habitacion'])
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            refrescar()
        else:
            messagebox.showerror("No se pudo eliminar", mensaje)

    botones = tk.Frame(panel, bg="#EBEBEB")
    botones.place(x=130, y=155)

    tk.Button(botones, text="Cancelar", bg="#999999", fg="white",
              font=("Aldrich", 10), relief=tk.FLAT, command=volver
              ).pack(side="left", padx=5)
    tk.Button(botones, text="Limpiar", bg="#999999", fg="white",
              font=("Aldrich", 10), relief=tk.FLAT, command=limpiar
              ).pack(side="left", padx=5)
    tk.Button(botones, text="Registrar" if datos is None else "Actualizar",
              bg="#333333", fg="white", font=("Aldrich", 10),
              relief=tk.FLAT, command=guardar
              ).pack(side="left", padx=5)

    # Borrar: rojo sutil al editar; apagado (se funde con el panel) al crear
    if datos is None:
        tk.Button(botones, text="Borrar", state=tk.DISABLED,
                  bg="#EBEBEB", fg="#C8C8C8", disabledforeground="#C8C8C8",
                  font=("Aldrich", 10), relief=tk.FLAT
                  ).pack(side="left", padx=5)
    else:
        tk.Button(botones, text="Borrar", bg="#E57373", fg="white",
                  activebackground="#D9534F", activeforeground="white",
                  font=("Aldrich", 10), relief=tk.FLAT, cursor="hand2",
                  command=borrar).pack(side="left", padx=5)

    frame_formulario.grid()


# ============================================================
# PANTALLA PRINCIPAL
# ============================================================
def contenido_habitaciones(parent):
    """Dibuja la pantalla de habitaciones dentro del parent."""

    for widget in parent.winfo_children():
        widget.destroy()

    parent.grid_columnconfigure(0, weight=1)
    parent.grid_rowconfigure(0, weight=0)
    parent.grid_rowconfigure(1, weight=1)

    def refrescar():
        contenido_habitaciones(parent)

    # Frame del formulario (arriba, oculto) y de la lista (abajo)
    frame_formulario = tk.Frame(parent, bg="white")
    frame_formulario.grid(row=0, column=0, sticky="ew")
    frame_formulario.grid_remove()

    frame_lista = tk.Frame(parent, bg="white")
    frame_lista.grid(row=1, column=0, sticky="nsew")
    frame_lista.grid_columnconfigure(0, weight=1)
    frame_lista.grid_rowconfigure(2, weight=1)

    # ----- Título + botón agregar -----
    contenedor = tk.Frame(frame_lista, bg="white", width=680, height=47)
    contenedor.grid(row=0, column=0, sticky="w", padx=30, pady=(20, 0))
    contenedor.grid_propagate(False)

    tk.Label(contenedor, text="ESTADO DE HABITACIONES", font=("Aldrich", 24),
             fg="#434343", bg="white", anchor="w"
             ).place(x=0, y=0, width=433, height=47)

    boton_agregar = tk.Button(contenedor, text="Agregar Habitación",
                              bg="#434343", fg="white", font=("Aldrich", 12),
                              relief=tk.FLAT, cursor="hand2")
    boton_agregar.place(x=453, y=0, width=227, height=47)

    # ----- Panel de filtros -----
    panel_filtros = tk.Frame(frame_lista, bg="#EBEBEB", width=680, height=82)
    panel_filtros.grid(row=1, column=0, sticky="w", padx=30, pady=(15, 0))
    panel_filtros.grid_propagate(False)

    tk.Label(panel_filtros, text="Tipo de Habitación", bg="#EBEBEB",
             fg="#434343", font=("Aldrich", 10)).place(x=41, y=15)
    tk.Label(panel_filtros, text="Estado", bg="#EBEBEB",
             fg="#434343", font=("Aldrich", 10)).place(x=236, y=15)

    var_tipo = tk.StringVar(value="Todos")
    menu_tipo = tk.OptionMenu(panel_filtros, var_tipo, "Todos", *TIPOS)
    estilo_menu(menu_tipo)
    menu_tipo.place(x=41, y=38, width=167, height=23)

    var_estado = tk.StringVar(value="Todos")
    menu_estado = tk.OptionMenu(panel_filtros, var_estado, "Todos", *ESTADOS)
    estilo_menu(menu_estado)
    menu_estado.place(x=236, y=38, width=167, height=23)

    def filtrar():
        tipo = None if var_tipo.get() == "Todos" else var_tipo.get().lower()
        estado = None if var_estado.get() == "Todos" else var_estado.get().lower()
        mostrar_tabla(listar_habitaciones(tipo, estado))

    tk.Button(panel_filtros, text="Filtrar", bg="#434343", fg="white",
              font=("Aldrich", 10), relief=tk.FLAT, cursor="hand2",
              command=filtrar).place(x=435, y=38, width=103, height=23)

    def quitar_filtros():
        var_tipo.set("Todos")
        var_estado.set("Todos")
        mostrar_tabla(listar_habitaciones())

    tk.Button(panel_filtros, text="Quitar filtros", bg="#555555", fg="white",
              font=("Aldrich", 9), relief=tk.FLAT, cursor="hand2",
              command=quitar_filtros).place(x=548, y=38, width=105, height=23)

    # ----- Contenedor de la tabla con scroll -----
    contenedor_tabla = tk.Frame(frame_lista, bg="white", width=680, height=300)
    contenedor_tabla.grid(row=2, column=0, sticky="nsew", padx=30, pady=(15, 20))
    contenedor_tabla.grid_propagate(False)

    encabezado = tk.Frame(contenedor_tabla, bg="#D9D9D9", width=680, height=42)
    encabezado.pack(fill=tk.X)
    encabezado.pack_propagate(False)

    for texto, x in [("Nro. Hab.", 16), ("Tipo", 90), ("Capacidad", 170),
                     ("Precio/Noche", 285), ("Estado", 400), ("Acción", 570)]:
        tk.Label(encabezado, text=texto, bg="#D9D9D9", fg="#434343",
                 font=("Aldrich", 10)).place(x=x, y=14)

    frame_scroll = tk.Frame(contenedor_tabla, bg="white")
    frame_scroll.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(frame_scroll, bg="white", highlightthickness=0)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    area_filas = tk.Frame(canvas, bg="white", width=680, height=300)
    canvas.create_window((0, 0), window=area_filas, anchor="nw")

    area_filas.bind("<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    def mostrar_tabla(lista):
        for widget in area_filas.winfo_children():
            widget.destroy()

        if not lista:
            tk.Label(area_filas, text="No hay habitaciones para mostrar.",
                     bg="white", fg="gray",
                     font=("Aldrich", 12)).place(x=16, y=20)
            area_filas.configure(width=680, height=100)
        else:
            for i, h in enumerate(lista):
                dibujar_fila_habitacion(area_filas, i * 47, h,
                                        al_editar, al_ver_reservas)
            area_filas.configure(width=680, height=len(lista) * 47 + 20)

        area_filas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    # ----- Acciones -----
    def al_editar(id_habitacion):
        abrir_formulario(frame_formulario, frame_lista, refrescar,
                         id_habitacion=id_habitacion)

    def al_ver_reservas(id_habitacion):
        reservas = listar_reservas_habitacion(id_habitacion)
        if not reservas:
            messagebox.showinfo(f"Habitación #{id_habitacion}",
                                "Esta habitación no tiene reservas registradas.")
            return
        lineas = []
        for r in reservas:
            titular = (f"{r['nombre']} {r['apellido']}"
                       if r['nombre'] else "Sin titular")
            lineas.append(
                f"Reserva #{r['id_reserva']}  |  "
                f"{r['fecha_ingreso'].strftime('%d/%m/%Y')} al "
                f"{r['fecha_salida'].strftime('%d/%m/%Y')}  |  "
                f"{r['estado_reserva'].capitalize()}  |  {titular}"
            )
        messagebox.showinfo(f"Reservas de la habitación #{id_habitacion}",
                            "\n".join(lineas))

    boton_agregar.configure(
        command=lambda: abrir_formulario(frame_formulario, frame_lista, refrescar)
    )

    # Carga inicial
    mostrar_tabla(listar_habitaciones())