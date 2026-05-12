/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE IF NOT EXISTS `classflow` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci */;
USE `classflow`;

CREATE TABLE IF NOT EXISTS `actividades` (
  `id_actividades` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  `descripcion` varchar(150) DEFAULT NULL,
  `tipo` varchar(200) DEFAULT NULL,
  `valor` int(11) DEFAULT NULL,
  `fecha_entrega` datetime DEFAULT NULL,
  `fecha_agregada` datetime DEFAULT NULL,
  `id_unidad` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_actividades`),
  KEY `FK_actividades_unidad` (`id_unidad`),
  CONSTRAINT `FK_actividades_unidad` FOREIGN KEY (`id_unidad`) REFERENCES `unidad` (`id_unidad`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

DELETE FROM `actividades`;

CREATE TABLE IF NOT EXISTS `alumnos` (
  `id_alumno` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` int(11) DEFAULT NULL,
  `correo` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_alumno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

DELETE FROM `alumnos`;

CREATE TABLE IF NOT EXISTS `alumnos_clase` (
  `id_alumno_clase` int(11) NOT NULL AUTO_INCREMENT,
  `id_alumno` int(11) NOT NULL,
  `id_clase` int(11) NOT NULL,
  PRIMARY KEY (`id_alumno_clase`),
  KEY `FK__clase` (`id_clase`),
  KEY `FK__alumnos` (`id_alumno`),
  CONSTRAINT `FK__alumnos` FOREIGN KEY (`id_alumno`) REFERENCES `alumnos` (`id_alumno`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK__clase` FOREIGN KEY (`id_clase`) REFERENCES `clase` (`id_clase`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

DELETE FROM `alumnos_clase`;

CREATE TABLE IF NOT EXISTS `clase` (
  `id_clase` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `id_profesor` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_clase`),
  KEY `id_profesor` (`id_profesor`),
  CONSTRAINT `FK_clase_profesores` FOREIGN KEY (`id_profesor`) REFERENCES `profesores` (`id_profesor`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

DELETE FROM `clase`;
INSERT INTO `clase` (`id_clase`, `nombre`, `descripcion`, `id_profesor`) VALUES
	(1, 'Mate', 'asdfdas', 2),
	(2, 'mates', 'holas', 2),
	(3, 'mate 1', 'grupo:2', 2),
	(4, 'Pruebas', 'Pruebas de unidades', 3),
	(5, 'dsdfffs', 'sdffsdf', 2);

CREATE TABLE IF NOT EXISTS `evaluacion` (
  `id_evaluacion` int(11) NOT NULL AUTO_INCREMENT,
  `id_alumno` int(11) DEFAULT NULL,
  `id_actividad` int(11) DEFAULT NULL,
  `calificacion` varchar(50) DEFAULT NULL,
  `autoevaluacion` varchar(50) DEFAULT NULL,
  `entregado` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_evaluacion`),
  KEY `FK_evaluacion_alumnos` (`id_alumno`),
  KEY `FK_evaluacion_actividades` (`id_actividad`),
  CONSTRAINT `FK_evaluacion_actividades` FOREIGN KEY (`id_actividad`) REFERENCES `actividades` (`id_actividades`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_evaluacion_alumnos` FOREIGN KEY (`id_alumno`) REFERENCES `alumnos` (`id_alumno`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

DELETE FROM `evaluacion`;

CREATE TABLE IF NOT EXISTS `profesores` (
  `id_profesor` int(10) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL DEFAULT '0',
  `correo` varchar(100) NOT NULL DEFAULT '0',
  `password` varchar(255) NOT NULL DEFAULT '0',
  `telefono` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id_profesor`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

DELETE FROM `profesores`;
INSERT INTO `profesores` (`id_profesor`, `nombre`, `correo`, `password`, `telefono`) VALUES
	(1, 'Jesus', 'prueba0@gamil.com', '$2b$12$66nLZhUDrzRSHhQTUIsgX.93jBCRPvX2ZKUZ1zEnDJ8/g4hkhiCE.', '6564235698'),
	(2, 'Kenia', 'prueba1@gmail.com', '$2b$12$pEyf.gvRsjk18BWNXXWTNurbRskr8OjmsBKkn3OeN4oriX3Geq0Lu', '7894562456'),
	(3, 'Pruebas', 'pruebas@gmail.com', '$2b$12$zTi3UHPq.NT8515rhUoxmeU0m7JoHvkjvUDujaXMuqMrIzt2zmu7m', '7894561230');

CREATE TABLE IF NOT EXISTS `unidad` (
  `id_unidad` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL DEFAULT '0',
  `id_clase` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id_unidad`),
  KEY `FK_unidad_clase` (`id_clase`),
  CONSTRAINT `FK_unidad_clase` FOREIGN KEY (`id_clase`) REFERENCES `clase` (`id_clase`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

DELETE FROM `unidad`;
INSERT INTO `unidad` (`id_unidad`, `nombre`, `id_clase`) VALUES
	(1, 'Unidad 1', 1),
	(2, 'Unidad 2', 1),
	(3, 'Unidad 4', 2);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;