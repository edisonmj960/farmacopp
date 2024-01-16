-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 05-01-2024 a las 14:34:16
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `db_farmacop`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carrito`
--

CREATE TABLE `carrito` (
  `id_carrito` int(11) NOT NULL,
  `id` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `carrito`
--

INSERT INTO `carrito` (`id_carrito`, `id`, `id_producto`, `cantidad`) VALUES
(20, 1091, 9, 1),
(22, 1091, 19, 1),
(26, 1093, 11, 0),
(27, 1093, 8, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categoria`
--

CREATE TABLE `categoria` (
  `id_categoria` int(11) NOT NULL,
  `nombre` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categoria`
--

INSERT INTO `categoria` (`id_categoria`, `nombre`) VALUES
(1, 'cuidado personal'),
(2, 'dermacosmetico'),
(3, 'nutricionales'),
(4, 'bebe'),
(5, 'medicamentos');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedido`
--

CREATE TABLE `pedido` (
  `id_pedido` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `correo` varchar(100) NOT NULL,
  `direccion` varchar(200) NOT NULL,
  `ciudad` varchar(50) NOT NULL,
  `departamento` varchar(50) NOT NULL,
  `pais` varchar(50) NOT NULL,
  `estado` char(12) NOT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedido`
--

INSERT INTO `pedido` (`id_pedido`, `nombre`, `apellido`, `telefono`, `correo`, `direccion`, `ciudad`, `departamento`, `pais`, `estado`, `id`) VALUES
(3, 'sggf', 'gfdgfg', '3435455', 'sdgdg@g.com', 'dgdgdfg', 'dfgfg', 'dgfdg', 'dfgdfg', 'pendiente', 25),
(4, 'fsg', 'dsgdfg', '464656', 'bdfh@g.com', 'dgdfgfd', 'gdgdf', 'gdgdf', 'gdfgfd', 'pendiente', 25),
(5, 'olivia', 'juarez', '3111567899', 'oliviajur@g.com', 'carrera 334', 'Ipiales', 'Nariño', 'Colombia', 'pendiente', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto`
--

CREATE TABLE `producto` (
  `id_producto` int(11) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `descripcion` varchar(400) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio` double NOT NULL,
  `proveedor` varchar(45) NOT NULL,
  `fecha_vencimiento` date NOT NULL,
  `imagen` text NOT NULL,
  `categoria` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `producto`
--

INSERT INTO `producto` (`id_producto`, `nombre`, `descripcion`, `cantidad`, `precio`, `proveedor`, `fecha_vencimiento`, `imagen`, `categoria`) VALUES
(8, 'maquillaje', 'cambia tu apariencia y embellece el rostro', 3, 5000, 'Nivea', '2023-12-15', 'maquillaje.jpg', 2),
(9, 'vitamina B', 'mejora tufuncionamiento celular, crecimiento y el desarrollo', 6, 58000, 'Colpatria', '2026-11-12', 'vitaminab.jpg', 3),
(10, 'tretinol', 'es un poderoso ingrediente contra el envejecimiento gracias a su función antioxidante', 4, 5799, 'axa', '2024-11-09', 'tetrinol.png', 5),
(11, 'desodorante', 'eliminar ese mal olor corporal', 18, 6000, 'NaN', '2023-11-12', 'desodorante.jpg', 1),
(12, 'Paracetamol', 'Alivia dolores de cabeza y fiebre', 50, 5.99, 'Laboratorios XYZ', '2024-06-30', 'paracetamol.jpg', 1),
(13, 'Ibuprofeno', 'Reduce la inflamación y el dolor', 75, 7.99, 'Laboratorios ABC', '2023-12-31', 'ibuprofeno.jpg', 1),
(14, 'Acetaminofén', 'Alivia dolores leves y moderados', 99, 4.99, 'Laboratorios DEF', '2025-02-28', 'acetaminofen.jpg', 1),
(17, 'Fluconazol', 'Antifúngico para infecciones por hongos', 20, 8.99, 'Laboratorios GHI', '2024-04-30', 'fluconazol.jpg', 2),
(18, 'Omeprazol', 'Reduce la producción de ácido en el estómago', 60, 9.99, 'Laboratorios XYZ', '2023-08-31', 'omeprazol.png', 3),
(19, 'Ranitidina', 'Alivia la acidez estomacal y úlceras', 39, 6.99, 'Laboratorios ABC', '2024-02-28', 'ranitidina.png', 3),
(21, 'Metoclopramida', 'Alivia las náuseas y los vómitos', 35, 5.99, 'Laboratorios GHI', '2025-01-31', 'meclopramida.png', 4),
(24, 'leche en polvo ', 'contribuye en gran medida al desarrollo muscular debido a su alto contenido en proteínas', 8, 80000, 'colanta', '2025-11-10', 'leche.jpg', 4),
(27, 'gotas', 'son esenciales para preservar la visión y proteger los ojos.', 30, 5000, 'nivea', '2024-11-10', 'gotas.jpg', 4),
(30, 'Aspirina', 'bajar la fiebre y aliviar el dolor leve a moderado', 19, 5000, 'bayer', '2024-01-02', 'aspirin2a.png', 5),
(31, 'acetato', 'ph 4.5', 29, 5000, 'Licol', '2026-10-10', 'acetato.jpg', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id` int(11) NOT NULL,
  `tipo_user` int(11) NOT NULL,
  `nombre` varchar(60) NOT NULL,
  `apellido` varchar(60) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `direccion` varchar(60) NOT NULL,
  `telefono` char(12) NOT NULL,
  `genero` varchar(20) NOT NULL,
  `password` text NOT NULL,
  `create_at` varchar(100) NOT NULL,
  `imagen` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id`, `tipo_user`, `nombre`, `apellido`, `correo`, `direccion`, `telefono`, `genero`, `password`, `create_at`, `imagen`) VALUES
(1089, 1, 'Pepito', 'Perez', 'pepito@gmail.com', 'Cordoba', '3131121121', 'M', 'sha256$DMytNJyRBqp2BjpR$592621f338e55a8e7ff7d36e5ed66f7a5eebca89ed7d0ee643a29d19401d17c6', '2023-12-1', NULL),
(1090, 0, 'Santiago A', 'Ortega', 'santiago@gmail.com', 'potosi', '3122345436', 'M', 'sha256$WpxYsnMIqSpmDgMT$d717ba6aa970c38556c2b4d944354a822a40d72f49a9aaf0feb59a2028aa5508', '2023-12-1', NULL),
(1091, 2, 'jose gabriel', 'nastul', 'jose@gmail.com', 'Puerres', '3123221122', 'F', 'sha256$SGsZTkoZCPGu6H8f$70b47f5aac9d64afc3a36964597f3c2094adbd3b9a79642ee92105213f778b56', '2023-12-1', NULL),
(1092, 2, 'Edison', 'Mejia', 'edison@gmail.com', 'Ipiales', '3136465306', 'M', 'sha256$yIREYul8UY5MDIcc$b2c2d5a30c775d0c54a2f399bacb56b8fc9c04c5f31b6e0587248ef47d549744', '2023-12-04', NULL),
(1093, 2, 'El profe2', 'Davila', 'elprofe@gmail.com', 'Ipiales', '3156621234', 'M', 'sha256$jKSU5uWjZa6YzoYA$d67183ee2a2cbd1908558dd8f9866e9b177dee867c8e18e7f5c544e4e96d21a1', '2023-12-05', NULL),
(1095, 2, 'alejandro', 'Mueses', 'alejop@gmail.com', 'asasd', '3105084629', 'M', 'sha256$N4nKHUZxaiKCrXAP$a331089b73a0d3a8b62c8886beaebbf0372865b43cd78053f1e53aaa6b0f20de', '2024-1-4', NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `carrito`
--
ALTER TABLE `carrito`
  ADD PRIMARY KEY (`id_carrito`),
  ADD KEY `id` (`id`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `categoria`
--
ALTER TABLE `categoria`
  ADD PRIMARY KEY (`id_categoria`);

--
-- Indices de la tabla `pedido`
--
ALTER TABLE `pedido`
  ADD PRIMARY KEY (`id_pedido`),
  ADD KEY `id_carrito` (`id`);

--
-- Indices de la tabla `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`id_producto`),
  ADD KEY `categoria` (`categoria`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `carrito`
--
ALTER TABLE `carrito`
  MODIFY `id_carrito` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT de la tabla `categoria`
--
ALTER TABLE `categoria`
  MODIFY `id_categoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `pedido`
--
ALTER TABLE `pedido`
  MODIFY `id_pedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `producto`
--
ALTER TABLE `producto`
  MODIFY `id_producto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1096;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `carrito`
--
ALTER TABLE `carrito`
  ADD CONSTRAINT `carrito_ibfk_1` FOREIGN KEY (`id`) REFERENCES `usuario` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `carrito_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`) ON DELETE CASCADE;

--
-- Filtros para la tabla `producto`
--
ALTER TABLE `producto`
  ADD CONSTRAINT `producto_ibfk_1` FOREIGN KEY (`categoria`) REFERENCES `categoria` (`id_categoria`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
