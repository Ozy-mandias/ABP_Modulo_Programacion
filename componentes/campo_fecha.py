"""Campo de fecha con máscara dd/mm/aaaa: el usuario solo teclea números."""

import tkinter as tk


def _formatear(texto, borrando=False):
    """
    Deja solo dígitos (máx. 8) e inserta las barras apenas se completa cada
    grupo: '25' -> '25/', '2512' -> '25/12/', '25122026' -> '25/12/2026'.
    Al borrar no se agrega la barra final, para poder retroceder.
    """
    digitos = "".join(c for c in texto if c.isdigit())[:8]
    if len(digitos) >= 4:
        resultado = f"{digitos[:2]}/{digitos[2:4]}/{digitos[4:]}"
    elif len(digitos) >= 2:
        resultado = f"{digitos[:2]}/{digitos[2:]}"
    else:
        resultado = digitos
    if borrando and resultado.endswith("/"):
        resultado = resultado[:-1]
    return resultado


def crear_campo_fecha(parent, x, y, ancho, alto=25, fuente=("Aldrich", 10), **opciones):
    """
    Crea un Entry con máscara dd/mm/aaaa ubicado con place().
    Devuelve (entry, StringVar). El texto queda como 'dd/mm/aaaa'.
    """
    var = tk.StringVar()
    entrada = tk.Entry(parent, textvariable=var, font=fuente, **opciones)
    entrada.place(x=x, y=y, width=ancho, height=alto)
    estado = {"activo": False, "largo": 0}

    def al_cambiar(*_):
        if estado["activo"]:
            return
        estado["activo"] = True
        try:
            actual = var.get()
            borrando = len(actual) < estado["largo"]
            nuevo = _formatear(actual, borrando)
            if nuevo != actual:
                var.set(nuevo)
                entrada.icursor(tk.END)
            estado["largo"] = len(nuevo)
        finally:
            estado["activo"] = False

    var.trace_add("write", al_cambiar)
    return entrada, var