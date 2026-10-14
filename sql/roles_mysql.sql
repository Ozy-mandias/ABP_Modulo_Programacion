USE gestarho;

-- ============================================================
-- ROLES Y PERMISOS - GestARHO (MySQL)
-- ============================================================

-- Rol 1: Administrador (acceso total)
CREATE ROLE IF NOT EXISTS 'admin_gestarho';
GRANT ALL PRIVILEGES ON gestarho.* TO 'admin_gestarho';

-- Rol 2: Recepcionista (solo lectura + escritura operativa)
CREATE ROLE IF NOT EXISTS 'recepcionista_gestarho';

-- Puede consultar TODAS las tablas
GRANT SELECT ON gestarho.* TO 'recepcionista_gestarho';

-- Puede insertar y modificar en tablas operativas
GRANT INSERT, UPDATE ON gestarho.huesped TO 'recepcionista_gestarho';
GRANT INSERT, UPDATE ON gestarho.reserva TO 'recepcionista_gestarho';
GRANT INSERT, UPDATE ON gestarho.reserva_huesped TO 'recepcionista_gestarho';
GRANT INSERT, UPDATE ON gestarho.reserva_habitacion TO 'recepcionista_gestarho';
GRANT INSERT, UPDATE ON gestarho.pago TO 'recepcionista_gestarho';
GRANT INSERT, UPDATE ON gestarho.consumo TO 'recepcionista_gestarho';
GRANT INSERT, UPDATE ON gestarho.consulta TO 'recepcionista_gestarho';

-- NO puede modificar: usuario, habitacion, concepto_consumo

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

SHOW GRANTS FOR 'admin_user'@'localhost';
SHOW GRANTS FOR 'recepcionista_user'@'localhost';