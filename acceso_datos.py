"""
Módulo de acceso a datos de GestARHO.
Contiene todas las funciones que ejecutan sentencias SQL
sobre la base de datos MySQL.
"""

from datetime import date, timedelta, datetime

import mysql.connector
from conexion import obtener_conexion, obtener_conexion_admin, cerrar_conexion


# ============================================================
# HABITACIONES
# Lectura: rol recepcionista (SELECT en todas las tablas).
# Alta y edición: rol administrador, porque el recepcionista
# no tiene permiso de escritura sobre la tabla habitacion.
# ============================================================

def insertar_habitacion(tipo, capacidad, precio_noche, estado):
    """
    Inserta una habitación nueva.
    Retorna (True, "mensaje") o (False, "mensaje de error").
    """
    conexion = obtener_conexion_admin()
    if not conexion:
        return False, "No se pudo conectar a la base de datos."

    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO habitacion
                (tipo_habitacion, capacidad, precio_noche, estado_habitacion)
            VALUES (%s, %s, %s, %s)
        """, (tipo, capacidad, precio_noche, estado))
        conexion.commit()
        return True, f"Habitación #{cursor.lastrowid} registrada correctamente."

    except mysql.connector.IntegrityError as e:
        conexion.rollback()
        return False, f"Los datos no cumplen las restricciones de la base: {e.msg}"

    except mysql.connector.Error as e:
        conexion.rollback()
        return False, f"Error de base de datos: {e}"

    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)


# Estado "real" de una habitación para una fecha: si figura como disponible
# pero tiene una reserva CONFIRMADA que cubre la fecha (ingreso <= fecha < salida),
# se considera ocupada. Usa 2 parámetros (fecha, fecha).
SQL_ESTADO_EFECTIVO = """
    CASE WHEN h.estado_habitacion = 'disponible' AND EXISTS (
        SELECT 1
        FROM reserva_habitacion rh
        INNER JOIN reserva r ON r.id_reserva = rh.id_reserva
        WHERE rh.id_habitacion = h.id_habitacion
          AND r.estado_reserva = 'confirmado'
          AND r.fecha_ingreso <= %s
          AND r.fecha_salida > %s
    ) THEN 'ocupada' ELSE h.estado_habitacion END
"""


def listar_habitaciones(tipo=None, estado=None, hoy=None):
    """
    Devuelve las habitaciones, con filtros opcionales por tipo y/o estado.
    El estado devuelto es el estado EFECTIVO de hoy: una habitación con una
    reserva confirmada vigente se muestra como ocupada.
    Los valores van como parámetros, nunca concatenados en el SQL.
    """
    conexion = obtener_conexion()
    if not conexion:
        return []

    hoy = hoy or date.today()
    sql = f"""
        SELECT h.id_habitacion, h.tipo_habitacion, h.capacidad,
               h.precio_noche, ({SQL_ESTADO_EFECTIVO}) AS estado_habitacion
        FROM habitacion h
    """
    condiciones = []
    parametros = [hoy, hoy]
    if tipo:
        condiciones.append("h.tipo_habitacion = %s")
        parametros.append(tipo)
    if estado:
        condiciones.append(f"({SQL_ESTADO_EFECTIVO}) = %s")
        parametros += [hoy, hoy, estado]
    if condiciones:
        sql += " WHERE " + " AND ".join(condiciones)
    sql += " ORDER BY h.id_habitacion"

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(sql, tuple(parametros))
        return cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Error al listar habitaciones: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)


def obtener_habitacion_por_id(id_habitacion):
    """Devuelve los datos de una habitación por su ID."""
    conexion = obtener_conexion()
    if not conexion:
        return None

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT id_habitacion, tipo_habitacion, capacidad,
                   precio_noche, estado_habitacion
            FROM habitacion
            WHERE id_habitacion = %s
        """, (id_habitacion,))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        print(f"Error al obtener habitación: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)


def actualizar_habitacion(id_habitacion, tipo, capacidad, precio_noche, estado):
    """
    Actualiza los datos de una habitación existente.
    Retorna (True, "mensaje") o (False, "mensaje de error").
    """
    conexion = obtener_conexion_admin()
    if not conexion:
        return False, "No se pudo conectar a la base de datos."

    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE habitacion
            SET tipo_habitacion = %s, capacidad = %s,
                precio_noche = %s, estado_habitacion = %s
            WHERE id_habitacion = %s
        """, (tipo, capacidad, precio_noche, estado, id_habitacion))
        conexion.commit()
        return True, "Habitación actualizada correctamente."

    except mysql.connector.IntegrityError as e:
        conexion.rollback()
        return False, f"Los datos no cumplen las restricciones de la base: {e.msg}"

    except mysql.connector.Error as e:
        conexion.rollback()
        return False, f"Error de base de datos: {e}"

    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)


def eliminar_habitacion(id_habitacion):
    """
    Elimina definitivamente una habitación.
    Si tiene reservas asociadas, la base lo impide (clave foránea).
    Retorna (True, "mensaje") o (False, "mensaje de error").
    """
    conexion = obtener_conexion_admin()
    if not conexion:
        return False, "No se pudo conectar a la base de datos."

    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM habitacion WHERE id_habitacion = %s",
                       (id_habitacion,))
        conexion.commit()
        return True, "Habitación eliminada correctamente."

    except mysql.connector.IntegrityError:
        conexion.rollback()
        return False, ("No se puede eliminar: la habitación tiene reservas "
                       "asociadas. Puede ponerla en estado Mantenimiento.")

    except mysql.connector.Error as e:
        conexion.rollback()
        return False, f"Error de base de datos: {e}"

    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)


def listar_reservas_habitacion(id_habitacion):
    """
    Consulta con JOIN entre habitación, reserva y huésped:
    devuelve las reservas de una habitación con su huésped titular.
    """
    conexion = obtener_conexion()
    if not conexion:
        return []

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT r.id_reserva, r.fecha_ingreso, r.fecha_salida,
                   r.estado_reserva, h.nombre, h.apellido
            FROM reserva_habitacion rh
            INNER JOIN reserva r ON r.id_reserva = rh.id_reserva
            LEFT JOIN reserva_huesped rhu
                   ON rhu.id_reserva = r.id_reserva AND rhu.rol = 'titular'
            LEFT JOIN huesped h ON h.id_huesped = rhu.id_huesped
            WHERE rh.id_habitacion = %s
            ORDER BY r.fecha_ingreso DESC
        """, (id_habitacion,))
        return cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Error al listar reservas de la habitación: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)


# ============================================================
# HUÉSPEDES - CRUD
# ============================================================

def insertar_huesped(nombre, apellido, dni, telefono, email=None):
    """
    Inserta un huésped en la base de datos.
    Si el DNI ya existe pero está inactivo, lo reactiva.
    Retorna (True, "mensaje") o (False, "mensaje de error").
    """
    conexion = obtener_conexion()
    if not conexion:
        return False, "No se pudo conectar a la base de datos."

    try:
        cursor = conexion.cursor(dictionary=True)

        # 1. Buscar si ya existe un huésped con ese DNI
        cursor.execute("""
            SELECT id_huesped, activo FROM huesped WHERE dni = %s
        """, (dni,))
        existente = cursor.fetchone()

        if existente:
            if existente['activo'] == 1:
                return False, f"El DNI '{dni}' ya está registrado en otro huésped activo."
            else:
                # Reactivar huésped inactivo con datos nuevos
                cursor.execute("""
                    UPDATE huesped
                    SET nombre = %s, apellido = %s, telefono = %s,
                        email = %s, activo = 1, fecha_modificacion = CURDATE()
                    WHERE id_huesped = %s
                """, (nombre, apellido, telefono, email, existente['id_huesped']))
                conexion.commit()
                return True, "Huésped reactivado y actualizado correctamente."

        # 2. Verificar email duplicado en otro activo
        if email:
            cursor.execute("""
                SELECT id_huesped FROM huesped
                WHERE email = %s AND activo = 1
            """, (email,))
            if cursor.fetchone():
                return False, f"El email '{email}' ya está registrado en otro huésped activo."

        # 3. Insertar huésped nuevo
        cursor.execute("""
            INSERT INTO huesped
                (nombre, apellido, dni, telefono, email, id_usuario_registro)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nombre, apellido, dni, telefono, email, 1))
        conexion.commit()
        return True, "Huésped registrado correctamente."

    except mysql.connector.IntegrityError as e:
        conexion.rollback()
        error_str = str(e).lower()
        if "email" in error_str and "duplicate" in error_str:
            return False, f"El email '{email}' ya está registrado en otro huésped."
        elif "dni" in error_str and "duplicate" in error_str:
            return False, f"El DNI '{dni}' ya está registrado en otro huésped."
        else:
            return False, f"Error de integridad: {e}"

    except Exception as e:
        conexion.rollback()
        return False, f"Error inesperado: {e}"

    finally:
        cursor.close()
        cerrar_conexion(conexion)


def listar_huespedes():
    """
    Devuelve una lista con todos los huéspedes activos.
    """
    conexion = obtener_conexion()
    if not conexion:
        return []

    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT id_huesped, nombre, apellido, dni, telefono, email
            FROM huesped
            WHERE activo = 1
            ORDER BY apellido, nombre
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al listar huéspedes: {e}")
        return []
    finally:
        cursor.close()
        cerrar_conexion(conexion)


def buscar_huesped_por_dni(dni):
    """
    Busca un huésped por su DNI exacto.
    """
    conexion = obtener_conexion()
    if not conexion:
        return None

    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT id_huesped, nombre, apellido, dni, telefono, email
            FROM huesped
            WHERE dni = %s AND activo = 1
        """, (dni,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error al buscar huésped: {e}")
        return None
    finally:
        cursor.close()
        cerrar_conexion(conexion)


def buscar_huespedes(criterio):
    """
    Busca huéspedes por DNI, nombre, apellido, teléfono o email.
    La búsqueda es parcial (LIKE %criterio%).
    """
    conexion = obtener_conexion()
    if not conexion:
        return []

    try:
        cursor = conexion.cursor(dictionary=True)
        patron = f"%{criterio}%"
        cursor.execute("""
            SELECT id_huesped, nombre, apellido, dni, telefono, email
            FROM huesped
            WHERE activo = 1
              AND (
                    dni LIKE %s
                 OR nombre LIKE %s
                 OR apellido LIKE %s
                 OR telefono LIKE %s
                 OR email LIKE %s
              )
            ORDER BY apellido, nombre
        """, (patron, patron, patron, patron, patron))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al buscar huéspedes: {e}")
        return []
    finally:
        cursor.close()
        cerrar_conexion(conexion)


def obtener_huesped_por_id(id_huesped):
    """
    Devuelve los datos completos de un huésped por su ID.
    """
    conexion = obtener_conexion()
    if not conexion:
        return None

    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT id_huesped, nombre, apellido, dni, telefono, email,
                   direccion, fecha_nacimiento, nacionalidad
            FROM huesped
            WHERE id_huesped = %s AND activo = 1
        """, (id_huesped,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error al obtener huésped: {e}")
        return None
    finally:
        cursor.close()
        cerrar_conexion(conexion)


def actualizar_huesped(id_huesped, nombre, apellido, dni, telefono,
                       email=None, direccion=None, nacionalidad=None):
    """
    Actualiza los datos de un huésped existente.
    Retorna (True, "mensaje") o (False, "mensaje de error").
    """
    conexion = obtener_conexion()
    if not conexion:
        return False, "No se pudo conectar a la base de datos."

    try:
        cursor = conexion.cursor()
        sql = """
            UPDATE huesped
            SET nombre = %s, apellido = %s, dni = %s,
                telefono = %s, email = %s, direccion = %s,
                nacionalidad = %s, fecha_modificacion = CURDATE()
            WHERE id_huesped = %s
        """
        valores = (nombre, apellido, dni, telefono, email,
                   direccion, nacionalidad, id_huesped)
        cursor.execute(sql, valores)
        conexion.commit()
        return True, "Huésped actualizado correctamente."

    except mysql.connector.IntegrityError as e:
        conexion.rollback()
        error_str = str(e).lower()
        if "email" in error_str and "duplicate" in error_str:
            return False, f"El email '{email}' ya está registrado en otro huésped."
        elif "dni" in error_str and "duplicate" in error_str:
            return False, f"El DNI '{dni}' ya está registrado en otro huésped."
        else:
            return False, f"Error de integridad: {e}"

    except Exception as e:
        conexion.rollback()
        return False, f"Error inesperado: {e}"

    finally:
        cursor.close()
        cerrar_conexion(conexion)


def eliminar_huesped(id_huesped):
    """
    Elimina un huésped (baja lógica: activo = 0).
    """
    conexion = obtener_conexion()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE huesped
            SET activo = 0, fecha_modificacion = CURDATE()
            WHERE id_huesped = %s
        """, (id_huesped,))
        conexion.commit()
        return True
    except Exception as e:
        conexion.rollback()
        print(f"Error al eliminar huésped: {e}")
        return False
    finally:
        cursor.close()
        cerrar_conexion(conexion)


# ============================================================
# HUÉSPEDES - PAPELERA (inactivos)
# ============================================================

def listar_huespedes_inactivos():
    """
    Devuelve los huéspedes dados de baja (activo = 0).
    """
    conexion = obtener_conexion()
    if not conexion:
        return []

    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT id_huesped, nombre, apellido, dni, telefono, email
            FROM huesped
            WHERE activo = 0
            ORDER BY apellido, nombre
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al listar huéspedes inactivos: {e}")
        return []
    finally:
        cursor.close()
        cerrar_conexion(conexion)


def restaurar_huesped(id_huesped):
    """
    Reactiva un huésped dado de baja (activo = 1).
    Retorna (True, "mensaje") o (False, "mensaje de error").
    """
    conexion = obtener_conexion()
    if not conexion:
        return False, "No se pudo conectar a la base de datos."

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE huesped
            SET activo = 1, fecha_modificacion = CURDATE()
            WHERE id_huesped = %s
        """, (id_huesped,))
        conexion.commit()
        return True, "Huésped restaurado correctamente."
    except Exception as e:
        conexion.rollback()
        return False, f"Error al restaurar: {e}"
    finally:
        cursor.close()
        cerrar_conexion(conexion)


def eliminar_huesped_definitivo(id_huesped):
    """
    Elimina físicamente un huésped de la base.
    Usa la conexión ADMIN (recepcionista no tiene permiso de DELETE).
    Falla si el huésped tiene reservas asociadas.
    Retorna (True, "mensaje") o (False, "mensaje de error").
    """
    conexion = obtener_conexion_admin()
    if not conexion:
        return False, "No se pudo conectar como administrador."

    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM huesped WHERE id_huesped = %s", (id_huesped,))
        conexion.commit()
        return True, "Huésped eliminado permanentemente."
    except mysql.connector.IntegrityError:
        conexion.rollback()
        return False, ("No se puede eliminar: el huésped tiene reservas asociadas. "
                       "Primero eliminá esas reservas o dejanlo dado de baja.")
    except mysql.connector.ProgrammingError as e:
        conexion.rollback()
        return False, f"Acceso denegado por el SGBD: {e}"
    except Exception as e:
        conexion.rollback()
        return False, f"Error inesperado: {e}"
    finally:
        cursor.close()
        cerrar_conexion(conexion)
# ============================================================
# RESERVAS - CONTROL DE SUPERPOSICIÓN (RN-01)
# ============================================================

def buscar_conflicto_reserva(cursor, id_habitacion, fecha_ingreso, fecha_salida,
                             id_reserva_excluida=None):
    """
    Devuelve (id_reserva, ingreso, salida) de una reserva activa que ocupa la
    habitación en ese rango, o None si está libre.
    Hay conflicto si: otra.ingreso < nueva.salida Y otra.salida > nueva.ingreso.
    Las canceladas no cuentan; el día de salida puede ser el ingreso de otra.
    """
    sql = """
        SELECT r.id_reserva, r.fecha_ingreso, r.fecha_salida
        FROM reserva_habitacion rh
        INNER JOIN reserva r ON r.id_reserva = rh.id_reserva
        WHERE rh.id_habitacion = %s
          AND r.estado_reserva <> 'cancelado'
          AND r.fecha_ingreso < %s
          AND r.fecha_salida > %s
    """
    params = [id_habitacion, fecha_salida, fecha_ingreso]
    if id_reserva_excluida is not None:
        sql += " AND r.id_reserva <> %s"
        params.append(id_reserva_excluida)
    sql += " LIMIT 1"
    cursor.execute(sql, tuple(params))
    return cursor.fetchone()


def _mensaje_conflicto(id_habitacion, conflicto):
    id_conf, ingreso, salida = conflicto
    return (f"La habitación #{id_habitacion} ya está reservada del "
            f"{ingreso.strftime('%d/%m/%Y')} al {salida.strftime('%d/%m/%Y')} "
            f"(reserva #{id_conf}). Elija otra habitación u otras fechas.")


# ============================================================
# RESERVAS - CRUD
# ============================================================

def insertar_reserva(id_huesped, id_habitacion, fecha_ingreso, fecha_salida,
                     precio_noche, nro_personas, estado_reserva):
    """
    Inserta una reserva completa (reserva + reserva_habitacion + reserva_huesped).
    Calcula el precio_total en base a las noches y el precio por noche.
    Retorna (True, "mensaje") o (False, "mensaje de error").
    """
    conexion = obtener_conexion()
    if not conexion:
        return False, "No se pudo conectar a la base de datos."

    cursor = None
    try:
        cursor = conexion.cursor()

        # Calcular cantidad de noches y precio total
        from datetime import datetime
        fi = datetime.strptime(fecha_ingreso, '%Y-%m-%d')
        fs = datetime.strptime(fecha_salida, '%Y-%m-%d')
        noches = (fs - fi).days
        precio_total = noches * float(precio_noche)

        # 0. Control de superposición (RN-01), salvo que se cree cancelada
        if estado_reserva != 'cancelado':
            conflicto = buscar_conflicto_reserva(cursor, id_habitacion,
                                                 fecha_ingreso, fecha_salida)
            if conflicto:
                return False, _mensaje_conflicto(id_habitacion, conflicto)

        # 1. Insertar en tabla reserva
        cursor.execute("""
            INSERT INTO reserva
                (fecha_ingreso, fecha_salida, nro_personas,
                 precio_total, estado_reserva, id_usuario_creacion)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (fecha_ingreso, fecha_salida, nro_personas,
              precio_total, estado_reserva, 1))
        id_reserva = cursor.lastrowid

        # 2. Insertar en reserva_habitacion
        cursor.execute("""
            INSERT INTO reserva_habitacion
                (id_reserva, id_habitacion, precio_noche_acordado)
            VALUES (%s, %s, %s)
        """, (id_reserva, id_habitacion, precio_noche))

        # 3. Insertar en reserva_huesped (titular)
        cursor.execute("""
            INSERT INTO reserva_huesped
                (id_reserva, id_huesped, rol)
            VALUES (%s, %s, 'titular')
        """, (id_reserva, id_huesped))

        conexion.commit()
        return True, f"Reserva #{id_reserva} registrada correctamente."

    except mysql.connector.IntegrityError as e:
        conexion.rollback()
        if "La habitación ya está reservada" in str(e):
            return False, "La habitación ya está reservada en ese rango de fechas."
        return False, f"Error de integridad: {e.msg}"
    except mysql.connector.Error as e:
        conexion.rollback()
        if e.errno == 1644:  # SIGNAL del trigger anti doble reserva
            return False, "La habitación ya está reservada en ese rango de fechas."
        return False, f"Error de base de datos: {e}"
    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)


def listar_reservas(filtro_texto=None, estado=None):
    """Devuelve las reservas con JOINs a huésped titular y habitación."""
    conexion = obtener_conexion()
    if not conexion:
        return []

    sql = """
        SELECT
            r.id_reserva,
            r.fecha_ingreso,
            r.fecha_salida,
            r.nro_personas,
            r.estado_reserva,
            r.precio_total,
            h.nombre AS nombre_huesped,
            h.apellido AS apellido_huesped,
            hab.id_habitacion,
            hab.tipo_habitacion,
            rhab.precio_noche_acordado
        FROM reserva r
        INNER JOIN reserva_huesped rh ON rh.id_reserva = r.id_reserva AND rh.rol = 'titular'
        INNER JOIN huesped h ON h.id_huesped = rh.id_huesped
        INNER JOIN reserva_habitacion rhab ON rhab.id_reserva = r.id_reserva
        INNER JOIN habitacion hab ON hab.id_habitacion = rhab.id_habitacion
    """

    condiciones = []
    parametros = []

    if filtro_texto:
        condiciones.append(
            "(h.nombre LIKE %s OR h.apellido LIKE %s OR CAST(r.id_reserva AS CHAR) LIKE %s)"
        )
        patron = f"%{filtro_texto}%"
        parametros.extend([patron, patron, patron])

    if estado:
        condiciones.append("r.estado_reserva = %s")
        parametros.append(estado)

    if condiciones:
        sql += " WHERE " + " AND ".join(condiciones)

    sql += " ORDER BY r.fecha_ingreso DESC"

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(sql, tuple(parametros))
        return cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Error al listar reservas: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)


def obtener_reserva_por_id(id_reserva):
    """Devuelve los datos de una reserva por su ID (para el formulario de edición)."""
    conexion = obtener_conexion()
    if not conexion:
        return None

    sql = """
        SELECT
            r.id_reserva, r.fecha_ingreso, r.fecha_salida,
            r.nro_personas, r.estado_reserva, r.precio_total,
            h.id_huesped, h.nombre, h.apellido, h.dni,
            hab.id_habitacion, hab.tipo_habitacion,
            hab.capacidad, hab.estado_habitacion,
            rhab.precio_noche_acordado
        FROM reserva r
        INNER JOIN reserva_huesped rh ON rh.id_reserva = r.id_reserva AND rh.rol = 'titular'
        INNER JOIN huesped h ON h.id_huesped = rh.id_huesped
        INNER JOIN reserva_habitacion rhab ON rhab.id_reserva = r.id_reserva
        INNER JOIN habitacion hab ON hab.id_habitacion = rhab.id_habitacion
        WHERE r.id_reserva = %s
    """
    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(sql, (id_reserva,))
        # Leer TODAS las filas (aunque solo usemos la primera)
        filas = cursor.fetchall()
        # Devolver la primera fila (o None si no hay)
        return filas[0] if filas else None
    except mysql.connector.Error as e:
        print(f"Error al obtener reserva: {e}")
        return None
    finally:
        if cursor:
            try:
                # Consumir cualquier resultado pendiente antes de cerrar
                cursor.fetchall()
            except Exception:
                pass
            cursor.close()
        cerrar_conexion(conexion)

def actualizar_reserva(id_reserva, id_huesped, id_habitacion, fecha_ingreso,
                       fecha_salida, precio_noche, nro_personas, estado_reserva,
                       id_habitacion_anterior=None):
    """
    Actualiza una reserva en las 3 tablas involucradas.
    id_habitacion_anterior: habitación que se está editando (la que tenía la
    reserva antes del cambio). Solo se modifica ESA fila de reserva_habitacion;
    las demás habitaciones de una reserva múltiple quedan intactas.
    """
    conexion = obtener_conexion()
    if not conexion:
        return False, "No se pudo conectar a la base de datos."

    cursor = None
    try:
        cursor = conexion.cursor()

        from datetime import datetime
        fi = datetime.strptime(fecha_ingreso, '%Y-%m-%d')
        fs = datetime.strptime(fecha_salida, '%Y-%m-%d')
        noches = (fs - fi).days

        # Habitación a modificar: la indicada, o la primera de la reserva
        if id_habitacion_anterior is None:
            cursor.execute(
                "SELECT MIN(id_habitacion) FROM reserva_habitacion WHERE id_reserva = %s",
                (id_reserva,))
            fila = cursor.fetchone()
            id_habitacion_anterior = fila[0] if fila else None
        if id_habitacion_anterior is None:
            return False, "La reserva no tiene ninguna habitación asociada."

        # Si se cambia a una habitación que ya tiene la misma reserva -> PK duplicada
        if int(id_habitacion) != int(id_habitacion_anterior):
            cursor.execute(
                "SELECT 1 FROM reserva_habitacion WHERE id_reserva = %s AND id_habitacion = %s",
                (id_reserva, id_habitacion))
            if cursor.fetchone():
                return False, (f"La reserva #{id_reserva} ya incluye la habitación "
                               f"#{id_habitacion}. Elija otra.")

        # Precio total = noches x (precio de la habitación editada + el de las demás)
        cursor.execute(
            """SELECT COALESCE(SUM(precio_noche_acordado), 0)
               FROM reserva_habitacion
               WHERE id_reserva = %s AND id_habitacion <> %s""",
            (id_reserva, id_habitacion_anterior))
        suma_otras = float(cursor.fetchone()[0])
        precio_total = noches * (float(precio_noche) + suma_otras)

        # Control de superposición (RN-01), salvo que quede cancelada
        if estado_reserva != 'cancelado':
            conflicto = buscar_conflicto_reserva(cursor, id_habitacion,
                                                 fecha_ingreso, fecha_salida,
                                                 id_reserva_excluida=id_reserva)
            if conflicto:
                return False, _mensaje_conflicto(id_habitacion, conflicto)

        cursor.execute("""
            UPDATE reserva
            SET fecha_ingreso = %s, fecha_salida = %s,
                nro_personas = %s, precio_total = %s, estado_reserva = %s
            WHERE id_reserva = %s
        """, (fecha_ingreso, fecha_salida, nro_personas,
              precio_total, estado_reserva, id_reserva))

        # Solo la fila de la habitación editada (antes cambiaba TODAS las filas)
        cursor.execute("""
            UPDATE reserva_habitacion
            SET precio_noche_acordado = %s, id_habitacion = %s
            WHERE id_reserva = %s AND id_habitacion = %s
        """, (precio_noche, id_habitacion, id_reserva, id_habitacion_anterior))

        cursor.execute("""
            UPDATE reserva_huesped
            SET id_huesped = %s
            WHERE id_reserva = %s AND rol = 'titular'
        """, (id_huesped, id_reserva))

        conexion.commit()
        return True, "Reserva actualizada correctamente."

    except mysql.connector.IntegrityError as e:
        conexion.rollback()
        if "La habitación ya está reservada" in str(e):
            return False, "La habitación ya está reservada en ese rango de fechas."
        return False, f"Error de integridad: {e.msg}"
    except mysql.connector.Error as e:
        conexion.rollback()
        if e.errno == 1644:  # SIGNAL del trigger anti doble reserva
            return False, "La habitación ya está reservada en ese rango de fechas."
        return False, f"Error de base de datos: {e}"
    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)


ID_USUARIO_ACTUAL = 1  # la app todavía no tiene login; mismo criterio que al crear reservas


def resumen_baja_reserva(id_reserva):
    """
    Resume lo que se perdería al eliminar una reserva (pagos y consumos), para
    mostrar el aviso antes de confirmar. Devuelve un dict o None si hay error.
    """
    conexion = obtener_conexion()
    if not conexion:
        return None
    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                COUNT(*) AS n_pagos,
                COALESCE(SUM(CASE WHEN estado_pago = 'aprobado'
                                  THEN total_pagado END), 0) AS monto_aprobado,
                COALESCE(SUM(CASE WHEN estado_pago = 'pendiente'
                                  THEN total_pagado END), 0) AS monto_pendiente
            FROM pago WHERE id_reserva = %s
        """, (id_reserva,))
        resumen = cursor.fetchone()
        cursor.execute("""
            SELECT COUNT(*) AS n_consumos,
                   COALESCE(SUM(cantidad * precio_unitario), 0) AS monto_consumos
            FROM consumo WHERE id_reserva = %s
        """, (id_reserva,))
        resumen.update(cursor.fetchone())
        return resumen
    except mysql.connector.Error as e:
        print(f"Error al resumir la baja de la reserva: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)


def resumen_registros_reserva(id_reserva):
    """
    Cuenta los pagos y consumos de una reserva (solo lectura) para avisar al
    administrador antes de eliminarla. Devuelve un dict o None si hay error.
    """
    conexion = obtener_conexion()
    if not conexion:
        return None
    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT COUNT(*) AS n_pagos,
                   COALESCE(SUM(CASE WHEN estado_pago = 'aprobado'
                                     THEN total_pagado END), 0) AS aprobado,
                   COALESCE(SUM(CASE WHEN estado_pago = 'pendiente'
                                     THEN total_pagado END), 0) AS pendiente
            FROM pago WHERE id_reserva = %s
        """, (id_reserva,))
        res = cursor.fetchone()
        cursor.execute("""
            SELECT COUNT(*) AS n_consumos,
                   COALESCE(SUM(cantidad * precio_unitario), 0) AS total_consumos
            FROM consumo WHERE id_reserva = %s
        """, (id_reserva,))
        res.update(cursor.fetchone())
        return res
    except mysql.connector.Error as e:
        print(f"Error al resumir registros de la reserva: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)


def eliminar_reserva(id_reserva, confirmado_con_registros=False,
                     id_usuario=ID_USUARIO_ACTUAL):
    """
    Elimina una reserva y sus asociaciones. Usa conexión ADMIN.

    Si la reserva tiene pagos o consumos, solo se elimina cuando el llamador
    indica confirmado_con_registros=True (la interfaz ya le mostró el aviso al
    administrador). En ese caso también se eliminan esos pagos y consumos.
    TODA baja deja un registro permanente en auditoria_accion, dentro de la
    misma transacción: si no se puede auditar, no se elimina nada.
    """
    conexion = obtener_conexion_admin()
    if not conexion:
        return False, "No se pudo conectar como administrador."

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT r.fecha_ingreso, r.fecha_salida, r.estado_reserva, r.precio_total,
                   hu.nombre, hu.apellido, hu.dni
            FROM reserva r
            LEFT JOIN reserva_huesped rhu
                   ON rhu.id_reserva = r.id_reserva AND rhu.rol = 'titular'
            LEFT JOIN huesped hu ON hu.id_huesped = rhu.id_huesped
            WHERE r.id_reserva = %s
        """, (id_reserva,))
        reserva = cursor.fetchone()
        if not reserva:
            return False, "La reserva no existe."

        cursor.execute("""
            SELECT COUNT(*) AS n,
                   COALESCE(SUM(CASE WHEN estado_pago = 'aprobado'
                                     THEN total_pagado END), 0) AS aprobado,
                   COALESCE(SUM(CASE WHEN estado_pago = 'pendiente'
                                     THEN total_pagado END), 0) AS pendiente
            FROM pago WHERE id_reserva = %s
        """, (id_reserva,))
        pagos = cursor.fetchone()
        cursor.execute("""
            SELECT COUNT(*) AS n,
                   COALESCE(SUM(cantidad * precio_unitario), 0) AS total
            FROM consumo WHERE id_reserva = %s
        """, (id_reserva,))
        consumos = cursor.fetchone()

        if (pagos['n'] > 0 or consumos['n'] > 0) and not confirmado_con_registros:
            return False, ("La reserva tiene pagos o consumos asociados. "
                           "Debe confirmarse la eliminación explícitamente.")

        detalle = (f"Reserva {reserva['estado_reserva']} del "
                   f"{reserva['fecha_ingreso'].strftime('%d/%m/%Y')} al "
                   f"{reserva['fecha_salida'].strftime('%d/%m/%Y')}, "
                   f"precio total ${reserva['precio_total']}. "
                   f"Pagos eliminados: {pagos['n']} "
                   f"(aprobado ${pagos['aprobado']}, pendiente ${pagos['pendiente']}). "
                   f"Consumos eliminados: {consumos['n']} (${consumos['total']}).")
        titular = (f"{reserva['nombre']} {reserva['apellido']}"
                   if reserva['nombre'] else None)

        # 1. Registro de auditoría (primero: si falla, no se elimina nada)
        cursor.execute("""
            INSERT INTO auditoria_accion
                (id_usuario, accion, entidad, id_entidad, titular, dni,
                 fecha_ingreso, fecha_salida, monto, detalle)
            VALUES (%s, 'ELIMINAR', 'reserva', %s, %s, %s, %s, %s, %s, %s)
        """, (id_usuario, id_reserva, titular, reserva['dni'],
              reserva['fecha_ingreso'], reserva['fecha_salida'],
              pagos['aprobado'], detalle))

        # 2. Desvincular consultas (la consulta se conserva, solo pierde el vínculo)
        cursor.execute("UPDATE consulta SET id_reserva = NULL WHERE id_reserva = %s",
                       (id_reserva,))

        # 3. Eliminar registros dependientes y la reserva
        cursor.execute("DELETE FROM pago WHERE id_reserva = %s", (id_reserva,))
        cursor.execute("DELETE FROM consumo WHERE id_reserva = %s", (id_reserva,))
        cursor.execute("DELETE FROM reserva_habitacion WHERE id_reserva = %s", (id_reserva,))
        cursor.execute("DELETE FROM reserva_huesped WHERE id_reserva = %s", (id_reserva,))
        cursor.execute("DELETE FROM reserva WHERE id_reserva = %s", (id_reserva,))

        conexion.commit()
        return True, "Reserva eliminada. La acción quedó registrada en la auditoría."

    except mysql.connector.ProgrammingError as e:
        conexion.rollback()
        if e.errno == 1146:  # tabla inexistente
            return False, ("No se eliminó nada: falta la tabla de auditoría. "
                           "Ejecute auditoria_mysql.sql en MySQL.")
        return False, f"Acceso denegado por el SGBD: {e}"
    except mysql.connector.IntegrityError:
        conexion.rollback()
        return False, "No se puede eliminar: la reserva tiene registros asociados."
    except Exception as e:
        conexion.rollback()
        return False, f"Error inesperado: {e}"
    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)


def listar_huespedes_para_combo():
    """
    Devuelve los huéspedes activos ordenados por fecha_creacion DESC
    (los más recientes primero). Pensado para llenar un desplegable.
    Retorna lista de dicts con id_huesped y nombre_completo.
    """
    conexion = obtener_conexion()
    if not conexion:
        return []

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT id_huesped, nombre, apellido, dni, fecha_creacion
            FROM huesped
            WHERE activo = 1
            ORDER BY fecha_creacion DESC, id_huesped DESC
        """)
        return cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Error al listar huéspedes para combo: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)
def listar_habitaciones_para_combo():
    """
    Devuelve las habitaciones que NO están en mantenimiento.
    Se excluyen las de mantenimiento porque según RN-09 no pueden reservarse.
    Retorna lista de dicts con id, tipo, capacidad, precio y estado.
    """
    conexion = obtener_conexion()
    if not conexion:
        return []

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT id_habitacion, tipo_habitacion, capacidad,
                   precio_noche, estado_habitacion
            FROM habitacion
            WHERE estado_habitacion != 'mantenimiento'
            ORDER BY id_habitacion
        """)
        return cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Error al listar habitaciones para combo: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)


def obtener_habitacion_por_id(id_habitacion):
    """
    Devuelve los datos de una habitación por su ID.
    (Si ya la tenés en acceso_datos.py, no la dupliques).
    """
    conexion = obtener_conexion()
    if not conexion:
        return None

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT id_habitacion, tipo_habitacion, capacidad,
                   precio_noche, estado_habitacion
            FROM habitacion
            WHERE id_habitacion = %s
        """, (id_habitacion,))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        print(f"Error al obtener habitación: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)


# ============================================================
# INICIO (DASHBOARD)
# Todas las cifras salen de la base y se calculan para la fecha "hoy"
# que recibe la función (la misma que muestra el reloj de la app).
# ============================================================

def obtener_resumen_dashboard(hoy=None):
    """
    Devuelve un diccionario con los indicadores del Inicio:
    ocupación, check-ins/outs de hoy, consultas pendientes, reservas por
    estado, saldo pendiente de cobro, cobrado en el mes y check-ins de la semana.
    Retorna None si no hay conexión.
    """
    conexion = obtener_conexion()
    if not conexion:
        return None

    hoy = hoy or date.today()
    lunes = hoy - timedelta(days=hoy.weekday())
    domingo = lunes + timedelta(days=6)
    primero_mes = hoy.replace(day=1)

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        r = {'hoy': hoy}

        # Habitaciones operativas y ocupadas hoy (estado efectivo)
        cursor.execute("""
            SELECT COUNT(*) AS n FROM habitacion h
            WHERE h.estado_habitacion <> 'mantenimiento'
        """)
        r['hab_operativas'] = cursor.fetchone()['n']

        cursor.execute(f"""
            SELECT COUNT(*) AS n FROM habitacion h
            WHERE ({SQL_ESTADO_EFECTIVO}) = 'ocupada'
        """, (hoy, hoy))
        r['hab_ocupadas'] = cursor.fetchone()['n']

        # Check-ins y check-outs de hoy (reservas no canceladas)
        cursor.execute("""
            SELECT COUNT(*) AS n FROM reserva
            WHERE fecha_ingreso = %s AND estado_reserva <> 'cancelado'
        """, (hoy,))
        r['checkins_hoy'] = cursor.fetchone()['n']

        cursor.execute("""
            SELECT COUNT(*) AS n FROM reserva
            WHERE fecha_salida = %s AND estado_reserva <> 'cancelado'
        """, (hoy,))
        r['checkouts_hoy'] = cursor.fetchone()['n']

        # Consultas sin responder
        cursor.execute("SELECT COUNT(*) AS n FROM consulta WHERE estado = 'Pendiente'")
        r['consultas_pendientes'] = cursor.fetchone()['n']

        # Reservas vigentes o futuras por estado
        cursor.execute("""
            SELECT estado_reserva, COUNT(*) AS n FROM reserva
            WHERE fecha_salida >= %s
            GROUP BY estado_reserva
        """, (hoy,))
        por_estado = {fila['estado_reserva']: fila['n'] for fila in cursor.fetchall()}
        r['reservas_pendientes'] = por_estado.get('pendiente', 0)
        r['reservas_confirmadas'] = por_estado.get('confirmado', 0)

        # Saldo pendiente de cobro (vista v_saldo_reserva, sin canceladas)
        cursor.execute("""
            SELECT COALESCE(SUM(saldo_pendiente), 0) AS total
            FROM v_saldo_reserva
            WHERE estado_reserva <> 'cancelado' AND saldo_pendiente > 0
        """)
        r['saldo_pendiente'] = cursor.fetchone()['total']

        # Cobrado en el mes (pagos aprobados)
        cursor.execute("""
            SELECT COALESCE(SUM(total_pagado), 0) AS total FROM pago
            WHERE estado_pago = 'aprobado' AND fecha_pago BETWEEN %s AND %s
        """, (primero_mes, hoy))
        r['cobrado_mes'] = cursor.fetchone()['total']

        # Check-ins de cada día de la semana actual (lunes a domingo)
        cursor.execute("""
            SELECT fecha_ingreso, COUNT(*) AS n FROM reserva
            WHERE fecha_ingreso BETWEEN %s AND %s AND estado_reserva <> 'cancelado'
            GROUP BY fecha_ingreso
        """, (lunes, domingo))
        por_dia = {fila['fecha_ingreso']: fila['n'] for fila in cursor.fetchall()}
        r['checkins_semana'] = [
            (lunes + timedelta(days=i), por_dia.get(lunes + timedelta(days=i), 0))
            for i in range(7)
        ]
        return r

    except mysql.connector.Error as e:
        print(f"Error al obtener el resumen del dashboard: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)


def listar_consultas_pendientes(limite=5):
    """Consultas sin responder, las más antiguas primero."""
    conexion = obtener_conexion()
    if not conexion:
        return []

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT id_consulta, fecha, remitente, medio, asunto
            FROM consulta
            WHERE estado = 'Pendiente'
            ORDER BY fecha ASC, id_consulta ASC
            LIMIT %s
        """, (int(limite),))
        return cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Error al listar consultas pendientes: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)


def listar_actividad_reciente(limite=5):
    """Últimas reservas registradas, con titular y habitaciones (JOIN)."""
    conexion = obtener_conexion()
    if not conexion:
        return []

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT r.id_reserva, r.estado_reserva, r.fecha_ingreso,
                   h.nombre, h.apellido,
                   GROUP_CONCAT(DISTINCT rh.id_habitacion
                                ORDER BY rh.id_habitacion SEPARATOR ', ') AS habitaciones
            FROM reserva r
            LEFT JOIN reserva_huesped rhu
                   ON rhu.id_reserva = r.id_reserva AND rhu.rol = 'titular'
            LEFT JOIN huesped h ON h.id_huesped = rhu.id_huesped
            LEFT JOIN reserva_habitacion rh ON rh.id_reserva = r.id_reserva
            GROUP BY r.id_reserva, r.estado_reserva, r.fecha_ingreso,
                     h.nombre, h.apellido
            ORDER BY r.id_reserva DESC
            LIMIT %s
        """, (int(limite),))
        return cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Error al listar actividad reciente: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)


def listar_habitaciones_ocupadas(hoy=None):
    """
    Habitaciones ocupadas hoy: con reserva confirmada vigente (ingreso <= hoy < salida)
    o marcadas manualmente como ocupadas. Incluye titular, fecha de check-out y
    saldo pendiente de la reserva (vista v_saldo_reserva).
    """
    conexion = obtener_conexion()
    if not conexion:
        return None

    hoy = hoy or date.today()
    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT h.id_habitacion, h.tipo_habitacion,
                   act.id_reserva, act.fecha_salida,
                   hu.nombre, hu.apellido, hu.dni,
                   v.saldo_pendiente
            FROM habitacion h
            LEFT JOIN (
                SELECT rh.id_habitacion, r.id_reserva, r.fecha_salida
                FROM reserva_habitacion rh
                INNER JOIN reserva r ON r.id_reserva = rh.id_reserva
                WHERE r.estado_reserva = 'confirmado'
                  AND r.fecha_ingreso <= %s
                  AND r.fecha_salida > %s
            ) act ON act.id_habitacion = h.id_habitacion
            LEFT JOIN reserva_huesped rhu
                   ON rhu.id_reserva = act.id_reserva AND rhu.rol = 'titular'
            LEFT JOIN huesped hu ON hu.id_huesped = rhu.id_huesped
            LEFT JOIN v_saldo_reserva v ON v.id_reserva = act.id_reserva
            WHERE h.estado_habitacion <> 'mantenimiento'
              AND (act.id_reserva IS NOT NULL OR h.estado_habitacion = 'ocupada')
            ORDER BY act.fecha_salida IS NULL, act.fecha_salida, h.id_habitacion
        """, (hoy, hoy))
        return cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Error al listar habitaciones ocupadas: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)


def obtener_auditoria_titulares(hoy=None, dias=60):
    """
    Movimientos de los titulares en los últimos `dias` días (hasta hoy inclusive):
    reservas registradas y modificadas, check-in, check-out, pagos y consumos.
    Une varias tablas con UNION ALL. Devuelve filas crudas (sin formato) o None
    si hubo un error.
    Seguridad en dos capas: la interfaz pide la contraseña de administrador y la
    consulta se ejecuta con el rol de administrador del SGBD (admin_gestarho).
    """
    conexion = obtener_conexion_admin()
    if not conexion:
        return None

    hoy = hoy or date.today()
    desde = hoy - timedelta(days=dias)

    base = """
        FROM reserva r
        LEFT JOIN reserva_huesped rhu
               ON rhu.id_reserva = r.id_reserva AND rhu.rol = 'titular'
        LEFT JOIN huesped hu ON hu.id_huesped = rhu.id_huesped
    """

    def parte(fecha, orden, tipo, monto, joins="", usuario=False,
              texto1="NULL", texto2="NULL", extra=""):
        u_nombre = "u.nombre" if usuario else "NULL"
        u_apellido = "u.apellido" if usuario else "NULL"
        return f"""
            SELECT {fecha} AS fecha, {orden} AS orden, '{tipo}' AS tipo,
                   r.id_reserva AS id_reserva, hu.nombre AS nombre,
                   hu.apellido AS apellido, hu.dni AS dni,
                   {u_nombre} AS u_nombre, {u_apellido} AS u_apellido,
                   {monto} AS monto, {texto1} AS texto1, {texto2} AS texto2,
                   r.fecha_ingreso AS f_ingreso, r.fecha_salida AS f_salida,
                   r.estado_reserva AS estado_reserva
            {base} {joins}
            WHERE {fecha} BETWEEN %s AND %s {extra}
        """

    partes = [
        parte("r.fecha_creacion", 1, "reserva", "r.precio_total",
              "LEFT JOIN usuario u ON u.id_usuario = r.id_usuario_creacion",
              usuario=True),
        parte("r.fecha_modificacion", 2, "modificacion", "r.precio_total"),
        parte("r.fecha_ingreso", 3, "checkin", "0",
              extra="AND r.estado_reserva <> 'cancelado'"),
        parte("p.fecha_pago", 4, "pago", "p.total_pagado",
              "INNER JOIN pago p ON p.id_reserva = r.id_reserva "
              "LEFT JOIN usuario u ON u.id_usuario = p.id_usuario_registro",
              usuario=True, texto1="p.metodo_pago", texto2="p.estado_pago"),
        parte("c.fecha_registro", 5, "consumo", "c.cantidad * c.precio_unitario",
              "INNER JOIN consumo c ON c.id_reserva = r.id_reserva "
              "INNER JOIN concepto_consumo cc ON cc.id_concepto = c.id_concepto "
              "LEFT JOIN usuario u ON u.id_usuario = c.id_usuario_registro",
              usuario=True, texto1="cc.nombre", texto2="c.cantidad"),
        parte("r.fecha_salida", 6, "checkout", "0",
              extra="AND r.estado_reserva <> 'cancelado'"),
    ]
    sql = " UNION ALL ".join(partes)
    parametros = []
    for _ in partes:
        parametros += [desde, hoy]

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(sql, tuple(parametros))
        filas = cursor.fetchall()
        # Bajas registradas en auditoria_accion (si la tabla aún no existe, se omiten)
        try:
            cursor.execute("""
                SELECT DATE(a.fecha_hora) AS fecha, 7 AS orden, 'eliminacion' AS tipo,
                       a.id_entidad AS id_reserva, COALESCE(a.titular, '') AS nombre,
                       '' AS apellido, a.dni AS dni,
                       u.nombre AS u_nombre, u.apellido AS u_apellido,
                       a.monto AS monto, a.detalle AS texto1, NULL AS texto2,
                       COALESCE(a.fecha_ingreso, DATE(a.fecha_hora)) AS f_ingreso,
                       COALESCE(a.fecha_salida, DATE(a.fecha_hora)) AS f_salida,
                       'eliminado' AS estado_reserva
                FROM auditoria_accion a
                LEFT JOIN usuario u ON u.id_usuario = a.id_usuario
                WHERE a.entidad = 'reserva' AND DATE(a.fecha_hora) BETWEEN %s AND %s
            """, (desde, hoy))
            filas += cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Aviso: no se leyó auditoria_accion ({e})")
        filas.sort(key=lambda f: (f['fecha'], f['id_reserva'], f['orden']),
                   reverse=True)
        return filas
    except mysql.connector.Error as e:
        print(f"Error al obtener la auditoría: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)
        
# ============================================================
# CONSULTAS - CRUD
# ============================================================
def listar_consultas(filtro_texto=None, estado=None, fecha_desde=None, fecha_hasta=None):
    """
    Devuelve las consultas aplicando filtros opcionales.
    Filtra por remitente/asunto (LIKE), estado exacto y rango de fechas.
    """
    conexion = obtener_conexion()
    if not conexion:
        return []

    sql = """
        SELECT id_consulta, fecha, remitente, medio, asunto,
               estado, id_reserva, id_usuario_asignado, fecha_creacion
        FROM consulta
        WHERE 1=1
    """
    parametros = []
    if filtro_texto:
        sql += " AND (remitente LIKE %s OR asunto LIKE %s)"
        patron = f"%{filtro_texto}%"
        parametros.extend([patron, patron])
    if estado:
        sql += " AND estado = %s"
        parametros.append(estado)
    if fecha_desde:
        sql += " AND fecha >= %s"
        parametros.append(fecha_desde)
    if fecha_hasta:
        sql += " AND fecha <= %s"
        parametros.append(fecha_hasta)
    sql += " ORDER BY fecha DESC, id_consulta DESC"

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(sql, tuple(parametros))
        return cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Error al listar consultas: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)


def obtener_consulta_por_id(id_consulta):
    """Devuelve los datos de una consulta por su ID."""
    conexion = obtener_conexion()
    if not conexion:
        return None

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT id_consulta, fecha, remitente, medio, asunto,
                   estado, id_reserva, id_usuario_asignado, fecha_creacion
            FROM consulta
            WHERE id_consulta = %s
        """, (id_consulta,))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        print(f"Error al obtener consulta: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)


def insertar_consulta(fecha, remitente, medio, asunto, estado,
                      id_reserva=None, id_usuario_asignado=None):
    """
    Inserta una consulta nueva.
    Retorna (True, "mensaje") o (False, "mensaje de error").
    """
    conexion = obtener_conexion()
    if not conexion:
        return False, "No se pudo conectar a la base de datos."

    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO consulta
                (fecha, remitente, medio, asunto, estado,
                 id_reserva, id_usuario_asignado, fecha_creacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, CURDATE())
        """, (fecha, remitente, medio, asunto, estado,
              id_reserva, id_usuario_asignado))
        conexion.commit()
        return True, f"Consulta #{cursor.lastrowid} registrada correctamente."

    except mysql.connector.IntegrityError as e:
        conexion.rollback()
        return False, f"Los datos no cumplen las restricciones de la base: {e.msg}"
    except mysql.connector.Error as e:
        conexion.rollback()
        return False, f"Error de base de datos: {e}"
    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)


def actualizar_consulta(id_consulta, fecha, remitente, medio, asunto, estado,
                        id_reserva=None, id_usuario_asignado=None):
    """
    Actualiza una consulta existente.
    Retorna (True, "mensaje") o (False, "mensaje de error").
    """
    conexion = obtener_conexion()
    if not conexion:
        return False, "No se pudo conectar a la base de datos."

    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE consulta
            SET fecha = %s, remitente = %s, medio = %s, asunto = %s,
                estado = %s, id_reserva = %s, id_usuario_asignado = %s
            WHERE id_consulta = %s
        """, (fecha, remitente, medio, asunto, estado,
              id_reserva, id_usuario_asignado, id_consulta))
        conexion.commit()
        return True, "Consulta actualizada correctamente."

    except mysql.connector.IntegrityError as e:
        conexion.rollback()
        return False, f"Los datos no cumplen las restricciones de la base: {e.msg}"
    except mysql.connector.Error as e:
        conexion.rollback()
        return False, f"Error de base de datos: {e}"
    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)
def eliminar_consulta(id_consulta):
    """
    Elimina una consulta. Usa conexión ADMIN (recepcionista no tiene DELETE).
    Retorna (True, "mensaje") o (False, "mensaje de error").
    """
    conexion = obtener_conexion_admin()
    if not conexion:
        return False, "No se pudo conectar como administrador."

    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM consulta WHERE id_consulta = %s",
                       (id_consulta,))
        conexion.commit()
        return True, "Consulta eliminada correctamente."

    except mysql.connector.IntegrityError:
        conexion.rollback()
        return False, "No se puede eliminar: la consulta tiene registros asociados."
    except mysql.connector.ProgrammingError as e:
        conexion.rollback()
        return False, f"Acceso denegado por el SGBD: {e}"
    except mysql.connector.Error as e:
        conexion.rollback()
        return False, f"Error de base de datos: {e}"
    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)


def obtener_cuenta_por_dni_o_reserva(criterio):
    """Busca una reserva por DNI o por N° de Reserva (ID) y arma el paquete de datos."""
    conexion = obtener_conexion()
    if not conexion:
        return None

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        
        sql_reserva = """
            SELECT r.id_reserva, r.precio_total, r.fecha_ingreso, r.fecha_salida,
                   h.nombre, h.apellido, hab.id_habitacion, hab.tipo_habitacion
            FROM reserva r
            INNER JOIN reserva_huesped rh ON rh.id_reserva = r.id_reserva AND rh.rol = 'titular'
            INNER JOIN huesped h ON h.id_huesped = rh.id_huesped
            INNER JOIN reserva_habitacion rhab ON rhab.id_reserva = r.id_reserva
            INNER JOIN habitacion hab ON hab.id_habitacion = rhab.id_habitacion
            WHERE h.dni = %s OR r.id_reserva = %s
            LIMIT 1
        """
        cursor.execute(sql_reserva, (criterio, criterio))
        res = cursor.fetchone()
        
        if not res:
            return None
            
        id_reserva = res['id_reserva']

        # Pagos
        cursor.execute("""
            SELECT fecha_pago AS fecha, metodo_pago AS metodo, total_pagado AS monto
            FROM pago WHERE id_reserva = %s
            ORDER BY fecha_pago DESC
        """, (id_reserva,))
        pagos = cursor.fetchall()
        for p in pagos:
            if hasattr(p['fecha'], 'strftime'):
                p['fecha'] = p['fecha'].strftime('%d/%m/%Y')

        # Consumos
        cursor.execute("""
            SELECT cc.nombre AS concepto, c.cantidad, c.precio_unitario
            FROM consumo c
            INNER JOIN concepto_consumo cc ON cc.id_concepto = c.id_concepto
            WHERE c.id_reserva = %s
        """, (id_reserva,))
        consumos = cursor.fetchall()

        return {
            "id_reserva": id_reserva,
            "confirmacion": str(id_reserva),
            "huespede": f"{res['nombre']} {res['apellido']}",
            "habitacion": f"{res['id_habitacion']} ({res['tipo_habitacion'].capitalize()})",
            "check_in": res['fecha_ingreso'].strftime('%d/%m/%Y'),
            "check_out": res['fecha_salida'].strftime('%d/%m/%Y'),
            "total_estadia": float(res['precio_total']),
            "pagos": pagos,
            "consumos": consumos
        }
    except Exception as e:
        print(f"Error al buscar cuenta: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        cerrar_conexion(conexion)


def insertar_pago_bd(id_reserva, monto, metodo):
    """Guarda un pago en la base de datos."""
    conexion = obtener_conexion()
    if not conexion:
        return False
    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO pago (id_reserva, fecha_pago, total_pagado, metodo_pago, estado_pago, id_usuario_registro)
            VALUES (%s, CURDATE(), %s, %s, 'aprobado', 1)
        """, (id_reserva, monto, metodo))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al guardar pago: {e}")
        return False
    finally:
        if cursor: cursor.close()
        cerrar_conexion(conexion)


def insertar_consumo_bd(id_reserva, concepto, cantidad, precio):
    """Guarda un consumo (creando el concepto si no existe) en la base de datos."""
    conexion = obtener_conexion()
    if not conexion:
        return False
    cursor = None
    try:
        cursor = conexion.cursor()
        
        # 1. Verificar si el concepto existe, si no, crearlo
        cursor.execute("SELECT id_concepto FROM concepto_consumo WHERE nombre = %s", (concepto,))
        row = cursor.fetchone()
        
        if row:
            id_concepto = row[0]
        else:
            cursor.execute("INSERT INTO concepto_consumo (nombre, precio_unitario) VALUES (%s, %s)", (concepto, precio))
            id_concepto = cursor.lastrowid
            
        # 2. Insertar el consumo
        cursor.execute("""
            INSERT INTO consumo (id_reserva, id_concepto, cantidad, precio_unitario, id_usuario_registro)
            VALUES (%s, %s, %s, %s, 1)
        """, (id_reserva, id_concepto, cantidad, precio))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al guardar consumo: {e}")
        return False
    finally:
        if cursor: cursor.close()
        cerrar_conexion(conexion)
