-- 创建数据库
CREATE DATABASE ruoyi_fastapi;

-- 连接到新数据库
\c ruoyi_fastapi

-- 执行初始化脚本
\i /tmp/ruoyi-fastapi-pg.sql
