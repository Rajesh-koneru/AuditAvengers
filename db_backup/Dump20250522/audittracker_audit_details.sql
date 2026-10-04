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
-- Table structure for table `audit_details`
--

DROP TABLE IF EXISTS `audit_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_details` (
  `Audit_id` varchar(20) NOT NULL,
  `Audit_type` varchar(40) DEFAULT NULL,
  `industry` varchar(20) DEFAULT NULL,
  `Date` datetime DEFAULT NULL,
  `Auditors_require` int DEFAULT NULL,
  `Days` int DEFAULT NULL,
  `Qualification` varchar(50) DEFAULT NULL,
  `equipment` varchar(20) DEFAULT NULL,
  `loction` varchar(50) DEFAULT NULL,
  `Amount` int DEFAULT NULL,
  `requirements` varchar(50) DEFAULT NULL,
  `Client_id` varchar(20) DEFAULT NULL,
  `state` varchar(30) DEFAULT NULL,
  `client` varchar(30) DEFAULT NULL,
  `whatsappLink` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`Audit_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_details`
--

LOCK TABLES `audit_details` WRITE;
/*!40000 ALTER TABLE `audit_details` DISABLE KEYS */;
INSERT INTO `audit_details` VALUES ('1','physical','educ','0001-03-25 00:00:00',1,2,'B.com','laptop required','hyd',1000,'bike required','ccaa01',NULL,NULL,NULL),('2','physical','educ','0001-03-25 00:00:00',1,2,'B.com','laptop required','hyd',1000,'bike required','ccaa01',NULL,NULL,NULL),('AA00010','phy','edu','2025-05-22 00:00:00',1,1,'cs/b.tech','laptop','hyd',500,'laptop','12345',NULL,NULL,NULL),('AA000154','phy','edu','2025-05-22 00:00:00',1,1,'cs/b.tech','laptop','hyd',560,'laptop','78648',NULL,NULL,'https://chat.whatsapp.com/BgZFmrhGZc12Lv6LWdRVJM'),('AA00017','phy','edu','2025-05-14 00:00:00',1,1,'cs','laptop','hyd',800,'laptop','12345',NULL,NULL,NULL),('AA00018','phy','edu','2025-05-22 00:00:00',1,2,'cs/b.tech','laptop','hyd',900,'bike','12345',NULL,NULL,NULL),('AA00019','phy','edu','2025-04-30 00:00:00',2,1,'cs/btech','laptop','vishakaptnam',1000,'laptop','12345',NULL,NULL,NULL);
/*!40000 ALTER TABLE `audit_details` ENABLE KEYS */;
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
