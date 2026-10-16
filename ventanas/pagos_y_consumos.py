#Pantalla de Pagos y Consumos

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

# ---------------------------------------------------------------- estilo
# Mismo estilo que el resto de la aplicación: fuente Aldrich, cuadros blancos con
# borde negro (como las cajas del dashboard) y botones gris oscuro.
COLOR_TITULO = "#434343"       # título de la pantalla
COLOR_TEXTO = "black"          # texto dentro de los cuadros
COLOR_FONDO = "white"
COLOR_ENCABEZADO = "#D9D9D9"   # encabezados de tabla
COLOR_SELECCION = "#EBEBEB"
COLOR_BOTON = "#434343"
COLOR_BOTON_ACTIVO = "#5A5A5A"
COLOR_PLACEHOLDER = "#9A9A9A"
COLOR_OK = "#3CA433"           # verde de la pantalla de Consultas
COLOR_ALERTA = "#C0392B"

FUENTE_TITULO = ("Aldrich", 24)
FUENTE_SUBTITULO = ("Aldrich", 12, "bold")
FUENTE_TEXTO = ("Aldrich", 10)
FUENTE_TEXTO_BOLD = ("Aldrich", 10, "bold")
FUENTE_ENCABEZADO = ("Aldrich", 9)

# Opciones que comparten los cuadros, botones y campos de texto
ESTILO_CAJA = dict(bg=COLOR_FONDO, relief=tk.SOLID, bd=2)   # cuadro con borde negro
ESTILO_BOTON = dict(bg=COLOR_BOTON, fg="white", font=FUENTE_TEXTO, relief=tk.FLAT, bd=0,
                    cursor="hand2", activebackground=COLOR_BOTON_ACTIVO, activeforeground="white")
ESTILO_ENTRADA = dict(font=FUENTE_TEXTO, bg=COLOR_BOTON, insertbackground="white", relief=tk.FLAT)

PLACEHOLDER_BUSQUEDA = "# De confirmación o DNI"

def buscar_reserva_mock(criterio):
    """Simula la búsqueda de una reserva por N° de confirmación o por DNI"""
    return{
        "confirmacion":"12345",
        "huesped":"Lautaro Valdez",
        "habitacion":"15 (Suite)",
        "check_in":"07/10/2026",
        "check_out":"07/11/2026",
        "total_estadia":250250,
        "pagos":[
            {"fecha": "3/11/2026", "metodo": "Transferencia", "monto": 104000},
            {"fecha": "24/10/2026", "metodo": "Transferencia", "monto": 24000},
            {"fecha": "15/10/2026", "metodo": "Transferencia", "monto": 2456},
            {"fecha": "14/10/2026", "metodo": "Efectivo", "monto": 75000},
        ],
        "consumos": [
            {"concepto": "Cochera", "cantidad": 3, "precio_unitario": 10000},
            {"concepto": "Frigobar", "cantidad": 2, "precio_unitario": 5000},
            {"concepto": "Lavandería", "cantidad": 1, "precio_unitario": 15000},
        ]

    }


def formato_moneda(monto):
    return f"${monto:,.0f}".replace(",", ".")


#Clase principal de la pantalla

class PantallaPagosConsumos:
    def __init__(self,contenedor):
        self.contenedor = contenedor
        self.reserva = None

        self._configurar_estilo_tablas()

        self.frame = tk.Frame(contenedor, bg=COLOR_FONDO)
        self.frame.pack(anchor="w", fill=tk.X, padx=(30, 40), pady=(20, 0))

        self._crear_titulo()
        self._crear_buscador()
        self._crear_detalle_reserva()
        self._crear_pagos_y_consumos()
        self._crear_resumen()

        self._cargar_reserva(buscar_reserva_mock(""))

        #Interfaz de Usuario

    def _configurar_estilo_tablas(self):
        """Da a las tablas (ttk.Treeview) el mismo aspecto que las del resto de la app."""
        estilo = ttk.Style()
        estilo.theme_use("clam")   # este tema permite cambiar los colores del encabezado
        estilo.configure("Hotel.Treeview", background=COLOR_FONDO, fieldbackground=COLOR_FONDO,
                         foreground=COLOR_TEXTO, font=FUENTE_TEXTO, rowheight=26, borderwidth=0)
        estilo.configure("Hotel.Treeview.Heading", background=COLOR_ENCABEZADO, foreground=COLOR_TEXTO,
                         font=FUENTE_ENCABEZADO, relief="flat", borderwidth=0, padding=(0, 5))
        estilo.map("Hotel.Treeview", background=[("selected", COLOR_SELECCION)],
                   foreground=[("selected", COLOR_TEXTO)])
        estilo.map("Hotel.Treeview.Heading", background=[("active", COLOR_ENCABEZADO)])
        estilo.layout("Hotel.Treeview", [("Treeview.treearea", {"sticky": "nswe"})])  # sin borde

    def _crear_titulo(self):
        tk.Label(
            self.frame, text="ESTADO DE CUENTA",
            font=FUENTE_TITULO, bg=COLOR_FONDO, fg=COLOR_TITULO, anchor="w"
        ).pack(anchor="w")

    def _crear_buscador(self):
        caja = tk.Frame(self.frame, **ESTILO_CAJA)
        caja.pack(fill=tk.X, pady=(12, 0))

        tk.Label(caja, text="Buscar Reserva", font=FUENTE_SUBTITULO, bg=COLOR_FONDO,
                 fg=COLOR_TEXTO).pack(anchor="w", padx=20, pady=(10, 4))

        fila = tk.Frame(caja, bg=COLOR_FONDO)
        fila.pack(fill=tk.X, padx=20, pady=(0, 12))

        self.entry_busqueda = tk.Entry(fila, fg=COLOR_PLACEHOLDER, **ESTILO_ENTRADA)
        self.entry_busqueda.insert(0, PLACEHOLDER_BUSQUEDA)
        self.entry_busqueda.bind("<FocusIn>", self._limpiar_placeholder)
        self.entry_busqueda.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)

        tk.Button(fila, text="Buscar", command=self._on_buscar, padx=25,
                  **ESTILO_BOTON).pack(side=tk.LEFT, padx=(20, 0))


    def _limpiar_placeholder(self, event):
        if self.entry_busqueda.get() == PLACEHOLDER_BUSQUEDA:
            self.entry_busqueda.delete(0, tk.END)
            self.entry_busqueda.config(fg="white")


    def _crear_detalle_reserva(self):
        caja = tk.Frame(self.frame, **ESTILO_CAJA)
        caja.pack(fill=tk.X, pady=(12, 0))

        self.lbl_detalle_titulo = tk.Label(
            caja, text="DETALLE DE LA RESERVA",
            font=FUENTE_SUBTITULO, bg=COLOR_FONDO, fg=COLOR_TEXTO
        )
        self.lbl_detalle_titulo.pack(anchor="w", padx=20, pady=(10, 8))

        # Una sola fila de datos: encabezado gris + fila blanca
        tabla = tk.Frame(caja, bg=COLOR_FONDO)
        tabla.pack(fill=tk.X, pady=(0, 8))

        encabezados = ["Confirmación", "Nombre Huésped", "Hab. #", "Fecha Check-In", "Fecha Check-Out"]
        self.vars_detalle = []
        for i, titulo in enumerate(encabezados):
            tabla.columnconfigure(i, weight=1, uniform="detalle")
            tk.Label(tabla, text=titulo, font=FUENTE_ENCABEZADO, bg=COLOR_ENCABEZADO, fg=COLOR_TEXTO,
                     anchor="w", padx=10, pady=4).grid(row=0, column=i, sticky="ew")
            var = tk.StringVar(value="—")
            tk.Label(tabla, textvariable=var, font=FUENTE_TEXTO, bg=COLOR_FONDO, fg=COLOR_TEXTO,
                     anchor="w", padx=10, pady=6).grid(row=1, column=i, sticky="ew")
            self.vars_detalle.append(var)

    def _crear_caja_tabla(self, parent, columna, titulo, columnas, texto_boton, comando):
        """Arma un cuadro con título, tabla, total y botón. Se usa para Pagos y para Consumos."""
        caja = tk.Frame(parent, **ESTILO_CAJA)
        caja.grid(row=0, column=columna, sticky="nsew",
                  padx=(0, 6) if columna == 0 else (6, 0))

        tk.Label(caja, text=titulo, font=FUENTE_SUBTITULO, bg=COLOR_FONDO,
                 fg=COLOR_TEXTO).pack(pady=(10, 8))

        tabla = ttk.Treeview(caja, columns=[c[0] for c in columnas], show="headings",
                             height=4, style="Hotel.Treeview")
        for col, encabezado, ancho in columnas:
            tabla.heading(col, text=encabezado)
            tabla.column(col, width=ancho, anchor="center")
        tabla.pack(fill=tk.X, padx=10)

        lbl_total = tk.Label(caja, text="Total Pagado: $0", font=FUENTE_TEXTO_BOLD,
                             bg=COLOR_FONDO, fg=COLOR_TEXTO)
        lbl_total.pack(anchor="e", padx=12, pady=(6, 4))

        tk.Button(caja, text=texto_boton, command=comando, padx=15,
                  **ESTILO_BOTON).pack(pady=(0, 10))
        return tabla, lbl_total

    def _crear_pagos_y_consumos(self):
        fila = tk.Frame(self.frame, bg=COLOR_FONDO)
        fila.pack(fill=tk.X, pady=(12, 0))
        fila.columnconfigure(0, weight=1, uniform="cajas")
        fila.columnconfigure(1, weight=1, uniform="cajas")

        self.tabla_pagos, self.lbl_total_pagado = self._crear_caja_tabla(
            fila, 0, "Historial de Pagos",
            [("fecha", "Fecha", 90), ("metodo", "Método", 110), ("monto", "Monto", 90)],
            "Agregar Pago", self._abrir_dialogo_pago)

        self.tabla_consumos, self.lbl_total_consumos = self._crear_caja_tabla(
            fila, 1, "Consumos Extras",
            [("concepto", "Concepto", 100), ("cantidad", "Cantidad", 80), ("total", "Total", 90)],
            "Agregar Consumo", self._abrir_dialogo_consumo)

    def _crear_resumen(self):
        caja = tk.Frame(self.frame, **ESTILO_CAJA)
        caja.pack(fill=tk.X, pady=(12, 0))

        interior = tk.Frame(caja, bg=COLOR_FONDO)
        interior.pack(fill=tk.X, padx=20, pady=10)
        interior.columnconfigure(0, weight=1)
        interior.columnconfigure(1, weight=1)

        tk.Label(interior, text="Resumen de la Cuenta", font=FUENTE_SUBTITULO, bg=COLOR_FONDO,
                 fg=COLOR_TEXTO).grid(row=0, column=0, sticky="w")

        # botones arriba a la derecha
        botones = tk.Frame(interior, bg=COLOR_FONDO)
        botones.grid(row=0, column=1, sticky="e")
        tk.Button(botones, text="Imprimir", command=self._on_imprimir, padx=15,
                  **ESTILO_BOTON).pack(side=tk.RIGHT, padx=(10, 0))
        tk.Button(botones, text="Finalizar / Cobrar", command=self._on_finalizar, padx=15,
                  **ESTILO_BOTON).pack(side=tk.RIGHT)

        # columna izquierda
        izq = tk.Frame(interior, bg=COLOR_FONDO)
        izq.grid(row=1, column=0, sticky="w", pady=(8, 0))
        self.lbl_estadia = tk.Label(izq, text="Estadía: $0", font=FUENTE_TEXTO, bg=COLOR_FONDO, fg=COLOR_TEXTO)
        self.lbl_estadia.pack(anchor="w", pady=2)
        self.lbl_consumo = tk.Label(izq, text="Consumo: $0", font=FUENTE_TEXTO, bg=COLOR_FONDO, fg=COLOR_TEXTO)
        self.lbl_consumo.pack(anchor="w", pady=2)

        # columna derecha
        der = tk.Frame(interior, bg=COLOR_FONDO)
        der.grid(row=1, column=1, sticky="e", pady=(8, 0))
        self.lbl_total = tk.Label(der, text="Total: $0", font=FUENTE_TEXTO, bg=COLOR_FONDO, fg=COLOR_TEXTO)
        self.lbl_total.pack(anchor="e", pady=2)
        self.lbl_pagado = tk.Label(der, text="Pagado: $0", font=FUENTE_TEXTO, bg=COLOR_FONDO, fg=COLOR_TEXTO)
        self.lbl_pagado.pack(anchor="e", pady=2)
        self.lbl_saldo = tk.Label(der, text="SALDO PENDIENTE: $0", font=FUENTE_TEXTO_BOLD,
                                  bg=COLOR_FONDO, fg=COLOR_ALERTA)
        self.lbl_saldo.pack(anchor="e", pady=(4, 2))

    # --------------------------------------------------------------- lógica
    def _cargar_reserva(self, reserva):
        self.reserva = reserva
        self.lbl_detalle_titulo.config(text=f"DETALLE DE LA RESERVA #{reserva['confirmacion']}")

        valores = [reserva["confirmacion"], reserva["huesped"], reserva["habitacion"],
                   reserva["check_in"], reserva["check_out"]]
        for var, valor in zip(self.vars_detalle, valores):
            var.set(valor)

        self._refrescar_tablas()

    def _refrescar_tablas(self):
        if not self.reserva:
            return

        # Pagos
        self.tabla_pagos.delete(*self.tabla_pagos.get_children())
        total_pagado = 0
        for pago in self.reserva["pagos"]:
            self.tabla_pagos.insert("", tk.END, values=(
                pago["fecha"], pago["metodo"], formato_moneda(pago["monto"])
            ))
            total_pagado += pago["monto"]
        self.lbl_total_pagado.config(text=f"Total Pagado: {formato_moneda(total_pagado)}")

        # Consumos
        self.tabla_consumos.delete(*self.tabla_consumos.get_children())
        total_consumos = 0
        for consumo in self.reserva["consumos"]:
            subtotal = consumo["cantidad"] * consumo["precio_unitario"]
            self.tabla_consumos.insert("", tk.END, values=(
                consumo["concepto"], consumo["cantidad"], formato_moneda(subtotal)
            ))
            total_consumos += subtotal
        self.lbl_total_consumos.config(text=f"Total Pagado: {formato_moneda(total_consumos)}")

        # Resumen
        total_estadia = self.reserva["total_estadia"]
        total_general = total_estadia + total_consumos
        saldo = total_general - total_pagado

        self.lbl_estadia.config(text=f"Estadía: {formato_moneda(total_estadia)}")
        self.lbl_consumo.config(text=f"Consumo: {formato_moneda(total_consumos)}")
        self.lbl_total.config(text=f"Total: {formato_moneda(total_general)}")
        self.lbl_pagado.config(text=f"Pagado: {formato_moneda(total_pagado)}")
        # rojo si queda saldo por cobrar, verde si la cuenta está saldada
        self.lbl_saldo.config(text=f"SALDO PENDIENTE: {formato_moneda(saldo)}",
                              fg=COLOR_ALERTA if saldo > 0 else COLOR_OK)

    # ---------------------------------------------------------- callbacks
    def _on_buscar(self):
        criterio = self.entry_busqueda.get().strip()
        if not criterio or criterio == PLACEHOLDER_BUSQUEDA:
            messagebox.showwarning("Buscar Reserva", "Ingresá un número de confirmación o DNI.")
            return
        # TODO: reemplazar por consulta real a la base de datos (tabla RESERVAS)
        reserva = buscar_reserva_mock(criterio)
        if reserva is None:
            messagebox.showerror("Buscar Reserva", "No se encontró ninguna reserva con ese dato.")
            return
        self._cargar_reserva(reserva)

    def _abrir_dialogo_pago(self):
        if not self.reserva:
            return
        self._abrir_dialogo_generico(
            titulo="Agregar Pago",
            campos=[("Monto", "monto"), ("Método (Efectivo/Transferencia/Tarjeta)", "metodo")],
            al_guardar=self._guardar_pago
        )

    def _guardar_pago(self, valores):
        try:
            monto = float(valores["monto"])
        except ValueError:
            messagebox.showerror("Agregar Pago", "El monto debe ser un número.")
            return False
        metodo = valores["metodo"].strip() or "Efectivo"
        self.reserva["pagos"].append({
            "fecha": date.today().strftime("%d/%m/%Y"),
            "metodo": metodo,
            "monto": monto,
        })
        self._refrescar_tablas()
        return True

    def _abrir_dialogo_consumo(self):
        if not self.reserva:
            return
        self._abrir_dialogo_generico(
            titulo="Agregar Consumo",
            campos=[("Concepto", "concepto"), ("Cantidad", "cantidad"), ("Precio unitario", "precio")],
            al_guardar=self._guardar_consumo
        )

    def _guardar_consumo(self, valores):
        try:
            cantidad = int(valores["cantidad"])
            precio = float(valores["precio"])
        except ValueError:
            messagebox.showerror("Agregar Consumo", "Cantidad y precio deben ser numéricos.")
            return False
        concepto = valores["concepto"].strip()
        if not concepto:
            messagebox.showerror("Agregar Consumo", "El concepto es obligatorio.")
            return False
        self.reserva["consumos"].append({
            "concepto": concepto,
            "cantidad": cantidad,
            "precio_unitario": precio,
        })
        self._refrescar_tablas()
        return True

    def _abrir_dialogo_generico(self, titulo, campos, al_guardar):
        """Crea un Toplevel simple con un Entry por campo y un botón Guardar."""
        ventana = tk.Toplevel(self.frame)
        ventana.title(titulo)
        ventana.configure(bg=COLOR_FONDO)
        ventana.resizable(False, False)
        ventana.grab_set()

        entradas = {}
        for i, (etiqueta, clave) in enumerate(campos):
            tk.Label(ventana, text=etiqueta, font=FUENTE_TEXTO, bg=COLOR_FONDO,
                     fg=COLOR_TEXTO).grid(row=i, column=0, sticky="w", padx=15, pady=8)
            entry = tk.Entry(ventana, width=26, fg="white", **ESTILO_ENTRADA)
            entry.grid(row=i, column=1, padx=15, pady=8, ipady=3)
            entradas[clave] = entry

        def guardar():
            valores = {clave: entry.get() for clave, entry in entradas.items()}
            if al_guardar(valores):
                ventana.destroy()

        tk.Button(ventana, text="Guardar", command=guardar, padx=25,
                  **ESTILO_BOTON).grid(row=len(campos), column=0, columnspan=2, pady=(5, 15))

    def _on_imprimir(self):
        # TODO: generar ticket/comprobante (PDF o impresión directa)
        messagebox.showinfo("Imprimir", "Generación de ticket todavía no implementada.")

    def _on_finalizar(self):
        if not self.reserva:
            return
        # TODO: cerrar la cuenta en la base de datos (marcar reserva como Finalizada)
        messagebox.showinfo("Finalizar / Cobrar", "Cuenta cerrada correctamente (placeholder).")


def contenido_pagos_consumos(frame):
    """Punto de entrada que usa main.py para montar esta pantalla."""
    PantallaPagosConsumos(frame)