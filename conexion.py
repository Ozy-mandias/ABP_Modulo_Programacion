"""
Módulo de conexión a la base de datos MySQL de forma segura.
GestARHO - Sistema de Gestión Hotelera.
"""

import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def verificar_password_admin(password):
    """True si la contraseña ingresada coincide con la de administrador de la app desde el entorno."""
    return password == os.getenv("APP_SUPER_ADMIN_KEY")


def obtener_conexion():
    """
    Conexión como recepcionista (rol por defecto).
    Tiene SELECT en todas las tablas e INSERT/UPDATE en tablas operativas.
    NO puede hacer DELETE.
    """
    try:
        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER_RECEP"),
            password=os.getenv("DB_PASS_RECEP"),
            database=os.getenv("DB_NAME")
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
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER_ADMIN"),
            password=os.getenv("DB_PASS_ADMIN"),
            database=os.getenv("DB_NAME")
        )
        return conexion
    except Error as e:
        print(f"Error al conectar (admin): {e}")
        return None


def cerrar_conexion(conexion):
    """Cierra la conexión si está abierta."""
    if conexion and conexion.is_connected():
        conexion.close()
