from collections.abc import Sequence
from datetime import datetime
from typing import Any

from sqlalchemy import ColumnElement, and_, delete, desc, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from common.vo import PageModel
from module_admin.entity.do.dept_do import SysDept
from module_admin.entity.do.user_do import SysUser
from module_device.entity.do.device_do import SysDeviceDO, SysDeviceGroupDO, SysDeviceGroupRelDO
from module_device.entity.vo.device_vo import (
    DeviceModel,
    DeviceQueryModel,
    DeviceAddModel,
    DeviceEditModel,
    DeviceGroupModel,
    DeviceGroupAddModel,
    DeviceGroupEditModel,
    DeviceGroupTreeModel,
    DeviceGroupRelModel,
)
from utils.page_util import PageUtil


class DeviceDao:
    """
    设备管理模块数据库操作层
    """

    @classmethod
    async def get_device_list_by_page(
        cls, db: AsyncSession, query_object: DeviceQueryModel, data_scope_sql: ColumnElement = None, is_page: bool = True
    ) -> PageModel | list[dict[str, Any]]:
        """
        根据查询参数获取设备列表

        :param db: orm对象
        :param query_object: 查询参数对象
        :param data_scope_sql: 数据权限对应的查询sql语句
        :param is_page: 是否开启分页
        :return: 设备分页列表
        """
        query = (
            select(SysDeviceDO)
            .where(
                SysDeviceDO.del_flag == '0',
                SysDeviceDO.device_name.like(f'%{query_object.device_name}%') if query_object.device_name else True,
                SysDeviceDO.device_code.like(f'%{query_object.device_code}%') if query_object.device_code else True,
                SysDeviceDO.device_type == query_object.device_type if query_object.device_type else True,
                SysDeviceDO.status == query_object.status if query_object.status else True,
                SysDeviceDO.department_id == query_object.department_id if query_object.department_id else True,
                data_scope_sql if data_scope_sql is not None else True,
            )
            .order_by(desc(SysDeviceDO.create_time))
        )

        device_list: PageModel | list[dict[str, Any]] = await PageUtil.paginate(
            db, query, query_object.page_num, query_object.page_size, is_page
        )

        return device_list

    @classmethod
    async def get_device_by_id(cls, db: AsyncSession, device_id: int) -> dict[str, Any] | None:
        """
        根据设备ID获取设备信息

        :param db: orm对象
        :param device_id: 设备ID
        :return: 设备信息对象
        """
        query = (
            select(SysDeviceDO)
            .where(SysDeviceDO.device_id == device_id, SysDeviceDO.del_flag == '0')
            .options(selectinload(SysDeviceDO.department), selectinload(SysDeviceDO.user))
        )

        device = (await db.execute(query)).scalars().first()

        if device:
            device_dict = {
                'device_id': device.device_id,
                'device_name': device.device_name,
                'device_code': device.device_code,
                'device_type': device.device_type,
                'device_model': device.device_model,
                'status': device.status,
                'ip_address': device.ip_address,
                'mac_address': device.mac_address,
                'location': device.location,
                'manufacturer': device.manufacturer,
                'supplier': device.supplier,
                'purchase_date': device.purchase_date,
                'warranty_end_date': device.warranty_end_date,
                'department_id': device.department_id,
                'department_name': device.department.dept_name if device.department else None,
                'user_id': device.user_id,
                'user_name': device.user.user_name if device.user else None,
                'remark': device.remark,
                'create_by': device.create_by,
                'create_time': device.create_time,
                'update_by': device.update_by,
                'update_time': device.update_time,
            }
            return device_dict

        return None

    @classmethod
    async def get_device_by_code(cls, db: AsyncSession, device_code: str) -> SysDeviceDO | None:
        """
        根据设备编码获取设备信息

        :param db: orm对象
        :param device_code: 设备编码
        :return: 设备信息对象
        """
        query = select(SysDeviceDO).where(
            SysDeviceDO.device_code == device_code, SysDeviceDO.del_flag == '0'
        )
        device = (await db.execute(query)).scalars().first()
        return device

    @classmethod
    async def add_device(cls, db: AsyncSession, device: SysDeviceDO) -> SysDeviceDO:
        """
        新增设备

        :param db: orm对象
        :param device: 设备对象
        :return: 新增后的设备对象
        """
        db.add(device)
        await db.flush()
        return device

    @classmethod
    async def edit_device(cls, db: AsyncSession, device: SysDeviceDO) -> SysDeviceDO:
        """
        编辑设备

        :param db: orm对象
        :param device: 设备对象
        :return: 编辑后的设备对象
        """
        await db.flush()
        return device

    @classmethod
    async def delete_device(cls, db: AsyncSession, device_id: int) -> int:
        """
        删除设备

        :param db: orm对象
        :param device_id: 设备ID
        :return: 删除结果
        """
        query = (
            update(SysDeviceDO)
            .where(SysDeviceDO.device_id == device_id, SysDeviceDO.del_flag == '0')
            .values(del_flag='2', update_time=datetime.now())
        )
        result = await db.execute(query)
        return result.rowcount

    @classmethod
    async def update_device_status(
        cls, db: AsyncSession, device_id: int, status: str
    ) -> int:
        """
        更新设备状态

        :param db: orm对象
        :param device_id: 设备ID
        :param status: 设备状态
        :return: 更新结果
        """
        query = (
            update(SysDeviceDO)
            .where(SysDeviceDO.device_id == device_id, SysDeviceDO.del_flag == '0')
            .values(status=status, update_time=datetime.now())
        )
        result = await db.execute(query)
        return result.rowcount


class DeviceGroupDao:
    """
    设备分组管理模块数据库操作层
    """

    @classmethod
    async def get_device_group_list(
        cls, db: AsyncSession, group_name: str | None, status: str | None
    ) -> Sequence[SysDeviceGroupDO]:
        """
        获取设备分组列表

        :param db: orm对象
        :param group_name: 分组名称
        :param status: 状态
        :return: 设备分组列表
        """
        query = (
            select(SysDeviceGroupDO)
            .where(SysDeviceGroupDO.del_flag == '0')
            .order_by(SysDeviceGroupDO.order_num)
        )

        if group_name:
            query = query.where(SysDeviceGroupDO.group_name.like(f'%{group_name}%'))
        if status:
            query = query.where(SysDeviceGroupDO.status == status)

        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_device_group_by_id(
        cls, db: AsyncSession, group_id: int
    ) -> SysDeviceGroupDO | None:
        """
        根据分组ID获取分组信息

        :param db: orm对象
        :param group_id: 分组ID
        :return: 分组信息对象
        """
        query = select(SysDeviceGroupDO).where(
            SysDeviceGroupDO.group_id == group_id, SysDeviceGroupDO.del_flag == '0'
        )
        group = (await db.execute(query)).scalars().first()
        return group

    @classmethod
    async def get_device_group_by_name(
        cls, db: AsyncSession, group_name: str, parent_id: int
    ) -> SysDeviceGroupDO | None:
        """
        根据分组名称和父ID获取分组信息

        :param db: orm对象
        :param group_name: 分组名称
        :param parent_id: 父分组ID
        :return: 分组信息对象
        """
        query = select(SysDeviceGroupDO).where(
            SysDeviceGroupDO.group_name == group_name,
            SysDeviceGroupDO.parent_id == parent_id,
            SysDeviceGroupDO.del_flag == '0',
        )
        group = (await db.execute(query)).scalars().first()
        return group

    @classmethod
    async def add_device_group(
        cls, db: AsyncSession, group: SysDeviceGroupDO
    ) -> SysDeviceGroupDO:
        """
        新增设备分组

        :param db: orm对象
        :param group: 设备分组对象
        :return: 新增后的设备分组对象
        """
        db.add(group)
        await db.flush()
        return group

    @classmethod
    async def edit_device_group(
        cls, db: AsyncSession, group: SysDeviceGroupDO
    ) -> SysDeviceGroupDO:
        """
        编辑设备分组

        :param db: orm对象
        :param group: 设备分组对象
        :return: 编辑后的设备分组对象
        """
        await db.flush()
        return group

    @classmethod
    async def delete_device_group(cls, db: AsyncSession, group_id: int) -> int:
        """
        删除设备分组

        :param db: orm对象
        :param group_id: 分组ID
        :return: 删除结果
        """
        query = (
            update(SysDeviceGroupDO)
            .where(SysDeviceGroupDO.group_id == group_id, SysDeviceGroupDO.del_flag == '0')
            .values(del_flag='2', update_time=datetime.now())
        )
        result = await db.execute(query)
        return result.rowcount

    @classmethod
    async def get_group_device_list(
        cls, db: AsyncSession, group_id: int
    ) -> Sequence[SysDeviceDO]:
        """
        获取分组下的设备列表

        :param db: orm对象
        :param group_id: 分组ID
        :return: 设备列表
        """
        query = (
            select(SysDeviceDO)
            .join(SysDeviceGroupRelDO, SysDeviceDO.device_id == SysDeviceGroupRelDO.device_id)
            .where(
                SysDeviceGroupRelDO.group_id == group_id, SysDeviceDO.del_flag == '0'
            )
            .options(selectinload(SysDeviceDO.department), selectinload(SysDeviceDO.user))
        )
        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def add_group_device(
        cls, db: AsyncSession, group_id: int, device_ids: list[int]
    ) -> None:
        """
        向分组添加设备

        :param db: orm对象
        :param group_id: 分组ID
        :param device_ids: 设备ID列表
        """
        for device_id in device_ids:
            rel = SysDeviceGroupRelDO(device_id=device_id, group_id=group_id)
            db.add(rel)
        await db.flush()

    @classmethod
    async def remove_group_device(
        cls, db: AsyncSession, group_id: int, device_ids: list[int]
    ) -> int:
        """
        从分组移除设备

        :param db: orm对象
        :param group_id: 分组ID
        :param device_ids: 设备ID列表
        :return: 移除结果
        """
        query = delete(SysDeviceGroupRelDO).where(
            SysDeviceGroupRelDO.group_id == group_id,
            SysDeviceGroupRelDO.device_id.in_(device_ids),
        )
        result = await db.execute(query)
        return result.rowcount
