"""
Módulo de conexión a la base de datos MySQL.
GestARHO - Sistema de Gestión Hotelera.
"""

import mysql.connector
from mysql.connector import Error

# Contraseña que pide la aplicación antes de un borrado definitivo.
# (Solo para desarrollo/prueba: en un sistema real no debe estar en el código.)
PASSWORD_ADMIN_APP = "Admin2026!"


def verificar_password_admin(password):
    """True si la contraseña ingresada coincide con la de administrador de la app."""
    return password == PASSWORD_ADMIN_APP


def obtener_conexion():
    """
    Conexión como recepcionista (rol por defecto).
    Tiene SELECT en todas las tablas e INSERT/UPDATE en tablas operativas.
    NO puede hacer DELETE.
    """
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='recepcionista_user',
            password='Recep2026!',
            database='gestarho'
        )
        return conexion
    except Error as e:
        print(f"Error al conectar (recepcionista): {e}")
        return None


def obtener_conexion_admin():
    """
    Conexión como administrador.
    Se usa SOLO para operaciones críticas (ej: DELETE definitivo).
    """
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='admin_user',
            password='Admin2026!',
            database='gestarho'
        )
        return conexion
    except Error as e:
        print(f"Error al conectar (admin): {e}")
        return None


def cerrar_conexion(conexion):
    """Cierra la conexión si está abierta."""
    if conexion and conexion.is_connected():
        conexion.close()