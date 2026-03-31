-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: tradeindia_data
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `trade_india_link`
--

DROP TABLE IF EXISTS `trade_india_link`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trade_india_link` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `URL` varchar(300) DEFAULT NULL,
  `CATEGORY` varchar(300) DEFAULT NULL,
  `STATUS` varchar(20) DEFAULT 'PENDING',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trade_india_link`
--

LOCK TABLES `trade_india_link` WRITE;
/*!40000 ALTER TABLE `trade_india_link` DISABLE KEYS */;
INSERT INTO `trade_india_link` VALUES (1,'https://www.tradeindia.com/seller/agriculture/','AGRICULTURE','Done'),(2,'https://www.tradeindia.com/seller/apparel-fashion/','APPAREL-FASHION','Done'),(3,'https://www.tradeindia.com/seller/automobile/','AUTOMOBILE','PENDING'),(4,'https://www.tradeindia.com/seller/brass-hardware-components/','BRASS-HARDWARE-COMPONENTS','PENDING'),(5,'https://www.tradeindia.com/seller/chemicals/','CHEMICALS','PENDING'),(6,'https://www.tradeindia.com/seller/computer-hardware-software/','COMPUTER-HARDWARE-SOFTWARE','PENDING'),(7,'https://www.tradeindia.com/seller/construction-real-estate/','CONSTRUCTION-REAL-ESTATE','PENDING'),(8,'https://www.tradeindia.com/seller/consumer-electronics/','CONSUMER-ELECTRONICS','PENDING'),(9,'https://www.tradeindia.com/seller/electronics-electrical-supplies/','ELECTRONICS-ELECTRICAL-SUPPLIES','PENDING'),(10,'https://www.tradeindia.com/seller/energy-power/','ENERGY-POWER','PENDING'),(11,'https://www.tradeindia.com/seller/environment-pollution/','ENVIRONMENT-POLLUTION','PENDING'),(12,'https://www.tradeindia.com/seller/food-beverage/','FOOD-BEVERAGE','PENDING'),(13,'https://www.tradeindia.com/seller/furniture/','FURNITURE','PENDING'),(14,'https://www.tradeindia.com/seller/gifts-crafts/','GIFTS-CRAFTS','PENDING'),(15,'https://www.tradeindia.com/seller/health-beauty/','HEALTH-BEAUTY','PENDING'),(16,'https://www.tradeindia.com/seller/home-supplies/','HOME-SUPPLIES','PENDING'),(17,'https://www.tradeindia.com/seller/home-textiles-furnishings/','HOME-TEXTILES-FURNISHINGS','PENDING'),(18,'https://www.tradeindia.com/seller/hospital-medical-supplies/','HOSPITAL-MEDICAL-SUPPLIES','PENDING'),(19,'https://www.tradeindia.com/seller/hotel-supplies-equipment/','HOTEL-SUPPLIES-EQUIPMENT','PENDING'),(20,'https://www.tradeindia.com/seller/industrial-supplies/','INDUSTRIAL-SUPPLIES','PENDING'),(21,'https://www.tradeindia.com/seller/jewelry-gemstones/','JEWELRY-GEMSTONES','PENDING'),(22,'https://www.tradeindia.com/seller/leather-leather-products/','LEATHER-LEATHER-PRODUCTS','PENDING'),(23,'https://www.tradeindia.com/seller/machinery/','MACHINERY','PENDING'),(24,'https://www.tradeindia.com/seller/mineral-metals/','MINERAL-METALS','PENDING'),(25,'https://www.tradeindia.com/seller/office-school-supplies/','OFFICE-SCHOOL-SUPPLIES','PENDING'),(26,'https://www.tradeindia.com/seller/packaging-paper/','PACKAGING-PAPER','PENDING'),(27,'https://www.tradeindia.com/seller/pharmaceuticals/','PHARMACEUTICALS','PENDING'),(28,'https://www.tradeindia.com/seller/pipes-tubes-fittings/','PIPES-TUBES-FITTINGS','PENDING'),(29,'https://www.tradeindia.com/seller/plastics-products/','PLASTICS-PRODUCTS','PENDING'),(30,'https://www.tradeindia.com/seller/printing-publishing/','PRINTING-PUBLISHING','PENDING'),(31,'https://www.tradeindia.com/seller/scientific-laboratory-instruments/','SCIENTIFIC-LABORATORY-INSTRUMENTS','PENDING'),(32,'https://www.tradeindia.com/seller/security-protection/','SECURITY-PROTECTION','PENDING'),(33,'https://www.tradeindia.com/seller/sports-entertainment/','SPORTS-ENTERTAINMENT','PENDING'),(34,'https://www.tradeindia.com/seller/telecommunications/','TELECOMMUNICATIONS','PENDING'),(35,'https://www.tradeindia.com/seller/textiles-fabrics/','TEXTILES-FABRICS','PENDING'),(36,'https://www.tradeindia.com/seller/toys/','TOYS','PENDING'),(37,'https://www.tradeindia.com/seller/transportation/','TRANSPORTATION','PENDING');
/*!40000 ALTER TABLE `trade_india_link` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-31 18:43:52
