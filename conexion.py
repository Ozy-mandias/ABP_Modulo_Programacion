"""
Módulo de conexión a la base de datos MySQL.
GestARHO - Sistema de Gestión Hotelera.
"""

import mysql.connector
from mysql.connector import Error


def obtener_conexion():
    """
    Devuelve una conexión activa a la base de datos gestarho.
    Retorna None si la conexión falla.
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
        print(f"Error al conectar a MySQL: {e}")
        return None


def cerrar_conexion(conexion):
    """Cierra la conexión si está abierta."""
    if conexion and conexion.is_connected():
        conexion.close()