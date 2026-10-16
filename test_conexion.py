"""
Script para probar la conexión a MySQL.
Ejecutar con: python test_conexion.py
"""

from conexion import obtener_conexion, cerrar_conexion

print("=" * 50)
print("PROBANDO CONEXIÓN A MYSQL")
print("=" * 50)

conexion = obtener_conexion()

if conexion:
    print("✅ Conexión exitosa a la base gestarho")
    
    cursor = conexion.cursor()
    
    # Probar consulta simple
    cursor.execute("SELECT COUNT(*) FROM huesped")
    cantidad_huespedes = cursor.fetchone()[0]
    print(f"Huéspedes en la base: {cantidad_huespedes}")
    
    cursor.execute("SELECT COUNT(*) FROM habitacion")
    cantidad_habitaciones = cursor.fetchone()[0]
    print(f" Habitaciones en la base: {cantidad_habitaciones}")
    
    cursor.execute("SELECT COUNT(*) FROM reserva")
    cantidad_reservas = cursor.fetchone()[0]
    print(f" Reservas en la base: {cantidad_reservas}")
    
    cursor.close()
    cerrar_conexion(conexion)
    
    print("=" * 50)
    print(" TODO FUNCIONA CORRECTAMENTE")
    print("=" * 50)
else:
    print(" No se pudo conectar a MySQL")
    print("Verificar:")
    print("  - MySQL Server está corriendo")
    print("  - Usuario/contraseña correctos")
    print("  - Base gestarho existe")