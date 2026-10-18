-- ============================================================
-- AUDITORÍA DE ACCIONES - GestARHO (MySQL 8.0)
-- Cubre RF-20 "Registrar auditoría de acciones".
-- Guarda un registro PERMANENTE de acciones destructivas (hoy: baja de
-- reservas). No depende de las tablas operativas: si la reserva se elimina,
-- el registro queda con una copia de sus datos.
-- Ejecutar con un usuario con permisos de DDL (root / admin).
-- El rol admin_gestarho ya tiene ALL sobre gestarho.* (cubre esta tabla);
-- el recepcionista solo la puede consultar (SELECT sobre gestarho.*).
-- ============================================================

USE gestarho;

CREATE TABLE IF NOT EXISTS auditoria_accion (
    id_auditoria  INT AUTO_INCREMENT PRIMARY KEY,
    fecha_hora    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_usuario    INT           NOT NULL,
    accion        VARCHAR(40)   NOT NULL,
    entidad       VARCHAR(30)   NOT NULL,
    id_entidad    INT           NOT NULL,
    titular       VARCHAR(150)  NULL,
    dni           VARCHAR(20)   NULL,
    fecha_ingreso DATE          NULL,
    fecha_salida  DATE          NULL,
    monto         DECIMAL(12,2) NOT NULL DEFAULT 0,
    detalle       TEXT          NOT NULL,
    KEY idx_auditoria_fecha (fecha_hora),
    CONSTRAINT fk_auditoria_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuario (id_usuario)
);

SHOW CREATE TABLE auditoria_accion;
