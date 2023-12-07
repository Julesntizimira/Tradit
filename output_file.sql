-- MySQL dump 10.13  Distrib 8.1.0, for macos13.3 (arm64)
--
-- Host: localhost    Database: bookdb
-- ------------------------------------------------------
-- Server version	8.1.0

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
-- Table structure for table `authors`
--

DROP TABLE IF EXISTS `authors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authors` (
  `name` varchar(250) NOT NULL,
  `biography` varchar(250) DEFAULT NULL,
  `id` varchar(60) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authors`
--

LOCK TABLES `authors` WRITE;
/*!40000 ALTER TABLE `authors` DISABLE KEYS */;
INSERT INTO `authors` VALUES ('Hanya Yanagihara',NULL,'07675acb-e3e4-4e2d-8cd8-eada2f4df177'),('Nicole',NULL,'2d6c606c-3674-4833-87fd-9ee79e2ad517'),('Jack Canfield',NULL,'659680ae-5ee3-4cba-83e3-74a9bac2fcfa'),('Don DeLillo',NULL,'68a395f5-7b8a-43ce-8ff5-13dcfa9ed28f'),('Alan Hollinghurst',NULL,'6f8c5444-d275-4c3e-ba20-4887cd8254db'),('CHINUA ACHEBE',NULL,'7bc8559e-87e7-4497-a288-71c34c1248c1'),(' Napoleon Hill ',NULL,'8b32f240-c800-4001-a71e-da1244b8d5cc'),('Douglas Stuart',NULL,'9423eb5e-a94d-4f9d-ab85-5a22cba4db02'),('Arundhati Roy',NULL,'9775fe2c-185e-45b9-bd89-f15572fd2485'),('Robert Kiyosaki',NULL,'b04a3eb6-55db-4fd1-a70e-537e8fe81da8'),('Bret Easton Ellis',NULL,'b57536cd-2560-44c5-857b-20a6414410f7'),('walker',NULL,'da46d3af-15d9-451e-8985-f5e80c28ab44'),('Cormac McCarthy',NULL,'e35d55e7-f450-4c6e-99b1-9275d8ecf2d3');
/*!40000 ALTER TABLE `authors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `title` varchar(250) NOT NULL,
  `release_date` int NOT NULL,
  `author_id` varchar(60) NOT NULL,
  `genre_id` varchar(60) NOT NULL,
  `user_id` varchar(60) NOT NULL,
  `description` varchar(500) NOT NULL,
  `id` varchar(60) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  KEY `genre_id` (`genre_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `books_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `authors` (`id`),
  CONSTRAINT `books_ibfk_2` FOREIGN KEY (`genre_id`) REFERENCES `genres` (`id`),
  CONSTRAINT `books_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES ('The Aladdin Factor: How to Ask for What You Want--and Get It ',2012,'659680ae-5ee3-4cba-83e3-74a9bac2fcfa','a06cae68-3fab-4ac9-8922-2442ada8a300','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','The Aladdin Factor helps us by pinpointing the major stumbling blocks to asking—and teaching simple techniques to overcome them. With inspirational stories about people who have succeeded by asking for what they want, this book shows us how to turn our lives around—no matter what kind of obstacles we face. And with this knowledge, we can reap the riches of a truly well-lived life—a treasure that comes not from an enchanted lamp, but from the heart.','27338261-7deb-4e81-b1fb-ad8556fe4e75'),('White Noise',2022,'68a395f5-7b8a-43ce-8ff5-13dcfa9ed28f','c33c80d4-d6a1-4a7a-9c00-2e162610c678','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','Jack Gladney is the creator and chairman of Hitler studies at the College-on-the-Hill. This is the story of his absurd life; a life that is going well enough, until a chemical spill from a train carriage releases an ‘Airborne Toxic Event’ and Jack is forced to confront his biggest fear – his own mortality.','27424fe2-dcc5-4ccd-abad-970b128433fe'),('Shuggie Bain',1980,'9423eb5e-a94d-4f9d-ab85-5a22cba4db02','25691c80-7571-41d7-9112-26074d0ebe09','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','Set in a poverty-stricken Glasgow in the early 1980s, Douglas Stuart’s Booker Prize-winning debut is a heartbreaking story which lays bare the ruthlessness of poverty and the limits of love. Agnes Bain has always dreamed of greater things, but when her husband abandons her she finds herself trapped in a decimated mining town with her three children, and descends deeper and deeper into drink. Her son Shuggie tries to help Agnes long after her other children have fled, but he too must abandon her ','2ec8db5a-9c8b-4fb3-aa11-f449fba79fba'),('A Little Life',1996,'07675acb-e3e4-4e2d-8cd8-eada2f4df177','a06cae68-3fab-4ac9-8922-2442ada8a300','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','When four graduates from a small Massachusetts college move to New York to make their way, they\'re broke, adrift, and buoyed only by their friendship and ambition. There is kind, handsome Willem, an aspiring actor; JB, a quick-witted, sometimes cruel Brooklyn-born painter seeking entry to the art world; Malcolm, a frustrated architect at a prominent firm; and withdrawn, brilliant, enigmatic Jude, who serves as their centre of gravity.','3ed6944b-f20c-4221-94ed-36809a943f2a'),('The Aladdin Factor: How to Ask for What You Want--and Get It ',2012,'659680ae-5ee3-4cba-83e3-74a9bac2fcfa','a06cae68-3fab-4ac9-8922-2442ada8a300','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','The Aladdin Factor helps us by pinpointing the major stumbling blocks to asking—and teaching simple techniques to overcome them. With inspirational stories about people who have succeeded by asking for what they want, this book shows us how to turn our lives around—no matter what kind of obstacles we face. And with this knowledge, we can reap the riches of a truly well-lived life—a treasure that comes not from an enchanted lamp, but from the heart.','4c15bdb8-ab1c-4820-9b5a-821c5b341b2a'),('The Line of Beauty',1983,'6f8c5444-d275-4c3e-ba20-4887cd8254db','ba9ce4cc-b301-4a8b-a8c9-fbfad56e992e','9fd8c169-bf9a-4798-a722-3688431d6b06','This Booker Prize-winning novel bottles the essence of the 1980s, as the story follows a quest for beauty against a backdrop of politics, greed and friendships turned toxic. When twenty-year-old Nick Guest moves into an attic room in the Notting Hill home of the wealthy Feddens he is innocent of politics and money. But as he is swept up into the Feddens’ world, Nick must confront the collisions between his own desires, and a world he can never truly belong to. Alan Hollinghurst’s writing style i','4dd23554-aaab-4010-b071-b444f5f01f79'),('Think & Grow Rich',1937,'8b32f240-c800-4001-a71e-da1244b8d5cc','25691c80-7571-41d7-9112-26074d0ebe09','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','Think and Grow Rich is one of the most influential personal success books of all time. With the help of industrialist Andrew Carnegie, self-help guru Napoleon Hill spent two decades interviewing hundreds of people renowned for their wealth and achievement. Hill\'s all-time bestseller offers priceless advice on positive thinking and overcoming adversity, distilled from the collective wisdom of Henry Ford, Thomas Edison, John D. Rockefeller, and other successful figures from the worlds of finance, ','64bf1298-1ecf-4cc0-bb8f-e76f6412b89f'),('Things Fall Apart',1994,'7bc8559e-87e7-4497-a288-71c34c1248c1','a06cae68-3fab-4ac9-8922-2442ada8a300','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','This tale of an Igbo warrior fighting to preserve his people’s culture in the face of British colonialism is a worldwide phenomenon and bestseller. As part of a trilogy, Achebe’s novel begins a story of three generations of a single Nigerian community. The novel helped earn Achebe the Nigerian National Merit Award and the Man Booker International Prize for lifetime achievement. Furthermore, having sold more than 20 million copies and been translated into 57 languages, it is one of the most illus','6d6fd392-f900-4116-a495-4b18b7b2ec17'),('The Aladdin Factor: How to Ask for What You Want--and Get It ',2012,'659680ae-5ee3-4cba-83e3-74a9bac2fcfa','a06cae68-3fab-4ac9-8922-2442ada8a300','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','The Aladdin Factor helps us by pinpointing the major stumbling blocks to asking—and teaching simple techniques to overcome them. With inspirational stories about people who have succeeded by asking for what they want, this book shows us how to turn our lives around—no matter what kind of obstacles we face. And with this knowledge, we can reap the riches of a truly well-lived life—a treasure that comes not from an enchanted lamp, but from the heart.','71f2c649-208a-407c-a2a2-37ce18a39a02'),('The Aladdin Factor: How to Ask for What You Want--and Get It ',2012,'659680ae-5ee3-4cba-83e3-74a9bac2fcfa','a06cae68-3fab-4ac9-8922-2442ada8a300','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','The Aladdin Factor helps us by pinpointing the major stumbling blocks to asking—and teaching simple techniques to overcome them. With inspirational stories about people who have succeeded by asking for what they want, this book shows us how to turn our lives around—no matter what kind of obstacles we face. And with this knowledge, we can reap the riches of a truly well-lived life—a treasure that comes not from an enchanted lamp, but from the heart.','a6affd52-c1ae-46bc-9bf3-92b05290e850'),('The God of Small Things',1996,'9775fe2c-185e-45b9-bd89-f15572fd2485','cffa6f7f-b143-484d-a154-039631ff480a','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','fraternal twins, Rahel and Estha, in the state of Kerala, India in 1969. Armed only with the invincible innocence of children, they fashion a childhood for themselves in the shade of the wreck that is their family. But when their English cousin and her mother arrive for a Christmas visit, the twins learn that things can change in a day. ','abbcd9e3-a0e5-4e93-89aa-35d63065f3da'),('Blood Meridian',1985,'e35d55e7-f450-4c6e-99b1-9275d8ecf2d3','c33c80d4-d6a1-4a7a-9c00-2e162610c678','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','Written in 1985, Blood Meridian is set in the anarchic world opened up by America’s westward expansion. Through the hostile landscape of the Texas–Mexico border wanders the Kid, a fourteen year-old Tennessean who is quickly swept up in the relentless tide of blood. ','e45c86cc-2a6a-4d17-bc33-2571e3c535a4'),('American Psycho',2005,'b57536cd-2560-44c5-857b-20a6414410f7','cffa6f7f-b143-484d-a154-039631ff480a','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','One of the most controversial and talked-about novels in modern history, American Psycho is the story of Patrick Bateman, a New York City high-flier with a penchant for fine wines, slickly cut suits and brutal murder. As Bateman\'s obsession with his hedonistic passions comes to a head, he descends into madness, with macabre and darkly comedic repercussions.','f1984a2e-d804-45bb-bd4d-3dd6fb6ea6e5'),('Rich Dad Poor Dad',1997,'b04a3eb6-55db-4fd1-a70e-537e8fe81da8','25691c80-7571-41d7-9112-26074d0ebe09','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','What the Rich Teach Their Kids About Money That the Poor and Middle Class Do Not','f28f0d4e-3437-4e17-a46e-631976e0de8c');
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comments` (
  `text` varchar(500) NOT NULL,
  `user_id` varchar(60) NOT NULL,
  `book_id` varchar(60) NOT NULL,
  `id` varchar(60) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `book_id` (`book_id`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
INSERT INTO `comments` VALUES ('kigali','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','6d6fd392-f900-4116-a495-4b18b7b2ec17','0c5f4588-835a-48ef-9c2d-48e56cd1b346'),('hello','9fd8c169-bf9a-4798-a722-3688431d6b06','6d6fd392-f900-4116-a495-4b18b7b2ec17','28c73c6e-986f-474e-99cd-220c1cbe3700'),('hh','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','6d6fd392-f900-4116-a495-4b18b7b2ec17','45c87595-e844-4585-bc3a-5fe23486e9d9'),('hhhhhh','bc8c77f7-74a7-4c47-906d-a61e0c9f9a27','6d6fd392-f900-4116-a495-4b18b7b2ec17','4b668d72-a935-4b5c-8423-211de9b98537'),('This tale of an Igbo warrior fighting to preserve his people’s culture in the face of British colonialism is a worldwide phenomenon and bestseller. As','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','6d6fd392-f900-4116-a495-4b18b7b2ec17','6f72a215-26aa-44a8-92fc-32af7e948eb3'),('books','9fd8c169-bf9a-4798-a722-3688431d6b06','6d6fd392-f900-4116-a495-4b18b7b2ec17','70bb298e-f1bc-45d2-af86-cf177566a9d4'),('yes','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','6d6fd392-f900-4116-a495-4b18b7b2ec17','87cbda97-f81c-45bc-8d7d-3aa24e189ff8'),('This tale of an Igbo warrior fighting to preserve his people’s culture in the face of British colonialism is a worldwide phenomenon and bestseller. As','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','6d6fd392-f900-4116-a495-4b18b7b2ec17','8cafec47-fbbe-4390-a079-bba326524da1'),('This tale of an Igbo warrior fighting to preserve his people’s culture in the face of British colonialism is a worldwide phenomenon and bestseller. As','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','6d6fd392-f900-4116-a495-4b18b7b2ec17','8f18ff02-a8a9-424a-a375-439c4cdf1232'),('this is a nice book ','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','6d6fd392-f900-4116-a495-4b18b7b2ec17','9315e938-5b64-43bd-af9a-b5d8be735f73'),(' Man Booker International Prize for lifetime achievement. Furthermore, having sold more than 20 million copies and been translated into 57 languages, it is one of the most illus','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','6d6fd392-f900-4116-a495-4b18b7b2ec17','972918e1-4e81-4f1d-bc60-cc7467c7fb1c'),('nars','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','6d6fd392-f900-4116-a495-4b18b7b2ec17','a70198cd-1e91-47c2-9aa0-91148fe8bcd8'),('This tale of an Igbo warrior fighting to preserve his people’s culture in the face of British colonialism is a worldwide phenomenon and bestseller. As','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','6d6fd392-f900-4116-a495-4b18b7b2ec17','ab7de513-39e7-4d2a-a8e2-4efcec46b298'),('ttt','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','6d6fd392-f900-4116-a495-4b18b7b2ec17','ad1a6c5e-0931-4203-bb39-85328da069bc'),('yyeyey','bc8c77f7-74a7-4c47-906d-a61e0c9f9a27','6d6fd392-f900-4116-a495-4b18b7b2ec17','cd24e871-7adb-4a4e-8eea-3e6ddf149703'),('hello','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','6d6fd392-f900-4116-a495-4b18b7b2ec17','f3c2b2d3-53fa-461a-8b91-049d93d98d0e');
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genres`
--

DROP TABLE IF EXISTS `genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genres` (
  `name` varchar(250) NOT NULL,
  `id` varchar(60) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genres`
--

LOCK TABLES `genres` WRITE;
/*!40000 ALTER TABLE `genres` DISABLE KEYS */;
INSERT INTO `genres` VALUES ('Business','25691c80-7571-41d7-9112-26074d0ebe09'),('Fiction','c33c80d4-d6a1-4a7a-9c00-2e162610c678'),('life','a06cae68-3fab-4ac9-8922-2442ada8a300'),('Mystery','ba9ce4cc-b301-4a8b-a8c9-fbfad56e992e'),('Novel','cffa6f7f-b143-484d-a154-039631ff480a'),('Romance','f7c47da8-dfd9-4db3-b383-5e3c31bf0961');
/*!40000 ALTER TABLE `genres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `text` varchar(1000) NOT NULL,
  `date` datetime DEFAULT NULL,
  `name` varchar(250) NOT NULL,
  `room_id` varchar(60) NOT NULL,
  `id` varchar(60) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `room_id` (`room_id`),
  CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES ('hi','1900-01-01 09:22:17','Julesntizimira','1a019fd7-08c1-45b4-ae82-8ce9316edca5','476c2366-169b-42f9-a591-e3de029952f3'),('hello ma men','1900-01-01 09:23:17','lucky','1a019fd7-08c1-45b4-ae82-8ce9316edca5','aac2f1d8-fe86-44f8-a7a1-a441773130e9');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offers`
--

DROP TABLE IF EXISTS `offers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `offers` (
  `user_id` varchar(60) NOT NULL,
  `book_id` varchar(60) NOT NULL,
  `id` varchar(60) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `book_id` (`book_id`),
  CONSTRAINT `offers_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `offers_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offers`
--

LOCK TABLES `offers` WRITE;
/*!40000 ALTER TABLE `offers` DISABLE KEYS */;
INSERT INTO `offers` VALUES ('4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','64bf1298-1ecf-4cc0-bb8f-e76f6412b89f','3499568f-21e5-48a7-99c5-ca0e9569e939'),('9fd8c169-bf9a-4798-a722-3688431d6b06','6d6fd392-f900-4116-a495-4b18b7b2ec17','4fba06f6-ce50-40c5-b6ab-372db55d2722'),('4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','4dd23554-aaab-4010-b071-b444f5f01f79','803cc24d-5520-4b0c-9048-074477dea515'),('4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','f1984a2e-d804-45bb-bd4d-3dd6fb6ea6e5','af349b33-193e-4696-8080-d505ac2290ce'),('4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','2ec8db5a-9c8b-4fb3-aa11-f449fba79fba','be7d3f77-e972-45f8-96b2-2157cf5bdb8e'),('4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','e45c86cc-2a6a-4d17-bc33-2571e3c535a4','cb8707a2-e485-4f1e-ad02-d5c953125f9b');
/*!40000 ALTER TABLE `offers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rooms`
--

DROP TABLE IF EXISTS `rooms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rooms` (
  `members` int NOT NULL,
  `id` varchar(60) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rooms`
--

LOCK TABLES `rooms` WRITE;
/*!40000 ALTER TABLE `rooms` DISABLE KEYS */;
INSERT INTO `rooms` VALUES (2,'1a019fd7-08c1-45b4-ae82-8ce9316edca5'),(2,'9d64b4ec-12c3-4ed5-b2cb-ab9251a44e3b'),(2,'c7d69ae2-6d14-41bc-a068-6bcf30ddae08'),(2,'d32eb855-434c-4897-92fa-5543adc6796c'),(2,'fa6a86a7-41a8-405a-8326-0aa838a36c7c');
/*!40000 ALTER TABLE `rooms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_room_relationship`
--

DROP TABLE IF EXISTS `user_room_relationship`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_room_relationship` (
  `user_id` varchar(60) DEFAULT NULL,
  `room_id` varchar(60) DEFAULT NULL,
  KEY `user_id` (`user_id`),
  KEY `room_id` (`room_id`),
  CONSTRAINT `user_room_relationship_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_room_relationship_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_room_relationship`
--

LOCK TABLES `user_room_relationship` WRITE;
/*!40000 ALTER TABLE `user_room_relationship` DISABLE KEYS */;
INSERT INTO `user_room_relationship` VALUES ('4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','d32eb855-434c-4897-92fa-5543adc6796c'),('9fd8c169-bf9a-4798-a722-3688431d6b06','d32eb855-434c-4897-92fa-5543adc6796c'),('9fd8c169-bf9a-4798-a722-3688431d6b06','c7d69ae2-6d14-41bc-a068-6bcf30ddae08'),('4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','c7d69ae2-6d14-41bc-a068-6bcf30ddae08'),('bc8c77f7-74a7-4c47-906d-a61e0c9f9a27','9d64b4ec-12c3-4ed5-b2cb-ab9251a44e3b'),('4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','9d64b4ec-12c3-4ed5-b2cb-ab9251a44e3b'),('4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','1a019fd7-08c1-45b4-ae82-8ce9316edca5'),('bc8c77f7-74a7-4c47-906d-a61e0c9f9a27','1a019fd7-08c1-45b4-ae82-8ce9316edca5'),('bc8c77f7-74a7-4c47-906d-a61e0c9f9a27','fa6a86a7-41a8-405a-8326-0aa838a36c7c'),('9fd8c169-bf9a-4798-a722-3688431d6b06','fa6a86a7-41a8-405a-8326-0aa838a36c7c');
/*!40000 ALTER TABLE `user_room_relationship` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `name` varchar(250) NOT NULL,
  `username` varchar(250) DEFAULT NULL,
  `email` varchar(250) DEFAULT NULL,
  `password` varchar(250) NOT NULL,
  `address` varchar(60) NOT NULL,
  `id` varchar(60) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('arthur ruyundo','arthur','arthur@gmail.com','$2b$12$SgHShWqv//z8NnXiV.nXQO0b3ZN9tnl8fglFP1F/kXxGxsH3sabHi','kigali','2cff2c43-ceb1-4193-8b63-9b36779a1a40'),('Jules Ntizimira','Julesntizimira','ntizimijules5@gmail.com','$2b$12$NjwKhBStzGbXKVB92rfkE..RMVg3x1KuUdP2xWJmGs/p0C6Ssd0XC','kigali','4925170b-7e7b-4e8c-9f31-3e3dffeefaf4'),('fany','fany','fany@gmail.com','$2b$12$x0kXqYkKVUPUPxrpUhQCRe3hNF9WLGpYtFkGF3JBVLjSY8mITEGba','kigali','6571dcc4-82cc-49a1-b48c-062d858400de'),('Ngoga Frank','frank','frank@gmail.com','$2b$12$WMR0/xwOT6uO3uexqy8p.uNzar1YnU5/.dxq/5LxkQFjK3i4IHtEK','kigali','9fd8c169-bf9a-4798-a722-3688431d6b06'),('cedrick','cedrick','cedrick@gmail.com','$2b$12$Mk1G9dCsqJ6zX2W6A/cPiuST2wc6PB4RlHPHjlzDm/VDQDbFkbqRa','kigali','b832c7ec-39b9-4b5b-904e-f6517e565239'),('Lucky Gabe','lucky','lucky@gmail.com','$2b$12$NNHtq.fCMkaOFqxDN9W7dOhwNWWepkCF9Oc1ETjSblvQtUyNo7aGe','kigali','bc8c77f7-74a7-4c47-906d-a61e0c9f9a27'),('gedeon','gedeon','gedeon@gmail.com','$2b$12$P9xQ/OGyFb9YxFzGN7Z5xOcH7706RA0aBjN6fZV5la5GX3cEJDaBe','kigali','c0f36825-6854-47fc-90d8-83fb04f10f4c'),('feris','feris','feris@gmail.com','$2b$12$sCEGiLPTBPJzt8vFh77U7eorU90h0TXJ.FH5umoKoY9UgdekQ5iBG','kigali','ce1fe7a8-c868-4bed-9e7f-3e2b07e327f9'),('saphi','saphi','saphi@gmail.com','$2b$12$3xhLfoncN/I5wRaFtzvIQOGCu8voZZ1QTtb/A7zcT3NpycF4yOdcS','kigali','ed773f7f-41a3-496c-a7c7-efaa78ef6c97');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wishes`
--

DROP TABLE IF EXISTS `wishes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wishes` (
  `user_id` varchar(60) NOT NULL,
  `book_id` varchar(60) NOT NULL,
  `id` varchar(60) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `book_id` (`book_id`),
  CONSTRAINT `wishes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `wishes_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wishes`
--

LOCK TABLES `wishes` WRITE;
/*!40000 ALTER TABLE `wishes` DISABLE KEYS */;
INSERT INTO `wishes` VALUES ('4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','f28f0d4e-3437-4e17-a46e-631976e0de8c','0e2bc081-9ad1-4039-bfb5-2b9f671523e4'),('4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','abbcd9e3-a0e5-4e93-89aa-35d63065f3da','3950da3b-2890-4f5b-8fc0-79b3ad0b35c8'),('4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','f1984a2e-d804-45bb-bd4d-3dd6fb6ea6e5','9964bf15-8b02-464a-bdf2-223dc2839676'),('4925170b-7e7b-4e8c-9f31-3e3dffeefaf4','6d6fd392-f900-4116-a495-4b18b7b2ec17','99a290d0-57c3-45c4-befc-8daee7a59ab4');
/*!40000 ALTER TABLE `wishes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-07 11:59:00
