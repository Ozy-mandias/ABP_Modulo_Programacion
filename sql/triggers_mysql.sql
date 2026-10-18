-- ============================================================
-- TRIGGERS - GestARHO (MySQL 8.0)
-- Impiden reservar dos veces la misma habitación en fechas
-- superpuestas (RN-01), tanto al crear como al modificar.
-- Regla: hay conflicto si  otra.ingreso < nueva.salida
--                      Y   otra.salida  > nueva.ingreso
-- (el día de salida de una reserva puede ser el ingreso de otra).
-- Las reservas 'cancelado' no bloquean la habitación.
-- ============================================================

USE gestarho;

DROP TRIGGER IF EXISTS trg_no_doble_reserva;
DROP TRIGGER IF EXISTS trg_no_doble_reserva_upd;
DROP TRIGGER IF EXISTS trg_no_doble_reserva_fechas;

DELIMITER //

-- 1) Al asignar una habitación a una reserva (INSERT)
CREATE TRIGGER trg_no_doble_reserva
BEFORE INSERT ON reserva_habitacion
FOR EACH ROW
BEGIN
    DECLARE v_conflicto INT;

    SELECT COUNT(*) INTO v_conflicto
    FROM reserva_habitacion rh
    INNER JOIN reserva r  ON rh.id_reserva = r.id_reserva
    INNER JOIN reserva rn ON rn.id_reserva = NEW.id_reserva
    WHERE rh.id_habitacion = NEW.id_habitacion
      AND rh.id_reserva <> NEW.id_reserva
      AND r.estado_reserva  <> 'cancelado'
      AND rn.estado_reserva <> 'cancelado'
      AND r.fecha_ingreso < rn.fecha_salida
      AND r.fecha_salida  > rn.fecha_ingreso;

    IF v_conflicto > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La habitación ya está reservada en ese rango de fechas';
    END IF;
END //

-- 2) Al cambiar de habitación una reserva existente (UPDATE)
CREATE TRIGGER trg_no_doble_reserva_upd
BEFORE UPDATE ON reserva_habitacion
FOR EACH ROW
BEGIN
    DECLARE v_conflicto INT;

    SELECT COUNT(*) INTO v_conflicto
    FROM reserva_habitacion rh
    INNER JOIN reserva r  ON rh.id_reserva = r.id_reserva
    INNER JOIN reserva rn ON rn.id_reserva = NEW.id_reserva
    WHERE rh.id_habitacion = NEW.id_habitacion
      AND rh.id_reserva <> NEW.id_reserva
      AND r.estado_reserva  <> 'cancelado'
      AND rn.estado_reserva <> 'cancelado'
      AND r.fecha_ingreso < rn.fecha_salida
      AND r.fecha_salida  > rn.fecha_ingreso;

    IF v_conflicto > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La habitación ya está reservada en ese rango de fechas';
    END IF;
END //

-- 3) Al cambiar fechas o estado de la reserva (UPDATE sobre reserva)
CREATE TRIGGER trg_no_doble_reserva_fechas
BEFORE UPDATE ON reserva
FOR EACH ROW
BEGIN
    DECLARE v_conflicto INT;

    IF NEW.estado_reserva <> 'cancelado' THEN
        SELECT COUNT(*) INTO v_conflicto
        FROM reserva_habitacion mia
        INNER JOIN reserva_habitacion otra
                ON otra.id_habitacion = mia.id_habitacion
               AND otra.id_reserva <> mia.id_reserva
        INNER JOIN reserva r ON r.id_reserva = otra.id_reserva
        WHERE mia.id_reserva = NEW.id_reserva
          AND r.estado_reserva <> 'cancelado'
          AND r.fecha_ingreso < NEW.fecha_salida
          AND r.fecha_salida  > NEW.fecha_ingreso;

        IF v_conflicto > 0 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'La habitación ya está reservada en ese rango de fechas';
        END IF;
    END IF;
END //

DELIMITER ;

SHOW TRIGGERS;
