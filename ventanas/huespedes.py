"""Pantalla de Huéspedes con formulario embebido, scroll y modo papelera."""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import messagebox, simpledialog
from acceso_datos import (
    insertar_huesped, listar_huespedes, buscar_huespedes,
    actualizar_huesped, eliminar_huesped, obtener_huesped_por_id,
    listar_huespedes_inactivos, restaurar_huesped, eliminar_huesped_definitivo
)
from validaciones import validar_huesped


# ============================================================
# FILA DE TABLA - MODO ACTIVO
# ============================================================
def dibujar_fila_huesped_activo(contenedor, y, datos, al_editar, al_eliminar):
    """Dibuja una fila de huésped ACTIVO con botones Editar / Dar de baja."""
    id_huesped = datos['id_huesped']
    dni = datos['dni']
    nombre = datos['nombre']
    apellido = datos['apellido']
    telefono = datos['telefono']
    email = datos['email'] or ""

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

    tk.Button(contenedor, text="Editar", bg="#5b9bd5", fg="white",
              font=("Aldrich", 8), relief=tk.FLAT, cursor="hand2",
              command=lambda: al_editar(id_huesped)
              ).place(x=580, y=y + 12, width=55, height=22)

    tk.Button(contenedor, text="Dar de baja", bg="#c0392b", fg="white",
              font=("Aldrich", 7), relief=tk.FLAT, cursor="hand2",
              command=lambda: al_eliminar(id_huesped)
              ).place(x=640, y=y + 12, width=55, height=22)

    tk.Frame(contenedor, bg="#D9D9D9", height=1, width=648).place(x=16, y=y + 47)


# ============================================================
# FILA DE TABLA - MODO INACTIVO
# ============================================================
def dibujar_fila_huesped_inactivo(contenedor, y, datos, al_restaurar, al_eliminar_def):
    """Dibuja una fila de huésped INACTIVO con botones Restaurar / Eliminar def."""
    id_huesped = datos['id_huesped']
    dni = datos['dni']
    nombre = datos['nombre']
    apellido = datos['apellido']
    telefono = datos['telefono']
    email = datos['email'] or ""

    tk.Label(contenedor, text=dni, bg="white", fg="#999999",
             font=("Aldrich", 10), anchor="w").place(x=16, y=y + 15)
    tk.Label(contenedor, text=nombre, bg="white", fg="#999999",
             font=("Aldrich", 10), anchor="w").place(x=112, y=y + 15)
    tk.Label(contenedor, text=apellido, bg="white", fg="#999999",
             font=("Aldrich", 10), anchor="w").place(x=209, y=y + 15)
    tk.Label(contenedor, text=telefono, bg="white", fg="#999999",
             font=("Aldrich", 10), anchor="w").place(x=327, y=y + 15)
    tk.Label(contenedor, text=email, bg="white", fg="#999999",
             font=("Aldrich", 10), anchor="w").place(x=432, y=y + 15)

    tk.Button(contenedor, text="Restaurar", bg="#27ae60", fg="white",
              font=("Aldrich", 7), relief=tk.FLAT, cursor="hand2",
              command=lambda: al_restaurar(id_huesped)
              ).place(x=580, y=y + 12, width=55, height=22)

    tk.Button(contenedor, text="Eliminar def.", bg="#c0392b", fg="white",
              font=("Aldrich", 7), relief=tk.FLAT, cursor="hand2",
              command=lambda: al_eliminar_def(id_huesped)
              ).place(x=640, y=y + 12, width=55, height=22)

    tk.Frame(contenedor, bg="#D9D9D9", height=1, width=648).place(x=16, y=y + 47)


# ============================================================
# FORMULARIO (agregar / editar)
# ============================================================
def abrir_formulario(parent, frame_formulario, contenedor, panel_busqueda,
                     refrescar, id_huesped=None):
    """Muestra el formulario embebido para agregar o editar un huésped."""

    datos = None
    if id_huesped is not None:
        datos = obtener_huesped_por_id(id_huesped)
        if not datos:
            messagebox.showerror("Error", "No se encontró el huésped.")
            return

    contenedor.grid_remove()
    panel_busqueda.grid_remove()

    for w in frame_formulario.winfo_children():
        w.destroy()

    def volver():
        frame_formulario.grid_remove()
        contenedor.grid()
        panel_busqueda.grid()

    # Header
    header = tk.Frame(frame_formulario, bg="white")
    header.pack(fill=tk.X, padx=30, pady=(15, 0))

    titulo_form = "HUÉSPEDES | Cargar" if datos is None else "HUÉSPEDES | Editar"
    tk.Label(header, text=titulo_form, font=("Aldrich", 20),
             fg="#434343", bg="white").pack(side="left")

    tk.Button(header, text="Volver", bg="#434343", fg="white",
              font=("Aldrich", 10), relief=tk.FLAT, command=volver
              ).pack(side="right")

    # Panel de campos
    panel = tk.Frame(frame_formulario, bg="#EBEBEB",
                     width=680, height=250)
    panel.pack(padx=30, pady=(10, 15))
    panel.pack_propagate(False)

    campos = [
        ("Ingrese DNI",  "dni",                30, 20),
        ("Nombres",      "nombre",             250, 20),
        ("Apellidos",    "apellido",           470, 20),
        ("Dirección",    "direccion",          30, 90),
        ("Teléfono",     "telefono",           250, 90),
        ("Fecha Nac.",   "fecha_nacimiento",   470, 90),
        ("Email",        "email",              30, 160),
        ("Nacionalidad", "nacionalidad",       250, 160),
    ]

    entradas = {}
    for etiqueta, clave, x, y in campos:
        tk.Label(panel, text=etiqueta, bg="#EBEBEB", fg="#434343",
                 font=("Aldrich", 10)).place(x=x, y=y)
        entry = tk.Entry(panel, font=("Aldrich", 10), relief=tk.FLAT)
        entry.place(x=x, y=y + 22, width=190, height=25)

        if datos and datos.get(clave):
            entry.insert(0, str(datos[clave]))
        entradas[clave] = entry

    def limpiar():
        for e in entradas.values():
            e.delete(0, tk.END)

    def guardar():
        nombre = entradas['nombre'].get().strip()
        apellido = entradas['apellido'].get().strip()
        dni = entradas['dni'].get().strip()
        telefono = entradas['telefono'].get().strip()
        email = entradas['email'].get().strip() or None
        direccion = entradas['direccion'].get().strip() or None
        nacionalidad = entradas['nacionalidad'].get().strip() or None
        fecha_nacimiento = entradas['fecha_nacimiento'].get().strip() or None

        datos_validar = {
            'nombre': nombre,
            'apellido': apellido,
            'dni': dni,
            'telefono': telefono,
            'email': email,
            'fecha_nacimiento': fecha_nacimiento,
        }
        es_valido, errores = validar_huesped(datos_validar)
        if not es_valido:
            messagebox.showwarning(
                "Faltan datos o son incorrectos",
                "No se registró el huésped. Complete o corrija estos campos:\n\n" +
                "\n".join(f"• {e}" for e in errores)
            )
            return

        if datos is None:
            exito, mensaje = insertar_huesped(
                nombre, apellido, dni, telefono, email
            )
        else:
            exito, mensaje = actualizar_huesped(
                datos['id_huesped'], nombre, apellido, dni,
                telefono, email, direccion, nacionalidad
            )

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            refrescar()
        else:
            messagebox.showerror("Error al guardar", mensaje)

    botones = tk.Frame(panel, bg="#EBEBEB")
    botones.place(x=180, y=210)

    tk.Button(botones, text="Cancelar", bg="#999999", fg="white",
              font=("Aldrich", 10), relief=tk.FLAT, command=volver
              ).pack(side="left", padx=5)

    tk.Button(botones, text="Limpiar", bg="#999999", fg="white",
              font=("Aldrich", 10), relief=tk.FLAT, command=limpiar
              ).pack(side="left", padx=5)

    tk.Button(botones,
              text="Registrar" if datos is None else "Actualizar",
              bg="#333333", fg="white", font=("Aldrich", 10),
              relief=tk.FLAT, command=guardar
              ).pack(side="left", padx=5)

    frame_formulario.grid()


# ============================================================
# PANTALLA PRINCIPAL
# ============================================================
def contenido_huespedes(parent):
    """Dibuja la pantalla de huéspedes dentro del parent."""

    for widget in parent.winfo_children():
        widget.destroy()

    parent.grid_columnconfigure(0, weight=1)
    parent.grid_rowconfigure(0, weight=0)
    parent.grid_rowconfigure(1, weight=1)

    def refrescar():
        contenido_huespedes(parent)

    # Frame del formulario (arriba, oculto)
    frame_formulario = tk.Frame(parent, bg="white")
    frame_formulario.grid(row=0, column=0, sticky="ew")
    frame_formulario.grid_remove()

    # Frame de la lista (abajo)
    frame_lista = tk.Frame(parent, bg="white")
    frame_lista.grid(row=1, column=0, sticky="nsew")

    frame_lista.grid_columnconfigure(0, weight=1)
    frame_lista.grid_rowconfigure(2, weight=1)

    # ----- Título + botón agregar -----
    contenedor = tk.Frame(frame_lista, bg="white", width=680, height=47)
    contenedor.grid(row=0, column=0, sticky="w", padx=30, pady=(20, 0))
    contenedor.grid_propagate(False)

    tk.Label(contenedor, text="HUÉSPEDES", font=("Aldrich", 24),
             fg="#434343", bg="white", anchor="w"
             ).place(x=0, y=0, width=433, height=47)

    boton_agregar = tk.Button(contenedor, text="Agregar Nuevo Huésped",
                              bg="#434343", fg="white", font=("Aldrich", 12),
                              relief=tk.FLAT, cursor="hand2")
    boton_agregar.place(x=453, y=0, width=227, height=47)

    # ----- Panel de búsqueda -----
    panel_busqueda = tk.Frame(frame_lista, bg="#EBEBEB",
                              width=680, height=82)
    panel_busqueda.grid(row=1, column=0, sticky="w", padx=30, pady=(15, 0))
    panel_busqueda.grid_propagate(False)

    tk.Label(panel_busqueda, text="Buscar Huéspedes",
             bg="#EBEBEB", fg="#434343",
             font=("Aldrich", 12)).place(x=41, y=10)

    campo_busqueda = tk.Entry(panel_busqueda, font=("Aldrich", 10),
                              bg="white", fg="gray", relief=tk.FLAT)
    campo_busqueda.place(x=41, y=42, width=280, height=23)
    campo_busqueda.insert(0, "Buscar por DNI o Apellido")

    # Estado del modo
    estado = {"modo": "activos"}

    def cambiar_modo():
        if estado["modo"] == "activos":
            estado["modo"] = "inactivos"
            boton_papelera.config(text="Ver activos", bg="#27ae60")
            mostrar_tabla(listar_huespedes_inactivos())
        else:
            estado["modo"] = "activos"
            boton_papelera.config(text="Ver dados de baja", bg="#555555")
            mostrar_tabla(listar_huespedes())

    boton_papelera = tk.Button(panel_busqueda, text="Ver dados de baja",
                                bg="#555555", fg="white", font=("Aldrich", 9),
                                relief=tk.FLAT, cursor="hand2",
                                command=cambiar_modo)
    boton_papelera.place(x=330, y=42, width=120, height=23)

    def buscar():
        criterio = campo_busqueda.get().strip()
        if criterio == "Buscar por DNI o Apellido" or not criterio:
            if estado["modo"] == "activos":
                mostrar_tabla(listar_huespedes())
            else:
                mostrar_tabla(listar_huespedes_inactivos())
            return
        mostrar_tabla(buscar_huespedes(criterio))

    tk.Button(panel_busqueda, text="Buscar",
              bg="#434343", fg="white", font=("Aldrich", 10),
              relief=tk.FLAT, cursor="hand2",
              command=buscar
              ).place(x=460, y=42, width=103, height=23)

    def limpiar_placeholder(event):
        if campo_busqueda.get() == "Buscar por DNI o Apellido":
            campo_busqueda.delete(0, tk.END)
            campo_busqueda.config(fg="#434343")

    campo_busqueda.bind("<FocusIn>", limpiar_placeholder)
    campo_busqueda.bind("<Return>", lambda e: buscar())

    # ----- Contenedor de la tabla con scroll -----
    contenedor_tabla = tk.Frame(frame_lista, bg="white",
                                width=680, height=300)
    contenedor_tabla.grid(row=2, column=0, sticky="nsew", padx=30, pady=(15, 20))
    contenedor_tabla.grid_propagate(False)

    encabezado = tk.Frame(contenedor_tabla, bg="#D9D9D9",
                          width=680, height=42)
    encabezado.pack(fill=tk.X)
    encabezado.pack_propagate(False)

    tk.Label(encabezado, text="DNI", bg="#D9D9D9", fg="#434343",
             font=("Aldrich", 10)).place(x=16, y=16)
    tk.Label(encabezado, text="Nombre", bg="#D9D9D9", fg="#434343",
             font=("Aldrich", 10)).place(x=112, y=16)
    tk.Label(encabezado, text="Apellido", bg="#D9D9D9", fg="#434343",
             font=("Aldrich", 10)).place(x=209, y=16)
    tk.Label(encabezado, text="Teléfono", bg="#D9D9D9", fg="#434343",
             font=("Aldrich", 10)).place(x=327, y=16)
    tk.Label(encabezado, text="Email", bg="#D9D9D9", fg="#434343",
             font=("Aldrich", 10)).place(x=432, y=16)
    tk.Label(encabezado, text="Acción", bg="#D9D9D9", fg="#434343",
             font=("Aldrich", 10)).place(x=590, y=16)

    frame_scroll = tk.Frame(contenedor_tabla, bg="white")
    frame_scroll.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(frame_scroll, bg="white", highlightthickness=0)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(frame_scroll, orient="vertical",
                             command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    area_filas = tk.Frame(canvas, bg="white", width=680, height=300)
    canvas.create_window((0, 0), window=area_filas, anchor="nw")

    def ajustar_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    area_filas.bind("<Configure>", ajustar_scroll)

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def activar_scroll(event):
        canvas.bind_all("<MouseWheel>", on_mousewheel)

    def desactivar_scroll(event):
        canvas.unbind_all("<MouseWheel>")

    canvas.bind("<Enter>", activar_scroll)
    canvas.bind("<Leave>", desactivar_scroll)

    def mostrar_tabla(lista):
        for widget in area_filas.winfo_children():
            widget.destroy()

        if not lista:
            texto = ("No hay huéspedes activos para mostrar."
                     if estado["modo"] == "activos"
                     else "No hay huéspedes dados de baja.")
            tk.Label(area_filas, text=texto,
                     bg="white", fg="gray",
                     font=("Aldrich", 12)).place(x=16, y=20)
            area_filas.configure(width=680, height=100)
        else:
            for i, h in enumerate(lista):
                y = i * 47
                if estado["modo"] == "activos":
                    dibujar_fila_huesped_activo(
                        area_filas, y, h, al_editar, al_eliminar
                    )
                else:
                    dibujar_fila_huesped_inactivo(
                        area_filas, y, h, al_restaurar, al_eliminar_definitivo
                    )
            area_filas.configure(width=680, height=len(lista) * 47 + 20)

        area_filas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    # ----- Acciones -----
    def al_editar(id_huesped):
        abrir_formulario(parent, frame_formulario, contenedor,
                         panel_busqueda, refrescar, id_huesped=id_huesped)

    def al_eliminar(id_huesped):
        if not messagebox.askyesno("Confirmar",
            "¿Está seguro de que desea dar de baja este huésped?"):
            return
        if eliminar_huesped(id_huesped):
            messagebox.showinfo("Éxito", "Huésped dado de baja correctamente.")
            mostrar_tabla(listar_huespedes())
        else:
            messagebox.showerror("Error", "No se pudo dar de baja el huésped.")

    def al_restaurar(id_huesped):
        if not messagebox.askyesno("Confirmar",
            "¿Desea restaurar este huésped? Volverá a estar activo."):
            return
        exito, mensaje = restaurar_huesped(id_huesped)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            mostrar_tabla(listar_huespedes_inactivos())
        else:
            messagebox.showerror("Error", mensaje)

    def al_eliminar_definitivo(id_huesped):
        if not messagebox.askyesno("Confirmar eliminación definitiva",
            "¿Está SEGURO? Esta acción NO se puede deshacer.\n"
            "El huésped se borrará permanentemente de la base."):
            return

        # Capa de seguridad: Solicitar contraseña de administrador
        password = simpledialog.askstring(
            "Seguridad", 
            "Ingrese la contraseña de administrador para continuar:", 
            show='*'
        )

        # Verificar la contraseña (puedes cambiar "Admin2026!" por la que prefieras)
        if password != "Admin2026!":
            messagebox.showerror("Acceso Denegado", "Contraseña incorrecta o cancelada. Operación abortada.")
            return

        # Si la contraseña es correcta, procede a eliminar
        exito, mensaje = eliminar_huesped_definitivo(id_huesped)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            mostrar_tabla(listar_huespedes_inactivos())
        else:
            messagebox.showerror("No se pudo eliminar", mensaje)

    # Conectar el botón agregar
    boton_agregar.configure(
        command=lambda: abrir_formulario(parent, frame_formulario,
                                         contenedor, panel_busqueda,
                                         refrescar)
    )

    # Cargar tabla inicial
    mostrar_tabla(listar_huespedes())