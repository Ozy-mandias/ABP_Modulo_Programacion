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

def validar_consulta(datos):
    """Valida datos de una consulta. Devuelve (es_valido, lista_errores)."""
    errores = []
    if not datos.get('remitente', '').strip():
        errores.append("El remitente es obligatorio.")
    if not datos.get('asunto', '').strip():
        errores.append("El asunto es obligatorio.")
    if datos.get('medio') not in ('WhatsApp', 'Web', 'Telefono', 'Email'):
        errores.append("El medio debe ser WhatsApp, Web, Telefono o Email.")
    if datos.get('estado') not in ('Pendiente', 'Terminado', 'Archivado'):
        errores.append("El estado debe ser Pendiente, Terminado o Archivado.")
    fecha = datos.get('fecha', '').strip()
    if fecha:
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            errores.append("La fecha debe tener formato AAAA-MM-DD.")
    else:
        errores.append("La fecha es obligatoria.")
    return (len(errores) == 0, errores)