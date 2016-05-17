CREATE DATABASE command;

USE DATABASE command;

--
-- Table structure for table `botInfo`
--

CREATE TABLE `botInfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `machineID` varchar(40) DEFAULT NULL,
  `osType` varchar(20) DEFAULT NULL,
  `httpCommand` varchar(250) DEFAULT NULL,
  `httpResults` mediumblob,
  `executed` varchar(1) DEFAULT 'N',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
