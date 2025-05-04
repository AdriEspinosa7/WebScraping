-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 04-05-2025 a las 11:15:49
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
-- Base de datos: `bolsa`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `composicion_ibex35`
--

CREATE TABLE `composicion_ibex35` (
  `id` int(11) NOT NULL,
  `simbolo` varchar(10) NOT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `titulos_antes` bigint(20) DEFAULT NULL,
  `estatus` varchar(50) DEFAULT NULL,
  `modificaciones` varchar(255) DEFAULT NULL,
  `comp` bigint(20) DEFAULT NULL,
  `coef_ff` decimal(5,2) DEFAULT NULL,
  `fecha_insercion` date NOT NULL,
  `nombre_pdf` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `composicion_ibex35`
--

INSERT INTO `composicion_ibex35` (`id`, `simbolo`, `nombre`, `titulos_antes`, `estatus`, `modificaciones`, `comp`, `coef_ff`, `fecha_insercion`, `nombre_pdf`) VALUES
(302, 'ACX', 'ACERINOX', 249335371, NULL, '', 249335371, 100.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(303, 'AENA', 'AENA', 120000000, NULL, '', 120000000, 80.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(304, 'AMS', 'AMADEUS IT', 450499205, NULL, '', 450499205, 100.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(305, 'ANA', 'ACCIONA', 43885322, NULL, '', 43885322, 80.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(306, 'ANE', 'ACCIONA ENER', 64952366, NULL, '', 64952366, 20.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(307, 'BBVA', 'BBVA', 5763285465, NULL, '', 5763285465, 100.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(308, 'BKT', 'BANKINTER', 898866154, NULL, '', 898866154, 100.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(309, 'CABK', 'CAIXABANK', 5739950277, NULL, '', 5739950277, 80.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(310, 'CLNX', 'CELLNEX', 706475375, NULL, '', 706475375, 100.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(311, 'COL', 'INM.COLONIAL', 250937875, NULL, '', 250937875, 40.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(312, 'ELE', 'ENDESA', 423500847, NULL, '', 423500847, 40.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(313, 'ENG', 'ENAGAS', 261990074, NULL, '', 261990074, 100.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(314, 'FDR', 'FLUIDRA', 115277442, NULL, '', 115277442, 60.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(315, 'FER', 'FERROVIAL SE', 739565455, NULL, '-10005504', 729559951, 100.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(316, 'GRF', 'GRIFOLS', 426129798, NULL, '', 426129798, 100.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(317, 'IAG', 'INT.AIRL.GRP', 4971476010, NULL, '', 4971476010, 100.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(318, 'IBE', 'IBERDROLA', 6364251000, NULL, '76310000', 6440561000, 100.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(319, 'IDR', 'INDRA A', 176654402, NULL, '', 176654402, 100.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(320, 'ITX', 'INDITEX', 1869991200, NULL, '', 1869991200, 60.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(321, 'LOG', 'LOGISTA', 106200000, NULL, '', 106200000, 80.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(322, 'MAP', 'MAPFRE', 1847731964, NULL, '', 1847731964, 60.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(323, 'MRL', 'MERLIN PROP.', 563724899, NULL, '', 563724899, 100.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(324, 'MTS', 'ARCEL.MITTAL', 170561954, NULL, '', 170561954, 20.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(325, 'NTGY', 'NATURGY', 193922760, NULL, '', 193922760, 20.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(326, 'RED', 'REDEIA CORPO', 541080000, NULL, '', 541080000, 100.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(327, 'REP', 'REPSOL', 1177396053, NULL, '-20000000', 1157396053, 100.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(328, 'ROVI', 'LABORAT.ROVI', 30741457, NULL, '', 30741457, 60.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(329, 'SAB', 'B. SABADELL', 5440221447, NULL, '-52531365', 5387690082, 100.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(330, 'SAN', 'SANTANDER', 15152492322, NULL, '', 15152492322, 100.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(331, 'SCYR', 'SACYR', 779906655, NULL, '16951143', 796857798, 100.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(332, 'SLR', 'SOLARIA', 124950876, NULL, '', 124950876, 100.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(333, 'TEF', 'TELEFONICA', 5670161554, NULL, '', 5670161554, 100.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(334, 'UNI', 'UNICAJA', 2057147574, NULL, '', 2057147574, 80.00, '2025-04-23', 'Aviso_Gestor_Indices_02-25.pdf'),
(697, 'PUIG', 'PUIG BRANDS', 174819678, NULL, '', 174819678, 100.00, '2025-04-27', 'Aviso_Gestor_Indices_02-25.pdf'),
(744, 'ACS', 'ACS CONST.', 271664594, NULL, '', 271664594, 100.00, '2025-04-27', 'Aviso_Gestor_Indices_02-25.pdf');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `datos_empresas`
--

CREATE TABLE `datos_empresas` (
  `id` int(11) NOT NULL,
  `empresa` varchar(10) NOT NULL,
  `anio` int(11) NOT NULL,
  `capitalizacion` bigint(20) DEFAULT NULL,
  `num_acciones` bigint(20) DEFAULT NULL,
  `precio_cierre` decimal(14,4) DEFAULT NULL,
  `ultimo_precio` decimal(14,4) DEFAULT NULL,
  `precio_max` decimal(14,4) DEFAULT NULL,
  `precio_min` decimal(14,4) DEFAULT NULL,
  `volumen` varchar(50) DEFAULT NULL,
  `efectivo` varchar(50) DEFAULT NULL,
  `fecha_registro` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `datos_empresas`
--

INSERT INTO `datos_empresas` (`id`, `empresa`, `anio`, `capitalizacion`, `num_acciones`, `precio_cierre`, `ultimo_precio`, `precio_max`, `precio_min`, `volumen`, `efectivo`, `fecha_registro`) VALUES
(1, 'BBVA', 2021, 35006405, 6667887, 5.2500, 5.2500, 6.2920, 3.7360, '5862801', '30213869', '2021-12-31'),
(2, 'BBVA', 2022, 33973677, 6030117, 5.6340, 5.6340, 6.1200, 3.9720, '5899707', '29549325', '2022-12-31'),
(3, 'BBVA', 2023, 48022898, 5837940, 8.2260, 8.2260, 8.7260, 5.6690, '4228993', '29433050', '2023-12-31'),
(4, 'BBVA', 2024, 54474574, 5763285, 9.4520, 9.4520, 11.2750, 7.9740, '3015739', '28861666', '2024-12-31'),
(5, 'BBVA', 2025, 68381382, 5763285, 11.8650, 11.8650, 13.5900, 8.9660, '951815', '11185516', '2025-04-17'),
(6, 'Inditex', 2021, 88918082, 3116652, 28.5300, 28.5300, 32.8500, 24.3400, '1174347', '34868943', '2021-12-31'),
(7, 'Inditex', 2022, 77448802, 3116652, 24.8500, 24.8500, 29.0600, 18.5450, '1108617', '25120695', '2022-12-31'),
(8, 'Inditex', 2023, 122889588, 3116652, 39.4300, 39.4300, 39.6700, 25.0000, '786169', '25565546', '2023-12-31'),
(9, 'Inditex', 2024, 154710605, 3116652, 49.6400, 49.6400, 56.3400, 37.1300, '555816', '25951808', '2024-12-31'),
(10, 'Inditex', 2025, 146108646, 3116652, 46.8800, 46.8800, 55.8400, 42.1000, '167035', '8078808', '2025-04-17'),
(11, 'Santander', 2021, 50990156, 17340641, 2.9405, 2.9405, 3.5090, 2.3750, '13483911', '41194831', '2021-12-31'),
(12, 'Santander', 2022, 47066310, 16794402, 2.8025, 2.8025, 3.4820, 2.3240, '14216831', '40261523', '2022-12-31'),
(13, 'Santander', 2023, 61167980, 16184146, 3.7795, 3.7795, 3.9695, 2.8120, '11132346', '38143523', '2023-12-31'),
(14, 'Santander', 2024, 67648302, 15152492, 4.4645, 4.4645, 4.9280, 3.5630, '7712591', '33409809', '2024-12-31'),
(15, 'Santander', 2025, 90036109, 15152492, 5.9420, 5.9420, 6.6610, 4.2555, '2950638', '16756634', '2025-04-17'),
(16, 'BBVA', 2025, 68669546, 5763285, 11.9150, 11.9150, 13.5900, 8.9660, '962539', '11312980', '2025-04-22'),
(17, 'Inditex', 2025, 148103303, 3116652, 47.5200, 47.5200, 55.8400, 42.1000, '172411', '8316989', '2025-04-22'),
(18, 'Santander', 2025, 91718036, 15152492, 6.0530, 6.0530, 6.6610, 4.2555, '2983341', '16946294', '2025-04-22'),
(19, 'BBVA', 2025, 71781720, 5763285, 12.4550, 12.4550, 13.5900, 8.9660, '987076', '11615488', '2025-04-25'),
(20, 'Inditex', 2025, 151780952, 3116652, 48.7000, 48.7000, 55.8400, 42.1000, '186852', '9017525', '2025-04-25'),
(21, 'Santander', 2025, 97218391, 15152492, 6.4160, 6.4160, 6.6610, 4.2555, '3149350', '17988535', '2025-04-25'),
(22, 'BBVA', 2025, 71118943, 5763285, 12.3400, 12.3400, 13.5900, 8.9660, '1007007', '11864053', '2025-04-29'),
(23, 'Inditex', 2025, 146170979, 3116652, 46.9000, 46.9000, 55.8400, 42.1000, '193295', '9326071', '2025-04-29'),
(24, 'Santander', 2025, 97475983, 15152492, 6.4330, 6.4330, 6.6610, 4.2555, '3221654', '18412633', '2025-04-29'),
(25, 'BBVA', 2025, 70427348, 5763285, 12.2200, 12.2200, 13.5900, 8.9660, '1030838', '12152812', '2025-05-02'),
(26, 'Inditex', 2025, 149318797, 3116652, 47.9100, 47.9100, 55.8400, 42.1000, '199649', '9626759', '2025-05-02'),
(27, 'Santander', 2025, 96021344, 15152492, 6.3370, 6.3370, 6.6610, 4.2555, '3331879', '19097120', '2025-05-02');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `indices`
--

CREATE TABLE `indices` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `variacion` varchar(20) NOT NULL,
  `porcentaje` varchar(20) NOT NULL,
  `fecha_hora` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `indices`
--

INSERT INTO `indices` (`id`, `nombre`, `precio`, `variacion`, `porcentaje`, `fecha_hora`) VALUES
(1, 'IBEX 35 (IBEX)', 12918.00, '0,00', '(0,00%)', '2025-04-20 11:44:32'),
(2, 'S&P 500 (SPX)', 5282.70, '+7,00', '(+0,13%)', '2025-04-20 11:44:38'),
(3, 'Nasdaq 100 (NDX)', 18258.09, '+0,45', '(+0,00%)', '2025-04-20 11:44:44'),
(4, 'DAX (GDAXI)', 21205.86, '-105,16', '(-0,49%)', '2025-04-20 11:44:51'),
(5, 'MSCI World (MIWO00000PUS)', 3476.06, '+2,00', '(+0,06%)', '2025-04-20 11:44:58'),
(6, 'IBEX 35 (IBEX)', 12918.00, '0,00', '(0,00%)', '2025-04-21 17:36:58'),
(7, 'S&P 500 (SPX)', 5136.94, '-145,76', '(-2,76%)', '2025-04-21 17:37:04'),
(8, 'Nasdaq 100 (NDX)', 17727.31, '-530,78', '(-2,91%)', '2025-04-21 17:37:11'),
(9, 'DAX (GDAXI)', 21205.86, '-105,16', '(-0,49%)', '2025-04-21 17:37:17'),
(10, 'MSCI World (MIWO00000PUS)', 3416.05, '-60,01', '(-1,73%)', '2025-04-21 17:37:23'),
(11, 'IBEX 35 (IBEX)', 13010.60, '+92,60', '(+0,72%)', '2025-04-22 21:08:25'),
(12, 'S&P 500 (SPX)', 5279.24, '+121,04', '(+2,35%)', '2025-04-22 21:08:32'),
(13, 'Nasdaq 100 (NDX)', 18248.39, '+440,09', '(+2,47%)', '2025-04-22 21:08:40'),
(14, 'DAX (GDAXI)', 21278.68, '+72,82', '(+0,34%)', '2025-04-22 21:08:47'),
(15, 'MSCI World (MIWO00000PUS)', 3481.01, '+56,68', '(+1,66%)', '2025-04-22 21:08:54'),
(16, 'IBEX 35 (IBEX)', 13169.10, '+158,50', '(+1,22%)', '2025-04-23 18:35:41'),
(17, 'S&P 500 (SPX)', 5385.52, '+97,77', '(+1,85%)', '2025-04-23 18:35:49'),
(18, 'Nasdaq 100 (NDX)', 18734.06, '+457,65', '(+2,50%)', '2025-04-23 18:35:56'),
(19, 'DAX (GDAXI)', 21932.19, '+638,66', '(+3,00%)', '2025-04-23 18:36:03'),
(20, 'MSCI World (MIWO00000PUS)', 3540.08, '+52,09', '(+1,49%)', '2025-04-23 18:36:10'),
(21, 'IBEX 35 (IBEX)', 13355.30, '+175,60', '(+1,33%)', '2025-04-27 23:52:12'),
(22, 'S&P 500 (SPX)', 5525.21, '+40,44', '(+0,74%)', '2025-04-27 23:52:19'),
(23, 'Nasdaq 100 (NDX)', 19432.56, '+218,16', '(+1,14%)', '2025-04-27 23:52:25'),
(24, 'DAX (GDAXI)', 22242.45, '+177,94', '(+0,81%)', '2025-04-27 23:52:32'),
(25, 'MSCI World (MIWO00000PUS)', 3618.48, '0,00', '(0,00%)', '2025-04-27 23:52:39'),
(26, 'IBEX 35 (IBEX)', 13366.90, '-89,20', '(-0,66%)', '2025-04-29 22:12:40'),
(27, 'S&P 500 (SPX)', 5563.90, '+35,15', '(+0,64%)', '2025-04-29 22:12:47'),
(28, 'Nasdaq 100 (NDX)', 19544.95, '+117,66', '(+0,61%)', '2025-04-29 22:12:54'),
(29, 'DAX (GDAXI)', 22425.83, '+154,16', '(+0,69%)', '2025-04-29 22:13:00'),
(30, 'MSCI World (MIWO00000PUS)', 3647.89, '+19,41', '(+0,53%)', '2025-04-29 22:13:06'),
(31, 'IBEX 35 (IBEX)', 13213.59, '-152,71', '(-1,14%)', '2025-04-30 10:08:52'),
(32, 'S&P 500 (SPX)', 5560.83, '+32,08', '(+0,58%)', '2025-04-30 10:08:59'),
(33, 'Nasdaq 100 (NDX)', 19544.95, '+117,66', '(+0,61%)', '2025-04-30 10:09:05'),
(34, 'DAX (GDAXI)', 22545.89, '+96,18', '(+0,43%)', '2025-04-30 10:09:12'),
(35, 'MSCI World (MIWO00000PUS)', 3651.04, '+3,83', '(+0,11%)', '2025-04-30 10:09:18'),
(36, 'IBEX 35 (IBEX)', 13446.70, '+158,90', '(+1,20%)', '2025-05-04 11:13:52'),
(37, 'S&P 500 (SPX)', 5686.67, '+82,53', '(+1,47%)', '2025-05-04 11:13:58'),
(38, 'Nasdaq 100 (NDX)', 20102.61, '+315,91', '(+1,60%)', '2025-05-04 11:14:05'),
(39, 'DAX (GDAXI)', 23086.65, '+589,67', '(+2,62%)', '2025-05-04 11:14:11'),
(40, 'MSCI World (MIWO00000PUS)', 3724.62, '+60,88', '(+1,66%)', '2025-05-04 11:14:17');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `composicion_ibex35`
--
ALTER TABLE `composicion_ibex35`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uk_pdf_simbolo` (`nombre_pdf`,`simbolo`);

--
-- Indices de la tabla `datos_empresas`
--
ALTER TABLE `datos_empresas`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `indices`
--
ALTER TABLE `indices`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `composicion_ibex35`
--
ALTER TABLE `composicion_ibex35`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2017;

--
-- AUTO_INCREMENT de la tabla `datos_empresas`
--
ALTER TABLE `datos_empresas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT de la tabla `indices`
--
ALTER TABLE `indices`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
