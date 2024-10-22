-- MySQL dump 10.13  Distrib 5.7.21, for Linux (x86_64)
--
-- Host: localhost    Database: LegendLeagueSeasons
-- ------------------------------------------------------
-- Server version	5.7.21-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `2015-08`
--

DROP TABLE IF EXISTS `2015-08`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `2015-08` (
  `rank` int(10) DEFAULT NULL,
  `trophies` int(5) DEFAULT NULL,
  `tag` varchar(15) DEFAULT NULL,
  `name` varchar(30) DEFAULT NULL,
  `expLevel` int(4) DEFAULT NULL,
  `attackWins` int(8) DEFAULT NULL,
  `defenseWins` int(8) DEFAULT NULL,
  `clanTag` varchar(15) DEFAULT NULL,
  `clanName` varchar(30) DEFAULT NULL,
  `clanBadgeURL` varchar(60) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `2015-08`
--

LOCK TABLES `2015-08` WRITE;
/*!40000 ALTER TABLE `2015-08` DISABLE KEYS */;
INSERT INTO `2015-08` VALUES (1,5015,'#LQVYV8VJ','almghool',140,271,7,'#PJUL80GY','GULF KNIGHTS','rU0ub0XoQRV14xrgDq2B8N0KvC_kPTBBWK4nm7W2H-8'),(2,4997,'#PRPV9G99','B0ssh0gg',164,15,1,'#YLQJQRJ8','.l.™','ncwnIvqHq0Fb3YWSWUNIoguTxOqQ2D2046RvbS7kjX8'),(3,4990,'#9LUQQ8RQ','skyreaper',143,253,8,'#PJUL80GY','GULF KNIGHTS','rU0ub0XoQRV14xrgDq2B8N0KvC_kPTBBWK4nm7W2H-8'),(4,4983,'#82CUU208','Up in smoke Pie',164,268,10,'#YUUGJ0R9','QW','owgIylfqmkTMSMHIWrm2MaguQ-t7LdElfJhc2nHxl2c'),(8,4976,'#PCLR29QC','Qatar',159,300,11,'#L002LPCL','Emirates','CA5Wbb0u_guAvM00fbdx8qUclAK9Z-Wq09UZu6VEaIU'),(11,4971,'#90LRVGP0','TWISTER',167,284,5,'#PJUL80GY','GULF KNIGHTS','rU0ub0XoQRV14xrgDq2B8N0KvC_kPTBBWK4nm7W2H-8'),(13,4968,'#8P92RUV2','big small',153,218,9,'#L002LPCL','Emirates','CA5Wbb0u_guAvM00fbdx8qUclAK9Z-Wq09UZu6VEaIU'),(15,4965,'#9V00LLQ8','༺࿅ོALLEXCEED࿅ོ༻',151,210,13,'#PJUL80GY','GULF KNIGHTS','rU0ub0XoQRV14xrgDq2B8N0KvC_kPTBBWK4nm7W2H-8'),(19,4958,'#P22PJVRQ','battlebee',160,241,10,'#PJUL80GY','GULF KNIGHTS','rU0ub0XoQRV14xrgDq2B8N0KvC_kPTBBWK4nm7W2H-8'),(20,4957,'#JGQ9CQQC','AL-CONGRESS',151,250,9,'#L002LPCL','Emirates','CA5Wbb0u_guAvM00fbdx8qUclAK9Z-Wq09UZu6VEaIU'),(29,4945,'#R0CGVR8U','Adel',171,250,12,'#L002LPCL','Emirates','CA5Wbb0u_guAvM00fbdx8qUclAK9Z-Wq09UZu6VEaIU'),(48,4921,'#GUV2GQGJ','༺།ོ༼A H K༽།ོ༻',191,284,12,'#PJUL80GY','GULF KNIGHTS','rU0ub0XoQRV14xrgDq2B8N0KvC_kPTBBWK4nm7W2H-8');
/*!40000 ALTER TABLE `2015-08` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-04-09  5:20:50
