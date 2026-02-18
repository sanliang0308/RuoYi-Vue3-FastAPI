from datetime import datetime

from sqlalchemy import CHAR, BigInteger, Column, DateTime, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship

from config.database import Base
from config.env import DataBaseConfig
from utils.common_util import SqlalchemyUtil


class SysDeviceDO(Base):
    """
    设备表
    """

    __tablename__ = 'sys_device'
    __table_args__ = {'comment': '设备表', 'extend_existing': True}

    device_id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True, comment='设备ID')
    device_name = Column(String(64), nullable=False, comment='设备名称')
    device_code = Column(String(64), nullable=False, comment='设备编码')
    device_type = Column(String(32), nullable=False, comment='设备类型')
    device_model = Column(String(64), nullable=False, comment='设备型号')
    status = Column(CHAR(1), nullable=False, server_default='0', comment='设备状态(0正常 1离线 2故障)')
    ip_address = Column(String(128), nullable=True, server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type), comment='IP地址')
    mac_address = Column(String(64), nullable=True, server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type), comment='MAC地址')
    location = Column(String(255), nullable=True, server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type), comment='设备位置')
    manufacturer = Column(String(128), nullable=True, server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type), comment='制造商')
    supplier = Column(String(128), nullable=True, server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type), comment='供应商')
    purchase_date = Column(Date, nullable=True, comment='购买日期')
    warranty_end_date = Column(Date, nullable=True, comment='保修截止日期')
    department_id = Column(BigInteger, ForeignKey('sys_dept.dept_id'), nullable=True, server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type, False), comment='所属部门ID')
    user_id = Column(BigInteger, ForeignKey('sys_user.user_id'), nullable=True, server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type, False), comment='负责人ID')
    remark = Column(String(500), nullable=True, server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type), comment='备注')
    create_by = Column(String(64), nullable=False, server_default="''", comment='创建者')
    create_time = Column(DateTime, nullable=False, comment='创建时间', default=datetime.now)
    update_by = Column(String(64), nullable=False, server_default="''", comment='更新者')
    update_time = Column(DateTime, nullable=True, comment='更新时间')
    del_flag = Column(CHAR(1), nullable=False, server_default='0', comment='删除标志(0存在 2删除)')

    department = relationship("SysDept", foreign_keys=[department_id], lazy='select')
    user = relationship("SysUser", foreign_keys=[user_id], lazy='select')


class SysDeviceGroupDO(Base):
    """
    设备分组表
    """

    __tablename__ = 'sys_device_group'
    __table_args__ = {'comment': '设备分组表', 'extend_existing': True}

    group_id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True, comment='分组ID')
    group_name = Column(String(64), nullable=False, comment='分组名称')
    parent_id = Column(BigInteger, nullable=False, server_default='0', comment='父分组ID')
    order_num = Column(Integer, nullable=False, server_default='0', comment='显示顺序')
    status = Column(CHAR(1), nullable=False, server_default='0', comment='状态(0正常 1停用)')
    remark = Column(String(500), nullable=True, server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type), comment='备注')
    create_by = Column(String(64), nullable=False, server_default="''", comment='创建者')
    create_time = Column(DateTime, nullable=False, comment='创建时间', default=datetime.now)
    update_by = Column(String(64), nullable=False, server_default="''", comment='更新者')
    update_time = Column(DateTime, nullable=True, comment='更新时间')
    del_flag = Column(CHAR(1), nullable=False, server_default='0', comment='删除标志(0存在 2删除)')


class SysDeviceGroupRelDO(Base):
    """
    设备分组关联表
    """

    __tablename__ = 'sys_device_group_rel'
    __table_args__ = {'comment': '设备分组关联表', 'extend_existing': True}

    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True, comment='主键ID')
    device_id = Column(BigInteger, ForeignKey('sys_device.device_id'), nullable=False, comment='设备ID')
    group_id = Column(BigInteger, ForeignKey('sys_device_group.group_id'), nullable=False, comment='分组ID')
