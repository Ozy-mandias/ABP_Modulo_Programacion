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