-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 28, 2023 at 10:26 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.1.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `realbuild`
--

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE `feedback` (
  `fid` int(11) NOT NULL,
  `feedback` varchar(300) NOT NULL,
  `uid` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tblallocation`
--

CREATE TABLE `tblallocation` (
  `allocid` int(11) NOT NULL,
  `requid` int(11) NOT NULL,
  `cid` varchar(50) NOT NULL,
  `status` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tblcontractor`
--

CREATE TABLE `tblcontractor` (
  `cName` varchar(50) NOT NULL,
  `cAddress` varchar(100) NOT NULL,
  `cContact` varchar(50) NOT NULL,
  `cEmail` varchar(50) NOT NULL,
  `cPhoto` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tblcustomer`
--

CREATE TABLE `tblcustomer` (
  `cName` varchar(50) NOT NULL,
  `cAddress` varchar(50) NOT NULL,
  `cContact` varchar(50) NOT NULL,
  `cEmail` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbllogin`
--

CREATE TABLE `tbllogin` (
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `utype` varchar(50) NOT NULL,
  `status` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tblplan`
--

CREATE TABLE `tblplan` (
  `planId` int(11) NOT NULL,
  `cEmail` varchar(50) NOT NULL,
  `reqId` int(11) NOT NULL,
  `plan` varchar(100) NOT NULL,
  `sqft` int(11) NOT NULL,
  `cost` bigint(20) NOT NULL,
  `planStatus` varchar(50) NOT NULL,
  `fees` int(11) NOT NULL,
  `feesstatus` varchar(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tblrequirement`
--

CREATE TABLE `tblrequirement` (
  `reqId` int(11) NOT NULL,
  `cEmail` varchar(50) NOT NULL,
  `bedroom` varchar(50) NOT NULL,
  `bathroom` varchar(50) NOT NULL,
  `attached` varchar(50) NOT NULL,
  `carporch` varchar(50) NOT NULL,
  `kitchen` varchar(50) NOT NULL,
  `sitout` varchar(50) NOT NULL,
  `workarea` varchar(50) NOT NULL,
  `floor` varchar(50) NOT NULL,
  `sqft` varchar(50) NOT NULL,
  `other` varchar(100) NOT NULL,
  `reqDate` datetime NOT NULL,
  `reqStatus` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`fid`);

--
-- Indexes for table `tblallocation`
--
ALTER TABLE `tblallocation`
  ADD PRIMARY KEY (`allocid`),
  ADD KEY `requid` (`requid`);

--
-- Indexes for table `tblcontractor`
--
ALTER TABLE `tblcontractor`
  ADD PRIMARY KEY (`cEmail`);

--
-- Indexes for table `tblcustomer`
--
ALTER TABLE `tblcustomer`
  ADD PRIMARY KEY (`cEmail`);

--
-- Indexes for table `tblplan`
--
ALTER TABLE `tblplan`
  ADD PRIMARY KEY (`planId`),
  ADD KEY `reqId` (`reqId`);

--
-- Indexes for table `tblrequirement`
--
ALTER TABLE `tblrequirement`
  ADD PRIMARY KEY (`reqId`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `feedback`
--
ALTER TABLE `feedback`
  MODIFY `fid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tblallocation`
--
ALTER TABLE `tblallocation`
  MODIFY `allocid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tblplan`
--
ALTER TABLE `tblplan`
  MODIFY `planId` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tblrequirement`
--
ALTER TABLE `tblrequirement`
  MODIFY `reqId` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tblallocation`
--
ALTER TABLE `tblallocation`
  ADD CONSTRAINT `tblallocation_ibfk_1` FOREIGN KEY (`requid`) REFERENCES `tblrequirement` (`reqId`);

--
-- Constraints for table `tblplan`
--
ALTER TABLE `tblplan`
  ADD CONSTRAINT `tblplan_ibfk_1` FOREIGN KEY (`reqId`) REFERENCES `tblrequirement` (`reqId`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
