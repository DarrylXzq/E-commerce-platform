-- MySQL dump 10.13  Distrib 5.7.40, for Win64 (x86_64)
--
-- Host: localhost    Database: WAD_WEB
-- ------------------------------------------------------
-- Server version	5.7.40-log

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
-- Table structure for table `addresses_customer`
--

DROP TABLE IF EXISTS `addresses_customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `addresses_customer` (
  `address_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) NOT NULL,
  `country_name` varchar(50) NOT NULL,
  `province_name` varchar(50) NOT NULL,
  `city_name` varchar(50) NOT NULL,
  `address` varchar(100) NOT NULL,
  `receiver_name` varchar(255) NOT NULL,
  `receiver_phone` varchar(255) NOT NULL,
  PRIMARY KEY (`address_id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `addresses_customer_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `addresses_customer`
--

LOCK TABLES `addresses_customer` WRITE;
/*!40000 ALTER TABLE `addresses_customer` DISABLE KEYS */;
INSERT INTO `addresses_customer` VALUES (1,1,'china','sichuan','chnegdu','cdut','xiang','13808243006'),(2,1,'china','sichuan','dazhou','xuanhan','xiang','13333333'),(3,4,'America','Oregon','DAIRY','OR','xiang','13808243006'),(4,4,'china','sichuan','chengdu','cdut','name','13808243006'),(5,5,'china','sichuang','chengdu','cdut','xzq','13808243005');
/*!40000 ALTER TABLE `addresses_customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `addresses_vendor`
--

DROP TABLE IF EXISTS `addresses_vendor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `addresses_vendor` (
  `address_id` int(11) NOT NULL AUTO_INCREMENT,
  `vendor_id` int(11) NOT NULL,
  `country_name` varchar(50) NOT NULL,
  `province_name` varchar(50) NOT NULL,
  `city_name` varchar(50) NOT NULL,
  `address` varchar(100) NOT NULL,
  PRIMARY KEY (`address_id`),
  KEY `vendor_id` (`vendor_id`),
  CONSTRAINT `addresses_vendor_ibfk_1` FOREIGN KEY (`vendor_id`) REFERENCES `vendors` (`vendor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `addresses_vendor`
--

LOCK TABLES `addresses_vendor` WRITE;
/*!40000 ALTER TABLE `addresses_vendor` DISABLE KEYS */;
INSERT INTO `addresses_vendor` VALUES (1,2,'chin','sichuang','cheng','cdut'),(2,1,'china','shanxi','datong','hhh'),(3,5,'china','sichuan','chengdu','cdut');
/*!40000 ALTER TABLE `addresses_vendor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `announcements`
--

DROP TABLE IF EXISTS `announcements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `announcements` (
  `announcement_id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) NOT NULL,
  `content` text NOT NULL,
  `announcement_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`announcement_id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `announcements_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `announcements`
--

LOCK TABLES `announcements` WRITE;
/*!40000 ALTER TABLE `announcements` DISABLE KEYS */;
INSERT INTO `announcements` VALUES (7,206,'None','2023-05-20 14:18:30'),(8,206,'None','2023-05-20 14:44:46'),(9,206,'None','2023-05-20 14:45:05');
/*!40000 ALTER TABLE `announcements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carts`
--

DROP TABLE IF EXISTS `carts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `carts` (
  `cart_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `add_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `selected` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`cart_id`),
  KEY `customer_id` (`customer_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `carts_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`),
  CONSTRAINT `carts_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carts`
--

LOCK TABLES `carts` WRITE;
/*!40000 ALTER TABLE `carts` DISABLE KEYS */;
INSERT INTO `carts` VALUES (11,1,45,1,'2023-05-20 13:58:00',1),(13,1,47,1,'2023-05-20 14:04:05',0),(14,1,46,1,'2023-05-20 14:30:53',0),(15,4,45,1,'2023-05-20 14:32:33',0),(17,4,59,10,'2023-05-20 15:30:57',1),(18,4,54,1,'2023-05-20 15:45:12',1),(19,5,59,1,'2023-05-21 23:23:48',1),(20,5,55,1,'2023-05-21 23:23:55',1);
/*!40000 ALTER TABLE `carts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `categories` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `category_name` varchar(255) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `level` int(11) NOT NULL,
  PRIMARY KEY (`category_id`),
  KEY `parent_id` (`parent_id`),
  KEY `level_idx` (`level`),
  CONSTRAINT `categories_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `categories` (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Electronics',NULL,1),(2,'Home & Living',NULL,1),(3,'Fashion',NULL,1),(4,'Health & Beauty',NULL,1),(5,'Baby & Kids',NULL,1),(6,'Smartphones',1,2),(7,'Computers',1,2),(8,'Tablets',1,2),(9,'Smartwatches',1,2),(10,'Accessories',1,2),(11,'Furniture',2,2),(12,'Home Decor',2,2),(13,'Kitchenware',2,2),(14,'Bedding',2,2),(15,'Bath',2,2),(16,'Men\'s Clothing',3,2),(17,'Women\'s Clothing',3,2),(18,'Shoes',3,2),(19,'Accessories',3,2),(20,'Bags & Luggage',3,2),(21,'Skincare',4,2),(22,'Makeup',4,2),(23,'Personal Care',4,2),(24,'Fragrances',4,2),(25,'Supplements',4,2),(26,'Baby Clothing',5,2),(27,'Toys',5,2),(28,'Baby Gear',5,2),(29,'Learning & Education',5,2),(30,'Children\'s Books',5,2);
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comments` (
  `comment_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `comment` text NOT NULL,
  `comment_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`comment_id`),
  KEY `customer_id` (`customer_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`),
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
INSERT INTO `comments` VALUES (36,1,59,'good','2023-05-20 12:35:41'),(37,1,58,'bad','2023-05-20 12:36:01'),(38,1,54,'good','2023-05-20 12:36:18'),(39,1,57,'too expensive','2023-05-20 12:36:44'),(40,1,55,'beautiful skirt','2023-05-20 12:37:15'),(41,1,53,'good','2023-05-20 12:37:46'),(42,1,50,'comfortable shoes','2023-05-20 12:38:14'),(43,1,51,'too high','2023-05-20 12:38:58'),(44,1,47,'not suitable for the young man','2023-05-20 12:40:02'),(45,1,46,'very cute shows','2023-05-20 12:40:47'),(46,1,48,'suitable for home wear','2023-05-20 12:41:22'),(47,4,45,'<h1>Happy</h1>','2023-05-20 15:25:59');
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customers` (
  `customer_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `birthday` date DEFAULT NULL,
  `gender` enum('Male','Female') DEFAULT NULL,
  `registration_c` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `avatar` varchar(255) NOT NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'xiang','8086f9d391f95076ed825d6e99ccd2bec3797e5b91228d1eb8562e1a84f3e4fd','darryl-xiang@outlook.com','13808243006',NULL,'Male','2023-05-01 13:18:32','static/uploads\\4_28.png'),(2,'pl980210','3c94118b561c163ce8179cfaee63d24a99751ef2b18726f5cd64f0c2496a5af4','1351946910@qq.com','13541811182',NULL,NULL,'2023-05-01 16:03:36','../static/uploads/default_avatar.png'),(3,'xiang3','8086f9d391f95076ed825d6e99ccd2bec3797e5b91228d1eb8562e1a84f3e4fd','2307604976@qq.com','13808243008',NULL,NULL,'2023-05-05 22:15:25','../static/uploads/default_avatar.png'),(4,'xiangr','8086f9d391f95076ed825d6e99ccd2bec3797e5b91228d1eb8562e1a84f3e4fd','darryl-xiang438@outlook.com','13808243089',NULL,NULL,'2023-05-20 14:32:18','../static/uploads/default_avatar.png'),(5,'xiangtest','8086f9d391f95076ed825d6e99ccd2bec3797e5b91228d1eb8562e1a84f3e4fd','darryl-xiang123@outlook.com','13808243888',NULL,NULL,'2023-05-21 23:23:31','../static/uploads/default_avatar.png');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `favorites`
--

DROP TABLE IF EXISTS `favorites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `favorites` (
  `favorite_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `favorite_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `like_button` tinyint(1) DEFAULT NULL,
  `dislike_button` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`favorite_id`),
  UNIQUE KEY `customer_id` (`customer_id`,`product_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `favorites_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`),
  CONSTRAINT `favorites_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=234 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favorites`
--

LOCK TABLES `favorites` WRITE;
/*!40000 ALTER TABLE `favorites` DISABLE KEYS */;
INSERT INTO `favorites` VALUES (202,1,45,'2023-05-20 13:57:59',1,0),(206,1,59,'2023-05-20 12:32:42',1,0),(207,1,57,'2023-05-20 12:48:03',1,0),(208,1,56,'2023-05-20 12:32:53',1,0),(209,1,55,'2023-05-20 12:32:58',0,1),(210,1,54,'2023-05-20 12:33:08',1,0),(211,1,53,'2023-05-20 12:33:13',1,0),(212,1,50,'2023-05-20 12:33:30',0,1),(213,1,46,'2023-05-20 12:33:25',0,1),(215,1,49,'2023-05-20 12:33:35',1,0),(216,1,58,'2023-05-20 12:33:45',0,1),(217,1,48,'2023-05-20 12:34:23',1,0),(218,1,51,'2023-05-20 12:34:57',1,0),(219,1,52,'2023-05-20 12:35:20',1,0),(220,1,47,'2023-05-20 12:42:19',1,0),(232,4,48,'2023-05-20 16:04:34',1,0),(233,5,59,'2023-05-21 23:23:47',1,0);
/*!40000 ALTER TABLE `favorites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `histories`
--

DROP TABLE IF EXISTS `histories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `histories` (
  `history_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `action_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`history_id`),
  KEY `customer_id` (`customer_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `histories_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`),
  CONSTRAINT `histories_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `histories`
--

LOCK TABLES `histories` WRITE;
/*!40000 ALTER TABLE `histories` DISABLE KEYS */;
/*!40000 ALTER TABLE `histories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `order_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `delivery_time` datetime DEFAULT NULL,
  `confirm_time` datetime DEFAULT NULL,
  `status` enum('pending','paid','shipped','completed','cancelled') DEFAULT NULL,
  `payment_id` int(11) DEFAULT NULL,
  `address_id` int(11) NOT NULL,
  PRIMARY KEY (`order_id`),
  KEY `customer_id` (`customer_id`),
  KEY `product_id` (`product_id`),
  KEY `payment_id` (`payment_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`),
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`),
  CONSTRAINT `orders_ibfk_3` FOREIGN KEY (`payment_id`) REFERENCES `payment` (`payment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=230 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (204,1,45,1,180.00,'2023-05-20 12:45:16',NULL,NULL,'paid',124,1),(205,1,47,1,17.60,'2023-05-20 12:45:16',NULL,NULL,'paid',124,1),(206,1,45,1,180.00,'2023-05-20 14:15:48','2023-05-24 00:00:00',NULL,'completed',127,1),(207,1,47,1,17.60,'2023-05-20 14:15:48',NULL,NULL,'paid',127,1),(208,4,45,1,180.00,'2023-05-20 14:52:16',NULL,NULL,'paid',131,3),(209,4,45,1,180.00,'2023-05-20 14:54:58',NULL,NULL,'paid',132,4),(211,4,59,10,950.00,'2023-05-20 15:31:38',NULL,NULL,'cancelled',134,3),(212,4,59,10,950.00,'2023-05-20 15:32:09',NULL,NULL,'paid',135,3),(213,4,59,10,950.00,'2023-05-20 15:45:24',NULL,NULL,'cancelled',136,3),(214,4,54,1,3600.00,'2023-05-20 15:45:24',NULL,NULL,'cancelled',136,3),(215,4,59,10,950.00,'2023-05-20 16:03:41',NULL,NULL,'cancelled',137,3),(216,4,54,1,3600.00,'2023-05-20 16:03:41',NULL,NULL,'cancelled',137,3),(217,1,46,1,45.00,'2023-05-20 22:13:56',NULL,NULL,'paid',138,1),(218,1,46,1,45.00,'2023-05-20 23:12:49',NULL,NULL,'pending',139,1),(219,1,46,1,45.00,'2023-05-20 23:14:02',NULL,NULL,'paid',140,1),(227,1,45,1,180.00,'2023-05-21 00:52:26',NULL,NULL,'paid',147,1),(228,5,59,1,95.00,'2023-05-21 23:24:44',NULL,NULL,'paid',149,5),(229,5,55,1,46.55,'2023-05-21 23:24:44',NULL,NULL,'paid',149,5);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payment` (
  `payment_id` int(11) NOT NULL AUTO_INCREMENT,
  `payment_date` datetime DEFAULT NULL,
  `payment_status` varchar(50) NOT NULL,
  `finish_time` datetime DEFAULT NULL,
  PRIMARY KEY (`payment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=150 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES (124,'2023-05-20 12:45:16','paid','2023-05-20 12:46:32'),(125,'2023-05-20 13:59:05','pending',NULL),(126,'2023-05-20 13:59:09','pending',NULL),(127,'2023-05-20 14:15:48','paid','2023-05-20 14:16:26'),(128,'2023-05-20 14:32:39','pending',NULL),(129,'2023-05-20 14:41:48','pending',NULL),(130,'2023-05-20 14:50:04','pending',NULL),(131,'2023-05-20 14:52:16','paid','2023-05-20 14:53:05'),(132,'2023-05-20 14:54:58','paid','2023-05-20 14:55:30'),(134,'2023-05-20 15:31:38','cancelled',NULL),(135,'2023-05-20 15:32:09','paid','2023-05-20 15:32:49'),(136,'2023-05-20 15:45:24','cancelled',NULL),(137,'2023-05-20 16:03:41','cancelled',NULL),(138,'2023-05-20 22:13:56','paid','2023-05-20 22:14:27'),(139,'2023-05-20 23:12:49','pending',NULL),(140,'2023-05-20 23:14:02','paid','2023-05-20 23:14:31'),(147,'2023-05-21 00:52:26','paid','2023-05-21 00:53:16'),(148,'2023-05-21 23:24:10','pending',NULL),(149,'2023-05-21 23:24:44','paid','2023-05-21 23:25:37');
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products` (
  `product_id` int(11) NOT NULL AUTO_INCREMENT,
  `vendor_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text,
  `price` decimal(10,2) NOT NULL,
  `stock` int(11) NOT NULL,
  `picture` varchar(255) DEFAULT NULL,
  `likes` int(11) DEFAULT '0',
  `dislikes` int(11) DEFAULT '0',
  `promotion` decimal(10,2) DEFAULT NULL,
  `duration_start` datetime DEFAULT NULL,
  `duration_end` datetime DEFAULT NULL,
  `last_comment` datetime DEFAULT NULL,
  `last_like_dis` datetime DEFAULT NULL,
  `release_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `product_status` enum('active','inactive') DEFAULT NULL,
  PRIMARY KEY (`product_id`),
  KEY `vendor_id` (`vendor_id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`vendor_id`) REFERENCES `vendors` (`vendor_id`),
  CONSTRAINT `products_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (45,1,9,'WATCH','The blue watch',200.00,24,'../static/products/1684553980-1.jpg',1,0,10.00,'2023-05-12 00:00:00','2023-05-31 00:00:00','2023-05-20 15:25:59','2023-05-20 13:57:59','2023-05-20 14:19:34','active'),(46,1,18,'shoes','the pick shoes',50.00,95,'../static/products/1684554178-1.jpg',0,1,10.00,'2023-05-19 00:00:00','2023-06-01 00:00:00','2023-05-20 12:40:47','2023-05-20 12:33:25','2023-05-20 11:42:58','active'),(47,1,19,'hat','The beautiful hat',20.00,394,'../static/products/1684554238-1.jpg',1,0,12.00,'2023-05-16 00:00:00','2023-05-31 00:00:00','2023-05-20 12:40:02','2023-05-20 12:42:19','2023-05-20 11:43:58','active'),(48,1,17,'clothes','The pick clothes',30.00,100,'../static/products/1684554356-1.jpg',2,0,12.00,'2023-05-18 00:00:00','2023-05-28 00:00:00','2023-05-20 12:41:22','2023-05-20 16:04:34','2023-05-20 11:45:56','active'),(49,1,18,'Brown shoes','The nice Shoes, suitable for man',400.00,500,'../static/products/1684554888-1.jpg',1,0,23.00,'2023-05-19 00:00:00','2023-06-04 00:00:00',NULL,'2023-05-20 12:33:35','2023-05-20 11:54:48','active'),(50,1,18,'sport shoes','The nike sport shoes',300.00,488,'../static/products/1684554981-1.jpg',0,1,12.00,'2023-05-12 00:00:00','2023-05-28 00:00:00','2023-05-20 12:38:14','2023-05-20 12:33:30','2023-05-20 11:56:21','active'),(51,1,18,'high-heeled shoes','suitbale for women',388.00,100,'../static/products/1684555180-1.jpg',1,0,10.00,'2023-05-13 00:00:00','2023-05-26 00:00:00','2023-05-20 12:38:58','2023-05-20 12:34:57','2023-05-20 11:59:40','active'),(52,1,16,'jacket','That jacket is beautifully tailored.',123.00,200,'../static/products/1684555355-1.jpg',1,0,10.00,'2023-05-25 00:00:00','2023-06-08 00:00:00',NULL,'2023-05-20 12:35:20','2023-05-20 12:02:35','active'),(53,1,19,'Belt','The belt has a unique design.',23.00,23,'../static/products/1684555426-1.jpg',1,0,10.00,'2023-05-05 00:00:00','2023-06-09 00:00:00','2023-05-20 12:37:46','2023-05-20 12:33:13','2023-05-20 12:03:46','active'),(54,1,19,'jewellery','The unique design',4000.00,30,'../static/products/1684555838-1.jpg',1,0,10.00,'2023-05-18 00:00:00','2023-05-31 00:00:00','2023-05-20 12:36:18','2023-05-20 12:33:08','2023-05-20 12:10:38','active'),(55,1,17,'skirt','That skirt has a unique design.',49.00,399,'../static/products/1684556013-1.jpg',0,1,5.00,'2023-05-12 00:00:00','2023-05-26 00:00:00','2023-05-20 12:37:15','2023-05-20 12:32:58','2023-05-20 12:13:33','active'),(56,1,19,'watch','This watch is made of high-quality material.',5000.00,40,'../static/products/1684556221-1.jpg',1,0,5.00,'2023-05-20 00:00:00','2023-06-01 00:00:00',NULL,'2023-05-20 12:32:53','2023-05-20 12:17:01','active'),(57,1,9,'watch','The watch are elegantly polished.',200.00,30,'../static/products/1684556406-1.jpg',1,0,10.00,'2023-05-20 00:00:00','2023-05-30 00:00:00','2023-05-20 12:36:44','2023-05-20 12:48:03','2023-05-20 12:20:06','active'),(58,1,16,'jacket','That jacket is beautifully tailored.',300.00,10,'../static/products/1684556619-1.jpg',0,1,10.00,'2023-05-18 00:00:00','2023-06-01 00:00:00','2023-05-20 12:36:01','2023-05-20 12:33:45','2023-05-20 12:23:39','active'),(59,1,19,'perfume','Good smell of perfume',100.00,29,'../static/products/1684556872-1.jpg',2,0,5.00,'2023-05-18 00:00:00','2023-05-31 00:00:00','2023-05-20 12:35:41','2023-05-21 23:23:47','2023-05-20 12:27:52','active'),(63,6,18,'shoes','very nice shoes',200.00,100,'../static/products/1684683146-6.jpg',0,0,10.00,'2023-05-12 00:00:00','2023-06-01 00:00:00',NULL,NULL,'2023-05-21 23:32:26','active');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors`
--

DROP TABLE IF EXISTS `vendors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vendors` (
  `vendor_id` int(11) NOT NULL AUTO_INCREMENT,
  `vendor_name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `registration_v` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`vendor_id`),
  UNIQUE KEY `vendor_name` (`vendor_name`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors`
--

LOCK TABLES `vendors` WRITE;
/*!40000 ALTER TABLE `vendors` DISABLE KEYS */;
INSERT INTO `vendors` VALUES (1,'xianghhh','8086f9d391f95076ed825d6e99ccd2bec3797e5b91228d1eb8562e1a84f3e4fd','darryl-3432@outlook.com','13808345656','2023-04-30 22:28:33'),(2,'xiang','8086f9d391f95076ed825d6e99ccd2bec3797e5b91228d1eb8562e1a84f3e4fd','darryl-xiangh@outlook.com','13808243010','2023-05-01 13:08:23'),(3,'xiang1','8086f9d391f95076ed825d6e99ccd2bec3797e5b91228d1eb8562e1a84f3e4fd','darryl-xiang@outlook.com','13808243006','2023-05-01 13:11:53'),(4,'xiang_v','8086f9d391f95076ed825d6e99ccd2bec3797e5b91228d1eb8562e1a84f3e4fd','darryl-xiang33@outlook.com','13808243666','2023-05-20 15:01:05'),(5,'xiang_vv','8086f9d391f95076ed825d6e99ccd2bec3797e5b91228d1eb8562e1a84f3e4fd','darryl-xian66@outlook.com','13808246666','2023-05-20 15:06:33'),(6,'vendor','8086f9d391f95076ed825d6e99ccd2bec3797e5b91228d1eb8562e1a84f3e4fd','darryl-xiang123@outlook.com','13808243888','2023-05-21 23:26:45');
/*!40000 ALTER TABLE `vendors` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-21 23:39:59
