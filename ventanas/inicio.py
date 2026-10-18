"""Pantalla de inicio (dashboard) con indicadores reales de la base de datos."""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import date
from acceso_datos import (
    obtener_resumen_dashboard, listar_consultas_pendientes,
    listar_actividad_reciente, listar_habitaciones_ocupadas
)
from ventanas.auditoria import mostrar_auditoria, crear_area_scroll
from conexion import verificar_password_admin

DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
COLOR_TEXTO = "#434343"
COLOR_ALERTA = "#c0392b"
COLOR_HOY = "#E8EEF4"
SEGUNDOS_REFRESCO = 60  # el dashboard se recalcula solo cada minuto

# Vista del recuadro izquierdo ("semana" u "ocupadas"); se conserva al refrescar.
VISTA_IZQUIERDA = {"modo": "semana"}


def formato_plata(valor):
    """45000 -> $45.000"""
    return f"${valor:,.0f}".replace(",", ".")


def recortar(texto, largo):
    return texto if len(texto) <= largo else texto[:largo - 1] + "…"


def crear_caja(parent, ancho, alto, columna_izq=False, pady=(10, 10)):
    """Caja con borde, como las del diseño original."""
    caja = tk.Frame(parent, bg="white", width=ancho, height=alto,
                    relief=tk.SOLID, bd=2)
    caja.pack(side=tk.LEFT, padx=(30 if columna_izq else 10, 10), pady=pady)
    caja.pack_propagate(False)
    return caja


def contenido_inicio(parent):
    """Dibuja el dashboard dentro del parent."""

    for widget in parent.winfo_children():
        widget.destroy()

    raiz = tk.Frame(parent, bg="white")
    raiz.pack(fill=tk.BOTH, expand=True)

    # Recalcular automáticamente (por ejemplo al cambiar el día) y liberar el
    # temporizador cuando se sale de la pantalla.
    refresco = {"id": raiz.after(SEGUNDOS_REFRESCO * 1000,
                                 lambda: contenido_inicio(parent))}

    def cancelar_refresco(event):
        if event.widget is raiz and refresco["id"]:
            raiz.after_cancel(refresco["id"])

    raiz.bind("<Destroy>", cancelar_refresco)

    hoy = date.today()
    resumen = obtener_resumen_dashboard(hoy)

    if resumen is None:
        tk.Label(raiz, text="No se pudo obtener la información de la base de datos.",
                 bg="white", fg=COLOR_ALERTA, font=("Aldrich", 12)
                 ).pack(pady=(60, 10))
        tk.Button(raiz, text="Reintentar", bg="#434343", fg="white",
                  font=("Aldrich", 10), relief=tk.FLAT, cursor="hand2",
                  command=lambda: contenido_inicio(parent)).pack()
        return

    consultas = listar_consultas_pendientes(4)
    actividad = listar_actividad_reciente(5)

    # ========================================================
    # FILA 1: indicadores principales
    # ========================================================
    fila1 = tk.Frame(raiz, bg="white", height=150)
    fila1.pack(side=tk.TOP, fill=tk.X)
    fila1.pack_propagate(False)

    operativas = resumen['hab_operativas']
    ocupadas = resumen['hab_ocupadas']
    porcentaje = round(ocupadas * 100 / operativas) if operativas else 0

    tarjetas = [
        ("Ocupación hoy:", f"{porcentaje}%",
         f"{ocupadas} de {operativas} hab.", COLOR_TEXTO),
        ("Check-Ins Hoy:", str(resumen['checkins_hoy']),
         "llegadas previstas", COLOR_TEXTO),
        ("Check-Outs Hoy:", str(resumen['checkouts_hoy']),
         "salidas previstas", COLOR_TEXTO),
        ("Consultas sin responder:", str(resumen['consultas_pendientes']),
         "requieren atención" if resumen['consultas_pendientes'] else "todo al día",
         COLOR_ALERTA if resumen['consultas_pendientes'] else COLOR_TEXTO),
    ]
    for i, (titulo, valor, detalle, color) in enumerate(tarjetas):
        caja = crear_caja(fila1, 160, 120, columna_izq=(i == 0), pady=(30, 0))
        tk.Label(caja, text=titulo, bg="white", fg=COLOR_TEXTO,
                 font=("Aldrich", 10), wraplength=140, justify=tk.CENTER
                 ).pack(pady=(14, 2))
        tk.Label(caja, text=valor, bg="white", fg=color,
                 font=("Aldrich", 18, "bold")).pack()
        tk.Label(caja, text=detalle, bg="white", fg="#888888",
                 font=("Aldrich", 8)).pack(pady=(2, 0))

    # ========================================================
    # FILA 2: resumen semanal y reservas / cobros
    # ========================================================
    fila2 = tk.Frame(raiz, bg="white", height=270)
    fila2.pack(side=tk.TOP, fill=tk.X)
    fila2.pack_propagate(False)

    caja_semana = crear_caja(fila2, 340, 250, columna_izq=True)

    encabezado_semana = tk.Frame(caja_semana, bg="white", height=44)
    encabezado_semana.pack(fill=tk.X)
    encabezado_semana.pack_propagate(False)
    titulo_semana = tk.Label(encabezado_semana, text="", bg="white", fg=COLOR_TEXTO,
                             font=("Aldrich", 12, "bold"), anchor="w")
    titulo_semana.place(x=16, y=8)
    subtitulo_semana = tk.Label(encabezado_semana, text="", bg="white", fg="#888888",
                                font=("Aldrich", 8), anchor="w")
    subtitulo_semana.place(x=16, y=28)
    boton_vista = tk.Button(encabezado_semana, text="", bg="#434343", fg="white",
                            font=("Aldrich", 8), relief=tk.FLAT, cursor="hand2")
    boton_vista.place(relx=1, x=-8, y=8, anchor="ne", width=92, height=22)

    cuerpo_semana = tk.Frame(caja_semana, bg="white")
    cuerpo_semana.pack(fill=tk.BOTH, expand=True)

    def dibujar_semana():
        for w in cuerpo_semana.winfo_children():
            w.destroy()
        titulo_semana.config(text="Resumen Semanal")
        subtitulo_semana.config(text="Check-ins por día")
        boton_vista.config(text="⇄ Ocupadas", command=lambda: cambiar_vista("ocupadas"))
        for dia, cantidad in resumen['checkins_semana']:
            es_hoy = dia == hoy
            fondo = COLOR_HOY if es_hoy else "white"
            fuente = ("Aldrich", 10, "bold") if es_hoy else ("Aldrich", 10)
            fila = tk.Frame(cuerpo_semana, bg=fondo)
            fila.pack(fill=tk.X, padx=40, pady=1)
            tk.Label(fila, text=f"{DIAS[dia.weekday()]} {dia.strftime('%d/%m')}:",
                     bg=fondo, fg=COLOR_TEXTO, font=fuente).pack(side=tk.LEFT)
            tk.Label(fila, text=str(cantidad), bg=fondo, fg=COLOR_TEXTO,
                     font=("Aldrich", 10, "bold")).pack(side=tk.RIGHT)

    def dibujar_ocupadas():
        for w in cuerpo_semana.winfo_children():
            w.destroy()
        titulo_semana.config(text="Habitaciones ocupadas")
        subtitulo_semana.config(text="Titular, check-out y saldo a abonar")
        boton_vista.config(text="⇄ Semana", command=lambda: cambiar_vista("semana"))

        ocupadas_hoy = listar_habitaciones_ocupadas(hoy)
        if ocupadas_hoy is None:
            tk.Label(cuerpo_semana, text="No se pudo obtener la información.",
                     bg="white", fg=COLOR_ALERTA, font=("Aldrich", 9)).pack(pady=30)
            return
        if not ocupadas_hoy:
            tk.Label(cuerpo_semana, text="No hay habitaciones ocupadas hoy.",
                     bg="white", fg="gray", font=("Aldrich", 10)).pack(pady=30)
            return

        contenedor, lista = crear_area_scroll(cuerpo_semana, 300, 190)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=(10, 6), pady=(0, 6))
        for i, o in enumerate(ocupadas_hoy):
            alto = 46
            fila = tk.Frame(lista, bg="white", width=300, height=alto)
            fila.place(x=0, y=i * alto)
            if o['id_reserva'] is None:
                tk.Label(fila, text=f"Hab. #{o['id_habitacion']} · Sin reserva asociada",
                         bg="white", fg=COLOR_TEXTO, font=("Aldrich", 9, "bold"),
                         anchor="w").place(x=4, y=5)
                tk.Label(fila, text="Marcada como ocupada manualmente", bg="white",
                         fg="#888888", font=("Aldrich", 8), anchor="w"
                         ).place(x=4, y=24)
            else:
                titular = recortar(f"{o['nombre']} {o['apellido']}", 17) if o['nombre'] else "Sin titular"
                tk.Label(fila, text=f"Hab. #{o['id_habitacion']} · {titular}",
                         bg="white", fg=COLOR_TEXTO, font=("Aldrich", 9, "bold"),
                         anchor="w").place(x=4, y=5)
                es_hoy_salida = o['fecha_salida'] == hoy
                salida = (f"Check-out: {'HOY' if es_hoy_salida else DIAS[o['fecha_salida'].weekday()][:3] + ' ' + o['fecha_salida'].strftime('%d/%m')}")
                tk.Label(fila, text=salida, bg="white",
                         fg=COLOR_ALERTA if es_hoy_salida else "#666666",
                         font=("Aldrich", 8, "bold" if es_hoy_salida else "normal"),
                         anchor="e").place(x=150, y=7, width=146)
                saldo_o = o['saldo_pendiente'] or 0
                if saldo_o > 0:
                    texto_saldo, color_saldo = f"Debe abonar: {formato_plata(saldo_o)}", COLOR_ALERTA
                else:
                    texto_saldo, color_saldo = "Cuenta saldada", "#1e6b34"
                tk.Label(fila, text=f"Reserva #{o['id_reserva']} · {texto_saldo}",
                         bg="white", fg=color_saldo, font=("Aldrich", 8), anchor="w"
                         ).place(x=4, y=25)
            tk.Frame(lista, bg="#E0E0E0", height=1, width=300
                     ).place(x=0, y=i * alto + alto - 1)
        lista.configure(height=len(ocupadas_hoy) * 46 + 4)

    def cambiar_vista(modo):
        VISTA_IZQUIERDA["modo"] = modo
        if modo == "ocupadas":
            dibujar_ocupadas()
        else:
            dibujar_semana()

    cambiar_vista(VISTA_IZQUIERDA["modo"])

    def pedir_acceso_auditoria():
        """Capa 1 de seguridad: contraseña de administrador en la interfaz."""
        password = simpledialog.askstring(
            "Seguridad",
            "Ingrese la contraseña de administrador para acceder a la auditoría:",
            show='*')
        if password is None:  # el usuario canceló
            return
        if not verificar_password_admin(password):
            messagebox.showerror("Acceso Denegado",
                                 "Contraseña incorrecta. No se abrió la auditoría.")
            return
        mostrar_auditoria(parent, lambda: contenido_inicio(parent))

    caja_reservas = crear_caja(fila2, 340, 250)
    tk.Label(caja_reservas, text="Reservas y Cobros", bg="white", fg=COLOR_TEXTO,
             font=("Aldrich", 12, "bold")).pack(pady=(12, 2))
    tk.Button(caja_reservas, text="Auditoría de acceso del titular", bg="#434343",
              fg="white", font=("Aldrich", 9), relief=tk.FLAT, cursor="hand2",
              command=pedir_acceso_auditoria
              ).pack(side=tk.BOTTOM, pady=(0, 12), ipadx=10, ipady=2)
    saldo = resumen['saldo_pendiente']
    renglones = [
        ("Pendientes de confirmar:", str(resumen['reservas_pendientes']), COLOR_TEXTO),
        ("Confirmadas vigentes:", str(resumen['reservas_confirmadas']), COLOR_TEXTO),
        ("Cobrado este mes:", formato_plata(resumen['cobrado_mes']), COLOR_TEXTO),
        ("Saldo pendiente de cobro:", formato_plata(saldo),
         COLOR_ALERTA if saldo > 0 else COLOR_TEXTO),
    ]
    for etiqueta, valor, color in renglones:
        fila = tk.Frame(caja_reservas, bg="white")
        fila.pack(fill=tk.X, padx=25, pady=(6, 3))
        tk.Label(fila, text=etiqueta, bg="white", fg=COLOR_TEXTO,
                 font=("Aldrich", 10, "bold")).pack(side=tk.LEFT)
        tk.Label(fila, text=valor, bg="white", fg=color,
                 font=("Aldrich", 13, "bold")).pack(side=tk.RIGHT)
        tk.Frame(caja_reservas, bg="#D9D9D9", height=2).pack(fill=tk.X, padx=25)

    # ========================================================
    # FILA 3: consultas sin responder y actividad reciente
    # ========================================================
    fila3 = tk.Frame(raiz, bg="white", height=270)
    fila3.pack(side=tk.TOP, fill=tk.X)
    fila3.pack_propagate(False)

    caja_consultas = crear_caja(fila3, 340, 250, columna_izq=True)
    tk.Label(caja_consultas, text="Consultas sin responder", bg="white",
             fg=COLOR_TEXTO, font=("Aldrich", 12, "bold")).pack(pady=(10, 8))

    if not consultas:
        tk.Label(caja_consultas, text="No hay consultas pendientes.", bg="white",
                 fg="gray", font=("Aldrich", 10)).pack(pady=20)
    else:
        for c in consultas:
            item = tk.Frame(caja_consultas, bg="white")
            item.pack(fill=tk.X, padx=15, pady=(3, 0))
            linea1 = tk.Frame(item, bg="white")
            linea1.pack(fill=tk.X)
            tk.Label(linea1, text=f"{recortar(c['remitente'], 20)} · {c['medio']}",
                     bg="white", fg=COLOR_TEXTO, font=("Aldrich", 9, "bold")
                     ).pack(side=tk.LEFT)
            tk.Label(linea1, text=c['fecha'].strftime("%d/%m/%Y"), bg="white",
                     fg="#888888", font=("Aldrich", 8)).pack(side=tk.RIGHT)
            tk.Label(item, text=recortar(c['asunto'], 48), bg="white", fg="#666666",
                     font=("Aldrich", 8), anchor="w").pack(fill=tk.X)
            tk.Frame(caja_consultas, bg="#E0E0E0", height=1).pack(fill=tk.X, padx=10,
                                                                   pady=(3, 0))
        restantes = resumen['consultas_pendientes'] - len(consultas)
        if restantes > 0:
            tk.Label(caja_consultas, text=f"+ {restantes} más en la pantalla Consultas",
                     bg="white", fg="#888888", font=("Aldrich", 8)
                     ).pack(pady=(6, 0))

    caja_actividad = crear_caja(fila3, 340, 250)
    tk.Label(caja_actividad, text="Actividad Reciente", bg="white",
             fg=COLOR_TEXTO, font=("Aldrich", 12, "bold")).pack(pady=(10, 8))

    encabezado = tk.Frame(caja_actividad, bg="#D9D9D9", height=25)
    encabezado.pack(fill=tk.X)
    tk.Label(encabezado, text="Reserva reciente", bg="#D9D9D9",
             font=("Aldrich", 9)).pack(side=tk.LEFT, padx=15)
    tk.Label(encabezado, text="Hab. #", bg="#D9D9D9",
             font=("Aldrich", 9)).pack(side=tk.RIGHT, padx=15)

    if not actividad:
        tk.Label(caja_actividad, text="Todavía no hay reservas.", bg="white",
                 fg="gray", font=("Aldrich", 10)).pack(pady=20)
    for a in actividad:
        titular = (recortar(f"{a['nombre']} {a['apellido']}", 18)
                   if a['nombre'] else "Sin titular")
        fila = tk.Frame(caja_actividad, bg="white")
        fila.pack(fill=tk.X, pady=4)
        tk.Label(fila, text=f"#{a['id_reserva']} · {titular} · "
                            f"{a['estado_reserva'].capitalize()}",
                 bg="white", fg=COLOR_TEXTO, font=("Aldrich", 9)
                 ).pack(side=tk.LEFT, padx=15)
        tk.Label(fila, text=f"#{a['habitaciones']}" if a['habitaciones'] else "-",
                 bg="white", fg=COLOR_TEXTO, font=("Aldrich", 9, "bold")
                 ).pack(side=tk.RIGHT, padx=15)
        tk.Frame(caja_actividad, bg="#E0E0E0", height=1).pack(fill=tk.X, padx=10)