USE gestarho;

-- ============================================================
-- ROLES Y PERMISOS - GestARHO (MySQL 8)
-- Actualizado: incluye la tabla auditoria_accion (RF-20).
-- Requisito previo: haber ejecutado auditoria_mysql.sql (crea la tabla).
-- Ejecutar con un usuario con privilegios de administración (root).
-- Se puede volver a ejecutar sin problema (deja los permisos en el estado final).
-- ============================================================

-- Rol 1: Administrador (acceso total, incluida auditoria_accion)
CREATE ROLE IF NOT EXISTS 'admin_gestarho';
GRANT ALL PRIVILEGES ON gestarho.* TO 'admin_gestarho';

-- Rol 2: Recepcionista (lectura + escritura operativa)
CREATE ROLE IF NOT EXISTS 'recepcionista_gestarho';

-- Se parte de cero para que no queden permisos viejos (por ejemplo el
-- SELECT sobre gestarho.* que incluía auditoria_accion).
REVOKE ALL PRIVILEGES, GRANT OPTION FROM 'recepcionista_gestarho';

-- Puede consultar las tablas operativas, una por una.
-- auditoria_accion queda FUERA a propósito: es un registro del administrador.
GRANT SELECT ON gestarho.usuario            TO 'recepcionista_gestarho';
GRANT SELECT ON gestarho.huesped            TO 'recepcionista_gestarho';
GRANT SELECT ON gestarho.habitacion         TO 'recepcionista_gestarho';
GRANT SELECT ON gestarho.reserva            TO 'recepcionista_gestarho';
GRANT SELECT ON gestarho.reserva_huesped    TO 'recepcionista_gestarho';
GRANT SELECT ON gestarho.reserva_habitacion TO 'recepcionista_gestarho';
GRANT SELECT ON gestarho.pago               TO 'recepcionista_gestarho';
GRANT SELECT ON gestarho.consumo            TO 'recepcionista_gestarho';
GRANT SELECT ON gestarho.concepto_consumo   TO 'recepcionista_gestarho';
GRANT SELECT ON gestarho.consulta           TO 'recepcionista_gestarho';
GRANT SELECT ON gestarho.v_saldo_reserva    TO 'recepcionista_gestarho';

-- Puede insertar y modificar en tablas operativas
GRANT INSERT, UPDATE ON gestarho.huesped            TO 'recepcionista_gestarho';
GRANT INSERT, UPDATE ON gestarho.reserva            TO 'recepcionista_gestarho';
GRANT INSERT, UPDATE ON gestarho.reserva_huesped    TO 'recepcionista_gestarho';
GRANT INSERT, UPDATE ON gestarho.reserva_habitacion TO 'recepcionista_gestarho';
GRANT INSERT, UPDATE ON gestarho.pago               TO 'recepcionista_gestarho';
GRANT INSERT, UPDATE ON gestarho.consumo            TO 'recepcionista_gestarho';
GRANT INSERT, UPDATE ON gestarho.consulta           TO 'recepcionista_gestarho';

-- El recepcionista NO puede:
--   * modificar usuario, habitacion ni concepto_consumo
--   * eliminar registros en ninguna tabla (no tiene DELETE)
--   * ver ni escribir auditoria_accion. Las bajas se auditan desde la app
--     con la conexión de administrador, tras validar la contraseña.

-- ============================================================
-- USUARIOS DE PRUEBA
-- ============================================================

CREATE USER IF NOT EXISTS 'admin_user'@'localhost'
    IDENTIFIED BY 'Admin2026!';
GRANT 'admin_gestarho' TO 'admin_user'@'localhost';
SET DEFAULT ROLE 'admin_gestarho' TO 'admin_user'@'localhost';

CREATE USER IF NOT EXISTS 'recepcionista_user'@'localhost'
    IDENTIFIED BY 'Recep2026!';
GRANT 'recepcionista_gestarho' TO 'recepcionista_user'@'localhost';
SET DEFAULT ROLE 'recepcionista_gestarho' TO 'recepcionista_user'@'localhost';

-- ============================================================
-- VERIFICACIÓN
-- ============================================================

SHOW GRANTS FOR 'admin_user'@'localhost' USING 'admin_gestarho';
SHOW GRANTS FOR 'recepcionista_user'@'localhost' USING 'recepcionista_gestarho';

-- Prueba sugerida (conectado como recepcionista_user):
--   SELECT * FROM auditoria_accion;   -- debe dar error 1142 (SELECT denegado)
--   DELETE FROM reserva WHERE id_reserva = 0;  -- debe dar error 1142 (DELETE denegado)
-- Conectado como admin_user:
--   SELECT * FROM auditoria_accion;   -- debe funcionar
