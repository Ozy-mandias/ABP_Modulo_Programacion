-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: gestarho
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `concepto_consumo`
--

DROP TABLE IF EXISTS `concepto_consumo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `concepto_consumo` (
  `id_concepto` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_spanish_ci NOT NULL,
  `descripcion` varchar(200) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `tipo` varchar(20) COLLATE utf8mb4_spanish_ci NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_concepto`),
  UNIQUE KEY `nombre` (`nombre`),
  CONSTRAINT `concepto_consumo_chk_1` CHECK ((`tipo` in (_utf8mb4'producto',_utf8mb4'servicio'))),
  CONSTRAINT `concepto_consumo_chk_2` CHECK ((`activo` in (0,1)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `concepto_consumo`
--

LOCK TABLES `concepto_consumo` WRITE;
/*!40000 ALTER TABLE `concepto_consumo` DISABLE KEYS */;
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
  `remitente` varchar(100) COLLATE utf8mb4_spanish_ci NOT NULL,
  `medio` varchar(30) COLLATE utf8mb4_spanish_ci NOT NULL,
  `asunto` text COLLATE utf8mb4_spanish_ci NOT NULL,
  `estado` varchar(20) COLLATE utf8mb4_spanish_ci NOT NULL DEFAULT 'Pendiente',
  `id_reserva` int DEFAULT NULL,
  `id_usuario_asignado` int DEFAULT NULL,
  `fecha_creacion` date NOT NULL DEFAULT (curdate()),
  PRIMARY KEY (`id_consulta`),
  KEY `id_usuario_asignado` (`id_usuario_asignado`),
  KEY `idx_consulta_estado` (`estado`),
  KEY `idx_consulta_reserva` (`id_reserva`),
  CONSTRAINT `consulta_ibfk_1` FOREIGN KEY (`id_reserva`) REFERENCES `reserva` (`id_reserva`),
  CONSTRAINT `consulta_ibfk_2` FOREIGN KEY (`id_usuario_asignado`) REFERENCES `usuario` (`id_usuario`),
  CONSTRAINT `consulta_chk_1` CHECK ((`medio` in (_utf8mb4'WhatsApp',_utf8mb4'Web',_utf8mb4'Telefono',_utf8mb4'Email'))),
  CONSTRAINT `consulta_chk_2` CHECK ((`estado` in (_utf8mb4'Pendiente',_utf8mb4'Terminado',_utf8mb4'Archivado')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consulta`
--

LOCK TABLES `consulta` WRITE;
/*!40000 ALTER TABLE `consulta` DISABLE KEYS */;
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
  KEY `id_usuario_registro` (`id_usuario_registro`),
  KEY `idx_consumo_reserva` (`id_reserva`),
  KEY `idx_consumo_concepto` (`id_concepto`),
  CONSTRAINT `consumo_ibfk_1` FOREIGN KEY (`id_reserva`) REFERENCES `reserva` (`id_reserva`),
  CONSTRAINT `consumo_ibfk_2` FOREIGN KEY (`id_concepto`) REFERENCES `concepto_consumo` (`id_concepto`),
  CONSTRAINT `consumo_ibfk_3` FOREIGN KEY (`id_usuario_registro`) REFERENCES `usuario` (`id_usuario`),
  CONSTRAINT `consumo_chk_1` CHECK ((`cantidad` > 0)),
  CONSTRAINT `consumo_chk_2` CHECK ((`precio_unitario` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consumo`
--

LOCK TABLES `consumo` WRITE;
/*!40000 ALTER TABLE `consumo` DISABLE KEYS */;
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
  `tipo_habitacion` varchar(20) COLLATE utf8mb4_spanish_ci NOT NULL,
  `capacidad` int NOT NULL,
  `precio_noche` decimal(10,2) NOT NULL,
  `estado_habitacion` varchar(20) COLLATE utf8mb4_spanish_ci NOT NULL DEFAULT 'disponible',
  PRIMARY KEY (`id_habitacion`),
  KEY `idx_habitacion_estado` (`estado_habitacion`),
  CONSTRAINT `habitacion_chk_1` CHECK ((`tipo_habitacion` in (_utf8mb4'familiar',_utf8mb4'simple',_utf8mb4'doble',_utf8mb4'suite'))),
  CONSTRAINT `habitacion_chk_2` CHECK ((`capacidad` > 0)),
  CONSTRAINT `habitacion_chk_3` CHECK ((`precio_noche` >= 0)),
  CONSTRAINT `habitacion_chk_4` CHECK ((`estado_habitacion` in (_utf8mb4'mantenimiento',_utf8mb4'disponible',_utf8mb4'ocupada')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `habitacion`
--

LOCK TABLES `habitacion` WRITE;
/*!40000 ALTER TABLE `habitacion` DISABLE KEYS */;
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
  `nombre` varchar(100) COLLATE utf8mb4_spanish_ci NOT NULL,
  `apellido` varchar(100) COLLATE utf8mb4_spanish_ci NOT NULL,
  `dni` varchar(20) COLLATE utf8mb4_spanish_ci NOT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `nacionalidad` varchar(50) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `telefono` varchar(20) COLLATE utf8mb4_spanish_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `direccion` text COLLATE utf8mb4_spanish_ci,
  `id_usuario_registro` int NOT NULL,
  `fecha_creacion` date NOT NULL DEFAULT (curdate()),
  `fecha_modificacion` date DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_huesped`),
  UNIQUE KEY `dni` (`dni`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_huesped_dni` (`dni`),
  KEY `idx_huesped_usuario` (`id_usuario_registro`),
  CONSTRAINT `huesped_ibfk_1` FOREIGN KEY (`id_usuario_registro`) REFERENCES `usuario` (`id_usuario`),
  CONSTRAINT `huesped_chk_1` CHECK ((`activo` in (0,1)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `huesped`
--

LOCK TABLES `huesped` WRITE;
/*!40000 ALTER TABLE `huesped` DISABLE KEYS */;
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
  `metodo_pago` varchar(30) COLLATE utf8mb4_spanish_ci NOT NULL,
  `estado_pago` varchar(20) COLLATE utf8mb4_spanish_ci NOT NULL DEFAULT 'pendiente',
  `nro_transaccion` varchar(50) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `observacion` text COLLATE utf8mb4_spanish_ci,
  `id_usuario_registro` int NOT NULL,
  `fecha_modificacion` date DEFAULT NULL,
  PRIMARY KEY (`id_pago`),
  UNIQUE KEY `nro_transaccion` (`nro_transaccion`),
  KEY `id_usuario_registro` (`id_usuario_registro`),
  KEY `idx_pago_reserva` (`id_reserva`),
  CONSTRAINT `pago_ibfk_1` FOREIGN KEY (`id_reserva`) REFERENCES `reserva` (`id_reserva`),
  CONSTRAINT `pago_ibfk_2` FOREIGN KEY (`id_usuario_registro`) REFERENCES `usuario` (`id_usuario`),
  CONSTRAINT `pago_chk_1` CHECK ((`total_pagado` > 0)),
  CONSTRAINT `pago_chk_2` CHECK ((`metodo_pago` in (_utf8mb4'Efectivo',_utf8mb4'Transferencia',_utf8mb4'Tarjeta'))),
  CONSTRAINT `pago_chk_3` CHECK ((`estado_pago` in (_utf8mb4'pendiente',_utf8mb4'aprobado',_utf8mb4'rechazado',_utf8mb4'reembolsado')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pago`
--

LOCK TABLES `pago` WRITE;
/*!40000 ALTER TABLE `pago` DISABLE KEYS */;
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
  `estado_reserva` varchar(20) COLLATE utf8mb4_spanish_ci NOT NULL DEFAULT 'pendiente',
  `id_usuario_creacion` int NOT NULL,
  `fecha_modificacion` date DEFAULT NULL,
  PRIMARY KEY (`id_reserva`),
  KEY `idx_reserva_usuario` (`id_usuario_creacion`),
  KEY `idx_reserva_estado` (`estado_reserva`),
  CONSTRAINT `reserva_ibfk_1` FOREIGN KEY (`id_usuario_creacion`) REFERENCES `usuario` (`id_usuario`),
  CONSTRAINT `reserva_chk_1` CHECK ((`nro_personas` > 0)),
  CONSTRAINT `reserva_chk_2` CHECK ((`precio_total` >= 0)),
  CONSTRAINT `reserva_chk_3` CHECK ((`estado_reserva` in (_utf8mb4'pendiente',_utf8mb4'confirmado',_utf8mb4'cancelado'))),
  CONSTRAINT `reserva_chk_4` CHECK ((`fecha_ingreso` < `fecha_salida`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserva`
--

LOCK TABLES `reserva` WRITE;
/*!40000 ALTER TABLE `reserva` DISABLE KEYS */;
/*!40000 ALTER TABLE `reserva` ENABLE KEYS */;
UNLOCK TABLES;

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
  KEY `id_habitacion` (`id_habitacion`),
  CONSTRAINT `reserva_habitacion_ibfk_1` FOREIGN KEY (`id_reserva`) REFERENCES `reserva` (`id_reserva`),
  CONSTRAINT `reserva_habitacion_ibfk_2` FOREIGN KEY (`id_habitacion`) REFERENCES `habitacion` (`id_habitacion`),
  CONSTRAINT `reserva_habitacion_chk_1` CHECK ((`precio_noche_acordado` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserva_habitacion`
--

LOCK TABLES `reserva_habitacion` WRITE;
/*!40000 ALTER TABLE `reserva_habitacion` DISABLE KEYS */;
/*!40000 ALTER TABLE `reserva_habitacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reserva_huesped`
--

DROP TABLE IF EXISTS `reserva_huesped`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reserva_huesped` (
  `id_reserva` int NOT NULL,
  `id_huesped` int NOT NULL,
  `rol` varchar(20) COLLATE utf8mb4_spanish_ci NOT NULL DEFAULT 'acompanante',
  `fecha_asociacion` date NOT NULL DEFAULT (curdate()),
  PRIMARY KEY (`id_reserva`,`id_huesped`),
  KEY `id_huesped` (`id_huesped`),
  CONSTRAINT `reserva_huesped_ibfk_1` FOREIGN KEY (`id_reserva`) REFERENCES `reserva` (`id_reserva`),
  CONSTRAINT `reserva_huesped_ibfk_2` FOREIGN KEY (`id_huesped`) REFERENCES `huesped` (`id_huesped`),
  CONSTRAINT `reserva_huesped_chk_1` CHECK ((`rol` in (_utf8mb4'titular',_utf8mb4'acompanante')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserva_huesped`
--

LOCK TABLES `reserva_huesped` WRITE;
/*!40000 ALTER TABLE `reserva_huesped` DISABLE KEYS */;
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
  `nombre` varchar(100) COLLATE utf8mb4_spanish_ci NOT NULL,
  `apellido` varchar(100) COLLATE utf8mb4_spanish_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_spanish_ci NOT NULL,
  `telefono` varchar(20) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_spanish_ci NOT NULL,
  `rol` varchar(20) COLLATE utf8mb4_spanish_ci NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  `fecha_creacion` date NOT NULL DEFAULT (curdate()),
  `fecha_modificacion` date DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_usuario_email` (`email`),
  CONSTRAINT `usuario_chk_1` CHECK ((`rol` in (_utf8mb4'admin',_utf8mb4'gerente',_utf8mb4'recepcionista'))),
  CONSTRAINT `usuario_chk_2` CHECK ((`activo` in (0,1)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
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
/*!50001 VIEW `v_saldo_reserva` AS select `subconsulta`.`id_reserva` AS `id_reserva`,`subconsulta`.`estado_reserva` AS `estado_reserva`,`subconsulta`.`precio_total` AS `precio_total`,`subconsulta`.`total_consumos` AS `total_consumos`,`subconsulta`.`total_pagado` AS `total_pagado`,((`subconsulta`.`precio_total` + `subconsulta`.`total_consumos`) - `subconsulta`.`total_pagado`) AS `saldo_pendiente` from (select `r`.`id_reserva` AS `id_reserva`,`r`.`estado_reserva` AS `estado_reserva`,`r`.`precio_total` AS `precio_total`,(select coalesce(sum((`c`.`cantidad` * `c`.`precio_unitario`)),0) from `consumo` `c` where (`c`.`id_reserva` = `r`.`id_reserva`)) AS `total_consumos`,(select coalesce(sum(`p`.`total_pagado`),0) from `pago` `p` where ((`p`.`id_reserva` = `r`.`id_reserva`) and (`p`.`estado_pago` = 'aprobado'))) AS `total_pagado` from `reserva` `r`) `subconsulta` */;
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

-- Dump completed on 2026-10-14 13:02:30
