"""
Módulo de acceso a datos de GestARHO.
Contiene todas las funciones que ejecutan sentencias SQL
sobre la base de datos MySQL.
"""

import mysql.connector
from conexion import obtener_conexion, cerrar_conexion


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
    Falla si el huésped tiene reservas asociadas.
    Retorna (True, "mensaje") o (False, "mensaje de error").
    """
    conexion = obtener_conexion()
    if not conexion:
        return False, "No se pudo conectar a la base de datos."

    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM huesped WHERE id_huesped = %s", (id_huesped,))
        conexion.commit()
        return True, "Huésped eliminado permanentemente."
    except mysql.connector.IntegrityError:
        conexion.rollback()
        return False, ("No se puede eliminar: el huésped tiene reservas asociadas. "
                       "Primero eliminá esas reservas o dejanlo dado de baja.")
    except Exception as e:
        conexion.rollback()
        return False, f"Error inesperado: {e}"
    finally:
        cursor.close()
        cerrar_conexion(conexion)