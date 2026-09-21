#Pantalla de Pagos y Consumos

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

COLOR_TEXTO = "#434343"
COLOR_BORDE = "#5b9bd5"
COLOR_FONDO = "white"
COLOR_GRIS_CLARO = "#f2f2f2"
COLOR_NEGRO = "black"

FUENTE_TITULO = ("Aldrich", 20, "bold")
FUENTE_SUBTITULO = ("Aldrich", 12, "bold")
FUENTE_TEXTO = ("Arial", 10) 
FUENTE_TEXTO_BOLD = ("Arial", 10, "bold")

def buscar_reserva_mock(criterio):
    """Simula la búsqueda de una reserva por N° de confirmación o por DNI"""
    return{
        "confirmacion":"12345",
        "huespede":"Lautaro Valdez",
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
        
        self.frame = tk.Frame(contenedor, bg=COLOR_FONDO)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        self._crear_titulo()
        self._crear_buscador()
        self._crear_detalle_reserva()
        self._crear_pagos_y_consumos()
        self._crear_resumen()

        self._cargar_reserva(buscar_reserva_mock("")) 

        #Interfaz de Usuario

    def _crear_titulo(self):
        tk.Label(
        self.frame, text="ESTADO DE CUENTA",
        font=FUENTE_TITULO, bg=COLOR_FONDO, fg=COLOR_NEGRO
    ).pack(anchor="w", pady=(0, 15))

    def _crear_buscador(self):
        caja = tk.Frame(self.frame, bg=COLOR_FONDO, highlightbackground=COLOR_BORDE, 
                    highlightthickness=1)
        caja.pack(fill=tk.X, pady=(0, 15))

        interior = tk.Frame(caja, bg=COLOR_FONDO)
        interior.pack(fill=tk.X, padx=15, pady=12)

        tk.Label(interior, text="Buscar Reserva", font=FUENTE_SUBTITULO, bg=COLOR_FONDO,
             fg=COLOR_NEGRO).pack(anchor="w")
        fila = tk.Frame(interior, bg=COLOR_FONDO)
        fila.pack(fill=tk.X, pady=(8, 0))

        self.entry_busqueda = tk.Entry(fila, font=FUENTE_TEXTO, fg="#999999")
        self.entry_busqueda.insert(0, "# De confirmación o DNI")
        self.entry_busqueda.bind("<FocusIn>", self._limpiar_placeholder)
        self.entry_busqueda.bind("<FocusIn>", self._limpiar_placeholder)
        self.entry_busqueda.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)

        tk.Button(
            fila, text="Buscar", font=FUENTE_TEXTO_BOLD, bg=COLOR_NEGRO, fg="white", activebackground="#333333",
                        activeforeground="white", bd=0, padx=20,command=self._on_buscar
                        ).pack(side=tk.LEFT, padx=(10, 0))


    def _limpiar_placeholder(self, event):
        if self.entry_busqueda.get() == "# De confirmación o DNI":
            self.entry_busqueda.delete(0, tk.END)
            self.entrcly_busqueda.config(fg=COLOR_NEGRO)


    def _crear_detalle_reserva(self):
        self.caja_detalle = tk.Frame(self.frame, bg=COLOR_FONDO,
                highlightbackground=COLOR_BORDE, highlightthickness=1)
        self.caja_detalle.pack(fill=tk.X, pady=(0, 15))
 
        self.lbl_detalle_titulo = tk.Label(
        self.caja_detalle, text="DETALLE DE LA RESERVA",
        font=FUENTE_SUBTITULO, bg=COLOR_FONDO, fg=COLOR_NEGRO
        )
        self.lbl_detalle_titulo.pack(anchor="w", padx=15, pady=(10, 5))

        linea = tk.Frame(self.caja_detalle, bg=COLOR_NEGRO, height=1)
        linea.pack(fill=tk.X, padx=15)

        columnas = tk.Frame(self.caja_detalle, bg=COLOR_FONDO)
        columnas.pack(fill=tk.X, padx=15, pady=10)
        encabezados = ["Confirmación", "Nombre Huésped", "Hab. #", "Fecha Check-In", "Fecha Check-Out"]
        self.vars_detalle = []
        for i, titulo in enumerate(encabezados):
            columnas.columnconfigure(i, weight=1)
            tk.Label(columnas, text=titulo, font=FUENTE_TEXTO_BOLD,
                     bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=0, column=i, sticky="w")
            var = tk.StringVar(value="—")
            tk.Label(columnas, textvariable=var, font=FUENTE_TEXTO,
                     bg=COLOR_FONDO, fg=COLOR_NEGRO).grid(row=1, column=i, sticky="w", pady=(4, 0))
            self.vars_detalle.append(var)

    def _crear_pagos_y_consumos(self):
        fila = tk.Frame(self.frame, bg=COLOR_FONDO)
        fila.pack(fill=tk.X, pady=(0, 15))
        fila.columnconfigure(0, weight=1)
        fila.columnconfigure(1, weight=1)


    #Historial de Pagos

        caja_pagos = tk.Frame(fila, bg=COLOR_FONDO, highlightbackground=COLOR_BORDE, highlightthickness=1)
        caja_pagos.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        tk.Label(caja_pagos, text="Historial de Pagos", font=FUENTE_SUBTITULO,
                    bg=COLOR_FONDO, fg=COLOR_NEGRO).pack(pady=(10, 5))
    
        self.tabla_pagos = ttk.Treeview(
            caja_pagos, columns=("fecha", "metodo", "monto"),
            show="headings", height=5
            )
        for col, titulo, ancho in [("fecha", "Fecha", 90), ("metodo", "Método", 110), ("monto", "Monto", 90)]:
            self.tabla_pagos.heading(col, text=titulo)
            self.tabla_pagos.column(col, width=ancho, anchor="center")
            self.tabla_pagos.pack(fill=tk.X, padx=10)
            self.lbl_total_pagado = tk.Label(caja_pagos, text="Total Pagado: $0", font=FUENTE_TEXTO_BOLD,
                            bg=COLOR_FONDO, fg=COLOR_NEGRO)
            self.lbl_total_pagado.pack(anchor="e", padx=10, pady=(8, 5))

        tk.Button(
            caja_pagos, text="Agregar Pago", font=FUENTE_TEXTO_BOLD, bg=COLOR_NEGRO,
            fg="white", activebackground="#333333", activeforeground="white", bd=0,
            command=self._abrir_dialogo_pago
        ).pack(pady=(0, 12))

    #Consumos extra

        caja_consumos = tk.Frame(fila, bg=COLOR_FONDO, highlightbackground=COLOR_BORDE,
                    highlightthickness=1)
        caja_consumos.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
    
        tk.Label(caja_consumos, text="Consumos Extras", font=FUENTE_SUBTITULO,
                    bg=COLOR_FONDO, fg=COLOR_NEGRO).pack(pady=(10, 5))
    
        self.tabla_consumos = ttk.Treeview(
            caja_consumos, columns=("concepto", "cantidad", "total"),
            show="headings", height=5
        )
        for col, titulo, ancho in [("concepto", "Concepto", 100), ("cantidad", "Cantidad", 80), ("total", "Total", 90)]:
            self.tabla_consumos.heading(col, text=titulo)
            self.tabla_consumos.column(col, width=ancho, anchor="center")
            self.tabla_consumos.pack(fill=tk.X, padx=10)
    
            self.lbl_total_consumos = tk.Label(caja_consumos, text="Total Pagado: $0",
                                                font=FUENTE_TEXTO_BOLD, bg=COLOR_FONDO, fg=COLOR_NEGRO)
            self.lbl_total_consumos.pack(anchor="e", padx=10, pady=(8, 5))
    
            tk.Button(
                caja_consumos, text="Agregar Consumo", font=FUENTE_TEXTO_BOLD, bg=COLOR_NEGRO,
                fg="white", activebackground="#333333", activeforeground="white", bd=0,
                command=self._abrir_dialogo_consumo
            ).pack(pady=(0, 12))
 
    def _crear_resumen(self):
        caja = tk.Frame(self.frame, bg=COLOR_FONDO, highlightbackground=COLOR_BORDE,
                         highlightthickness=1)
        caja.pack(fill=tk.X)
 
        tk.Label(caja, text="Resumen de la Cuenta", font=FUENTE_SUBTITULO,
                 bg=COLOR_FONDO, fg=COLOR_NEGRO).pack(pady=(10, 8))
 
        cuerpo = tk.Frame(caja, bg=COLOR_FONDO)
        cuerpo.pack(fill=tk.X, padx=25)
        cuerpo.columnconfigure(0, weight=1)
        cuerpo.columnconfigure(1, weight=1)
 
        # columna izquierda
        izq = tk.Frame(cuerpo, bg=COLOR_FONDO)
        izq.grid(row=0, column=0, sticky="w")
        self.lbl_estadia = tk.Label(izq, text="Estadía: $0", font=FUENTE_TEXTO, bg=COLOR_FONDO)
        self.lbl_estadia.pack(anchor="w", pady=2)
        self.lbl_consumo = tk.Label(izq, text="Consumo: $0", font=FUENTE_TEXTO, bg=COLOR_FONDO)
        self.lbl_consumo.pack(anchor="w", pady=2)
 
        # columna derecha
        der = tk.Frame(cuerpo, bg=COLOR_FONDO)
        der.grid(row=0, column=1, sticky="e")
        self.lbl_total = tk.Label(der, text="Total: $0", font=FUENTE_TEXTO, bg=COLOR_FONDO)
        self.lbl_total.pack(anchor="e", pady=2)
        self.lbl_pagado = tk.Label(der, text="Pagado: $0", font=FUENTE_TEXTO, bg=COLOR_FONDO)
        self.lbl_pagado.pack(anchor="e", pady=2)
        self.lbl_saldo = tk.Label(der, text="SALDO PENDIENTE: $0", font=FUENTE_TEXTO_BOLD,
                                   bg=COLOR_FONDO, fg="#c0392b")
        self.lbl_saldo.pack(anchor="e", pady=(6, 2))
 
        botones = tk.Frame(caja, bg=COLOR_FONDO)
        botones.pack(fill=tk.X, padx=25, pady=(10, 15))
 
        tk.Button(
            botones, text="Imprimir", font=FUENTE_TEXTO_BOLD, bg=COLOR_NEGRO, fg="white",
            activebackground="#333333", activeforeground="white", bd=0, padx=15,
            command=self._on_imprimir
        ).pack(side=tk.RIGHT, padx=(10, 0))
 
        tk.Button(
            botones, text="Finalizar / Cobrar", font=FUENTE_TEXTO_BOLD, bg=COLOR_NEGRO,
            fg="white", activebackground="#333333", activeforeground="white", bd=0, padx=15,
            command=self._on_finalizar
        ).pack(side=tk.RIGHT)
 
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
        self.lbl_saldo.config(text=f"SALDO PENDIENTE: {formato_moneda(saldo)}")
 
    # ---------------------------------------------------------- callbacks
    def _on_buscar(self):
        criterio = self.entry_busqueda.get().strip()
        if not criterio or criterio == "# De Confirmación o DNI":
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
            tk.Label(ventana, text=etiqueta, font=FUENTE_TEXTO, bg=COLOR_FONDO).grid(
                row=i, column=0, sticky="w", padx=10, pady=8
            )
            entry = tk.Entry(ventana, font=FUENTE_TEXTO)
            entry.grid(row=i, column=1, padx=10, pady=8)
            entradas[clave] = entry
 
        def guardar():
            valores = {clave: entry.get() for clave, entry in entradas.items()}
            if al_guardar(valores):
                ventana.destroy()
 
        tk.Button(
            ventana, text="Guardar", font=FUENTE_TEXTO_BOLD, bg=COLOR_NEGRO, fg="white",
            activebackground="#333333", activeforeground="white", bd=0, command=guardar
        ).grid(row=len(campos), column=0, columnspan=2, pady=(5, 12))
 
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