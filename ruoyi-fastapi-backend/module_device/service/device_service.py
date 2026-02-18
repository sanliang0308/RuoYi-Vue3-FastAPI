from datetime import datetime
from typing import Any

from sqlalchemy import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import CrudResponseModel, PageModel
from exceptions.exception import ServiceException
from module_device.dao.device_dao import DeviceDao, DeviceGroupDao
from module_device.entity.do.device_do import SysDeviceDO, SysDeviceGroupDO
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


class DeviceService:
    """
    设备管理模块服务层
    """

    @classmethod
    async def get_device_list_services(
        cls,
        query_db: AsyncSession,
        query_object: DeviceQueryModel,
        data_scope_sql: ColumnElement = None,
        is_page: bool = True,
    ) -> PageModel | list[dict[str, Any]]:
        """
        获取设备列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param data_scope_sql: 数据权限对应的查询sql语句
        :param is_page: 是否开启分页
        :return: 设备列表信息对象
        """
        query_result = await DeviceDao.get_device_list_by_page(query_db, query_object, data_scope_sql, is_page)
        return query_result

    @classmethod
    async def get_device_by_id_services(
        cls, query_db: AsyncSession, device_id: int
    ) -> dict[str, Any]:
        """
        根据设备ID获取设备信息service

        :param query_db: orm对象
        :param device_id: 设备ID
        :return: 设备信息对象
        """
        device = await DeviceDao.get_device_by_id(query_db, device_id)
        if not device:
            raise ServiceException(message='设备不存在')
        return device

    @classmethod
    async def add_device_services(
        cls, query_db: AsyncSession, page_object: DeviceAddModel
    ) -> CrudResponseModel:
        """
        新增设备信息service

        :param query_db: orm对象
        :param page_object: 新增设备对象
        :return: 新增设备结果
        """
        device = await DeviceDao.get_device_by_code(query_db, page_object.device_code)
        if device:
            raise ServiceException(message='设备编码已存在')
        try:
            device = SysDeviceDO(
                device_name=page_object.device_name,
                device_code=page_object.device_code,
                device_type=page_object.device_type,
                device_model=page_object.device_model,
                status=page_object.status,
                ip_address=page_object.ip_address,
                mac_address=page_object.mac_address,
                location=page_object.location,
                manufacturer=page_object.manufacturer,
                supplier=page_object.supplier,
                purchase_date=page_object.purchase_date,
                warranty_end_date=page_object.warranty_end_date,
                department_id=page_object.department_id,
                user_id=page_object.user_id,
                remark=page_object.remark,
                create_by='',
                create_time=datetime.now(),
                update_by='',
                del_flag='0',
            )
            await DeviceDao.add_device(query_db, device)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增设备成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_device_services(
        cls, query_db: AsyncSession, page_object: DeviceEditModel
    ) -> CrudResponseModel:
        """
        编辑设备信息service

        :param query_db: orm对象
        :param page_object: 编辑设备对象
        :return: 编辑设备结果
        """
        device_dict = await DeviceDao.get_device_by_id(query_db, page_object.device_id)
        if not device_dict:
            raise ServiceException(message='设备不存在')

        if device_dict.get('device_code') != page_object.device_code:
            device = await DeviceDao.get_device_by_code(query_db, page_object.device_code)
            if device:
                raise ServiceException(message='设备编码已存在')

        try:
            device = await DeviceDao.get_device_by_id(query_db, page_object.device_id)
            device = SysDeviceDO(**device)
            device.device_name = page_object.device_name
            device.device_code = page_object.device_code
            device.device_type = page_object.device_type
            device.device_model = page_object.device_model
            device.status = page_object.status
            device.ip_address = page_object.ip_address
            device.mac_address = page_object.mac_address
            device.location = page_object.location
            device.manufacturer = page_object.manufacturer
            device.supplier = page_object.supplier
            device.purchase_date = page_object.purchase_date
            device.warranty_end_date = page_object.warranty_end_date
            device.department_id = page_object.department_id
            device.user_id = page_object.user_id
            device.remark = page_object.remark
            device.update_by = ''
            device.update_time = datetime.now()
            await DeviceDao.edit_device(query_db, device)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='编辑设备成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def delete_device_services(
        cls, query_db: AsyncSession, device_id: int
    ) -> CrudResponseModel:
        """
        删除设备信息service

        :param query_db: orm对象
        :param device_id: 设备ID
        :return: 删除设备结果
        """
        device_dict = await DeviceDao.get_device_by_id(query_db, device_id)
        if not device_dict:
            raise ServiceException(message='设备不存在')

        try:
            await DeviceDao.delete_device(query_db, device_id)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='删除设备成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def update_device_status_services(
        cls, query_db: AsyncSession, device_id: int, status: str
    ) -> CrudResponseModel:
        """
        更新设备状态service

        :param query_db: orm对象
        :param device_id: 设备ID
        :param status: 设备状态
        :return: 更新设备状态结果
        """
        device_dict = await DeviceDao.get_device_by_id(query_db, device_id)
        if not device_dict:
            raise ServiceException(message='设备不存在')

        try:
            await DeviceDao.update_device_status(query_db, device_id, status)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='更新设备状态成功')
        except Exception as e:
            await query_db.rollback()
            raise e


class DeviceGroupService:
    """
    设备分组管理模块服务层
    """

    @classmethod
    async def get_device_group_list_services(
        cls, query_db: AsyncSession, group_name: str | None, status: str | None
    ) -> list[DeviceGroupModel]:
        """
        获取设备分组列表信息service

        :param query_db: orm对象
        :param group_name: 分组名称
        :param status: 状态
        :return: 设备分组列表信息对象
        """
        group_list = await DeviceGroupDao.get_device_group_list(query_db, group_name, status)
        result = []
        for group in group_list:
            group_dict = {
                'group_id': group.group_id,
                'group_name': group.group_name,
                'parent_id': group.parent_id,
                'order_num': group.order_num,
                'status': group.status,
                'remark': group.remark,
                'create_by': group.create_by,
                'create_time': group.create_time,
                'update_by': group.update_by,
                'update_time': group.update_time,
            }
            result.append(DeviceGroupModel(**group_dict))
        return result

    @classmethod
    async def get_device_group_tree_services(
        cls, query_db: AsyncSession
    ) -> list[DeviceGroupTreeModel]:
        """
        获取设备分组树service

        :param query_db: orm对象
        :return: 设备分组树对象
        """
        group_list = await DeviceGroupDao.get_device_group_list(query_db, None, None)

        group_map = {group.group_id: group for group in group_list}
        root_groups = [group for group in group_list if group.parent_id == 0]

        def build_tree(group_id: int) -> DeviceGroupTreeModel:
            group = group_map[group_id]
            children = []
            for child_group in group_list:
                if child_group.parent_id == group_id:
                    children.append(build_tree(child_group.group_id))

            return DeviceGroupTreeModel(
                value=group.group_id,
                label=group.group_name,
                children=children if children else None,
            )

        tree = [build_tree(group.group_id) for group in root_groups]
        return tree

    @classmethod
    async def add_device_group_services(
        cls, query_db: AsyncSession, page_object: DeviceGroupAddModel
    ) -> CrudResponseModel:
        """
        新增设备分组信息service

        :param query_db: orm对象
        :param page_object: 新增设备分组对象
        :return: 新增设备分组结果
        """
        group = await DeviceGroupDao.get_device_group_by_name(
            query_db, page_object.group_name, page_object.parent_id
        )
        if group:
            raise ServiceException(message='分组名称已存在')
        try:
            group = SysDeviceGroupDO(
                group_name=page_object.group_name,
                parent_id=page_object.parent_id,
                order_num=page_object.order_num,
                status=page_object.status,
                remark=page_object.remark,
                create_by='',
                create_time=datetime.now(),
                update_by='',
                del_flag='0',
            )
            await DeviceGroupDao.add_device_group(query_db, group)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增设备分组成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_device_group_services(
        cls, query_db: AsyncSession, page_object: DeviceGroupEditModel
    ) -> CrudResponseModel:
        """
        编辑设备分组信息service

        :param query_db: orm对象
        :param page_object: 编辑设备分组对象
        :return: 编辑设备分组结果
        """
        group = await DeviceGroupDao.get_device_group_by_id(query_db, page_object.group_id)
        if not group:
            raise ServiceException(message='分组不存在')

        if group.group_name != page_object.group_name or group.parent_id != page_object.parent_id:
            check_group = await DeviceGroupDao.get_device_group_by_name(
                query_db, page_object.group_name, page_object.parent_id
            )
            if check_group:
                raise ServiceException(message='分组名称已存在')

        try:
            group.group_name = page_object.group_name
            group.parent_id = page_object.parent_id
            group.order_num = page_object.order_num
            group.status = page_object.status
            group.remark = page_object.remark
            group.update_by = ''
            group.update_time = datetime.now()
            await DeviceGroupDao.edit_device_group(query_db, group)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='编辑设备分组成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def delete_device_group_services(
        cls, query_db: AsyncSession, group_id: int
    ) -> CrudResponseModel:
        """
        删除设备分组信息service

        :param query_db: orm对象
        :param group_id: 分组ID
        :return: 删除设备分组结果
        """
        group = await DeviceGroupDao.get_device_group_by_id(query_db, group_id)
        if not group:
            raise ServiceException(message='分组不存在')

        group_list = await DeviceGroupDao.get_device_group_list(query_db, None, None)
        child_groups = [g for g in group_list if g.parent_id == group_id]
        if child_groups:
            raise ServiceException(message='该分组下存在子分组，无法删除')

        try:
            await DeviceGroupDao.delete_device_group(query_db, group_id)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='删除设备分组成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def get_group_device_list_services(
        cls, query_db: AsyncSession, group_id: int
    ) -> list[DeviceModel]:
        """
        获取分组下的设备列表service

        :param query_db: orm对象
        :param group_id: 分组ID
        :return: 设备列表对象
        """
        group = await DeviceGroupDao.get_device_group_by_id(query_db, group_id)
        if not group:
            raise ServiceException(message='分组不存在')

        device_list = await DeviceGroupDao.get_group_device_list(query_db, group_id)
        result = []
        for device in device_list:
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
            result.append(DeviceModel(**device_dict))
        return result

    @classmethod
    async def add_group_device_services(
        cls, query_db: AsyncSession, page_object: DeviceGroupRelModel
    ) -> CrudResponseModel:
        """
        向分组添加设备service

        :param query_db: orm对象
        :param page_object: 添加设备到分组对象
        :return: 添加设备到分组结果
        """
        group = await DeviceGroupDao.get_device_group_by_id(query_db, page_object.group_id)
        if not group:
            raise ServiceException(message='分组不存在')

        try:
            await DeviceGroupDao.add_group_device(
                query_db, page_object.group_id, page_object.device_ids
            )
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='添加设备到分组成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def remove_group_device_services(
        cls, query_db: AsyncSession, page_object: DeviceGroupRelModel
    ) -> CrudResponseModel:
        """
        从分组移除设备service

        :param query_db: orm对象
        :param page_object: 从分组移除设备对象
        :return: 从分组移除设备结果
        """
        group = await DeviceGroupDao.get_device_group_by_id(query_db, page_object.group_id)
        if not group:
            raise ServiceException(message='分组不存在')

        try:
            await DeviceGroupDao.remove_group_device(
                query_db, page_object.group_id, page_object.device_ids
            )
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='从分组移除设备成功')
        except Exception as e:
            await query_db.rollback()
            raise e
