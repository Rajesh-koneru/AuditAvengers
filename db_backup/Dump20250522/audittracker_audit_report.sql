-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: audittracker
-- ------------------------------------------------------
-- Server version	9.1.0

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
-- Table structure for table `audit_report`
--

DROP TABLE IF EXISTS `audit_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_report` (
  `Audit_id` varchar(10) NOT NULL,
  `auditor_id` varchar(20) DEFAULT NULL,
  `planned_date` datetime DEFAULT NULL,
  `State` varchar(20) DEFAULT NULL,
  `Client_id` varchar(20) NOT NULL,
  `Contact` bigint DEFAULT NULL,
  `Audit_status` varchar(20) DEFAULT NULL,
  `payment_amount` int DEFAULT NULL,
  `payment_status` varchar(20) DEFAULT NULL,
  `auditor_name` varchar(20) DEFAULT NULL,
  `audit_type` varchar(20) DEFAULT NULL,
  `location` varchar(20) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_report`
--

LOCK TABLES `audit_report` WRITE;
/*!40000 ALTER TABLE `audit_report` DISABLE KEYS */;
INSERT INTO `audit_report` VALUES ('1','AUD001',NULL,'undefined','ccaa01',934524684,'Pending',1000,'Requested','raju','physical','hyd','raju@gmail.com'),('AA000154','AUD004','2025-05-22 00:00:00','undefined','78648',9390193971,'Pending',1000,'Paid','rajesh koneru','phy','hyd','rajeshkoneru1929@gmail.com'),('AA000154','AUD018','2025-05-22 00:00:00','undefined','78648',9390193971,'Completed',800,'Unpaid','rajesh koneru','phy','hyd','rajeshkoneru1929@gmail.com'),('AA000154','AUD019','2025-05-22 00:00:00','undefined','78648',9390193971,'In Progress',800,'Requested','rajesh koneru','phy','hyd','rajeshkoneru1929@gmail.com'),('AA000154','AUD005','2025-05-22 00:00:00','undefined','78648',9390193971,'pending',1000,'pending','rajesh koneru','phy','hyd','rajeshkoneru1929@gmail.com'),('1','AUD009',NULL,'undefined','ccaa01',9390193971,'pending',2000,'pending','rajesh koneru','physical','hyd','rajeshkoneru1929@gmail.com'),('1','AUD001',NULL,'undefined','ccaa01',934524684,'pending',1000,'Requested','raju','physical','hyd','raju@gmail.com'),('1','AUD007',NULL,'undefined','ccaa01',965875596,'pending',500,'pending','rajesh','physical','hyd','raju11@gmail.com'),('2','AUD015',NULL,'undefined','ccaa01',9390193971,'pending',800,'pending','rajesh koneru','physical','hyd','rajeshkoneru1929@gmail.com'),('1','AUD001',NULL,'undefined','ccaa01',934524684,'pending',1000,'Requested','raju','physical','hyd','raju@gmail.com'),('1','AUD001',NULL,'undefined','ccaa01',934524684,'pending',1000,'Requested','raju','physical','hyd','raju@gmail.com'),('AA000154','AUD012','2025-05-22 00:00:00','undefined','78648',9390193971,'pending',1000,'pending','rajesh koneru','phy','hyd','rajeshkoneru1929@gmail.com'),('AA000154','AUD014','2025-05-22 00:00:00','undefined','78648',9390193971,'pending',800,'pending','rajesh koneru','phy','hyd','rajeshkoneru1929@gmail.com'),('AA000154','AUD012','2025-05-22 00:00:00','undefined','78648',9390193971,'pending',1000,'pending','rajesh koneru','phy','hyd','rajeshkoneru1929@gmail.com'),('AA000154','AUD017','2025-05-22 00:00:00','undefined','78648',9390193971,'pending',800,'pending','rajesh koneru','phy','hyd','rajeshkoneru1929@gmail.com'),('1','AUD001',NULL,'undefined','ccaa01',983748279,'pending',1000,'Requested','raghu','physical','hyd','raghu1234@gmail.com'),('AA000154','AUD020','2025-05-22 00:00:00','undefined','78648',8459218265,'pending',1000,'pending','shiva','phy','hyd','shiva1234@gmail.com'),('AA000154','AUD020','2025-05-22 00:00:00','undefined','78648',8459218265,'pending',1000,'pending','shiva','phy','hyd','shiva1234@gmail.com'),('AA000154','AUD020','2025-05-22 00:00:00','undefined','78648',8459218265,'pending',1000,'pending','shiva','phy','hyd','shiva1234@gmail.com'),('AA000154','AUD020','2025-05-22 00:00:00','undefined','78648',8459218265,'pending',1000,'pending','shiva','phy','hyd','shiva1234@gmail.com'),('AA000154','AUD020','2025-05-22 00:00:00','undefined','78648',8459218265,'pending',8000,'pending','shiva','phy','hyd','shiva1234@gmail.com'),('AA00010','AUD021','2025-05-22 00:00:00','undefined','12345',9685741233,'pending',100,'pending','ravi','phy','hyd','ravi54321@gmail.com'),('AA00010','AUD021','2025-05-22 00:00:00','undefined','12345',9390193971,'pending',8222,'pending','sai','phy','hyd','rajeshkoneru1929@gmail.com'),('AA00010','AUD022','2025-05-22 00:00:00','undefined','12345',9685741233,'pending',1000,'pending','ravi','phy','hyd','ravi54321@gmail.com'),('2','AUD023',NULL,'undefined','ccaa01',9390193971,'pending',1000,'pending','rajesh koneru','physical','hyd','rajeshkoneru1929@gmail.com'),('1','AUD024',NULL,'undefined','ccaa01',9390193971,'pending',1000,'pending','rajesh koneru','physical','hyd','rajeshkoneru1929@gmail.com'),('2','AUD025',NULL,'undefined','ccaa01',9390193971,'pending',1000,'pending','rajesh koneru','physical','hyd','rajeshkoneru1929@gmail.com'),('2','AUD026',NULL,'undefined','ccaa01',9390193971,'pending',1000,'pending','rajesh koneru','physical','hyd','rajeshkoneru1929@gmail.com'),('AA00019','AUD027','2025-04-30 00:00:00','undefined','12345',9390193971,'pending',1000,'pending','shibv','phy','vishakaptnam','rajeshkoneru1929@gmail.com'),('AA00018','AUD028','2025-05-22 00:00:00','undefined','12345',9390193971,'pending',800,'pending','rajesh koneru','phy','hyd','rajeshkoneru1929@gmail.com'),('AA000154','AUD029','2025-05-22 00:00:00','undefined','78648',9390193971,'pending',899,'pending','rajesh koneru','phy','hyd','rajeshkoneru1929@gmail.com'),('AA00019','AUD030','2025-04-30 00:00:00','undefined','12345',9390193971,'pending',1000,'pending','shibv','phy','vishakaptnam','rajeshkoneru1929@gmail.com'),('AA00018','AUD031','2025-05-22 00:00:00','undefined','12345',9390193971,'pending',5222,'pending','rajesh koneru','phy','hyd','rajeshkoneru1929@gmail.com'),('AA000154','AUD032','2025-05-22 00:00:00','undefined','78648',9390193971,'pending',1000,'pending','rajesh koneru','phy','hyd','rajeshkoneru1929@gmail.com'),('1','AUD033',NULL,'undefined','ccaa01',9390193971,'pending',1000,'pending','rajesh koneru','physical','hyd','rajeshkoneru1929@gmail.com'),('2','AUD034',NULL,'undefined','ccaa01',8008129943,'pending',1000,'pending','Raghu','physical','hyd','raghavendhargpth@gmail.com');
/*!40000 ALTER TABLE `audit_report` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-22  9:54:32
