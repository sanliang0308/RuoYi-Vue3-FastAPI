-- ============================================
-- 设备管理模块 SQL脚本（RuoYi标准）
-- ============================================

-- ----------------------------
-- 设备表
-- ----------------------------
DROP TABLE IF EXISTS sys_device;
CREATE TABLE sys_device (
    device_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    device_name VARCHAR(64) NOT NULL COMMENT '设备名称',
    device_code VARCHAR(64) NOT NULL COMMENT '设备编码',
    device_type VARCHAR(32) NOT NULL COMMENT '设备类型',
    device_model VARCHAR(64) NOT NULL COMMENT '设备型号',
    status CHAR(1) NOT NULL DEFAULT '0' COMMENT '设备状态(0正常 1停用)',
    ip_address VARCHAR(128) DEFAULT NULL COMMENT 'IP地址',
    mac_address VARCHAR(64) DEFAULT NULL COMMENT 'MAC地址',
    location VARCHAR(255) DEFAULT NULL COMMENT '设备位置',
    manufacturer VARCHAR(128) DEFAULT NULL COMMENT '制造商',
    supplier VARCHAR(128) DEFAULT NULL COMMENT '供应商',
    purchase_date DATE DEFAULT NULL COMMENT '购买日期',
    warranty_end_date DATE DEFAULT NULL COMMENT '保修截止日期',
    department_id BIGINT DEFAULT NULL COMMENT '所属部门ID',
    user_id BIGINT DEFAULT NULL COMMENT '负责人ID',
    remark VARCHAR(500) DEFAULT NULL COMMENT '备注',
    create_by VARCHAR(64) NOT NULL DEFAULT '' COMMENT '创建者',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_by VARCHAR(64) NOT NULL DEFAULT '' COMMENT '更新者',
    update_time DATETIME DEFAULT NULL COMMENT '更新时间',
    del_flag CHAR(1) NOT NULL DEFAULT '0' COMMENT '删除标志(0存在 2删除)'
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='设备表';

-- 索引
CREATE INDEX idx_device_code ON sys_device(device_code) USING BTREE;
CREATE INDEX idx_device_name ON sys_device(device_name) USING BTREE;
CREATE INDEX idx_device_type ON sys_device(device_type) USING BTREE;
CREATE INDEX idx_device_status ON sys_device(status) USING BTREE;
CREATE UNIQUE INDEX idx_device_code_unique ON sys_device(device_code) WHERE del_flag = '0';

-- ----------------------------
-- 初始化设备数据
-- ----------------------------
INSERT INTO sys_device (device_id, device_name, device_code, device_type, device_model, status, ip_address, mac_address, location, manufacturer, supplier, purchase_date, warranty_end_date, department_id, user_id, remark, create_by, create_time, del_flag)
VALUES
(1, '核心交换机', 'SW-001', '交换机', 'H3C S5500', '0', '192.168.1.1', '00:0C:29:XX:XX:01', '机房A区', 'H3C', '华三通信', '2024-01-15', '2027-01-15', 103, 1, '核心网络设备', 'admin', NOW(), '0'),
(2, '应用服务器', 'SRV-001', '服务器', 'Dell R740', '0', '192.168.1.10', '00:0C:29:XX:XX:02', '机房B区', 'Dell', '戴尔科技', '2024-02-20', '2027-02-20', 103, 2, '应用服务器', 'admin', NOW(), '0'),
(3, '数据库服务器', 'SRV-002', '服务器', 'HP DL380', '0', '192.168.1.11', '00:0C:29:XX:XX:03', '机房B区', 'HP', '惠普科技', '2024-03-10', '2027-03-10', 103, 3, '数据库服务器', 'admin', NOW(), '0');

-- ----------------------------
-- 设备管理菜单SQL
-- ----------------------------
-- 设备管理父菜单
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, menu_type, perms, icon, is_frame, is_cache, visible, status, create_time, create_by)
VALUES ('设备管理', 0, 6, 'device', NULL, 'M', NULL, 'device', 1, 0, '0', '0', NOW(), 'admin');

-- 获取刚插入的父菜单ID
SET @deviceParentId = LAST_INSERT_ID();

-- 设备列表子菜单
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, menu_type, perms, icon, is_frame, is_cache, visible, status, create_time, create_by)
VALUES ('设备列表', @deviceParentId, 1, 'index', 'device/index', 'C', 'device:device:list', 'list', 1, 0, '0', '0', NOW(), 'admin');

-- 按钮权限
INSERT INTO sys_menu (menu_name, parent_id, order_num, menu_type, perms, visible, status, create_time, create_by)
SELECT '设备查询', menu_id, 1, 'F', 'device:device:query', '0', '0', NOW(), 'admin'
FROM sys_menu WHERE menu_name = '设备列表' LIMIT 1;

INSERT INTO sys_menu (menu_name, parent_id, order_num, menu_type, perms, visible, status, create_time, create_by)
SELECT '设备新增', menu_id, 2, 'F', 'device:device:add', '0', '0', NOW(), 'admin'
FROM sys_menu WHERE menu_name = '设备列表' LIMIT 1;

INSERT INTO sys_menu (menu_name, parent_id, order_num, menu_type, perms, visible, status, create_time, create_by)
SELECT '设备修改', menu_id, 3, 'F', 'device:device:edit', '0', '0', NOW(), 'admin'
FROM sys_menu WHERE menu_name = '设备列表' LIMIT 1;

INSERT INTO sys_menu (menu_name, parent_id, order_num, menu_type, perms, visible, status, create_time, create_by)
SELECT '设备删除', menu_id, 4, 'F', 'device:device:remove', '0', '0', NOW(), 'admin'
FROM sys_menu WHERE menu_name = '设备列表' LIMIT 1;

INSERT INTO sys_menu (menu_name, parent_id, order_num, menu_type, perms, visible, status, create_time, create_by)
SELECT '设备导出', menu_id, 5, 'F', 'device:device:export', '0', '0', NOW(), 'admin'
FROM sys_menu WHERE menu_name = '设备列表' LIMIT 1;
