@echo off
echo 创建数据库...
docker exec -it device_postgres psql -U device_user -d postgres -c "CREATE DATABASE ruoyi_fastapi;"

echo 初始化数据库表...
docker exec -it device_postgres psql -U device_user -d ruoyi_fastapi -f /tmp/ruoyi-fastapi-pg.sql

echo 完成！
pause
