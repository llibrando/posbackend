-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 28, 2024 at 05:47 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pos`
--

-- --------------------------------------------------------

--
-- Table structure for table `cashier`
--

CREATE TABLE `cashier` (
  `cashierID` int(11) NOT NULL,
  `username` varchar(30) DEFAULT NULL,
  `password` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cashier`
--

INSERT INTO `cashier` (`cashierID`, `username`, `password`) VALUES
(1, 'JohnDoe', 'password1'),
(2, 'AliceSmith', 'password2'),
(3, 'BobJohnson', 'password3'),
(4, 'EmmaBrown', 'password4'),
(5, 'DavidMiller', 'password5');

-- --------------------------------------------------------

--
-- Table structure for table `menu`
--

CREATE TABLE `menu` (
  `ItemID` int(11) NOT NULL,
  `menuItemCategory` varchar(15) DEFAULT NULL,
  `menuItemName` varchar(15) DEFAULT NULL,
  `menuItemPrice` int(11) DEFAULT NULL,
  `menuItemPic` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `menu`
--

INSERT INTO `menu` (`ItemID`, `menuItemCategory`, `menuItemName`, `menuItemPrice`, `menuItemPic`) VALUES
(1, 'Viand', 'ChknAdobo', 30, NULL),
(2, 'Viand', 'PrkAdobo', 35, NULL),
(3, 'Viand', 'Pastil', 15, NULL),
(4, 'Main Course', 'Rice', 10, NULL),
(5, 'test', 'test', 8, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `OrderID` int(10) NOT NULL,
  `OrderStatus` varchar(10) DEFAULT NULL,
  `orderDate` date DEFAULT NULL,
  `orderTime` time DEFAULT NULL,
  `orderTotal` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`OrderID`, `OrderStatus`, `orderDate`, `orderTime`, `orderTotal`) VALUES
(1, 'Pending', '2024-04-01', '10:00:00', 50),
(2, 'Complete', '2024-04-02', '12:30:00', 75),
(3, 'Pending', '2024-04-03', '09:45:00', 100),
(4, 'Pending', '2024-04-04', '11:15:00', 80),
(5, 'Complete', '2024-04-05', '13:00:00', 200);


-- --------------------------------------------------------

--
-- Table structure for table `payment`
--

CREATE TABLE `payment` (
  `PaymentID` int(11) NOT NULL,
  `TransactionID` int(10) DEFAULT NULL,
  `PaymentType` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payment`
--

INSERT INTO `payment` (`PaymentID`, `TransactionID`, `PaymentType`) VALUES
(1, 1, 'Cash'),
(2, 2, 'Credit Card'),
(3, 3, 'Debit Card'),
(4, 4, 'Cash'),
(5, 5, 'GCash');

-- --------------------------------------------------------

--
-- Table structure for table `transaction`
--

CREATE TABLE `transaction` (
  `TransactionID` int(10) NOT NULL,
  `ItemID` int(11) DEFAULT NULL,
  `OrderID` int(11) DEFAULT NULL,
  `Subtotal` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transaction`
--

INSERT INTO `transaction` (`TransactionID`, `ItemID`, `OrderID`, `Subtotal`) VALUES
(1, 1, 1, 50),
(2, 2, 2, 75),
(3, 3, 3, 100),
(4, 4, 4, 80),
(5, 5, 5, 200);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cashier`
--
ALTER TABLE `cashier`
  ADD PRIMARY KEY (`cashierID`);

--
-- Indexes for table `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`ItemID`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`OrderID`);

--
-- Indexes for table `payment`
--
ALTER TABLE `payment`
  ADD PRIMARY KEY (`PaymentID`),
  ADD KEY `TransactionID` (`TransactionID`);

--
-- Indexes for table `transaction`
--
ALTER TABLE `transaction`
  ADD PRIMARY KEY (`TransactionID`),
  ADD KEY `FK_ItemID` (`ItemID`),
  ADD KEY `FK_OrderID` (`OrderID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `payment`
--
ALTER TABLE `payment`
  ADD CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`TransactionID`) REFERENCES `transaction` (`TransactionID`);

--
-- Constraints for table `transaction`
--
ALTER TABLE `transaction`
  ADD CONSTRAINT `FK_ItemID` FOREIGN KEY (`ItemID`) REFERENCES `menu` (`ItemID`),
  ADD CONSTRAINT `FK_OrderID` FOREIGN KEY (`OrderID`) REFERENCES `orders` (`OrderID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
