"""
Módulo de conexión a la base de datos MySQL.
GestARHO - Sistema de Gestión Hotelera.
"""

import mysql.connector
from mysql.connector import Error


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