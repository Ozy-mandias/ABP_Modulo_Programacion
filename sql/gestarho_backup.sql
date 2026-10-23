-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: gestarho
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auditoria_accion`
--

DROP TABLE IF EXISTS `auditoria_accion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auditoria_accion` (
  `id_auditoria` int NOT NULL AUTO_INCREMENT,
  `fecha_hora` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `id_usuario` int NOT NULL,
  `accion` varchar(40) NOT NULL,
  `entidad` varchar(30) NOT NULL,
  `id_entidad` int NOT NULL,
  `titular` varchar(150) DEFAULT NULL,
  `dni` varchar(20) DEFAULT NULL,
  `fecha_ingreso` date DEFAULT NULL,
  `fecha_salida` date DEFAULT NULL,
  `monto` decimal(12,2) NOT NULL DEFAULT '0.00',
  `detalle` text NOT NULL,
  PRIMARY KEY (`id_auditoria`),
  KEY `idx_auditoria_fecha` (`fecha_hora`),
  KEY `fk_auditoria_usuario` (`id_usuario`),
  CONSTRAINT `fk_auditoria_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auditoria_accion`
--

LOCK TABLES `auditoria_accion` WRITE;
/*!40000 ALTER TABLE `auditoria_accion` DISABLE KEYS */;
/*!40000 ALTER TABLE `auditoria_accion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `concepto_consumo`
--

DROP TABLE IF EXISTS `concepto_consumo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `concepto_consumo` (
  `id_concepto` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(200) DEFAULT NULL,
  `tipo` varchar(20) NOT NULL,
  `activo` tinyint NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_concepto`),
  UNIQUE KEY `nombre` (`nombre`),
  CONSTRAINT `chk_concepto_activo` CHECK ((`activo` in (0,1))),
  CONSTRAINT `chk_concepto_tipo` CHECK ((`tipo` in (_utf8mb4'producto',_utf8mb4'servicio')))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `concepto_consumo`
--

LOCK TABLES `concepto_consumo` WRITE;
/*!40000 ALTER TABLE `concepto_consumo` DISABLE KEYS */;
INSERT INTO `concepto_consumo` VALUES (1,'Minibar','Bebidas y snacks de la heladera','producto',1),(2,'Restaurante','Comidas y cenas','servicio',1),(3,'Lavandería','Servicio de lavado y planchado','servicio',1),(4,'Cochera','Estacionamiento cubierto','servicio',1),(5,'Spa','Servicios de spa y masajes','servicio',1),(6,'Servicio de pileta','Acceso a la pileta del hotel','servicio',1),(7,'Room service','Servicio a la habitación','servicio',1),(8,'Bar','Bebidas alcohólicas y sin alcohol','producto',1),(9,'Wi-Fi premium','Internet de alta velocidad','servicio',1),(10,'Cuna','Alquiler de cuna para bebés','producto',1);
/*!40000 ALTER TABLE `concepto_consumo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `consulta`
--

DROP TABLE IF EXISTS `consulta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `consulta` (
  `id_consulta` int NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `remitente` varchar(100) NOT NULL,
  `medio` varchar(30) NOT NULL,
  `asunto` text NOT NULL,
  `estado` varchar(20) NOT NULL DEFAULT 'Pendiente',
  `id_reserva` int DEFAULT NULL,
  `id_usuario_asignado` int DEFAULT NULL,
  `fecha_creacion` date NOT NULL DEFAULT (curdate()),
  PRIMARY KEY (`id_consulta`),
  KEY `fk_consulta_reserva` (`id_reserva`),
  KEY `fk_consulta_usuario` (`id_usuario_asignado`),
  KEY `idx_consulta_estado` (`estado`),
  CONSTRAINT `fk_consulta_reserva` FOREIGN KEY (`id_reserva`) REFERENCES `reserva` (`id_reserva`),
  CONSTRAINT `fk_consulta_usuario` FOREIGN KEY (`id_usuario_asignado`) REFERENCES `usuario` (`id_usuario`),
  CONSTRAINT `chk_consulta_estado` CHECK ((`estado` in (_utf8mb4'Pendiente',_utf8mb4'Terminado',_utf8mb4'Archivado'))),
  CONSTRAINT `chk_consulta_medio` CHECK ((`medio` in (_utf8mb4'WhatsApp',_utf8mb4'Web',_utf8mb4'Telefono',_utf8mb4'Email')))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consulta`
--

LOCK TABLES `consulta` WRITE;
/*!40000 ALTER TABLE `consulta` DISABLE KEYS */;
INSERT INTO `consulta` VALUES (1,'2026-09-30','María López','WhatsApp','Disponibilidad para fin de semana largo','Pendiente',NULL,2,'2026-10-15'),(2,'2026-10-01','Marcos Rivas','Web','Horario de check-in de la reserva','Terminado',1,2,'2026-10-15'),(3,'2026-10-02','Laura Gómez','Telefono','Tarifas de habitación familiar','Archivado',NULL,1,'2026-10-15'),(4,'2026-10-03','Valeria Bustos','Email','Solicitud de late check-out','Terminado',2,4,'2026-10-15'),(5,'2026-10-05','Carlos Medina','WhatsApp','Consulta si admiten mascotas pequeñas','Pendiente',NULL,5,'2026-10-15'),(6,'2026-10-06','Camila Soria','Telefono','Consulta por factura de la reserva','Pendiente',4,3,'2026-10-15'),(7,'2026-10-08','Roberto Ibáñez','Web','Consulta por cochera para una camioneta','Terminado',NULL,4,'2026-10-15'),(8,'2026-10-09','Lucas Ferreyra','WhatsApp','Pedido de cambio de fecha de la reserva','Terminado',7,2,'2026-10-15'),(9,'2026-10-11','Ana Torres','Email','Presupuesto para un grupo de 10 personas','Pendiente',NULL,3,'2026-10-15'),(10,'2026-10-12','Martina Gutiérrez','WhatsApp','Confirmación de la reserva y datos para la seña','Pendiente',9,5,'2026-10-15');
/*!40000 ALTER TABLE `consulta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `consumo`
--

DROP TABLE IF EXISTS `consumo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `consumo` (
  `id_consumo` int NOT NULL AUTO_INCREMENT,
  `id_reserva` int NOT NULL,
  `id_concepto` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `fecha_registro` date NOT NULL DEFAULT (curdate()),
  `id_usuario_registro` int NOT NULL,
  PRIMARY KEY (`id_consumo`),
  KEY `fk_consumo_reserva` (`id_reserva`),
  KEY `fk_consumo_concepto` (`id_concepto`),
  KEY `fk_consumo_usuario` (`id_usuario_registro`),
  CONSTRAINT `fk_consumo_concepto` FOREIGN KEY (`id_concepto`) REFERENCES `concepto_consumo` (`id_concepto`),
  CONSTRAINT `fk_consumo_reserva` FOREIGN KEY (`id_reserva`) REFERENCES `reserva` (`id_reserva`),
  CONSTRAINT `fk_consumo_usuario` FOREIGN KEY (`id_usuario_registro`) REFERENCES `usuario` (`id_usuario`),
  CONSTRAINT `chk_consumo_cantidad` CHECK ((`cantidad` > 0)),
  CONSTRAINT `chk_consumo_precio` CHECK ((`precio_unitario` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consumo`
--

LOCK TABLES `consumo` WRITE;
/*!40000 ALTER TABLE `consumo` DISABLE KEYS */;
INSERT INTO `consumo` VALUES (1,1,1,2,1500.00,'2026-10-01',1),(2,1,2,1,5000.00,'2026-10-02',1),(3,2,3,3,800.00,'2026-10-03',2),(4,2,4,1,3000.00,'2026-10-04',2),(5,3,7,1,2000.00,'2026-10-05',1),(6,3,1,1,1500.00,'2026-10-05',1),(7,4,8,2,2500.00,'2026-10-06',2),(8,4,5,1,8000.00,'2026-10-06',2),(9,5,9,1,1000.00,'2026-10-07',1),(10,5,10,1,3000.00,'2026-10-07',1);
/*!40000 ALTER TABLE `consumo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `habitacion`
--

DROP TABLE IF EXISTS `habitacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `habitacion` (
  `id_habitacion` int NOT NULL AUTO_INCREMENT,
  `tipo_habitacion` varchar(20) NOT NULL,
  `capacidad` int NOT NULL,
  `precio_noche` decimal(10,2) NOT NULL,
  `estado_habitacion` varchar(20) NOT NULL DEFAULT 'disponible',
  PRIMARY KEY (`id_habitacion`),
  KEY `idx_habitacion_estado` (`estado_habitacion`),
  CONSTRAINT `chk_hab_capacidad` CHECK ((`capacidad` > 0)),
  CONSTRAINT `chk_hab_estado` CHECK ((`estado_habitacion` in (_utf8mb4'mantenimiento',_utf8mb4'disponible',_utf8mb4'ocupada'))),
  CONSTRAINT `chk_hab_precio` CHECK ((`precio_noche` >= 0)),
  CONSTRAINT `chk_hab_tipo` CHECK ((`tipo_habitacion` in (_utf8mb4'familiar',_utf8mb4'simple',_utf8mb4'doble',_utf8mb4'suite')))
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `habitacion`
--

LOCK TABLES `habitacion` WRITE;
/*!40000 ALTER TABLE `habitacion` DISABLE KEYS */;
INSERT INTO `habitacion` VALUES (1,'simple',2,25000.00,'disponible'),(2,'doble',2,45000.00,'disponible'),(3,'doble',3,48000.00,'disponible'),(4,'suite',4,85000.00,'disponible'),(5,'suite',5,95000.00,'mantenimiento'),(6,'familiar',6,120000.00,'disponible'),(7,'familiar',8,140000.00,'disponible'),(8,'simple',2,25000.00,'disponible'),(9,'doble',2,45000.00,'disponible'),(10,'suite',4,85000.00,'disponible'),(11,'simple',2,100000.00,'disponible');
/*!40000 ALTER TABLE `habitacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `huesped`
--

DROP TABLE IF EXISTS `huesped`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `huesped` (
  `id_huesped` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `dni` varchar(20) NOT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `nacionalidad` varchar(50) DEFAULT NULL,
  `telefono` varchar(20) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `direccion` text,
  `id_usuario_registro` int NOT NULL,
  `fecha_creacion` date NOT NULL DEFAULT (curdate()),
  `fecha_modificacion` date DEFAULT NULL,
  `activo` tinyint NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_huesped`),
  UNIQUE KEY `dni` (`dni`),
  UNIQUE KEY `email` (`email`),
  KEY `fk_huesped_usuario` (`id_usuario_registro`),
  KEY `idx_huesped_apellido` (`apellido`,`nombre`),
  CONSTRAINT `fk_huesped_usuario` FOREIGN KEY (`id_usuario_registro`) REFERENCES `usuario` (`id_usuario`),
  CONSTRAINT `chk_huesped_activo` CHECK ((`activo` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `huesped`
--

LOCK TABLES `huesped` WRITE;
/*!40000 ALTER TABLE `huesped` DISABLE KEYS */;
INSERT INTO `huesped` VALUES (1,'Marcos','Rivas','30111222','1983-04-12','Argentina','3515550001','marcos.rivas@mail.test','Av. Colón 1200, Córdoba',3,'2026-10-15',NULL,1),(2,'Sofía','Ledesma','32444555','1986-09-30','Argentina','3515550002','sofia.ledesma@mail.test','Bv. San Juan 450, Córdoba',3,'2026-10-15',NULL,1),(3,'Julián','Herrera','28999000','1981-01-22','Argentina','3515550003',NULL,NULL,4,'2026-10-15',NULL,1),(4,'Camila','Soria','35123456','1991-06-05','Argentina','3515550004','camila.soria@mail.test','Av. Vélez Sarsfield 800, Córdoba',4,'2026-10-15',NULL,1),(5,'Tomás','Aguirre','40111333','1997-11-18','Argentina','3515550005',NULL,'tunsri',4,'2026-10-15','2026-10-18',1),(6,'Valeria','Bustos','33222111','1988-02-14','Argentina','3515550006','valeria.bustos@mail.test','Mendoza 321, Rosario',3,'2026-10-15','2026-10-16',0),(7,'Nicolás','Paz','37555666','1993-07-27','Argentina','3515550007',NULL,'Belgrano 90, Villa María',5,'2026-10-15',NULL,1),(8,'Lucas','Ferreya','29888777','1982-12-03','Argentina','3515550008','lucas.ferreya@mail.test','San Martín 1500, Río Cuarto',5,'2026-10-15',NULL,1),(9,'Martina','Gutiérrez','41222333','1999-03-09','Uruguay','3515550009','martina.gutierrez@mail.test',NULL,3,'2026-10-15',NULL,1),(10,'Diego','Castro','31666777','1984-08-21','Chile','3515550010',NULL,NULL,2,'2026-10-15',NULL,1),(11,'Test','Prueba','99999999',NULL,NULL,'351-9999999','test@mail.com',NULL,1,'2026-10-16','2026-10-16',0),(12,'carlos','uyaba','2539232352',NULL,NULL,'231','123',NULL,1,'2026-10-16','2026-10-16',0),(19,'juan','tomas','39232333',NULL,NULL,'1231232133','au@gmail.com',NULL,1,'2026-10-16','2026-10-16',0),(23,'adrian','alcarez','25505221',NULL,NULL,'3535088497','adrian@gmail.com',NULL,1,'2026-10-16',NULL,1),(28,'Esteban','Aviles','30252562',NULL,NULL,'353656568','a@gmail.com',NULL,1,'2026-10-21',NULL,1);
/*!40000 ALTER TABLE `huesped` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pago`
--

DROP TABLE IF EXISTS `pago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pago` (
  `id_pago` int NOT NULL AUTO_INCREMENT,
  `id_reserva` int NOT NULL,
  `fecha_pago` date NOT NULL DEFAULT (curdate()),
  `total_pagado` decimal(10,2) NOT NULL,
  `metodo_pago` varchar(30) NOT NULL,
  `estado_pago` varchar(20) NOT NULL DEFAULT 'pendiente',
  `nro_transaccion` varchar(50) DEFAULT NULL,
  `observacion` text,
  `id_usuario_registro` int NOT NULL,
  `fecha_modificacion` date DEFAULT NULL,
  PRIMARY KEY (`id_pago`),
  UNIQUE KEY `nro_transaccion` (`nro_transaccion`),
  KEY `fk_pago_reserva` (`id_reserva`),
  KEY `fk_pago_usuario` (`id_usuario_registro`),
  CONSTRAINT `fk_pago_reserva` FOREIGN KEY (`id_reserva`) REFERENCES `reserva` (`id_reserva`),
  CONSTRAINT `fk_pago_usuario` FOREIGN KEY (`id_usuario_registro`) REFERENCES `usuario` (`id_usuario`),
  CONSTRAINT `chk_pago_estado` CHECK ((`estado_pago` in (_utf8mb4'pendiente',_utf8mb4'aprobado',_utf8mb4'rechazado',_utf8mb4'reembolsado'))),
  CONSTRAINT `chk_pago_metodo` CHECK ((`metodo_pago` in (_utf8mb4'Efectivo',_utf8mb4'Transferencia',_utf8mb4'Tarjeta'))),
  CONSTRAINT `chk_pago_total` CHECK ((`total_pagado` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pago`
--

LOCK TABLES `pago` WRITE;
/*!40000 ALTER TABLE `pago` DISABLE KEYS */;
INSERT INTO `pago` VALUES (1,1,'2026-09-22',22500.00,'Transferencia','aprobado','TRF-0001','Seña 30%',1,NULL),(2,1,'2026-10-04',52500.00,'Efectivo','pendiente',NULL,'Saldo a abonar en el check-out',1,NULL),(3,2,'2026-09-25',40500.00,'Tarjeta','aprobado','TJ-0002','Seña 30%',2,NULL),(4,3,'2026-09-28',51000.00,'Efectivo','aprobado',NULL,'Seña 30%',1,NULL),(5,4,'2026-09-29',103500.00,'Transferencia','aprobado','TRF-0004','Seña 30%',2,NULL),(6,5,'2026-10-05',7500.00,'Efectivo','pendiente',NULL,'Seña 30% a la espera',1,NULL),(7,6,'2026-10-03',27000.00,'Transferencia','reembolsado','TRF-0006','Cancelación con más de 48 hs: devolución total',2,NULL),(8,7,'2026-10-02',126000.00,'Transferencia','aprobado','TRF-0008','Seña 30%',3,NULL),(9,8,'2026-10-06',76500.00,'Tarjeta','aprobado','TJ-0009','Seña 30%',4,NULL),(10,10,'2026-10-01',27000.00,'Transferencia','aprobado','TRF-0010','Seña 30%',2,NULL),(11,10,'2026-10-11',13500.00,'Transferencia','reembolsado','TRF-0011','Cancelación con menos de 48 hs: devolución del 50%',2,NULL);
/*!40000 ALTER TABLE `pago` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reserva`
--

DROP TABLE IF EXISTS `reserva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reserva` (
  `id_reserva` int NOT NULL AUTO_INCREMENT,
  `fecha_creacion` date NOT NULL DEFAULT (curdate()),
  `fecha_ingreso` date NOT NULL,
  `fecha_salida` date NOT NULL,
  `nro_personas` int NOT NULL,
  `precio_total` decimal(10,2) NOT NULL,
  `estado_reserva` varchar(20) NOT NULL DEFAULT 'pendiente',
  `id_usuario_creacion` int NOT NULL,
  `fecha_modificacion` date DEFAULT NULL,
  PRIMARY KEY (`id_reserva`),
  KEY `fk_reserva_usuario` (`id_usuario_creacion`),
  KEY `idx_reserva_estado` (`estado_reserva`),
  KEY `idx_reserva_fechas` (`fecha_ingreso`,`fecha_salida`),
  CONSTRAINT `fk_reserva_usuario` FOREIGN KEY (`id_usuario_creacion`) REFERENCES `usuario` (`id_usuario`),
  CONSTRAINT `chk_reserva_estado` CHECK ((`estado_reserva` in (_utf8mb4'pendiente',_utf8mb4'confirmado',_utf8mb4'cancelado'))),
  CONSTRAINT `chk_reserva_fechas` CHECK ((`fecha_ingreso` < `fecha_salida`)),
  CONSTRAINT `chk_reserva_personas` CHECK ((`nro_personas` > 0)),
  CONSTRAINT `chk_reserva_precio` CHECK ((`precio_total` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserva`
--

LOCK TABLES `reserva` WRITE;
/*!40000 ALTER TABLE `reserva` DISABLE KEYS */;
INSERT INTO `reserva` VALUES (1,'2026-09-22','2026-10-01','2026-10-04',2,75000.00,'confirmado',1,NULL),(2,'2026-09-25','2026-10-02','2026-10-05',2,135000.00,'confirmado',2,NULL),(3,'2026-09-28','2026-10-05','2026-10-07',4,170000.00,'confirmado',1,NULL),(4,'2026-09-29','2026-10-06','2026-10-09',5,345000.00,'confirmado',2,NULL),(5,'2026-10-05','2026-10-07','2026-10-08',2,25000.00,'pendiente',1,NULL),(6,'2026-10-01','2026-11-10','2026-11-12',2,90000.00,'cancelado',2,NULL),(7,'2026-10-02','2026-10-10','2026-10-13',6,420000.00,'confirmado',3,NULL),(8,'2026-10-06','2026-10-15','2026-10-18',3,255000.00,'confirmado',4,NULL),(9,'2026-10-12','2026-10-20','2026-10-22',4,100000.00,'pendiente',5,NULL),(10,'2026-10-01','2026-10-12','2026-10-14',2,90000.00,'cancelado',2,NULL),(11,'2026-10-17','2026-10-18','2026-10-25',3,336000.00,'confirmado',1,NULL),(12,'2026-10-18','2026-12-24','2026-12-25',2,25000.00,'confirmado',1,NULL),(13,'2026-10-18','2026-12-24','2026-12-25',2,25000.00,'confirmado',1,NULL),(14,'2026-10-21','2026-10-21','2026-10-28',2,700000.00,'confirmado',1,NULL);
/*!40000 ALTER TABLE `reserva` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_no_doble_reserva_fechas` BEFORE UPDATE ON `reserva` FOR EACH ROW BEGIN
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
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `reserva_habitacion`
--

DROP TABLE IF EXISTS `reserva_habitacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reserva_habitacion` (
  `id_reserva` int NOT NULL,
  `id_habitacion` int NOT NULL,
  `precio_noche_acordado` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id_reserva`,`id_habitacion`),
  KEY `fk_rh_habitacion` (`id_habitacion`),
  CONSTRAINT `fk_rh_habitacion` FOREIGN KEY (`id_habitacion`) REFERENCES `habitacion` (`id_habitacion`),
  CONSTRAINT `fk_rh_reserva` FOREIGN KEY (`id_reserva`) REFERENCES `reserva` (`id_reserva`),
  CONSTRAINT `chk_rh_precio` CHECK ((`precio_noche_acordado` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserva_habitacion`
--

LOCK TABLES `reserva_habitacion` WRITE;
/*!40000 ALTER TABLE `reserva_habitacion` DISABLE KEYS */;
INSERT INTO `reserva_habitacion` VALUES (1,1,25000.00),(2,2,45000.00),(3,4,85000.00),(4,6,115000.00),(5,8,25000.00),(6,9,45000.00),(7,7,140000.00),(8,10,85000.00),(9,1,25000.00),(9,8,25000.00),(10,2,45000.00),(11,3,48000.00),(12,1,25000.00),(13,1,25000.00),(14,11,100000.00);
/*!40000 ALTER TABLE `reserva_habitacion` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_no_doble_reserva` BEFORE INSERT ON `reserva_habitacion` FOR EACH ROW BEGIN
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
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_no_doble_reserva_upd` BEFORE UPDATE ON `reserva_habitacion` FOR EACH ROW BEGIN
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
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `reserva_huesped`
--

DROP TABLE IF EXISTS `reserva_huesped`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reserva_huesped` (
  `id_reserva` int NOT NULL,
  `id_huesped` int NOT NULL,
  `rol` varchar(20) NOT NULL DEFAULT 'acompanante',
  `fecha_asociacion` date NOT NULL DEFAULT (curdate()),
  PRIMARY KEY (`id_reserva`,`id_huesped`),
  KEY `fk_ruh_huesped` (`id_huesped`),
  CONSTRAINT `fk_ruh_huesped` FOREIGN KEY (`id_huesped`) REFERENCES `huesped` (`id_huesped`),
  CONSTRAINT `fk_ruh_reserva` FOREIGN KEY (`id_reserva`) REFERENCES `reserva` (`id_reserva`),
  CONSTRAINT `chk_ruh_rol` CHECK ((`rol` in (_utf8mb4'titular',_utf8mb4'acompanante')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserva_huesped`
--

LOCK TABLES `reserva_huesped` WRITE;
/*!40000 ALTER TABLE `reserva_huesped` DISABLE KEYS */;
INSERT INTO `reserva_huesped` VALUES (1,1,'titular','2026-09-22'),(1,2,'acompanante','2026-09-22'),(2,6,'titular','2026-09-25'),(3,3,'titular','2026-09-28'),(3,7,'acompanante','2026-09-28'),(4,4,'titular','2026-09-29'),(4,5,'acompanante','2026-09-29'),(5,10,'titular','2026-10-05'),(6,1,'titular','2026-10-01'),(7,6,'acompanante','2026-10-02'),(7,8,'titular','2026-10-02'),(7,9,'acompanante','2026-10-02'),(8,1,'acompanante','2026-10-06'),(8,2,'titular','2026-10-06'),(9,4,'acompanante','2026-10-12'),(9,9,'titular','2026-10-12'),(10,7,'titular','2026-10-01'),(11,23,'titular','2026-10-17'),(12,23,'titular','2026-10-18'),(13,2,'titular','2026-10-18'),(14,28,'titular','2026-10-21');
/*!40000 ALTER TABLE `reserva_huesped` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `rol` varchar(20) NOT NULL,
  `activo` tinyint NOT NULL DEFAULT '1',
  `fecha_creacion` date NOT NULL DEFAULT (curdate()),
  `fecha_modificacion` date DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `email` (`email`),
  CONSTRAINT `chk_usuario_activo` CHECK ((`activo` in (0,1))),
  CONSTRAINT `chk_usuario_rol` CHECK ((`rol` in (_utf8mb4'admin',_utf8mb4'gerente',_utf8mb4'recepcionista')))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'Admin','Sistema','admin@gestarho.test','3511000001','hash_demo_admin','admin',1,'2026-10-15',NULL),(2,'Lucía','Pérez','recepcion@gestarho.test','3511000002','hash_demo_recep','recepcionista',1,'2026-10-15',NULL),(3,'Carolina','Méndez','gerencia@gestarho.test','3511000003','hash_demo_gerente','gerente',1,'2026-10-15',NULL),(4,'Federico','Olmos','folmos@gestarho.test','3511000004','hash_demo_recep','recepcionista',1,'2026-10-15',NULL),(5,'Natalia','Vega','nvega@gestarho.test','3511000005','hash_demo_recep','recepcionista',1,'2026-10-15',NULL),(6,'Ramiro','Bazán','rbazan@gestarho.test','3511000006','hash_demo_recep','recepcionista',1,'2026-10-15',NULL),(7,'Silvana','Cabrera','scabrera@gestarho.test','3511000007','hash_demo_gerente','gerente',1,'2026-10-15',NULL),(8,'Gonzalo','Funes','gfunes@gestarho.test','3511000008','hash_demo_recep','recepcionista',1,'2026-10-15',NULL),(9,'Paula','Domínguez','pdominguez@gestarho.test','3511000009','hash_demo_recep','recepcionista',1,'2026-10-15',NULL),(10,'Héctor','Salas','hsalas@gestarho.test','3511000010','hash_demo_recep','recepcionista',0,'2026-10-15',NULL);
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `v_saldo_reserva`
--

DROP TABLE IF EXISTS `v_saldo_reserva`;
/*!50001 DROP VIEW IF EXISTS `v_saldo_reserva`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_saldo_reserva` AS SELECT 
 1 AS `id_reserva`,
 1 AS `estado_reserva`,
 1 AS `precio_total`,
 1 AS `total_consumos`,
 1 AS `total_pagado`,
 1 AS `saldo_pendiente`*/;
SET character_set_client = @saved_cs_client;

--
-- Dumping events for database 'gestarho'
--

--
-- Dumping routines for database 'gestarho'
--

--
-- Final view structure for view `v_saldo_reserva`
--

/*!50001 DROP VIEW IF EXISTS `v_saldo_reserva`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_saldo_reserva` AS select `t`.`id_reserva` AS `id_reserva`,`t`.`estado_reserva` AS `estado_reserva`,`t`.`precio_total` AS `precio_total`,`t`.`total_consumos` AS `total_consumos`,`t`.`total_pagado` AS `total_pagado`,((`t`.`precio_total` + `t`.`total_consumos`) - `t`.`total_pagado`) AS `saldo_pendiente` from (select `r`.`id_reserva` AS `id_reserva`,`r`.`estado_reserva` AS `estado_reserva`,`r`.`precio_total` AS `precio_total`,(select coalesce(sum((`c`.`cantidad` * `c`.`precio_unitario`)),0) from `consumo` `c` where (`c`.`id_reserva` = `r`.`id_reserva`)) AS `total_consumos`,(select coalesce(sum(`p`.`total_pagado`),0) from `pago` `p` where ((`p`.`id_reserva` = `r`.`id_reserva`) and (`p`.`estado_pago` = 'aprobado'))) AS `total_pagado` from `reserva` `r`) `t` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-23 12:07:40
