create database bookpurchasesystem;
use bookpurchasesystem;
show tables;
/*Table structure for table `userAccount` */
DROP TABLE IF EXISTS `userAccount`;

CREATE TABLE `userAccount` (
  `userId` int(15) NOT NULL,
  `customerName` varchar(50) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `emailId` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`userId`)
  );

CREATE TABLE `order` (
  `orderId` int(15) NOT NULL,
  `userId` int(15) NOT NULL,
  `bookId` varchar(15) NOT NULL,
  `orderDate` date NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `type` varchar(15) NOT NULL,
  `status` varchar(15) NOT NULL,
  PRIMARY KEY (`orderId`,`userId`),
  KEY `orderId` (`orderId`),
  CONSTRAINT `order_fk1` FOREIGN KEY (`userId`) REFERENCES `userAccount` (`userId`),
  CONSTRAINT `order_fk2` FOREIGN KEY (`bookId`) REFERENCES `books` (`bookId`)
);

desc order;

DROP TABLE IF EXISTS `payments`;

CREATE TABLE `payments` (
  `userId` int(15) NOT NULL,
  `paymentId` varchar(50) NOT NULL,
  `paymentDate` date NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  PRIMARY KEY (`userId`,`paymentId`),
  CONSTRAINT `payments_fk` FOREIGN KEY (`userId`) REFERENCES `userAccount` (`userId`)
);
select * from payments;
DROP TABLE IF EXISTS `books`;

CREATE TABLE `books` (
  `bookId` varchar(15) NOT NULL,
  `bookTitle` varchar(70) NOT NULL,
  `Edition` varchar(15) NOT NULL,
  `type` varchar(15) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`bookId`)
);

insert  into `books`(`bookId`,`bookTitle`,`Edition`,`type`,`price`) values 
('ML001','Machine learning using Python','second','new','461.00');

insert  into `books`(`bookId`,`bookTitle`,`Edition`,`type`,`price`) values 
('MKTG001','Marketing Management','sixteenth','new','578.00'),
('BA001','Data Analysis and Decision Making with MindTap','7th','new','1150.00'),
('BA002','Supply Chain Analytics','1st','new','748.00'),
('BA003','Lean Analytics: Use Data to Build a Better Startup Faster','1st','new','409.00'),
('BA004','Big Data Analytics','paperback','new','668.00'),
('BA005','Fundamentals of Business Analytics','2nd edition','new','319.00'),
('BA006','Data Analytics using Python','1st edition','new','671.00'),
('STO001','108 Panchatantra Stories (Illustrated) for children','1st edition','new','120.00'),
('STO002','50 Greatest Short Stories','1st edition','new','208.00'),
('MGMT001','Sales Management Essentials You Always Wanted To Know','1st edition','new','208.00'),
('MGMT002','Fundamentals of Management','9th edition','new','734.00');

commit;
select * from books;
DROP TABLE IF EXISTS `discussion`;

CREATE TABLE `discussion` (
	`topicTitle` varchar(70) NOT NULL,
    `userId` int(15) NOT NULL,
    `comments` varchar(250) NOT NULL
);
select * from discussion;
DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
	`bookTitle` varchar(70) NOT NULL,
    `userId` int(15) NOT NULL,
    `feedbackTxt` varchar(250) NOT NULL
);

insert  into `feedback`(`bookTitle`,`userId`,`feedbackTxt`) values 
('Machine learning using Python','123','Nice book. The examples are really helpful.');

delete from userAccount where userId='125';
select * from userAccount;
select * from `order` where orderId='589567';
select orderDate from `order`;
SELECT * FROM `order` WHERE DATE(orderDate) < CURDATE() and userId='123';
select * from payments;
delete from payments where userId ='125';
select * from bookpurchasesystem.order where orderId='58956';
select * from feedback;
select * from `order`;
delete from `order` where orderId='58956'