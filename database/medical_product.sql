-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 09, 2025 at 03:56 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `medical_product`
--

-- --------------------------------------------------------

--
-- Table structure for table `pr_admin`
--

CREATE TABLE `pr_admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pr_admin`
--

INSERT INTO `pr_admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `pr_blockchain`
--

CREATE TABLE `pr_blockchain` (
  `id` int(11) NOT NULL default '0',
  `block_id` int(11) NOT NULL,
  `pre_hash` varchar(200) NOT NULL,
  `hash_value` varchar(200) NOT NULL,
  `sdata` varchar(200) NOT NULL,
  `ptype` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pr_blockchain`
--


-- --------------------------------------------------------

--
-- Table structure for table `pr_category`
--

CREATE TABLE `pr_category` (
  `id` int(11) NOT NULL,
  `category` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pr_category`
--

INSERT INTO `pr_category` (`id`, `category`) VALUES
(1, 'Tablet'),
(2, 'Drops'),
(3, 'Injection');

-- --------------------------------------------------------

--
-- Table structure for table `pr_complaint`
--

CREATE TABLE `pr_complaint` (
  `id` int(11) NOT NULL,
  `company` varchar(30) NOT NULL,
  `pid` int(11) NOT NULL,
  `pcode` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `message` varchar(100) NOT NULL,
  `rdate` varchar(20) NOT NULL,
  `product` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pr_complaint`
--


-- --------------------------------------------------------

--
-- Table structure for table `pr_manufacture`
--

CREATE TABLE `pr_manufacture` (
  `id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `address` varchar(40) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pr_manufacture`
--


-- --------------------------------------------------------

--
-- Table structure for table `pr_online_sale`
--

CREATE TABLE `pr_online_sale` (
  `id` int(11) NOT NULL,
  `shop` varchar(20) NOT NULL,
  `web_url` varchar(200) NOT NULL,
  `status` int(11) NOT NULL,
  `rdate` varchar(20) NOT NULL,
  `supplier` varchar(20) NOT NULL,
  `company` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pr_online_sale`
--

INSERT INTO `pr_online_sale` (`id`, `shop`, `web_url`, `status`, `rdate`, `supplier`, `company`) VALUES
(1, 'rt1', 'http://iotcloud.co.in/shopping', 2, '16-03-2024', 'bks', 'aks');

-- --------------------------------------------------------

--
-- Table structure for table `pr_product`
--

CREATE TABLE `pr_product` (
  `id` int(11) NOT NULL,
  `category` varchar(30) NOT NULL,
  `product` varchar(40) NOT NULL,
  `company` varchar(20) NOT NULL,
  `price` double NOT NULL,
  `description` varchar(200) NOT NULL,
  `location` varchar(50) NOT NULL,
  `mdate` varchar(15) NOT NULL,
  `edate` varchar(15) NOT NULL,
  `pcode` varchar(20) NOT NULL,
  `rdate` varchar(15) NOT NULL,
  `ttype` varchar(20) NOT NULL,
  `transport` varchar(50) NOT NULL,
  `tlocation` varchar(30) NOT NULL,
  `tdate` varchar(15) NOT NULL,
  `supplier` varchar(20) NOT NULL,
  `retailer` varchar(20) NOT NULL,
  `slocation` varchar(50) NOT NULL,
  `sdate` varchar(15) NOT NULL,
  `exp_st` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `num_piece` int(11) NOT NULL,
  `code1` varchar(30) NOT NULL,
  `code2` varchar(30) NOT NULL,
  `distribute` int(11) NOT NULL,
  `balance` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pr_product`
--

INSERT INTO `pr_product` (`id`, `category`, `product`, `company`, `price`, `description`, `location`, `mdate`, `edate`, `pcode`, `rdate`, `ttype`, `transport`, `tlocation`, `tdate`, `supplier`, `retailer`, `slocation`, `sdate`, `exp_st`, `status`, `num_piece`, `code1`, `code2`, `distribute`, `balance`) VALUES
(1, 'Millet', 'Foxtail Millet', 'aks', 200, '2 kg in each pack', 'Salem', '2024-02-15', '2024-03-15', 'K0001', '16-03-2024', '', '', '', '2024-03-15', '', '', '', '', 0, 0, 20, 'K0001P01', 'K0001P20', 20, 0),
(2, 'Millet', 'Pearl Millet', 'aks', 100, 'each pack 3 kg', 'Salem', '2024-03-10', '2024-04-10', 'K0002', '16-03-2024', '', '', '', '2024-04-10', '', '', '', '', 0, 0, 10, 'K0002P01', 'K0002P10', 5, 5),
(3, 'Millet', 'Finger Millet', 'aks', 50, '2kg per pack', 'Thanjavur', '2023-12-20', '2024-01-20', 'K0003', '16-03-2024', '', '', '', '2024-01-20', '', '', '', '', 0, 0, 5, 'K0003P1', 'K0003P5', 0, 0),
(4, 'Millet', 'Foxtail Millet', 'aks', 100, '2 kg in each pack', 'Thanjavur', '2025-02-10', '2025-08-10', 'K0004', '29-03-2025', '', '', '', '2025-08-10', '', '', '', '', 0, 0, 300, 'K0004P001', 'K0004P300', 100, 200);

-- --------------------------------------------------------

--
-- Table structure for table `pr_product1`
--

CREATE TABLE `pr_product1` (
  `id` int(11) NOT NULL,
  `shop` varchar(20) NOT NULL,
  `product` varchar(50) NOT NULL,
  `pcode` varchar(20) NOT NULL,
  `price` double NOT NULL,
  `img1` varchar(50) NOT NULL,
  `img2` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pr_product1`
--


-- --------------------------------------------------------

--
-- Table structure for table `pr_productcode`
--

CREATE TABLE `pr_productcode` (
  `id` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `company` varchar(30) NOT NULL,
  `product_code` varchar(20) NOT NULL,
  `pcount` int(11) NOT NULL,
  `supplier` varchar(20) NOT NULL,
  `shop` varchar(20) NOT NULL,
  `sale` int(11) NOT NULL,
  `sale_date` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pr_productcode`
--


-- --------------------------------------------------------

--
-- Table structure for table `pr_request`
--

CREATE TABLE `pr_request` (
  `id` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `num_prd` int(11) NOT NULL,
  `supplier` varchar(20) NOT NULL,
  `company` varchar(20) NOT NULL,
  `rdate` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pr_request`
--


-- --------------------------------------------------------

--
-- Table structure for table `pr_request2`
--

CREATE TABLE `pr_request2` (
  `id` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `num_prd` int(11) NOT NULL,
  `shop` varchar(20) NOT NULL,
  `supplier` varchar(20) NOT NULL,
  `company` varchar(20) NOT NULL,
  `rdate` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pr_request2`
--


-- --------------------------------------------------------

--
-- Table structure for table `pr_sale`
--

CREATE TABLE `pr_sale` (
  `id` int(11) NOT NULL,
  `shop` varchar(20) NOT NULL,
  `pid` int(11) NOT NULL,
  `rid` int(11) NOT NULL,
  `kid` int(11) NOT NULL,
  `pcode` varchar(30) NOT NULL,
  `rdate` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pr_sale`
--


-- --------------------------------------------------------

--
-- Table structure for table `pr_send`
--

CREATE TABLE `pr_send` (
  `id` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `num_prd` int(11) NOT NULL,
  `prd_from` varchar(30) NOT NULL,
  `prd_to` varchar(30) NOT NULL,
  `prd1` int(11) NOT NULL,
  `prd2` int(11) NOT NULL,
  `company` varchar(20) NOT NULL,
  `supplier` varchar(30) NOT NULL,
  `rdate` varchar(15) NOT NULL,
  `distribute` int(11) NOT NULL,
  `balance` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pr_send`
--


-- --------------------------------------------------------

--
-- Table structure for table `pr_send2`
--

CREATE TABLE `pr_send2` (
  `id` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `num_prd` int(11) NOT NULL,
  `prd_from` varchar(30) NOT NULL,
  `prd_to` varchar(30) NOT NULL,
  `prd1` int(11) NOT NULL,
  `prd2` int(11) NOT NULL,
  `company` varchar(20) NOT NULL,
  `supplier` varchar(30) NOT NULL,
  `rdate` varchar(15) NOT NULL,
  `distribute` int(11) NOT NULL,
  `balance` int(11) NOT NULL,
  `shop` varchar(20) NOT NULL,
  `rid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pr_send2`
--


-- --------------------------------------------------------

--
-- Table structure for table `pr_shop`
--

CREATE TABLE `pr_shop` (
  `id` int(11) NOT NULL,
  `owner` varchar(20) NOT NULL,
  `distributor` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `city` varchar(40) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `status` int(11) NOT NULL,
  `name2` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pr_shop`
--


-- --------------------------------------------------------

--
-- Table structure for table `pr_supplier`
--

CREATE TABLE `pr_supplier` (
  `id` int(11) NOT NULL,
  `owner` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `city` varchar(40) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `rdate` varchar(20) NOT NULL,
  `status` int(11) NOT NULL,
  `name2` varchar(20) NOT NULL,
  `gst_number` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pr_supplier`
--

