-- 删除旧的设备管理菜单
delete from sys_role_menu where menu_id >= 2000 and menu_id <= 2010;
delete from sys_menu where menu_id >= 2000 and menu_id <= 2010;

-- 设备管理一级菜单
insert into sys_menu values(2000, '设备管理', 0, '5', 'device', null, '', '', 1, 0, 'M', '0', '0', '', 'device', 'admin', current_timestamp, '', null, '设备管理目录');

-- 设备型号二级菜单 (路由地址使用 deviceModel 避免与其他模块冲突)
insert into sys_menu values(2001, '设备型号', 2000, '1', 'deviceModel', 'device/views/index', '', '', 1, 0, 'C', '0', '0', 'device:model:list', 'component', 'admin', current_timestamp, '', null, '设备型号菜单');

-- 设备型号按钮权限
insert into sys_menu values(2002, '设备型号查询', 2001, '1', '', '', '', '', 1, 0, 'F', '0', '0', 'device:model:query', '#', 'admin', current_timestamp, '', null, '');
insert into sys_menu values(2003, '设备型号新增', 2001, '2', '', '', '', '', 1, 0, 'F', '0', '0', 'device:model:add', '#', 'admin', current_timestamp, '', null, '');
insert into sys_menu values(2004, '设备型号修改', 2001, '3', '', '', '', '', 1, 0, 'F', '0', '0', 'device:model:edit', '#', 'admin', current_timestamp, '', null, '');
insert into sys_menu values(2005, '设备型号删除', 2001, '4', '', '', '', '', 1, 0, 'F', '0', '0', 'device:model:remove', '#', 'admin', current_timestamp, '', null, '');

-- 设备分组二级菜单 (路由地址使用 deviceGroup 避免与其他模块冲突)
insert into sys_menu values(2006, '设备分组', 2000, '2', 'deviceGroup', 'device/views/group/index', '', '', 1, 0, 'C', '0', '0', 'device:group:list', 'tree', 'admin', current_timestamp, '', null, '设备分组菜单');

-- 设备分组按钮权限
insert into sys_menu values(2007, '设备分组查询', 2006, '1', '', '', '', '', 1, 0, 'F', '0', '0', 'device:group:query', '#', 'admin', current_timestamp, '', null, '');
insert into sys_menu values(2008, '设备分组新增', 2006, '2', '', '', '', '', 1, 0, 'F', '0', '0', 'device:group:add', '#', 'admin', current_timestamp, '', null, '');
insert into sys_menu values(2009, '设备分组修改', 2006, '3', '', '', '', '', 1, 0, 'F', '0', '0', 'device:group:edit', '#', 'admin', current_timestamp, '', null, '');
insert into sys_menu values(2010, '设备分组删除', 2006, '4', '', '', '', '', 1, 0, 'F', '0', '0', 'device:group:remove', '#', 'admin', current_timestamp, '', null, '');

-- 为管理员角色分配设备管理菜单权限
insert into sys_role_menu values(1, 2000);
insert into sys_role_menu values(1, 2001);
insert into sys_role_menu values(1, 2002);
insert into sys_role_menu values(1, 2003);
insert into sys_role_menu values(1, 2004);
insert into sys_role_menu values(1, 2005);
insert into sys_role_menu values(1, 2006);
insert into sys_role_menu values(1, 2007);
insert into sys_role_menu values(1, 2008);
insert into sys_role_menu values(1, 2009);
insert into sys_role_menu values(1, 2010);
