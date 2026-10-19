import re
from datetime import datetime

def validar_huesped(datos):
    """
    Valida los datos de un huésped antes de registrarlo o actualizarlo.
    Cada mensaje indica el CAMPO y el TIPO de dato esperado.
    Retorna una tupla: (booleano_es_valido, lista_de_errores)
    """
    errores = []

    def texto(clave):
        # Los campos opcionales vacíos llegan como None: se tratan como ''
        return (datos.get(clave) or '').strip()

    # Nombre
    nombre = texto('nombre')
    if not nombre:
        errores.append("Nombre: falta completarlo (texto, mínimo 2 letras).")
    elif len(nombre) < 2:
        errores.append("Nombre: debe ser texto de al menos 2 caracteres.")

    # Apellido
    apellido = texto('apellido')
    if not apellido:
        errores.append("Apellido: falta completarlo (texto, mínimo 2 letras).")
    elif len(apellido) < 2:
        errores.append("Apellido: debe ser texto de al menos 2 caracteres.")

    # DNI
    dni = texto('dni')
    if not dni:
        errores.append("DNI: falta completarlo (solo números, 7 a 9 dígitos, sin puntos).")
    elif not dni.isdigit():
        errores.append("DNI: debe contener solo números, sin puntos ni espacios.")
    elif not (7 <= len(dni) <= 9):
        errores.append("DNI: debe tener entre 7 y 9 dígitos.")

    # Teléfono
    telefono = texto('telefono')
    if not telefono:
        errores.append("Teléfono: falta completarlo (solo números, sin espacios ni guiones).")
    elif not telefono.isdigit():
        errores.append("Teléfono: debe contener solo números, sin espacios ni guiones.")

    # Email (opcional, pero si se escribe debe ser válido)
    email = texto('email')
    if email:
        patron_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(patron_email, email):
            errores.append("Email: formato inválido (ejemplo: nombre@correo.com).")

    # Fecha de nacimiento (opcional, formato AAAA-MM-DD)
    fecha_nac = texto('fecha_nacimiento')
    if fecha_nac:
        try:
            datetime.strptime(fecha_nac, '%Y-%m-%d')
        except ValueError:
            errores.append("Fecha de nacimiento: debe ser una fecha real con formato "
                           "AAAA-MM-DD (ejemplo: 1990-05-20).")

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


# ============================================================
# FECHAS dd/mm/aaaa (campo con máscara)
# ============================================================
def parsear_fecha(texto):
    """
    Convierte 'dd/mm/aaaa' en un objeto date.
    Devuelve None si el texto está incompleto o no es una fecha real.
    """
    texto = (texto or "").strip()
    if not re.match(r'^\d{2}/\d{2}/\d{4}$', texto):
        return None
    try:
        fecha = datetime.strptime(texto, "%d/%m/%Y").date()
    except ValueError:
        return None
    return fecha if 2000 <= fecha.year <= 2100 else None