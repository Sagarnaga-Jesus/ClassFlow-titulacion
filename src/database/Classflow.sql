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
  `id_google` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_actividades`),
  KEY `FK_actividades_unidad` (`id_unidad`),
  CONSTRAINT `FK_actividades_unidad` FOREIGN KEY (`id_unidad`) REFERENCES `unidad` (`id_unidad`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

DELETE FROM `actividades`;
INSERT INTO `actividades` (`id_actividades`, `nombre`, `descripcion`, `tipo`, `valor`, `fecha_entrega`, `fecha_agregada`, `id_unidad`, `id_google`) VALUES
	(4, 'Prueba 1', 'Prueba de actividad a estudiantes ', 'Actividad', 10, NULL, NULL, 31, '865886988730');

CREATE TABLE IF NOT EXISTS `alumnos` (
  `id_alumno` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `correo` varchar(200) DEFAULT NULL,
  `id_google` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id_alumno`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

DELETE FROM `alumnos`;
INSERT INTO `alumnos` (`id_alumno`, `nombre`, `correo`, `id_google`) VALUES
	(9, 'Luisito (LuisitoGoat)', NULL, '104240977640611220486'),
	(10, 'Karla Andres', NULL, '107006843594341589811');

CREATE TABLE IF NOT EXISTS `alumnos_clase` (
  `id_alumno_clase` int(11) NOT NULL AUTO_INCREMENT,
  `id_alumno` int(11) NOT NULL,
  `id_clase` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id_alumno_clase`),
  KEY `FK__alumnos` (`id_alumno`),
  CONSTRAINT `FK__alumnos` FOREIGN KEY (`id_alumno`) REFERENCES `alumnos` (`id_alumno`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

DELETE FROM `alumnos_clase`;
INSERT INTO `alumnos_clase` (`id_alumno_clase`, `id_alumno`, `id_clase`) VALUES
	(8, 9, '865000419090'),
	(9, 10, '865000419090'),
	(10, 9, '865000419090'),
	(11, 10, '865000419090'),
	(12, 9, '865000419090'),
	(13, 10, '865000419090'),
	(14, 9, '865000419090'),
	(15, 10, '865000419090'),
	(16, 9, '865000419090'),
	(17, 10, '865000419090'),
	(18, 9, '865000419090'),
	(19, 10, '865000419090'),
	(20, 9, '865000419090'),
	(21, 10, '865000419090'),
	(22, 9, '865000419090'),
	(23, 10, '865000419090'),
	(24, 9, '865000419090'),
	(25, 10, '865000419090'),
	(26, 9, '865000419090'),
	(27, 10, '865000419090'),
	(28, 9, '865000419090'),
	(29, 10, '865000419090'),
	(30, 9, '865000419090'),
	(31, 10, '865000419090'),
	(32, 9, '865000419090'),
	(33, 10, '865000419090'),
	(34, 9, '865000419090'),
	(35, 10, '865000419090');

CREATE TABLE IF NOT EXISTS `clase` (
  `id_clase` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `id_profesor` int(11) DEFAULT NULL,
  `id_google` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id_clase`),
  KEY `id_profesor` (`id_profesor`),
  CONSTRAINT `FK_clase_profesores` FOREIGN KEY (`id_profesor`) REFERENCES `profesores` (`id_profesor`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

DELETE FROM `clase`;
INSERT INTO `clase` (`id_clase`, `nombre`, `descripcion`, `id_profesor`, `id_google`) VALUES
	(1, 'Mate', 'asdfdas', 2, NULL),
	(2, 'mates', 'holas', 2, NULL),
	(3, 'mate 1', 'grupo:2', 2, NULL),
	(4, 'Pruebas', 'Pruebas de unidades', 3, NULL),
	(5, 'dsdfffs', 'sdffsdf', 2, NULL),
	(6, 'hola', 'descripcion', 4, NULL),
	(7, 'prueba', '', 5, '865000419090'),
	(11, 'Clasr', 'Programación ', 5, '854717875166'),
	(13, 'Prueba2', '', 5, '854565081343');

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
  `foto` text DEFAULT NULL,
  `fecha_registro` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id_profesor`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

DELETE FROM `profesores`;
INSERT INTO `profesores` (`id_profesor`, `nombre`, `correo`, `foto`, `fecha_registro`) VALUES
	(1, 'Jesus', 'prueba0@gamil.com', NULL, NULL),
	(2, 'Kenia', 'prueba1@gmail.com', NULL, NULL),
	(3, 'Pruebas', 'pruebas@gmail.com', NULL, NULL),
	(4, 'JESUS ANTONIO SAGARNAGA MACIAS', '23308060610335@cetis61.edu.mx', 'https://lh3.googleusercontent.com/a/ACg8ocJU5Y9NoNnuNEz1D_t_LxsiC4tam97XWGj1I0wMXKU8gGuFni0=s96-c', NULL),
	(5, 'ShadyGalaxy', 'shadysagarnaga@gmail.com', 'https://lh3.googleusercontent.com/a/ACg8ocI9Z08zsxVfkBayGw5l4fhRCGmDwCVlREUx5DWwPoTNN2WC5Q4=s96-c', NULL);

CREATE TABLE IF NOT EXISTS `unidad` (
  `id_unidad` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL DEFAULT '0',
  `examen` int(11) NOT NULL DEFAULT 0,
  `proyecto` int(11) NOT NULL DEFAULT 0,
  `lista` int(11) NOT NULL DEFAULT 0,
  `actividades` int(11) NOT NULL DEFAULT 0,
  `extra` int(11) NOT NULL DEFAULT 0,
  `id_clase` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id_unidad`),
  KEY `FK_unidad_clase` (`id_clase`),
  CONSTRAINT `FK_unidad_clase` FOREIGN KEY (`id_clase`) REFERENCES `clase` (`id_clase`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

DELETE FROM `unidad`;
INSERT INTO `unidad` (`id_unidad`, `nombre`, `examen`, `proyecto`, `lista`, `actividades`, `extra`, `id_clase`) VALUES
	(1, 'Unidad 1', 0, 0, 0, 0, 0, 1),
	(2, 'Unidad 2', 0, 0, 0, 0, 0, 1),
	(3, 'Unidad 4', 0, 0, 0, 0, 0, 2),
	(31, 'Unidad 1', 20, 20, 20, 20, 20, 7),
	(32, 'unidad 2', 40, 20, 10, 30, 0, 7),
	(33, 'unidad 1', 50, 30, 0, 20, 0, 11);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
