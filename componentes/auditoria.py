"""Auditoría de acceso del titular: historial contable de movimientos (60 días)."""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import messagebox
from datetime import date, datetime, timedelta
from acceso_datos import obtener_auditoria_titulares

DIAS_AUDITORIA = 60
COLOR_TEXTO = "#434343"
COLOR_ENCABEZADO = "#434343"
COLOR_ZEBRA = "#F5F5F5"
COLOR_DEBE = "#9c2b20"
COLOR_HABER = "#1e6b34"
FUENTE_NUMEROS = ("Consolas", 9)
ANCHO = 700
FEMENINO = {"confirmado": "confirmada", "pendiente": "pendiente", "cancelado": "cancelada"}

# Posiciones (x, ancho) de cada columna dentro del ancho de 700 px
COL_FECHA = (8, 72)
COL_RESERVA = (84, 44)
COL_TITULAR = (132, 134)
COL_MOVIMIENTO = (270, 202)
COL_USUARIO = (476, 66)
COL_DEBE = (546, 72)
COL_HABER = (622, 72)


# ============================================================
# UTILIDADES
# ============================================================
def formato_importe(valor):
    """Importe contable: 1186900 -> 1.186.900,00 (vacío si no hay importe)."""
    if valor is None:
        return ""
    texto = f"{valor:,.2f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def recortar(texto, largo):
    texto = texto or ""
    return texto if len(texto) <= largo else texto[:largo - 1] + "…"


def crear_area_scroll(parent, ancho, alto=None):
    """
    Crea un área con barra y rueda del mouse. Devuelve (contenedor, interior):
    se empaqueta/ubica el contenedor y se dibuja dentro del interior.
    """
    contenedor = tk.Frame(parent, bg="white")
    canvas = tk.Canvas(contenedor, bg="white", highlightthickness=0, width=ancho)
    if alto:
        canvas.configure(height=alto)
    barra = tk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=barra.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    barra.pack(side=tk.RIGHT, fill=tk.Y)

    interior = tk.Frame(canvas, bg="white", width=ancho)
    canvas.create_window((0, 0), window=interior, anchor="nw", width=ancho)
    interior.bind("<Configure>",
                  lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def rueda(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", rueda))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
    interior.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", rueda))
    return contenedor, interior


# ============================================================
# ARMADO CONTABLE DE LOS ASIENTOS
# ============================================================
def armar_asiento(fila):
    """
    Convierte una fila de la base en un asiento: movimiento, detalle, debe, haber.
    Debe  = cargos al titular (estadía, consumos) y reembolsos entregados.
    Haber = pagos aprobados recibidos.
    """
    tipo = fila['tipo']
    estado = (fila['estado_reserva'] or '').lower()
    ingreso = fila['f_ingreso'].strftime("%d/%m/%Y")
    salida = fila['f_salida'].strftime("%d/%m/%Y")
    debe = haber = None

    if tipo == 'reserva':
        movimiento = "Reserva registrada"
        detalle = f"Estadía {ingreso} al {salida}"
        if estado == 'cancelado':
            detalle += " (cancelada, sin cargo)"
        else:
            debe = fila['monto']
    elif tipo == 'modificacion':
        movimiento = "Reserva modificada"
        detalle = f"Estado actual: {estado.capitalize()}"
    elif tipo == 'checkin':
        movimiento = "Ingreso (check-in)"
        detalle = f"Reserva {FEMENINO.get(estado, estado)}"
    elif tipo == 'checkout':
        movimiento = "Egreso (check-out)"
        detalle = f"Reserva {FEMENINO.get(estado, estado)}"
    elif tipo == 'pago':
        metodo = fila['texto1']
        estado_pago = (fila['texto2'] or '').lower()
        if estado_pago == 'aprobado':
            movimiento, detalle, haber = "Pago recibido", f"{metodo} · aprobado", fila['monto']
        elif estado_pago == 'reembolsado':
            movimiento, detalle, debe = "Reembolso", f"{metodo} · devolución", fila['monto']
        else:
            movimiento = "Pago " + estado_pago
            detalle = f"{metodo} · sin imputar (${formato_importe(fila['monto'])})"
    else:  # consumo
        movimiento = "Consumo"
        detalle = f"{fila['texto1']} x{fila['texto2']}"
        debe = fila['monto']

    if fila['u_nombre']:
        usuario = f"{fila['u_nombre']} {fila['u_apellido']}"
    else:
        usuario = "Sistema"
    titular = (f"{fila['nombre']} {fila['apellido']}" if fila['nombre']
               else "Sin titular")

    return {
        'fecha': fila['fecha'],
        'id_reserva': fila['id_reserva'],
        'titular': titular,
        'dni': fila['dni'] or "-",
        'movimiento': movimiento,
        'detalle': detalle,
        'usuario': usuario,
        'debe': debe,
        'haber': haber,
    }


def totalizar(asientos):
    """Devuelve (total_debe, total_haber, saldo = debe - haber)."""
    total_debe = sum((a['debe'] or 0) for a in asientos)
    total_haber = sum((a['haber'] or 0) for a in asientos)
    return total_debe, total_haber, total_debe - total_haber


# ============================================================
# PANTALLA
# ============================================================
def mostrar_auditoria(parent, al_volver):
    """Reemplaza el contenido de `parent` por la auditoría a pantalla completa."""

    for widget in parent.winfo_children():
        widget.destroy()

    hoy = date.today()
    desde = hoy - timedelta(days=DIAS_AUDITORIA)
    filas = obtener_auditoria_titulares(hoy, DIAS_AUDITORIA)

    raiz = tk.Frame(parent, bg="white")
    raiz.pack(fill=tk.BOTH, expand=True, padx=20, pady=(12, 10))

    # ----- Encabezado del documento -----
    cabecera = tk.Frame(raiz, bg="white")
    cabecera.pack(fill=tk.X)
    tk.Label(cabecera, text="AUDITORÍA DE ACCESO DEL TITULAR", bg="white",
             fg=COLOR_TEXTO, font=("Aldrich", 16, "bold")).pack(side=tk.LEFT)

    def imprimir():
        messagebox.showinfo(
            "Imprimir", "La impresión de la auditoría estará disponible próximamente.")

    tk.Button(cabecera, text="← Volver", bg="#999999", fg="white",
              font=("Aldrich", 9), relief=tk.FLAT, cursor="hand2",
              command=al_volver).pack(side=tk.RIGHT)
    tk.Button(cabecera, text="Imprimir", bg=COLOR_ENCABEZADO, fg="white",
              font=("Aldrich", 9), relief=tk.FLAT, cursor="hand2",
              command=imprimir).pack(side=tk.RIGHT, padx=(0, 8))

    asientos = [armar_asiento(f) for f in filas] if filas is not None else []

    ahora = datetime.now()
    tk.Label(raiz,
             text=(f"Período auditado: {desde.strftime('%d/%m/%Y')} al "
                   f"{hoy.strftime('%d/%m/%Y')} ({DIAS_AUDITORIA} días)   |   "
                   f"Emitido: {ahora.strftime('%d/%m/%Y %H:%M')}   |   "
                   f"Movimientos: {len(asientos)}"),
             bg="white", fg="#666666", font=("Aldrich", 8), anchor="w"
             ).pack(fill=tk.X, pady=(2, 6))
    tk.Frame(raiz, bg=COLOR_ENCABEZADO, height=2).pack(fill=tk.X)

    if filas is None:
        tk.Label(raiz, text="No se pudo obtener la auditoría de la base de datos.",
                 bg="white", fg="#c0392b", font=("Aldrich", 11)).pack(pady=40)
        return

    # ----- Encabezado de columnas -----
    columnas = tk.Frame(raiz, bg=COLOR_ENCABEZADO, height=26, width=ANCHO)
    columnas.pack(anchor="w", pady=(6, 0))
    columnas.pack_propagate(False)
    encabezados = [("FECHA", COL_FECHA, "w"), ("RESERVA", COL_RESERVA, "w"),
                   ("TITULAR / DNI", COL_TITULAR, "w"),
                   ("MOVIMIENTO / DETALLE", COL_MOVIMIENTO, "w"),
                   ("USUARIO", COL_USUARIO, "w"),
                   ("DEBE ($)", COL_DEBE, "e"), ("HABER ($)", COL_HABER, "e")]
    for texto, (x, ancho), ancla in encabezados:
        tk.Label(columnas, text=texto, bg=COLOR_ENCABEZADO, fg="white",
                 font=("Aldrich", 8, "bold"), anchor=ancla
                 ).place(x=x, y=4, width=ancho, height=18)

    # ----- Totales (fijos abajo, siempre visibles) -----
    total_debe, total_haber, saldo = totalizar(asientos)
    pie = tk.Frame(raiz, bg="white", width=ANCHO, height=70)
    pie.pack(side=tk.BOTTOM, anchor="w", pady=(4, 0))
    pie.pack_propagate(False)
    tk.Frame(pie, bg=COLOR_ENCABEZADO, height=2).place(x=0, y=0, width=ANCHO)
    tk.Label(pie, text="TOTALES DEL PERÍODO", bg="white", fg=COLOR_TEXTO,
             font=("Aldrich", 9, "bold"), anchor="w").place(x=8, y=8, width=300)
    tk.Label(pie, text=formato_importe(total_debe), bg="white", fg=COLOR_DEBE,
             font=("Consolas", 10, "bold"), anchor="e"
             ).place(x=COL_DEBE[0], y=7, width=COL_DEBE[1])
    tk.Label(pie, text=formato_importe(total_haber), bg="white", fg=COLOR_HABER,
             font=("Consolas", 10, "bold"), anchor="e"
             ).place(x=COL_HABER[0], y=7, width=COL_HABER[1])
    tk.Frame(pie, bg="#999999", height=1).place(x=COL_DEBE[0], y=30,
                                                width=COL_HABER[0] + COL_HABER[1] - COL_DEBE[0])
    tk.Label(pie, text="SALDO NETO (Debe − Haber)", bg="white", fg=COLOR_TEXTO,
             font=("Aldrich", 9, "bold"), anchor="w").place(x=8, y=38, width=300)
    tk.Label(pie, text=formato_importe(saldo), bg="white",
             fg=COLOR_DEBE if saldo > 0 else COLOR_HABER,
             font=("Consolas", 11, "bold"), anchor="e"
             ).place(x=COL_HABER[0] - 40, y=36, width=COL_HABER[1] + 40)
    tk.Frame(pie, bg="#999999", height=1).place(x=COL_DEBE[0], y=58,
                                                width=COL_HABER[0] + COL_HABER[1] - COL_DEBE[0])
    tk.Frame(pie, bg="#999999", height=1).place(x=COL_DEBE[0], y=60,
                                                width=COL_HABER[0] + COL_HABER[1] - COL_DEBE[0])

    # ----- Historial con rueda del mouse -----
    contenedor, interior = crear_area_scroll(raiz, ANCHO)
    contenedor.pack(fill=tk.BOTH, expand=True, anchor="w")

    ALTO_FILA = 38
    if not asientos:
        tk.Label(interior, text="No hay movimientos en los últimos 60 días.",
                 bg="white", fg="gray", font=("Aldrich", 11)
                 ).place(x=20, y=30)
        interior.configure(height=100)

    for i, a in enumerate(asientos):
        y = i * ALTO_FILA
        fondo = COLOR_ZEBRA if i % 2 else "white"
        fila = tk.Frame(interior, bg=fondo, width=ANCHO, height=ALTO_FILA)
        fila.place(x=0, y=y)

        def texto(contenido, columna, y_rel, fuente, color=COLOR_TEXTO, ancla="w"):
            tk.Label(fila, text=contenido, bg=fondo, fg=color, font=fuente,
                     anchor=ancla).place(x=columna[0], y=y_rel, width=columna[1])

        texto(a['fecha'].strftime("%d/%m/%Y"), COL_FECHA, 10, ("Aldrich", 9))
        texto(f"#{a['id_reserva']}", COL_RESERVA, 10, ("Aldrich", 9, "bold"))
        texto(recortar(a['titular'], 19), COL_TITULAR, 4, ("Aldrich", 9, "bold"))
        texto(f"DNI {a['dni']}", COL_TITULAR, 20, ("Aldrich", 8), "#888888")
        texto(a['movimiento'], COL_MOVIMIENTO, 4, ("Aldrich", 9, "bold"))
        texto(recortar(a['detalle'], 36), COL_MOVIMIENTO, 20, ("Aldrich", 8), "#666666")
        texto(recortar(a['usuario'], 11), COL_USUARIO, 10, ("Aldrich", 8))
        texto(formato_importe(a['debe']), COL_DEBE, 10, FUENTE_NUMEROS, COLOR_DEBE, "e")
        texto(formato_importe(a['haber']), COL_HABER, 10, FUENTE_NUMEROS, COLOR_HABER, "e")
        tk.Frame(interior, bg="#D9D9D9", height=1, width=ANCHO
                 ).place(x=0, y=y + ALTO_FILA - 1)

    y_final = max(len(asientos), 1) * ALTO_FILA

    # Cierre del documento: leyenda y firmas
    leyenda = ("Debe: cargos al titular (estadías, consumos) y reembolsos. "
               "Haber: pagos aprobados recibidos. Los pagos pendientes o rechazados "
               "no se imputan.")
    tk.Label(interior, text=leyenda, bg="white", fg="#888888", font=("Aldrich", 8),
             wraplength=ANCHO - 20, justify=tk.LEFT, anchor="w"
             ).place(x=8, y=y_final + 14, width=ANCHO - 16)
    for x, rotulo in [(40, "Responsable de auditoría"), (400, "Gerencia")]:
        tk.Frame(interior, bg=COLOR_TEXTO, height=1).place(x=x, y=y_final + 100, width=240)
        tk.Label(interior, text=rotulo, bg="white", fg=COLOR_TEXTO,
                 font=("Aldrich", 8)).place(x=x, y=y_final + 104)
    interior.configure(height=y_final + 140)
