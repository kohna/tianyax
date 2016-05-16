-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb2+deb7u1
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2016 年 03 月 03 日 19:37
-- 服务器版本: 5.5.40
-- PHP 版本: 5.4.44-0+deb7u1

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `tianyax`
--

-- --------------------------------------------------------

--
-- 表的结构 `bloginfo`
--

CREATE TABLE IF NOT EXISTS `bloginfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `bonam` varchar(64) NOT NULL,
  `bourl` varchar(255) NOT NULL COMMENT '博客地址',
  `bosig` varchar(255) NOT NULL COMMENT '博客签名',
  `bovis` int(11) NOT NULL COMMENT '总访问量',
  `botim` date NOT NULL COMMENT '开博时间',
  `bonum` int(11) NOT NULL COMMENT '博文数量',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `comminfo`
--

CREATE TABLE IF NOT EXISTS `comminfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `cousr` varchar(64) NOT NULL COMMENT '回复人',
  `coblg` varchar(255) NOT NULL COMMENT '回复人博客',
  `cocon` text NOT NULL COMMENT '回复内容',
  `cotex` varchar(255) NOT NULL COMMENT '回复标题',
  `courl` varchar(255) NOT NULL COMMENT '回复地址',
  `cotim` varchar(64) NOT NULL COMMENT '回复时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `fansinfo`
--

CREATE TABLE IF NOT EXISTS `fansinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL COMMENT '博主ID',
  `aid` int(11) NOT NULL COMMENT '粉丝ID',
  `fanam` varchar(64) NOT NULL COMMENT '粉丝名字',
  `faurl` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `follinfo`
--

CREATE TABLE IF NOT EXISTS `follinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL COMMENT '博主ID',
  `fid` int(11) NOT NULL COMMENT '关注ID',
  `fonam` varchar(64) NOT NULL,
  `fourl` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `textinfo`
--

CREATE TABLE IF NOT EXISTS `textinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL COMMENT '博主ID',
  `tid` int(11) NOT NULL COMMENT '文章ID',
  `txtit` varchar(255) NOT NULL COMMENT '博文标题',
  `txurl` varchar(255) NOT NULL COMMENT '博文地址',
  `txtim` varchar(64) NOT NULL COMMENT '博文时间',
  `txcon` text NOT NULL COMMENT '博文内容',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `userinfo`
--

CREATE TABLE IF NOT EXISTS `userinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL COMMENT '博主ID',
  `usnam` varchar(64) NOT NULL COMMENT '博主名字',
  `usurl` varchar(255) NOT NULL COMMENT '博主地址',
  `usfan` int(11) NOT NULL COMMENT '粉丝数量',
  `usfol` int(11) NOT NULL COMMENT '关注数量',
  `uslon` int(11) NOT NULL COMMENT '登录次数',
  `uslal` varchar(32) NOT NULL COMMENT '最新登录',
  `usreg` varchar(32) NOT NULL COMMENT '注册时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
