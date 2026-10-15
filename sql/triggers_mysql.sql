-- ============================================================
-- TRIGGERS - GestARHO (MySQL 8.0)
-- Trigger que impide reservar dos veces la misma habitación
-- en fechas superpuestas (RN-01)
-- ============================================================

USE gestarho;

DROP TRIGGER IF EXISTS trg_no_doble_reserva;

DELIMITER //

CREATE TRIGGER trg_no_doble_reserva
BEFORE INSERT ON reserva_habitacion
FOR EACH ROW
BEGIN
    DECLARE v_conflicto INT;
    
    SELECT COUNT(*) INTO v_conflicto
    FROM reserva_habitacion rh
    INNER JOIN reserva r ON rh.id_reserva = r.id_reserva
    INNER JOIN reserva rn ON rn.id_reserva = NEW.id_reserva
    WHERE rh.id_habitacion = NEW.id_habitacion
      AND r.estado_reserva != 'cancelado'
      AND rn.estado_reserva != 'cancelado'
      AND r.fecha_ingreso < rn.fecha_salida
      AND r.fecha_salida > rn.fecha_ingreso;
    
    IF v_conflicto > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La habitación ya está reservada en ese rango de fechas';
    END IF;
END //

DELIMITER ;
USE gestarho;
SHOW TRIGGERS;