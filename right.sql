-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- 主机： 127.0.0.1
-- 生成日期： 2025-06-04 07:48:32
-- 服务器版本： 8.0.36
-- PHP 版本： 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `xlhd`
--

-- --------------------------------------------------------

--
-- 表的结构 `admin`
--

CREATE TABLE `admin` (
  `id` int NOT NULL COMMENT '主键ID',
  `username` char(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '用户名',
  `password` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '登录密码',
  `salt` char(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT '' COMMENT '随机码',
  `is_activited` tinyint NOT NULL DEFAULT '0' COMMENT '是否激活：0=否，1=是',
  `activated_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '激活时间',
  `admin_type` tinyint NOT NULL COMMENT '1管理员 2超级管理员',
  `permissions` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '权限，json存储',
  `create_time` int NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int NOT NULL DEFAULT '0' COMMENT '最后更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='管理员';

-- --------------------------------------------------------

--
-- 表的结构 `advertising`
--

CREATE TABLE `advertising` (
  `id` int NOT NULL COMMENT '主键ID',
  `title` varchar(256) CHARACTER SET utf8mb3 NOT NULL DEFAULT '' COMMENT '标题',
  `type` tinyint(1) NOT NULL DEFAULT '1' COMMENT '广告类型：1=首页banner',
  `link_type` tinyint(1) NOT NULL DEFAULT '1' COMMENT '跳转方式：1=不跳转，2=跳转到当前小程序页，3=跳转到其他小程序页，4=H5页面',
  `app_id` varchar(32) CHARACTER SET utf8mb3 NOT NULL DEFAULT '' COMMENT '小程序app_id',
  `link_url` varchar(256) CHARACTER SET utf8mb3 NOT NULL DEFAULT '' COMMENT '跳转地址',
  `web_url` varchar(256) CHARACTER SET utf8mb3 NOT NULL DEFAULT '' COMMENT 'web页面地址',
  `file_id` int NOT NULL DEFAULT '0' COMMENT '图片ID',
  `sort` int NOT NULL DEFAULT '0' COMMENT '排序 小的靠前',
  `source_id` varchar(35) CHARACTER SET utf8mb3 NOT NULL DEFAULT '' COMMENT '资源Id',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='广告表';

-- --------------------------------------------------------

--
-- 表的结构 `ad_channel`
--

CREATE TABLE `ad_channel` (
  `id` int NOT NULL COMMENT '主键ID',
  `adv_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '广告渠道标识Id',
  `title` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '标题',
  `link_url` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '广告跳转页面链接',
  `update_time` int UNSIGNED NOT NULL COMMENT '更新时间',
  `create_time` int UNSIGNED NOT NULL COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='广告渠道表';

-- --------------------------------------------------------

--
-- 表的结构 `change_settle_blank`
--

CREATE TABLE `change_settle_blank` (
  `id` int NOT NULL COMMENT '主键ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `sub_mch_apply_id` int NOT NULL DEFAULT '0' COMMENT '商户进件ID',
  `sub_mch_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '特约商户号',
  `application_no` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '申请单号',
  `account_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '账户类型',
  `account_bank` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '开户银行',
  `bank_address_code` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '开户银行省市编码',
  `bank_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '开户银行全称（含支行）',
  `account_number` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '银行账号',
  `account_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '开户名称',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态 1审核中 2审核成功 3审核驳回',
  `fail_reason` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '驳回原因',
  `update_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='修改结算银行申请表';

-- --------------------------------------------------------

--
-- 表的结构 `channel_log`
--

CREATE TABLE `channel_log` (
  `id` int NOT NULL COMMENT '主键ID',
  `adv_id` char(8) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '渠道ID',
  `user_id` int DEFAULT NULL COMMENT '用户ID',
  `event_count` int NOT NULL DEFAULT '0' COMMENT '用户发起活动数',
  `create_time` int DEFAULT NULL COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;

-- --------------------------------------------------------

--
-- 表的结构 `comm_file`
--

CREATE TABLE `comm_file` (
  `id` int NOT NULL COMMENT '主键ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '上传用户ID',
  `file_name` varchar(225) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '原文件名',
  `file_path` varchar(225) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '文件存放路径',
  `file_ext` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '文件扩展名',
  `file_size` int NOT NULL DEFAULT '0' COMMENT '文件大小',
  `deleted_at` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '删除时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='附件信息表';

-- --------------------------------------------------------

--
-- 表的结构 `config`
--

CREATE TABLE `config` (
  `id` int NOT NULL,
  `datakey` varchar(64) CHARACTER SET utf8mb3 NOT NULL,
  `datavalue` text CHARACTER SET utf8mb3 NOT NULL,
  `updated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='保存配置信息' ROW_FORMAT=DYNAMIC;

-- --------------------------------------------------------

--
-- 表的结构 `district_tx`
--

CREATE TABLE `district_tx` (
  `id` int NOT NULL COMMENT '主键ID',
  `pid` int NOT NULL DEFAULT '0' COMMENT '父级ID',
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '城市名',
  `fullname` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '全称',
  `level` tinyint(1) NOT NULL DEFAULT '0' COMMENT '级别',
  `pinyin` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '拼音',
  `initial` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '首字母',
  `has_children` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否有下级：1=有',
  `latitude` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '纬度',
  `longitude` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '经度',
  `cidx` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT 'cidx',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='腾讯地址库';

-- --------------------------------------------------------

--
-- 表的结构 `event`
--

CREATE TABLE `event` (
  `id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '活动ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '发布用户ID',
  `team_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '所属组织ID',
  `category_pid` int NOT NULL DEFAULT '0' COMMENT '分类父级ID',
  `category_id` int DEFAULT '0' COMMENT '分类ID',
  `title` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动标题',
  `content` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '活动内容',
  `banner` int NOT NULL DEFAULT '0' COMMENT 'banner，附件ID',
  `address` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动地址',
  `city` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '城市',
  `latitude` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '纬度',
  `longitude` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '经度',
  `start_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '活动开始时间',
  `end_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '活动结束时间',
  `sign_starttime` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '报名开始时间',
  `sign_endtime` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '报名结束时间',
  `mark_id` int NOT NULL DEFAULT '0' COMMENT '标记ID',
  `is_online` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否线上活动',
  `is_privacy` tinyint(1) DEFAULT '0' COMMENT '是否为私密活动',
  `is_show` tinyint(1) DEFAULT '0' COMMENT '首页是否显示 0否 1是',
  `transfer_open` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否允许转让。0=不允许 ，1=允许',
  `share_only_admin` tinyint(1) DEFAULT '0' COMMENT '只有管理人员可以分享',
  `check_signed` tinyint(1) NOT NULL DEFAULT '0' COMMENT '报名需要审核：1=是，0=否',
  `public_signdata` tinyint(1) DEFAULT '0' COMMENT '公开显示已报名的用户',
  `cancel_sign` tinyint(1) DEFAULT '1' COMMENT '是否可以取消报名',
  `edit_sign` tinyint NOT NULL DEFAULT '0' COMMENT '是否可以修改报名',
  `hide_viewcount` tinyint(1) DEFAULT '0' COMMENT '公开展示浏览量',
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '状态：0=草稿，1=正常',
  `source` tinyint(1) DEFAULT '0' COMMENT '来源，0小程序 1PC 网页',
  `sign_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '显示设置，哪些字段显示或隐藏',
  `sign_count` int NOT NULL DEFAULT '0' COMMENT '报名人数，包括未支付的',
  `fee_count` int NOT NULL COMMENT '费用使用总数',
  `sign_upper_limit` int NOT NULL DEFAULT '0' COMMENT '报名总人数上限',
  `fee_upper_limit` int NOT NULL COMMENT '报名费总库存上限',
  `view_count` int NOT NULL DEFAULT '0' COMMENT '浏览次数',
  `subscribe_count` int NOT NULL DEFAULT '0' COMMENT '关注人数',
  `qrcode_group` int NOT NULL DEFAULT '0' COMMENT '群二维码，7天有效期，需要定期更换',
  `qrcode` int NOT NULL DEFAULT '0' COMMENT '小程序二维码',
  `qrcode_sign` int NOT NULL DEFAULT '0' COMMENT '签到二维码',
  `service_conf` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现场服务配置',
  `qrcode_posters` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '海报，可能会有多个',
  `event_point_type` tinyint(1) NOT NULL DEFAULT '0' COMMENT '活动积分类型',
  `join_type` tinyint(1) NOT NULL DEFAULT '0' COMMENT '加入限制。0=正常开放，1=仅限会员参加',
  `is_from_bm` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否来自小立报名 0否 1是',
  `service_tel` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '客服电话',
  `multi_sign` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否允许多个报名 0=不允许 1=允许',
  `fee_kind_limit` int NOT NULL DEFAULT '1' COMMENT '一次报名可选票种数量上限',
  `deleted_at` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '删除时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '活动创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='活动信息表';

-- --------------------------------------------------------

--
-- 表的结构 `event_fee`
--

CREATE TABLE `event_fee` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `title` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '名称',
  `amount` int NOT NULL DEFAULT '0' COMMENT '费用，单位分',
  `refund_amount` int NOT NULL DEFAULT '0' COMMENT '诚意金退款金额',
  `everylimit` int NOT NULL DEFAULT '0' COMMENT '每人限买个数',
  `upperlimit` int NOT NULL DEFAULT '0' COMMENT '票种总数量',
  `used_count` int NOT NULL DEFAULT '0' COMMENT '已用数量',
  `is_bird` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否为早鸟票：1=是',
  `bird_end_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '早鸟票购买截止时间',
  `is_earnest` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否为诚意金：1=是',
  `member_fee_type` tinyint(1) NOT NULL DEFAULT '0' COMMENT '会员活动报名费。0=普通费，1=定值费，2=变值费',
  `info` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '费用描述',
  `deleted_at` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '删除时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='活动票种';

-- --------------------------------------------------------

--
-- 表的结构 `event_locale_confirmation`
--

CREATE TABLE `event_locale_confirmation` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `type_key` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '用户类型key',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='现场确认函';

-- --------------------------------------------------------

--
-- 表的结构 `event_locale_confirmation_user`
--

CREATE TABLE `event_locale_confirmation_user` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `confirmation_id` int NOT NULL DEFAULT '0' COMMENT '确认函ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `signed_id` int NOT NULL COMMENT '报名ID',
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '状态：1=未推送，2=已推送待确认，3=不能到场，4=确认能到场',
  `remark` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '备注',
  `deal_user_id` int NOT NULL DEFAULT '0' COMMENT '操作人ID',
  `mobile` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '手机号',
  `mark_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '处理状态：1=未推送，2=已推送待确认，3=不能到场，4=确认能到场',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='现场-确认函用户';

-- --------------------------------------------------------

--
-- 表的结构 `event_locale_prize`
--

CREATE TABLE `event_locale_prize` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `title` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '名称',
  `type_key` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '抽奖对象key',
  `odds_type` tinyint(1) NOT NULL DEFAULT '1' COMMENT '中奖概率类型：1=所有人一样，2=与报名费成正比...',
  `deleted_at` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '删除时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='现场-抽奖';

-- --------------------------------------------------------

--
-- 表的结构 `event_locale_prize_log`
--

CREATE TABLE `event_locale_prize_log` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `prize_id` int NOT NULL DEFAULT '0' COMMENT '抽奖ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '中奖用户ID',
  `batch_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '批次时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='现场-抽奖的中奖名单';

-- --------------------------------------------------------

--
-- 表的结构 `event_locale_prize_user`
--

CREATE TABLE `event_locale_prize_user` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `prize_id` int NOT NULL DEFAULT '0' COMMENT '抽奖ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `odds_num` int NOT NULL DEFAULT '1' COMMENT '抽奖基数，基数越大中奖概率越大',
  `has_win` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否已中奖',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='现场-抽奖用户';

-- --------------------------------------------------------

--
-- 表的结构 `event_locale_psq`
--

CREATE TABLE `event_locale_psq` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `title` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '问卷名称',
  `is_anonymity` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否为匿名问卷',
  `end_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '结束时间',
  `is_public` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否公开：1=是',
  `deleted_at` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '删除时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='现场-问卷';

-- --------------------------------------------------------

--
-- 表的结构 `event_locale_psq_log`
--

CREATE TABLE `event_locale_psq_log` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `psq_id` int NOT NULL DEFAULT '0' COMMENT '问卷ID',
  `psq_user_id` int NOT NULL DEFAULT '0' COMMENT 'psq_user 表ID',
  `option_id` int NOT NULL DEFAULT '0' COMMENT '题目ID',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '问卷回答内容',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='现场-问卷日志';

-- --------------------------------------------------------

--
-- 表的结构 `event_locale_psq_option`
--

CREATE TABLE `event_locale_psq_option` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `psq_id` int NOT NULL DEFAULT '0' COMMENT '文件ID',
  `title` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '题目标题',
  `type` tinyint(1) NOT NULL DEFAULT '1' COMMENT '题目类型：0=单行，1=多行，2=单选，3=多选',
  `option_json` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '选项内容',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='问卷选项';

-- --------------------------------------------------------

--
-- 表的结构 `event_locale_psq_user`
--

CREATE TABLE `event_locale_psq_user` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `psq_id` int NOT NULL DEFAULT '0' COMMENT '问卷ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '答卷时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='填写问卷用户';

-- --------------------------------------------------------

--
-- 表的结构 `event_locale_question`
--

CREATE TABLE `event_locale_question` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '提问内容',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='现场-提问';

-- --------------------------------------------------------

--
-- 表的结构 `event_locale_question_setting`
--

CREATE TABLE `event_locale_question_setting` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `is_public` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否公开：1=是',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='现场-提问配置';

-- --------------------------------------------------------

--
-- 表的结构 `event_locale_review`
--

CREATE TABLE `event_locale_review` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `title` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '评审名称',
  `rev_type` tinyint(1) NOT NULL DEFAULT '0' COMMENT '评审方式 0=网络评审 1=现场评审',
  `rev_endtime` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '评审结束时间',
  `score_type` tinyint(1) NOT NULL DEFAULT '0' COMMENT '计分方式 0=均分 1=中间分',
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '状态 0=未发布 1=已发布 2=已结束',
  `locale_item_id` int NOT NULL DEFAULT '0' COMMENT '评审对象ID',
  `deleted_at` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '删除时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='评审表' ROW_FORMAT=DYNAMIC;

-- --------------------------------------------------------

--
-- 表的结构 `event_locale_review_item`
--

CREATE TABLE `event_locale_review_item` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `title` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '评审对象名称',
  `review_id` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '评审ID',
  `sort` int NOT NULL COMMENT '排序值，小在前',
  `item_pic` int NOT NULL DEFAULT '0' COMMENT '对象图片ID',
  `deleted_at` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '删除时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='评审对象表' ROW_FORMAT=DYNAMIC;

-- --------------------------------------------------------

--
-- 表的结构 `event_locale_review_judges`
--

CREATE TABLE `event_locale_review_judges` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `review_id` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '评审ID',
  `judges_name` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '评审名称',
  `judges_img_id` int NOT NULL COMMENT '评审头像ID',
  `deleted_at` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '删除时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='评审评委表' ROW_FORMAT=DYNAMIC;

-- --------------------------------------------------------

--
-- 表的结构 `event_locale_review_rule`
--

CREATE TABLE `event_locale_review_rule` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `title` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '评审规则名称',
  `rule_notes` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '备注',
  `review_id` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '评审ID',
  `sort` int NOT NULL COMMENT '排序值，小在前',
  `score_limit` int NOT NULL DEFAULT '0' COMMENT '分数上限',
  `deleted_at` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '删除时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='评审规则表' ROW_FORMAT=DYNAMIC;

-- --------------------------------------------------------

--
-- 表的结构 `event_locale_review_score`
--

CREATE TABLE `event_locale_review_score` (
  `id` int NOT NULL COMMENT '主键ID',
  `review_id` int NOT NULL DEFAULT '0' COMMENT '评审ID',
  `item_id` int NOT NULL DEFAULT '0' COMMENT '评审对象ID',
  `judges_id` int NOT NULL DEFAULT '0' COMMENT '评委ID',
  `rule_id` int NOT NULL DEFAULT '0' COMMENT '评审规则ID',
  `score` int NOT NULL DEFAULT '0' COMMENT '分数',
  `deleted_at` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '删除时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='评审明细表' ROW_FORMAT=DYNAMIC;

-- --------------------------------------------------------

--
-- 表的结构 `event_locale_screen_process`
--

CREATE TABLE `event_locale_screen_process` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `type` tinyint(1) NOT NULL DEFAULT '1' COMMENT '彩排类型：1=大屏，2=签到墙，3=投票，4=抽奖，5=现场提问，6=问卷',
  `ref_id` int NOT NULL DEFAULT '0' COMMENT '类型关联ID',
  `sort` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '排序值，小在前',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='现场-彩排流程';

-- --------------------------------------------------------

--
-- 表的结构 `event_locale_screen_setting`
--

CREATE TABLE `event_locale_screen_setting` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `title` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '投屏标题',
  `title_color` char(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '标题颜色值',
  `title_sub` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '投屏副标题',
  `title_sub_color` char(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '副标题颜色值',
  `banner` int NOT NULL DEFAULT '0' COMMENT '背景图',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='现场-屏幕设置';

-- --------------------------------------------------------

--
-- 表的结构 `event_locale_signin`
--

CREATE TABLE `event_locale_signin` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '签到名称',
  `type` tinyint(1) NOT NULL DEFAULT '1' COMMENT '签到方式：1=用户扫码，2=管理员扫码',
  `type_key` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '参与用户类型',
  `user_type` tinyint(1) NOT NULL DEFAULT '0' COMMENT '签到用户类型 0=允许谁签到 1=禁止谁签到',
  `deleted_at` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '删除时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='活动签到';

-- --------------------------------------------------------

--
-- 表的结构 `event_locale_signin_statistics`
--

CREATE TABLE `event_locale_signin_statistics` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `signed_id` int NOT NULL DEFAULT '0' COMMENT '报名ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `signin_count` int NOT NULL DEFAULT '0' COMMENT '签到次数',
  `last_signin_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '最后签到时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='现场-签到用户统计';

-- --------------------------------------------------------

--
-- 表的结构 `event_locale_signin_user`
--

CREATE TABLE `event_locale_signin_user` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `signin_id` int NOT NULL DEFAULT '0' COMMENT '签到ID',
  `signed_id` int NOT NULL COMMENT '报名ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `signin_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '签到时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='现场-签到用户';

-- --------------------------------------------------------

--
-- 表的结构 `event_locale_vote`
--

CREATE TABLE `event_locale_vote` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `title` varchar(264) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '投票名称',
  `can_vote_type_key` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '可投屏人范围，为空则表示不限制',
  `upperlimit` int NOT NULL DEFAULT '0' COMMENT '每人投票上限',
  `start_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '投票开始时间',
  `end_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '投票结束时间',
  `is_public` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否公开：1=是',
  `deleted_at` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '删除时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='现场-投票';

-- --------------------------------------------------------

--
-- 表的结构 `event_locale_vote_item`
--

CREATE TABLE `event_locale_vote_item` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `vote_id` int NOT NULL DEFAULT '0' COMMENT '投票ID',
  `custom_title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '选项名称',
  `custom_cover` int NOT NULL DEFAULT '0' COMMENT '选项封面',
  `custom_base` int NOT NULL DEFAULT '0' COMMENT '选项初始票数',
  `custom_code` int NOT NULL DEFAULT '0' COMMENT '选项编号',
  `vote_result` int NOT NULL DEFAULT '0' COMMENT '投票数',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='现场-投票对象';

-- --------------------------------------------------------

--
-- 表的结构 `event_locale_vote_log`
--

CREATE TABLE `event_locale_vote_log` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `vote_id` int NOT NULL DEFAULT '0' COMMENT '投票ID',
  `item_id` int NOT NULL DEFAULT '0' COMMENT '投票对象ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='现场-投票日志';

-- --------------------------------------------------------

--
-- 表的结构 `event_member_fee`
--

CREATE TABLE `event_member_fee` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `team_id` char(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '组织ID',
  `event_member_fee` int NOT NULL DEFAULT '0' COMMENT '会员活动报名费',
  `event_member_fee_type` tinyint(1) NOT NULL DEFAULT '0' COMMENT '会员活动报名费。0=普通费，1=定值费，2=变值费',
  `team_level_id` int NOT NULL DEFAULT '0' COMMENT '报名费关联等级',
  `event_fee_id` int NOT NULL DEFAULT '0' COMMENT '票种ID',
  `create_time` int UNSIGNED NOT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;

-- --------------------------------------------------------

--
-- 表的结构 `event_refund_log`
--

CREATE TABLE `event_refund_log` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `signed_id` int NOT NULL DEFAULT '0' COMMENT '报名ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `fee` int NOT NULL COMMENT '单位：分',
  `action` tinyint(1) NOT NULL DEFAULT '0' COMMENT '1：取消报名，2：排队失败，3：管理员取消报名',
  `pay_way` tinyint(1) NOT NULL DEFAULT '0' COMMENT '收款方式 0=普通商户 1服务商特约商户',
  `sub_mch_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '特约商户号',
  `reason` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '退款原因',
  `result` tinyint(1) NOT NULL DEFAULT '0' COMMENT '退款是否成功，1成，0败',
  `err_msg` tinytext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '退款失败信息',
  `create_time` int UNSIGNED NOT NULL COMMENT '创建时间',
  `update_time` int UNSIGNED NOT NULL COMMENT '更新时间',
  `out_refund_no` char(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '商户退款单号'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='退款记录';

-- --------------------------------------------------------

--
-- 表的结构 `event_setting`
--

CREATE TABLE `event_setting` (
  `Id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '活动ID',
  `button_label` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '按键设置',
  `share_title` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '分享标题',
  `share_pic` int DEFAULT '0' COMMENT '分享图片',
  `show_msg` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '报名提醒文字',
  `show_pic` int DEFAULT '0' COMMENT '报名提醒图片',
  `show_pics` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `create_time` int NOT NULL COMMENT '创建时间',
  `update_time` int NOT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;

-- --------------------------------------------------------

--
-- 表的结构 `event_settle_apply`
--

CREATE TABLE `event_settle_apply` (
  `id` int NOT NULL COMMENT '主键ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `fee` int NOT NULL COMMENT '结算金额，单位：分',
  `fee_get` int NOT NULL COMMENT '到手金额，单位：分',
  `sub_mch_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '特约商户号',
  `merchant_shortname` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '商户简称',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '结算申请状态 1处理中 2处理成功 3部分成功 4处理失败',
  `err_message` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '失败描述',
  `finish_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '结算成功时间',
  `update_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='结算申请';

-- --------------------------------------------------------

--
-- 表的结构 `event_signed`
--

CREATE TABLE `event_signed` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `old_user_id` int NOT NULL DEFAULT '0' COMMENT '报名原始用户ID',
  `fee_id` int DEFAULT '0' COMMENT '票种ID',
  `sign_data` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '报名内容',
  `sign_no` int NOT NULL COMMENT '报名编号，从1开始递增',
  `sign_count` int NOT NULL DEFAULT '1' COMMENT '报名数量',
  `signfee` int DEFAULT '0' COMMENT '报名费,单位：分',
  `event_member_fee_id` int NOT NULL DEFAULT '0' COMMENT '会员报名费ID',
  `sign_mobile` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT '' COMMENT '报名手机号',
  `pay_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '支付状态，0默认未支付，1已支付 2已退款，3支付超时 4诚意金退款',
  `discount_money` int NOT NULL DEFAULT '0' COMMENT '打折金额，单位分',
  `deleted_type` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否已删除 0=未删除 1=用户取消报名 2=管理员删除 3=付款超时|定时任务',
  `check_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '审核状态，0待审核，1审核通过 2审核不通过',
  `check_msg` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '审核信息',
  `des` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '备注',
  `mark` tinyint NOT NULL DEFAULT '1' COMMENT '标记',
  `add_way` tinyint(1) NOT NULL DEFAULT '0' COMMENT '报名添加方式 0用户报名  1管理员添加',
  `deleted_at` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '删除时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='报名名单';

-- --------------------------------------------------------

--
-- 表的结构 `event_signed_edit_log`
--

CREATE TABLE `event_signed_edit_log` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) NOT NULL DEFAULT '' COMMENT '活动ID',
  `signed_id` int NOT NULL DEFAULT '0' COMMENT '报名id',
  `operator_id` int NOT NULL DEFAULT '0' COMMENT '操作人id',
  `before_sign_data` text NOT NULL COMMENT '报名前内容',
  `after_sign_data` text NOT NULL COMMENT '报名后内容',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '修改时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='报名修改记录';

-- --------------------------------------------------------

--
-- 表的结构 `event_signed_fee`
--

CREATE TABLE `event_signed_fee` (
  `id` int NOT NULL,
  `event_id` char(32) COLLATE utf8mb4_general_ci NOT NULL,
  `signed_id` int NOT NULL,
  `fee_id` int NOT NULL,
  `title` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `amount` int NOT NULL COMMENT '费用，单位分	',
  `refund_amount` int NOT NULL DEFAULT '0' COMMENT '诚意金退款金额',
  `is_earnest` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否为诚意金：1=是',
  `buy_count` int NOT NULL DEFAULT '0' COMMENT '购买数量',
  `deleted_at` int NOT NULL DEFAULT '0',
  `create_time` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='缓存用户报名时的报名费，防止管理员修改后发生变化';

-- --------------------------------------------------------

--
-- 表的结构 `event_signed_group`
--

CREATE TABLE `event_signed_group` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '分组名称',
  `user_open` tinyint(1) NOT NULL DEFAULT '0' COMMENT '用户可见，0=否，1=是',
  `user_count` int NOT NULL COMMENT '用户数',
  `deleted_at` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '删除时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='报名分组';

-- --------------------------------------------------------

--
-- 表的结构 `event_signed_group_user`
--

CREATE TABLE `event_signed_group_user` (
  `id` int NOT NULL COMMENT '主键ID',
  `group_id` int NOT NULL DEFAULT '0' COMMENT '分组ID',
  `signed_id` int NOT NULL DEFAULT '0' COMMENT '报名ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `deleted_at` int NOT NULL DEFAULT '0' COMMENT '删除时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='报名分组用户';

-- --------------------------------------------------------

--
-- 表的结构 `event_signed_order`
--

CREATE TABLE `event_signed_order` (
  `id` int NOT NULL,
  `event_id` char(32) CHARACTER SET utf8mb3 NOT NULL COMMENT '活动ID',
  `signed_id` int NOT NULL DEFAULT '0' COMMENT '报名ID',
  `order_name` varchar(256) CHARACTER SET utf8mb3 NOT NULL DEFAULT '' COMMENT '订单名称',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `amount` int NOT NULL DEFAULT '0' COMMENT '订单金额，单位：分',
  `residue_amount` int NOT NULL DEFAULT '0' COMMENT '订单金额余额，单位：分',
  `out_trade_no` char(32) CHARACTER SET utf8mb3 NOT NULL DEFAULT '',
  `transaction_id` varchar(32) CHARACTER SET utf8mb3 NOT NULL COMMENT '微信支付订单号',
  `sub_mch_id` varchar(32) CHARACTER SET utf8mb3 NOT NULL DEFAULT '' COMMENT '特约商户号',
  `is_settled` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否已结算 0=未结算 1已结算',
  `status` tinyint NOT NULL DEFAULT '0' COMMENT '状态，0=未支付 1=已支付 2=已退款 ',
  `paid_time` int NOT NULL DEFAULT '0' COMMENT '付款时间',
  `deleted_at` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '删除时间',
  `create_time` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='报名费订单';

-- --------------------------------------------------------

--
-- 表的结构 `event_sms_order`
--

CREATE TABLE `event_sms_order` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `title` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '发送名称',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `qty` int NOT NULL DEFAULT '0' COMMENT '发送手机号个数',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '短信内容',
  `amount` int NOT NULL DEFAULT '0' COMMENT '支付金额',
  `out_trade_no` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT '',
  `transaction_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT '' COMMENT '微信支付订单号',
  `code_url` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '扫描支付url',
  `is_paid` tinyint NOT NULL DEFAULT '0' COMMENT '是否支付',
  `is_send` tinyint NOT NULL DEFAULT '0' COMMENT '是否已发送',
  `is_refund` tinyint NOT NULL DEFAULT '0' COMMENT '是否退款，0 未，1已退 2退款出错',
  `paid_time` int NOT NULL DEFAULT '0' COMMENT '付款时间',
  `mobiles` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '发送的手机号列表',
  `create_time` int NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='短信群发订单';

-- --------------------------------------------------------

--
-- 表的结构 `event_sms_result`
--

CREATE TABLE `event_sms_result` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `order_id` int NOT NULL DEFAULT '0' COMMENT '订单ID',
  `product_id` int NOT NULL DEFAULT '0' COMMENT '短信来源对象ID',
  `mobile` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '手机号',
  `sms_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '发送ID',
  `event_type` tinyint NOT NULL DEFAULT '0' COMMENT '发送类型:短信来源 0群发短信,1报名审核通知,2确认函',
  `status_code` int NOT NULL DEFAULT '0' COMMENT '发送状态',
  `fail_msg` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '失败信息',
  `create_time` int NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='短信群发日志';

-- --------------------------------------------------------

--
-- 表的结构 `event_spread_channel`
--

CREATE TABLE `event_spread_channel` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '渠道名称',
  `qrcode` int NOT NULL DEFAULT '0' COMMENT '渠道二维码，发展管理员用',
  `deleted_at` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '删除时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='活动渠道商';

-- --------------------------------------------------------

--
-- 表的结构 `event_spread_channel_admin`
--

CREATE TABLE `event_spread_channel_admin` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `channel_id` int NOT NULL DEFAULT '0' COMMENT '渠道商ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `type` tinyint(1) NOT NULL DEFAULT '0' COMMENT '类型：1=管理员，2=普通推广人员',
  `qrcode` int NOT NULL DEFAULT '0' COMMENT '推广二维码',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='活动渠道商推广人员';

-- --------------------------------------------------------

--
-- 表的结构 `event_spread_channel_detail`
--

CREATE TABLE `event_spread_channel_detail` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `channel_id` int NOT NULL DEFAULT '0' COMMENT '渠道商ID',
  `channel_user_id` int NOT NULL DEFAULT '0' COMMENT '推广人员ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '参与用户ID',
  `action` tinyint(1) NOT NULL DEFAULT '0' COMMENT '触发类型：1=点击，2=报名',
  `signed_id` int NOT NULL DEFAULT '0' COMMENT '报名ID',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='活动渠道商推广的用户';

-- --------------------------------------------------------

--
-- 表的结构 `event_spread_user_record`
--

CREATE TABLE `event_spread_user_record` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '参与用户ID',
  `click_count` int NOT NULL DEFAULT '0' COMMENT '点击次数',
  `signed_count` int NOT NULL DEFAULT '0' COMMENT '报名次数',
  `is_used` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否已使用，只能使用报名一次',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='参与转发赠票的用户';

-- --------------------------------------------------------

--
-- 表的结构 `event_spread_user_record_detail`
--

CREATE TABLE `event_spread_user_record_detail` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `record_id` int NOT NULL DEFAULT '0' COMMENT '用户推广ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '参与用户ID',
  `action` tinyint(1) NOT NULL DEFAULT '0' COMMENT '触发类型：1=点击，2=报名',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='转发赠票被推广的用户';

-- --------------------------------------------------------

--
-- 表的结构 `event_spread_user_rule`
--

CREATE TABLE `event_spread_user_rule` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `type` tinyint(1) NOT NULL DEFAULT '1' COMMENT '类型：1=赠票，2=打折',
  `action` tinyint(1) NOT NULL DEFAULT '0' COMMENT '维度：1=点击，2=点击且报名',
  `min_limit` int NOT NULL DEFAULT '0' COMMENT '最小数量',
  `event_fee_id` int NOT NULL DEFAULT '0' COMMENT '赠送票种',
  `discount` int NOT NULL DEFAULT '0' COMMENT '折扣，0-100',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='转发赠票规则';

-- --------------------------------------------------------

--
-- 表的结构 `event_spread_user_setting`
--

CREATE TABLE `event_spread_user_setting` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `give_uplimit` int NOT NULL DEFAULT '0' COMMENT '赠票上限',
  `discount_uplimit` int NOT NULL DEFAULT '0' COMMENT '打折人数上限',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='个人推广设置';

-- --------------------------------------------------------

--
-- 表的结构 `event_withdraw_log`
--

CREATE TABLE `event_withdraw_log` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `rev_user_id` int NOT NULL COMMENT '收款用户Id,是活动创建者',
  `apply_user_id` int NOT NULL DEFAULT '0' COMMENT '申请用户ID',
  `fee` int NOT NULL DEFAULT '0' COMMENT '提现金额',
  `fee_get` int NOT NULL DEFAULT '0' COMMENT '到手金额',
  `openid` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '提现账号openid',
  `realname` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '提现姓名',
  `result` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0 处理中 1成功，2失败',
  `err_msg` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '失败信息',
  `retry_time` int DEFAULT '0' COMMENT '重试时间，超过这个时间后再重试',
  `done_time` int DEFAULT '0' COMMENT '提现处理时间',
  `create_time` int UNSIGNED NOT NULL COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='活动提现记录';

-- --------------------------------------------------------

--
-- 表的结构 `event_wxbalance`
--

CREATE TABLE `event_wxbalance` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `wxbalance_total` int DEFAULT '0' COMMENT '报名总金额（含排队用户）',
  `wxbalance_usable` int DEFAULT '0' COMMENT '可用余额',
  `wxbalance_withdraw` int DEFAULT '0' COMMENT '已提现金额（含申请中）',
  `wxbalance_withdrawing` int DEFAULT '0' COMMENT '提现中',
  `wxbalance_withdraw_finish` int DEFAULT '0' COMMENT '提现已到手',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '活动创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='活动结算表';

-- --------------------------------------------------------

--
-- 表的结构 `export_token`
--

CREATE TABLE `export_token` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `token` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '导出数据权限认证token',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='导出数据权限认证token';

-- --------------------------------------------------------

--
-- 表的结构 `feedback`
--

CREATE TABLE `feedback` (
  `id` int NOT NULL COMMENT '主键ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户id',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '内容',
  `reply` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '回复',
  `reply_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '回复时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='用户反馈';

-- --------------------------------------------------------

--
-- 表的结构 `fields`
--

CREATE TABLE `fields` (
  `id` int NOT NULL COMMENT '主键ID',
  `team_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '组织ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '添加用户ID',
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '字段名称',
  `datatype` tinyint NOT NULL COMMENT '"单行输入框", "多行输入框","单选", "多选","系统取值，如定位"',
  `inputtype` tinyint(1) NOT NULL DEFAULT '0' COMMENT '1 数字,0 默认文本',
  `tip` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '字段提示',
  `options` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '选项内容',
  `deleted_at` int UNSIGNED DEFAULT '0' COMMENT '删除时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='自定义数据类型';

-- --------------------------------------------------------

--
-- 表的结构 `help`
--

CREATE TABLE `help` (
  `id` int NOT NULL COMMENT '主键ID',
  `title` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '标题',
  `h5_link` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT 'H5链接地址',
  `sort` int DEFAULT '0' COMMENT '排序 大的在前',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='帮助文章';

-- --------------------------------------------------------

--
-- 表的结构 `member_order_settle_log`
--

CREATE TABLE `member_order_settle_log` (
  `id` int NOT NULL COMMENT '主键ID',
  `team_id` char(32) NOT NULL DEFAULT '' COMMENT '组织ID',
  `order_id` int NOT NULL DEFAULT '0' COMMENT '订单ID',
  `fee` int NOT NULL COMMENT '结算金额，单位：分',
  `fee_get` int NOT NULL COMMENT '到手金额，单位：分',
  `sub_mch_id` varchar(32) NOT NULL DEFAULT '' COMMENT '特约商户号',
  `merchant_shortname` varchar(256) NOT NULL DEFAULT '' COMMENT '商户简称',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '结算申请状态 1处理中 2处理成功 3处理失败',
  `err_message` varchar(256) NOT NULL DEFAULT '' COMMENT '失败描述',
  `update_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='会费订单结算记录';

-- --------------------------------------------------------

--
-- 表的结构 `member_refund_log`
--

CREATE TABLE `member_refund_log` (
  `id` int NOT NULL COMMENT '主键ID',
  `team_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '组织ID',
  `member_id` int NOT NULL DEFAULT '0' COMMENT '报名ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `order_id` int NOT NULL DEFAULT '0' COMMENT '订单ID',
  `fee` int NOT NULL COMMENT '单位：分',
  `action` tinyint(1) NOT NULL DEFAULT '0' COMMENT '1：审核未通过退款，2：未审核自主退出组织',
  `reason` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '退款原因',
  `result` tinyint(1) NOT NULL DEFAULT '0' COMMENT '退款是否成功，1成，0败',
  `err_msg` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '退款失败信息',
  `create_time` int UNSIGNED NOT NULL COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='组织会员退款记录';

-- --------------------------------------------------------

--
-- 表的结构 `message`
--

CREATE TABLE `message` (
  `id` int NOT NULL COMMENT '主键ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `title` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '消息标题',
  `content` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '消息内容',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='用户消息';

-- --------------------------------------------------------

--
-- 表的结构 `message_config`
--

CREATE TABLE `message_config` (
  `id` int NOT NULL COMMENT '主键ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `signed_sw` tinyint(1) DEFAULT '0' COMMENT '报名结果通知：1=开，0=关',
  `event_start_sw` tinyint(1) DEFAULT '0' COMMENT '活动开始通知：1=开，0=关',
  `new_event_sw` tinyint(1) DEFAULT '0' COMMENT '关注的组织发布新活动：1=开，0=关',
  `signed_check_sw` tinyint(1) DEFAULT '0' COMMENT '报名审核结果：1=开，0=关',
  `new_signed_sw` tinyint(1) DEFAULT '0' COMMENT '新报名：1=开，0=关',
  `daycount_signed_sw` tinyint(1) DEFAULT '0' COMMENT '新报名按天汇总：1=开，0=关',
  `event_qrcode_group_sw` tinyint(1) DEFAULT '0' COMMENT '群二维码过期：1=开，0=关',
  `event_start_sms_sw` int NOT NULL DEFAULT '1' COMMENT '活动开始短信通知',
  `new_event_sms_sw` int NOT NULL DEFAULT '1' COMMENT '关注的组织发布新活动短信通知',
  `new_signed_sms_sw` int NOT NULL DEFAULT '0' COMMENT '新报名短信通知',
  `new_event_member_sms_sw` int NOT NULL DEFAULT '0' COMMENT '新报名短信通知',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='用户开关设置';

-- --------------------------------------------------------

--
-- 表的结构 `order_settle_log`
--

CREATE TABLE `order_settle_log` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `settle_apply_id` int NOT NULL DEFAULT '0' COMMENT '结算申请ID',
  `order_id` int NOT NULL DEFAULT '0' COMMENT '订单ID',
  `fee` int NOT NULL DEFAULT '0' COMMENT '结算金额',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '分账状态 1处理中 2分账完成',
  `update_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='订单结算记录';

-- --------------------------------------------------------

--
-- 表的结构 `oss_black_user`
--

CREATE TABLE `oss_black_user` (
  `id` int NOT NULL COMMENT '主键ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='oss黑名单用户';

-- --------------------------------------------------------

--
-- 表的结构 `recommend_position`
--

CREATE TABLE `recommend_position` (
  `id` int NOT NULL COMMENT '主键ID',
  `pos_code` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '编号',
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '推荐位名称',
  `source_table` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '来源table',
  `deleted_at` int NOT NULL DEFAULT '0' COMMENT '是否删除',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='推荐位管理';

-- --------------------------------------------------------

--
-- 表的结构 `recommend_position_ref`
--

CREATE TABLE `recommend_position_ref` (
  `id` int NOT NULL COMMENT '主键ID',
  `pos_id` int NOT NULL DEFAULT '0' COMMENT '位置ID',
  `source_id` varchar(35) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0' COMMENT '目标ID',
  `sort` int NOT NULL DEFAULT '0' COMMENT '排序值',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='推荐位关系';

-- --------------------------------------------------------

--
-- 表的结构 `settle_receivers`
--

CREATE TABLE `settle_receivers` (
  `id` int NOT NULL COMMENT '主键ID',
  `sub_mch_id` varchar(256) COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '子商户号（分账出资方）',
  `service_mch_id` varchar(256) COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '服务商商户号（分账接收方）',
  `update_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='结算分账接收关系表';

-- --------------------------------------------------------

--
-- 表的结构 `statistics`
--

CREATE TABLE `statistics` (
  `id` int NOT NULL COMMENT '主键ID',
  `date` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '统计日期',
  `event_count` int NOT NULL DEFAULT '0' COMMENT '当日新增活动数',
  `team_count` int NOT NULL DEFAULT '0' COMMENT '当日新增组织数',
  `user_count` int NOT NULL DEFAULT '0' COMMENT '当日新增用户数',
  `sign_fee` int NOT NULL DEFAULT '0' COMMENT '当日新增报名费收入',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='每日数据统计表';

-- --------------------------------------------------------

--
-- 表的结构 `sub_mch_apply`
--

CREATE TABLE `sub_mch_apply` (
  `id` int NOT NULL COMMENT '主键ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `business_code` varchar(124) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '业务申请编号',
  `subject_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '主体类型',
  `contact_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '超级管理员信息',
  `subject_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '主体资料',
  `business_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '经营资料',
  `settlement_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '结算规则',
  `bank_account_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '结算银行账户',
  `addition_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '补充材料',
  `applyment_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0' COMMENT '微信支付申请单号',
  `sub_mchid` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '特约商户号',
  `merchant_shortname` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '商户简称',
  `sign_url` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '超级管理员签约链接',
  `applyment_state` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0' COMMENT '申请单状态',
  `applyment_state_msg` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '申请状态描述',
  `audit_detail` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '驳回原因详情',
  `update_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='特约商户进件申请单';

-- --------------------------------------------------------

--
-- 表的结构 `sub_mch_file`
--

CREATE TABLE `sub_mch_file` (
  `id` int NOT NULL COMMENT '主键ID',
  `media_id` varchar(256) NOT NULL DEFAULT '' COMMENT '微信资源id',
  `oss_path` varchar(256) NOT NULL DEFAULT '' COMMENT 'oss文件路径',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='服务商进件申请资源路径表';

-- --------------------------------------------------------

--
-- 表的结构 `team`
--

CREATE TABLE `team` (
  `id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `category_pid` int NOT NULL DEFAULT '0' COMMENT '父级ID',
  `category_id` int NOT NULL DEFAULT '0' COMMENT '分类ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '圈主ID',
  `title` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '组织标题',
  `type` tinyint(1) NOT NULL DEFAULT '1' COMMENT '类型：1=个人，2=企业',
  `address` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '组织地址',
  `city` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '组织所在城市',
  `latitude` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '纬度',
  `longitude` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '经度',
  `cover` int NOT NULL DEFAULT '0' COMMENT '组织封面',
  `logo` int NOT NULL DEFAULT '0' COMMENT '组织logo',
  `introduce` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '组织介绍',
  `qrcode` int NOT NULL DEFAULT '0' COMMENT '组织二维码',
  `qrcode_posters` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '组织海报',
  `license` int NOT NULL DEFAULT '0' COMMENT '营业执照',
  `owner_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '圈主姓名',
  `owner_mobile` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '圈主电话',
  `owner_wechat` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '微信号',
  `idcard_pros` int NOT NULL DEFAULT '0' COMMENT '身份证正面',
  `idcard_cons` int NOT NULL DEFAULT '0' COMMENT '身份证反面',
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '状态：0=初始，1=待认证，2=认证通过，3=认证不通过',
  `status_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '状态处理时间',
  `err_msg` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '认证失败原因',
  `last_event_time` int NOT NULL COMMENT '最新发布的活动时间',
  `event_count` int NOT NULL DEFAULT '0' COMMENT '发布活动量',
  `view_count` int NOT NULL DEFAULT '0' COMMENT '浏览量',
  `subscribe_count` int NOT NULL DEFAULT '0' COMMENT '关注量',
  `is_privacy` tinyint(1) DEFAULT '0' COMMENT '是否为私密组织',
  `is_show` tinyint(1) DEFAULT '0' COMMENT '首页是否显示 0否 1是',
  `is_join_open` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否开放加入组织',
  `feerate` int NOT NULL DEFAULT '10' COMMENT '组织的提现费率，千分之几',
  `is_banned` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否被禁',
  `deleted_at` int UNSIGNED DEFAULT '0' COMMENT '删除时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '更新时间',
  `team_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '显示设置，哪些字段显示或隐藏',
  `team_member_switch` tinyint(1) NOT NULL DEFAULT '0' COMMENT '会员系统开关 1=开启',
  `level_depend` tinyint NOT NULL COMMENT '会员等级确定方式，默认0：老版本，1：积分 2会员费',
  `team_member_fee` int NOT NULL DEFAULT '0' COMMENT '入会费',
  `team_member_valid_time` int NOT NULL DEFAULT '0' COMMENT '会员有效期，单位月，0永久',
  `is_from_bm` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否来自小立报名 0否 1是',
  `pay_way` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='组织信息表';

-- --------------------------------------------------------

--
-- 表的结构 `team_admin`
--

CREATE TABLE `team_admin` (
  `id` int NOT NULL COMMENT '主键ID',
  `team_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '组织ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `user_type` tinyint(1) NOT NULL DEFAULT '0' COMMENT '用户类型：1=圈主，2=管理员',
  `recv_new_signed` tinyint NOT NULL DEFAULT '0' COMMENT '是否接收汇总通知，0未设置，1接收，2不接收',
  `recv_daycount` tinyint NOT NULL DEFAULT '0' COMMENT '是否接收每日汇总通知，0未设置，1接收，2不接收',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态：1=正常，0=禁用',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '加入时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='组织管理员';

-- --------------------------------------------------------

--
-- 表的结构 `team_album`
--

CREATE TABLE `team_album` (
  `id` int NOT NULL COMMENT '主键ID',
  `team_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '组织ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '创建者用户ID',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '相册名称',
  `deleted_at` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '删除时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='组织相册';

-- --------------------------------------------------------

--
-- 表的结构 `team_album_photo`
--

CREATE TABLE `team_album_photo` (
  `id` int NOT NULL COMMENT '主键ID',
  `team_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '组织ID',
  `album_id` int NOT NULL DEFAULT '0' COMMENT '相册ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `file_id` int NOT NULL DEFAULT '0' COMMENT '附件ID',
  `sort` int NOT NULL DEFAULT '0' COMMENT '排序值',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='组织相册-照片';

-- --------------------------------------------------------

--
-- 表的结构 `team_assign_log`
--

CREATE TABLE `team_assign_log` (
  `id` int NOT NULL COMMENT '主键ID',
  `team_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '组织ID',
  `from_user_id` int NOT NULL DEFAULT '0' COMMENT '发起转让用户ID',
  `to_user_id` int NOT NULL DEFAULT '0' COMMENT '转让目标用户ID',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='转让日志';

-- --------------------------------------------------------

--
-- 表的结构 `team_black_user`
--

CREATE TABLE `team_black_user` (
  `id` int NOT NULL COMMENT '主键ID',
  `team_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '组织ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户id',
  `black_user_id` int NOT NULL DEFAULT '0' COMMENT '黑名单用户id',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 表的结构 `team_event_point`
--

CREATE TABLE `team_event_point` (
  `id` int NOT NULL COMMENT '主键ID',
  `event_id` char(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `team_id` char(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '组织ID',
  `event_point` int NOT NULL DEFAULT '0' COMMENT '积分值',
  `event_point_type` tinyint(1) NOT NULL DEFAULT '0' COMMENT '活动积分类型。0=定值积分，1=变值积分',
  `team_level_id` int NOT NULL DEFAULT '0' COMMENT '积分关联等级',
  `create_time` int UNSIGNED NOT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;

-- --------------------------------------------------------

--
-- 表的结构 `team_fee`
--

CREATE TABLE `team_fee` (
  `id` int NOT NULL COMMENT '主键ID',
  `team_id` char(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '组织ID',
  `title` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '名称',
  `amount` int NOT NULL DEFAULT '0' COMMENT '费用，单位分',
  `info` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '费用描述',
  `deleted_at` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '删除时间',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='组织会员费票种' ROW_FORMAT=DYNAMIC;

-- --------------------------------------------------------

--
-- 表的结构 `team_member`
--

CREATE TABLE `team_member` (
  `id` int NOT NULL COMMENT '主键ID',
  `team_id` char(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '组织ID',
  `phone_number` varchar(11) COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '会员手机号',
  `user_id` int NOT NULL COMMENT '用户ID',
  `member_status` tinyint(1) NOT NULL COMMENT '成员状态: 0=待审核 1=通过审核 2审核不通过',
  `event_count` int NOT NULL COMMENT '活动计数',
  `member_message` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '申请信息',
  `des` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '备注',
  `member_level_id` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '成员等级ID',
  `member_point` int NOT NULL DEFAULT '0' COMMENT '成员积分',
  `pay_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '状态，0=未支付 1=已支付',
  `member_fee` int NOT NULL DEFAULT '0' COMMENT '报名费,单位：分，实际支付费用',
  `member_fee_payable` int NOT NULL COMMENT '应付金额，有可能旧续费折算，实付金额会小于这个',
  `member_fee_id` int NOT NULL DEFAULT '0' COMMENT '入会费ID',
  `member_type` tinyint(1) NOT NULL DEFAULT '0' COMMENT '会员类型 0=永久会员 1=时效会员',
  `start_time` int NOT NULL DEFAULT '0' COMMENT '本期会员的开始时间',
  `overdue_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '会员过期时间',
  `deleted_at` int NOT NULL DEFAULT '0' COMMENT '删除时间',
  `create_time` int UNSIGNED NOT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;

-- --------------------------------------------------------

--
-- 表的结构 `team_member_level`
--

CREATE TABLE `team_member_level` (
  `id` int NOT NULL,
  `name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `info` text COLLATE utf8mb4_general_ci NOT NULL COMMENT '等级介绍',
  `team_id` char(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `fee_id` int NOT NULL COMMENT '如果是按会费确定等级时使用',
  `amount` int NOT NULL DEFAULT '0' COMMENT '入会费，根据付费确定等级时有效',
  `member_count` int NOT NULL COMMENT '会员人数',
  `sort` int NOT NULL COMMENT '等级积分上限',
  `deleted_at` int NOT NULL DEFAULT '0',
  `create_time` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='会员等级' ROW_FORMAT=DYNAMIC;

-- --------------------------------------------------------

--
-- 表的结构 `team_member_log`
--

CREATE TABLE `team_member_log` (
  `id` int NOT NULL COMMENT '主键ID',
  `member_id` int NOT NULL COMMENT '组织成员ID',
  `signed_id` int NOT NULL COMMENT '活动报名ID',
  `event_point` int NOT NULL COMMENT '活动积分',
  `point_type` tinyint(1) NOT NULL DEFAULT '0' COMMENT '积分操作类型 0=增加 1=扣除',
  `des` varchar(256) CHARACTER SET utf8mb3 NOT NULL DEFAULT '' COMMENT '备注',
  `deleted_at` int NOT NULL DEFAULT '0' COMMENT '删除时间',
  `create_time` int UNSIGNED NOT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;

-- --------------------------------------------------------

--
-- 表的结构 `team_member_order`
--

CREATE TABLE `team_member_order` (
  `id` int NOT NULL,
  `team_id` char(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '组织ID',
  `member_id` int NOT NULL DEFAULT '0' COMMENT '组织成员ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `order_name` varchar(256) CHARACTER SET utf8mb3 NOT NULL DEFAULT '' COMMENT '订单名称',
  `amount` int NOT NULL DEFAULT '0' COMMENT '订单金额，单位：分',
  `amount_payable` int NOT NULL DEFAULT '0' COMMENT '应付金额',
  `out_trade_no` char(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `transaction_id` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '微信支付订单号',
  `status` tinyint NOT NULL DEFAULT '0' COMMENT '状态，0=未支付 1=已支付 2=已退款 ',
  `order_type` tinyint(1) NOT NULL DEFAULT '0' COMMENT '订单类型 1入会 2续费',
  `member_level_id` int NOT NULL DEFAULT '0' COMMENT '续费等级id',
  `is_settled` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否已结算 0=未结算 1结算中 2已结算',
  `paid_time` int NOT NULL DEFAULT '0' COMMENT '付款时间',
  `deleted_at` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '删除时间',
  `create_time` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='组织会员费订单' ROW_FORMAT=DYNAMIC;

-- --------------------------------------------------------

--
-- 表的结构 `team_message_config`
--

CREATE TABLE `team_message_config` (
  `id` int NOT NULL COMMENT '主键ID',
  `team_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '组织ID',
  `new_event_sw` tinyint(1) DEFAULT '0' COMMENT '新活动通知：1=开，0=关',
  `new_signed_sw` tinyint(1) DEFAULT '0' COMMENT '新报名实时：1=开，0=关',
  `daycount_signed_sw` tinyint(1) DEFAULT '0' COMMENT '新报名按天汇总：1=开，0=关',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='组织开关设置';

-- --------------------------------------------------------

--
-- 表的结构 `team_withdraw_log`
--

CREATE TABLE `team_withdraw_log` (
  `id` int NOT NULL COMMENT '主键ID',
  `team_id` char(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '组织ID',
  `rev_user_id` int NOT NULL COMMENT '收款用户Id,是组织拥有者',
  `apply_user_id` int NOT NULL DEFAULT '0' COMMENT '申请用户ID',
  `fee` int NOT NULL DEFAULT '0' COMMENT '提现金额',
  `fee_get` int NOT NULL DEFAULT '0' COMMENT '到手金额',
  `openid` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '提现账号openid',
  `realname` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '提现姓名',
  `result` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0 处理中 1成功，2失败',
  `err_msg` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '失败信息',
  `retry_time` int DEFAULT '0' COMMENT '重试时间，超过这个时间后再重试',
  `done_time` int DEFAULT '0' COMMENT '提现处理时间',
  `create_time` int UNSIGNED NOT NULL COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='活动提现记录' ROW_FORMAT=DYNAMIC;

-- --------------------------------------------------------

--
-- 表的结构 `team_wxbalance`
--

CREATE TABLE `team_wxbalance` (
  `id` int NOT NULL COMMENT '主键ID',
  `team_id` char(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '组织ID',
  `wxbalance_total` int DEFAULT '0' COMMENT '入会费总金额（含排队用户）',
  `wxbalance_usable` int DEFAULT '0' COMMENT '可用余额',
  `wxbalance_withdraw` int DEFAULT '0' COMMENT '已提现金额（含申请中）',
  `wxbalance_withdrawing` int DEFAULT '0' COMMENT '提现中',
  `wxbalance_withdraw_finish` int DEFAULT '0' COMMENT '提现已到手',
  `sub_wxbalance_total` int NOT NULL DEFAULT '0' COMMENT '入会费总金额(特约商户)',
  `sub_wxbalance_usable` int NOT NULL DEFAULT '0' COMMENT '可用余额(特约商户)',
  `sub_wxbalance_settle` int NOT NULL DEFAULT '0' COMMENT '已结算金额(特约商户)',
  `sub_wxbalance_settling` int NOT NULL DEFAULT '0' COMMENT '结算中',
  `sub_wxbalance_settle_finish` int NOT NULL DEFAULT '0' COMMENT '结算成功',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '活动创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='活动结算表' ROW_FORMAT=DYNAMIC;

-- --------------------------------------------------------

--
-- 表的结构 `user`
--

CREATE TABLE `user` (
  `id` int UNSIGNED NOT NULL,
  `openid` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT '' COMMENT '微信openid',
  `openid_xchx` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT '' COMMENT '小程序openid',
  `unionid` varchar(32) CHARACTER SET utf8mb3 NOT NULL DEFAULT '' COMMENT '微信unionId',
  `session_key` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT '' COMMENT 'session_key',
  `subscribe` tinyint DEFAULT '0' COMMENT '是否关注：0=否，1=是',
  `nickname` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT '' COMMENT '微信昵称',
  `sex` tinyint(1) DEFAULT '0' COMMENT '用户的性别，1=男性，2=女性，0=未知',
  `city` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT '' COMMENT '用户所在城市',
  `country` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT '' COMMENT '用户所在国家',
  `province` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT '' COMMENT '用户所在省份',
  `language` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT '' COMMENT '用户的语言，简体中文为zh_CN',
  `headimgurl` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT '' COMMENT '微信头像',
  `phone_number` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '手机号，带区号',
  `pure_phone_number` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '手机号，没区号',
  `country_code` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '国家码',
  `subscribe_time` int DEFAULT '0' COMMENT '用户关注时间,如果用户曾多次关注，则取最后关注时间',
  `subscribe_scene` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT '' COMMENT '返回用户关注的渠道来源',
  `email` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT '' COMMENT '邮箱',
  `is_banned` tinyint(1) DEFAULT '0' COMMENT '是否被禁用，0否 1是',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '最后更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='用户微信信息';

-- --------------------------------------------------------

--
-- 表的结构 `user_copy_data_log`
--

CREATE TABLE `user_copy_data_log` (
  `id` int NOT NULL COMMENT '主键ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `team_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '组织ID',
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '迁移数据处理状态 0待处理 1处理成功 2处理失败',
  `err_msg` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '失败信息',
  `update_time` int UNSIGNED NOT NULL COMMENT '创建时间',
  `create_time` int UNSIGNED NOT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='旧版小立报名数据迁移记录表';

-- --------------------------------------------------------

--
-- 表的结构 `user_follow`
--

CREATE TABLE `user_follow` (
  `id` int NOT NULL COMMENT '主键ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `action` tinyint NOT NULL DEFAULT '0' COMMENT '关注类型：1=活动，2=组织',
  `action_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '关注对象的ID',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='用户关注信息表';

-- --------------------------------------------------------

--
-- 表的结构 `wxacode_scene`
--

CREATE TABLE `wxacode_scene` (
  `id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '主键ID',
  `user_id` int NOT NULL DEFAULT '0' COMMENT '用户ID',
  `team_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '组织ID',
  `event_id` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '活动ID',
  `ref_type` tinyint NOT NULL DEFAULT '0' COMMENT '业务类型',
  `ref_id` int NOT NULL DEFAULT '0' COMMENT '业务ID',
  `expires_in` int NOT NULL DEFAULT '0' COMMENT '时效，0=永久（单位秒）',
  `salt` char(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '随机码',
  `create_time` int UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='微信二维码关系表';

--
-- 转储表的索引
--

--
-- 表的索引 `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `advertising`
--
ALTER TABLE `advertising`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `ad_channel`
--
ALTER TABLE `ad_channel`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `change_settle_blank`
--
ALTER TABLE `change_settle_blank`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `channel_log`
--
ALTER TABLE `channel_log`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- 表的索引 `comm_file`
--
ALTER TABLE `comm_file`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `config`
--
ALTER TABLE `config`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `district_tx`
--
ALTER TABLE `district_tx`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `event`
--
ALTER TABLE `event`
  ADD PRIMARY KEY (`id`),
  ADD KEY `team_id` (`team_id`),
  ADD KEY `user_id` (`user_id`);

--
-- 表的索引 `event_fee`
--
ALTER TABLE `event_fee`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_locale_confirmation`
--
ALTER TABLE `event_locale_confirmation`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_locale_confirmation_user`
--
ALTER TABLE `event_locale_confirmation_user`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_locale_prize`
--
ALTER TABLE `event_locale_prize`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_locale_prize_log`
--
ALTER TABLE `event_locale_prize_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_locale_prize_user`
--
ALTER TABLE `event_locale_prize_user`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_locale_psq`
--
ALTER TABLE `event_locale_psq`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_locale_psq_log`
--
ALTER TABLE `event_locale_psq_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_locale_psq_option`
--
ALTER TABLE `event_locale_psq_option`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `event_locale_psq_user`
--
ALTER TABLE `event_locale_psq_user`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_locale_question`
--
ALTER TABLE `event_locale_question`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_locale_question_setting`
--
ALTER TABLE `event_locale_question_setting`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_locale_review`
--
ALTER TABLE `event_locale_review`
  ADD PRIMARY KEY (`id`) USING BTREE,
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_locale_review_item`
--
ALTER TABLE `event_locale_review_item`
  ADD PRIMARY KEY (`id`) USING BTREE,
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_locale_review_judges`
--
ALTER TABLE `event_locale_review_judges`
  ADD PRIMARY KEY (`id`) USING BTREE,
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_locale_review_rule`
--
ALTER TABLE `event_locale_review_rule`
  ADD PRIMARY KEY (`id`) USING BTREE,
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_locale_review_score`
--
ALTER TABLE `event_locale_review_score`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- 表的索引 `event_locale_screen_process`
--
ALTER TABLE `event_locale_screen_process`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_locale_screen_setting`
--
ALTER TABLE `event_locale_screen_setting`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_locale_signin`
--
ALTER TABLE `event_locale_signin`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_locale_signin_statistics`
--
ALTER TABLE `event_locale_signin_statistics`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_locale_signin_user`
--
ALTER TABLE `event_locale_signin_user`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_locale_vote`
--
ALTER TABLE `event_locale_vote`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_locale_vote_item`
--
ALTER TABLE `event_locale_vote_item`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_locale_vote_log`
--
ALTER TABLE `event_locale_vote_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_member_fee`
--
ALTER TABLE `event_member_fee`
  ADD PRIMARY KEY (`id`) USING BTREE,
  ADD KEY `event_id` (`event_id`);

--
-- 表的索引 `event_refund_log`
--
ALTER TABLE `event_refund_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_setting`
--
ALTER TABLE `event_setting`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_settle_apply`
--
ALTER TABLE `event_settle_apply`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `event_signed`
--
ALTER TABLE `event_signed`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`,`event_id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_signed_edit_log`
--
ALTER TABLE `event_signed_edit_log`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `event_signed_fee`
--
ALTER TABLE `event_signed_fee`
  ADD PRIMARY KEY (`id`),
  ADD KEY `signed_id` (`signed_id`);

--
-- 表的索引 `event_signed_group`
--
ALTER TABLE `event_signed_group`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_signed_group_user`
--
ALTER TABLE `event_signed_group_user`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `event_signed_order`
--
ALTER TABLE `event_signed_order`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`);

--
-- 表的索引 `event_sms_order`
--
ALTER TABLE `event_sms_order`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_sms_result`
--
ALTER TABLE `event_sms_result`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_spread_channel`
--
ALTER TABLE `event_spread_channel`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_spread_channel_admin`
--
ALTER TABLE `event_spread_channel_admin`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_spread_channel_detail`
--
ALTER TABLE `event_spread_channel_detail`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_spread_user_record`
--
ALTER TABLE `event_spread_user_record`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_spread_user_record_detail`
--
ALTER TABLE `event_spread_user_record_detail`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_spread_user_rule`
--
ALTER TABLE `event_spread_user_rule`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_spread_user_setting`
--
ALTER TABLE `event_spread_user_setting`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_withdraw_log`
--
ALTER TABLE `event_withdraw_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`) USING BTREE;

--
-- 表的索引 `event_wxbalance`
--
ALTER TABLE `event_wxbalance`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `event_id` (`event_id`);

--
-- 表的索引 `export_token`
--
ALTER TABLE `export_token`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `fields`
--
ALTER TABLE `fields`
  ADD PRIMARY KEY (`id`),
  ADD KEY `team_id` (`team_id`);

--
-- 表的索引 `help`
--
ALTER TABLE `help`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `member_order_settle_log`
--
ALTER TABLE `member_order_settle_log`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `member_refund_log`
--
ALTER TABLE `member_refund_log`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `message`
--
ALTER TABLE `message`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `message_config`
--
ALTER TABLE `message_config`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `order_settle_log`
--
ALTER TABLE `order_settle_log`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `oss_black_user`
--
ALTER TABLE `oss_black_user`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- 表的索引 `recommend_position`
--
ALTER TABLE `recommend_position`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `recommend_position_ref`
--
ALTER TABLE `recommend_position_ref`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `settle_receivers`
--
ALTER TABLE `settle_receivers`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `statistics`
--
ALTER TABLE `statistics`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `sub_mch_apply`
--
ALTER TABLE `sub_mch_apply`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `sub_mch_file`
--
ALTER TABLE `sub_mch_file`
  ADD PRIMARY KEY (`id`),
  ADD KEY `media_idx` (`media_id`) USING BTREE;

--
-- 表的索引 `team`
--
ALTER TABLE `team`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- 表的索引 `team_admin`
--
ALTER TABLE `team_admin`
  ADD PRIMARY KEY (`id`),
  ADD KEY `team_id` (`team_id`,`user_id`);

--
-- 表的索引 `team_album`
--
ALTER TABLE `team_album`
  ADD PRIMARY KEY (`id`),
  ADD KEY `team_id` (`team_id`) USING BTREE;

--
-- 表的索引 `team_album_photo`
--
ALTER TABLE `team_album_photo`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `team_assign_log`
--
ALTER TABLE `team_assign_log`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `team_black_user`
--
ALTER TABLE `team_black_user`
  ADD PRIMARY KEY (`id`),
  ADD KEY `team_id` (`team_id`) USING BTREE;

--
-- 表的索引 `team_event_point`
--
ALTER TABLE `team_event_point`
  ADD PRIMARY KEY (`id`) USING BTREE,
  ADD KEY `team_id` (`team_id`) USING BTREE;

--
-- 表的索引 `team_fee`
--
ALTER TABLE `team_fee`
  ADD PRIMARY KEY (`id`) USING BTREE,
  ADD KEY `team_id` (`team_id`) USING BTREE;

--
-- 表的索引 `team_member`
--
ALTER TABLE `team_member`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- 表的索引 `team_member_level`
--
ALTER TABLE `team_member_level`
  ADD PRIMARY KEY (`id`) USING BTREE,
  ADD KEY `team_id` (`team_id`) USING BTREE;

--
-- 表的索引 `team_member_log`
--
ALTER TABLE `team_member_log`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- 表的索引 `team_member_order`
--
ALTER TABLE `team_member_order`
  ADD PRIMARY KEY (`id`) USING BTREE,
  ADD KEY `team_id` (`team_id`) USING BTREE;

--
-- 表的索引 `team_message_config`
--
ALTER TABLE `team_message_config`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `team_withdraw_log`
--
ALTER TABLE `team_withdraw_log`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- 表的索引 `team_wxbalance`
--
ALTER TABLE `team_wxbalance`
  ADD PRIMARY KEY (`id`) USING BTREE,
  ADD UNIQUE KEY `event_id` (`team_id`) USING BTREE;

--
-- 表的索引 `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unionid` (`unionid`),
  ADD UNIQUE KEY `unionid_2` (`unionid`),
  ADD KEY `idx_openid_xchx` (`openid_xchx`);

--
-- 表的索引 `user_copy_data_log`
--
ALTER TABLE `user_copy_data_log`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `user_follow`
--
ALTER TABLE `user_follow`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `wxacode_scene`
--
ALTER TABLE `wxacode_scene`
  ADD PRIMARY KEY (`id`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `advertising`
--
ALTER TABLE `advertising`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `ad_channel`
--
ALTER TABLE `ad_channel`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `change_settle_blank`
--
ALTER TABLE `change_settle_blank`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `channel_log`
--
ALTER TABLE `channel_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `comm_file`
--
ALTER TABLE `comm_file`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `config`
--
ALTER TABLE `config`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `district_tx`
--
ALTER TABLE `district_tx`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_fee`
--
ALTER TABLE `event_fee`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_locale_confirmation`
--
ALTER TABLE `event_locale_confirmation`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_locale_confirmation_user`
--
ALTER TABLE `event_locale_confirmation_user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_locale_prize`
--
ALTER TABLE `event_locale_prize`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_locale_prize_log`
--
ALTER TABLE `event_locale_prize_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_locale_prize_user`
--
ALTER TABLE `event_locale_prize_user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_locale_psq`
--
ALTER TABLE `event_locale_psq`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_locale_psq_log`
--
ALTER TABLE `event_locale_psq_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_locale_psq_option`
--
ALTER TABLE `event_locale_psq_option`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_locale_psq_user`
--
ALTER TABLE `event_locale_psq_user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_locale_question`
--
ALTER TABLE `event_locale_question`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_locale_question_setting`
--
ALTER TABLE `event_locale_question_setting`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_locale_review`
--
ALTER TABLE `event_locale_review`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_locale_review_item`
--
ALTER TABLE `event_locale_review_item`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_locale_review_judges`
--
ALTER TABLE `event_locale_review_judges`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_locale_review_rule`
--
ALTER TABLE `event_locale_review_rule`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_locale_review_score`
--
ALTER TABLE `event_locale_review_score`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_locale_screen_process`
--
ALTER TABLE `event_locale_screen_process`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_locale_screen_setting`
--
ALTER TABLE `event_locale_screen_setting`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_locale_signin`
--
ALTER TABLE `event_locale_signin`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_locale_signin_statistics`
--
ALTER TABLE `event_locale_signin_statistics`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_locale_signin_user`
--
ALTER TABLE `event_locale_signin_user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_locale_vote`
--
ALTER TABLE `event_locale_vote`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_locale_vote_item`
--
ALTER TABLE `event_locale_vote_item`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_locale_vote_log`
--
ALTER TABLE `event_locale_vote_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_member_fee`
--
ALTER TABLE `event_member_fee`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_refund_log`
--
ALTER TABLE `event_refund_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_setting`
--
ALTER TABLE `event_setting`
  MODIFY `Id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_settle_apply`
--
ALTER TABLE `event_settle_apply`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_signed`
--
ALTER TABLE `event_signed`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_signed_edit_log`
--
ALTER TABLE `event_signed_edit_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_signed_fee`
--
ALTER TABLE `event_signed_fee`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `event_signed_group`
--
ALTER TABLE `event_signed_group`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_signed_group_user`
--
ALTER TABLE `event_signed_group_user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_signed_order`
--
ALTER TABLE `event_signed_order`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `event_sms_order`
--
ALTER TABLE `event_sms_order`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_sms_result`
--
ALTER TABLE `event_sms_result`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_spread_channel`
--
ALTER TABLE `event_spread_channel`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_spread_channel_admin`
--
ALTER TABLE `event_spread_channel_admin`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_spread_channel_detail`
--
ALTER TABLE `event_spread_channel_detail`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_spread_user_record`
--
ALTER TABLE `event_spread_user_record`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_spread_user_record_detail`
--
ALTER TABLE `event_spread_user_record_detail`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_spread_user_rule`
--
ALTER TABLE `event_spread_user_rule`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_spread_user_setting`
--
ALTER TABLE `event_spread_user_setting`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_withdraw_log`
--
ALTER TABLE `event_withdraw_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `event_wxbalance`
--
ALTER TABLE `event_wxbalance`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `export_token`
--
ALTER TABLE `export_token`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `feedback`
--
ALTER TABLE `feedback`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `fields`
--
ALTER TABLE `fields`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `help`
--
ALTER TABLE `help`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `member_order_settle_log`
--
ALTER TABLE `member_order_settle_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `member_refund_log`
--
ALTER TABLE `member_refund_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `message`
--
ALTER TABLE `message`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `message_config`
--
ALTER TABLE `message_config`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `order_settle_log`
--
ALTER TABLE `order_settle_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `oss_black_user`
--
ALTER TABLE `oss_black_user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `recommend_position`
--
ALTER TABLE `recommend_position`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `recommend_position_ref`
--
ALTER TABLE `recommend_position_ref`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `settle_receivers`
--
ALTER TABLE `settle_receivers`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `statistics`
--
ALTER TABLE `statistics`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `sub_mch_apply`
--
ALTER TABLE `sub_mch_apply`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `sub_mch_file`
--
ALTER TABLE `sub_mch_file`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `team_admin`
--
ALTER TABLE `team_admin`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `team_album`
--
ALTER TABLE `team_album`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `team_album_photo`
--
ALTER TABLE `team_album_photo`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `team_assign_log`
--
ALTER TABLE `team_assign_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `team_black_user`
--
ALTER TABLE `team_black_user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `team_event_point`
--
ALTER TABLE `team_event_point`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `team_fee`
--
ALTER TABLE `team_fee`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `team_member`
--
ALTER TABLE `team_member`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `team_member_level`
--
ALTER TABLE `team_member_level`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `team_member_log`
--
ALTER TABLE `team_member_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `team_member_order`
--
ALTER TABLE `team_member_order`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `team_message_config`
--
ALTER TABLE `team_message_config`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `team_withdraw_log`
--
ALTER TABLE `team_withdraw_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `team_wxbalance`
--
ALTER TABLE `team_wxbalance`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `user`
--
ALTER TABLE `user`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `user_copy_data_log`
--
ALTER TABLE `user_copy_data_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';

--
-- 使用表AUTO_INCREMENT `user_follow`
--
ALTER TABLE `user_follow`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID';
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
