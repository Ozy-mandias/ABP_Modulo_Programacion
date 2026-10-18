"""Campo de fecha con formato dd/mm/aaaa automático (el usuario solo teclea números)."""

import re
import tkinter as tk


def crear_campo_fecha(parent, x, y, ancho, alto=25, fuente=("Aldrich", 10), **opciones):
    """
    Crea un Entry ubicado con place() que solo acepta números y agrega las
    barras solo: al teclear 25102026 el campo muestra 25/10/2026.
    Devuelve (entry, variable). Se le puede hacer insert/delete/get como a
    cualquier Entry, y el formato se aplica igual.
    """
    var = tk.StringVar()
    entry = tk.Entry(parent, textvariable=var, font=fuente, relief=tk.FLAT, **opciones)
    entry.place(x=x, y=y, width=ancho, height=alto)

    def formatear(*_):
        digitos = re.sub(r"\D", "", var.get())[:8]
        texto = digitos[:2]
        if len(digitos) > 2:
            texto += "/" + digitos[2:4]
        if len(digitos) > 4:
            texto += "/" + digitos[4:]
        if texto != var.get():
            var.set(texto)
            entry.icursor(tk.END)

    var.trace_add("write", formatear)
    return entry, var
