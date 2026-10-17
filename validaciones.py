import re
from datetime import datetime

def validar_huesped(datos):
    """
    Valida los datos de un huésped antes de registrarlo o actualizarlo.
    Retorna una tupla: (booleano_es_valido, lista_de_errores)
    """
    errores = []

    # Validar Nombre
    nombre = datos.get('nombre', '').strip()
    if not nombre:
        errores.append("El nombre es obligatorio.")
    elif len(nombre) < 2:
        errores.append("El nombre debe tener al menos 2 caracteres.")

    # Validar Apellido
    apellido = datos.get('apellido', '').strip()
    if not apellido:
        errores.append("El apellido es obligatorio.")
    elif len(apellido) < 2:
        errores.append("El apellido debe tener al menos 2 caracteres.")

    # Validar DNI
    dni = datos.get('dni', '').strip()
    if not dni:
        errores.append("El DNI es obligatorio.")
    elif not dni.isdigit():
        errores.append("El DNI debe contener solo números, sin puntos ni espacios.")
    elif not (7 <= len(dni) <= 9):
        errores.append("El DNI debe tener entre 7 y 9 dígitos.")

    # Validar Teléfono
    telefono = datos.get('telefono', '').strip()
    if not telefono:
        errores.append("El teléfono es obligatorio.")
    elif not telefono.isdigit():
        errores.append("El teléfono debe contener solo números.")

    # Validar Email (Es opcional, pero si se escribe debe ser válido)
    email = datos.get('email', '').strip()
    if email:
        patron_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(patron_email, email):
            errores.append("El formato del correo electrónico no es válido.")

    # Validar Fecha de Nacimiento (Es opcional, formato AAAA-MM-DD)
    fecha_nac = datos.get('fecha_nacimiento', '').strip()
    if fecha_nac:
        try:
            datetime.strptime(fecha_nac, '%Y-%m-%d')
        except ValueError:
            errores.append("La fecha de nacimiento debe tener el formato AAAA-MM-DD (ejemplo: 1990-05-20).")

    es_valido = len(errores) == 0
    return es_valido, errores


TIPOS_HABITACION = ("simple", "doble", "suite", "familiar")
ESTADOS_HABITACION = ("disponible", "ocupada", "mantenimiento")


def validar_habitacion(datos):
    """
    Valida los datos de una habitación antes de registrarla o actualizarla.
    Retorna una tupla: (booleano_es_valido, lista_de_errores)
    """
    errores = []

    if datos.get('tipo', '') not in TIPOS_HABITACION:
        errores.append("Debe seleccionar un tipo de habitación válido.")

    capacidad = datos.get('capacidad', '').strip()
    if not capacidad:
        errores.append("La capacidad es obligatoria.")
    elif not capacidad.isdigit():
        errores.append("La capacidad debe ser un número entero.")
    elif not (1 <= int(capacidad) <= 20):
        errores.append("La capacidad debe estar entre 1 y 20 personas.")

    precio = datos.get('precio_noche', '').strip().replace(",", ".")
    if not precio:
        errores.append("El precio por noche es obligatorio.")
    elif not re.match(r'^\d+(\.\d{1,2})?$', precio):
        errores.append("El precio debe ser un número sin puntos de miles ni símbolos (ejemplo: 45000).")
    elif float(precio) <= 0:
        errores.append("El precio por noche debe ser mayor a cero.")

    if datos.get('estado', '') not in ESTADOS_HABITACION:
        errores.append("Debe seleccionar un estado válido.")

    return len(errores) == 0, errores
"""Validaciones específicas para la entidad Reserva."""

from datetime import datetime


# ============================================================
# RESERVAS
# ============================================================

def validar_reserva(datos):
    """
    Valida los datos de una reserva antes de registrarla o actualizarla.
    Retorna una tupla: (booleano_es_valido, lista_de_errores)
    """
    errores = []

    # --- Huésped ---
    huesped = str(datos.get('huesped', '')).strip()
    if not huesped or huesped == "Seleccione un huésped":
        errores.append("Debe seleccionar un huésped de la lista.")

    # --- Fechas ---
    fecha_ingreso_str = datos.get('fecha_ingreso', '').strip()
    fecha_salida_str = datos.get('fecha_salida', '').strip()

    fecha_ingreso = None
    fecha_salida = None

    if not fecha_ingreso_str:
        errores.append("La fecha de ingreso es obligatoria.")
    else:
        try:
            fecha_ingreso = datetime.strptime(fecha_ingreso_str, '%Y-%m-%d')
        except ValueError:
            errores.append("La fecha de ingreso debe tener el formato AAAA-MM-DD (ej: 2026-10-07).")

    if not fecha_salida_str:
        errores.append("La fecha de salida es obligatoria.")
    else:
        try:
            fecha_salida = datetime.strptime(fecha_salida_str, '%Y-%m-%d')
        except ValueError:
            errores.append("La fecha de salida debe tener el formato AAAA-MM-DD (ej: 2026-11-07).")

    if fecha_ingreso and fecha_salida and fecha_salida <= fecha_ingreso:
        errores.append("La fecha de salida debe ser posterior a la fecha de ingreso.")

    # --- Habitación ---
    habitacion = str(datos.get('habitacion', '')).strip()
    if not habitacion or habitacion == "Seleccione una habitación":
        errores.append("Debe seleccionar una habitación de la lista.")

    # --- Precio ---
    precio_str = str(datos.get('precio_noche', '')).strip().replace(",", ".")
    if not precio_str:
        errores.append("El precio por noche es obligatorio.")
    else:
        try:
            if float(precio_str) <= 0:
                errores.append("El precio debe ser mayor a cero.")
        except ValueError:
            errores.append("El precio debe ser un número válido (ej: 25000 o 25000.50).")

    # --- Nro Personas ---
    personas_str = str(datos.get('nro_personas', '')).strip()
    if not personas_str:
        errores.append("El número de personas es obligatorio.")
    elif not personas_str.isdigit():
        errores.append("El número de personas debe ser un número entero.")
    else:
        personas = int(personas_str)
        if personas < 1:
            errores.append("Debe haber al menos 1 persona.")
        elif personas > 20:
            errores.append("El número de personas no puede superar las 20.")

    # --- Estado ---
    estados_validos = ("pendiente", "confirmado", "cancelado")
    if datos.get('estado', '').lower() not in estados_validos:
        errores.append(f"El estado debe ser uno de: {', '.join(estados_validos)}.")

    return len(errores) == 0, errores