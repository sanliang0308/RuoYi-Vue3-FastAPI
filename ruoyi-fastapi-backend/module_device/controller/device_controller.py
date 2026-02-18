from typing import Annotated

from fastapi import Path, Query, Request, Response
from pydantic_validation_decorator import ValidateFields
from sqlalchemy import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession

from common.annotation.log_annotation import Log
from common.aspect.data_scope import DataScopeDependency
from common.aspect.db_seesion import DBSessionDependency
from common.aspect.interface_auth import UserInterfaceAuthDependency
from common.aspect.pre_auth import PreAuthDependency
from common.enums import BusinessType
from common.router import APIRouterPro
from common.vo import DataResponseModel, PageResponseModel, ResponseBaseModel
from module_device.entity.do.device_do import SysDeviceDO
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
from module_device.service.device_service import DeviceService, DeviceGroupService
from utils.log_util import logger
from utils.response_util import ResponseUtil

device_controller = APIRouterPro(
    prefix='/device/model', order_num=10, tags=['设备管理-设备型号'], dependencies=[PreAuthDependency()]
)


@device_controller.get(
    '/list',
    summary='获取设备型号列表接口',
    description='用于获取设备型号分页列表',
    response_model=PageResponseModel[DeviceModel],
    dependencies=[UserInterfaceAuthDependency('device:model:list')],
)
async def get_device_list(
    request: Request,
    device_query: Annotated[DeviceQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    data_scope_sql: Annotated[ColumnElement, DataScopeDependency(SysDeviceDO)],
) -> Response:
    device_list_result = await DeviceService.get_device_list_services(
        query_db, device_query, data_scope_sql, is_page=True
    )
    logger.info('获取设备型号列表成功')

    return ResponseUtil.success(model_content=device_list_result)


@device_controller.get(
    '/get/{device_id}',
    summary='获取设备型号详情接口',
    description='用于根据设备ID获取设备型号详情',
    response_model=DataResponseModel[DeviceModel],
    dependencies=[UserInterfaceAuthDependency('device:model:query')],
)
async def get_device_detail(
    request: Request,
    device_id: Annotated[int, Path(description='设备ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    device = await DeviceService.get_device_by_id_services(query_db, device_id)
    logger.info(f'获取设备型号{device_id}详情成功')

    return ResponseUtil.success(data=device)


@device_controller.post(
    '/add',
    summary='新增设备型号接口',
    description='用于新增设备型号',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('device:model:add')],
)
@Log(title='设备型号管理', business_type=BusinessType.INSERT)
@ValidateFields(validate_model='device_add')
async def add_device(
    request: Request,
    device_add: DeviceAddModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    add_result = await DeviceService.add_device_services(query_db, device_add)
    logger.info(add_result.message)

    return ResponseUtil.success(msg=add_result.message)


@device_controller.put(
    '/edit',
    summary='编辑设备型号接口',
    description='用于编辑设备型号',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('device:model:edit')],
)
@Log(title='设备型号管理', business_type=BusinessType.UPDATE)
@ValidateFields(validate_model='device_edit')
async def edit_device(
    request: Request,
    device_edit: DeviceEditModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    edit_result = await DeviceService.edit_device_services(query_db, device_edit)
    logger.info(edit_result.message)

    return ResponseUtil.success(msg=edit_result.message)


@device_controller.delete(
    '/delete/{device_id}',
    summary='删除设备型号接口',
    description='用于删除设备型号',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('device:model:remove')],
)
@Log(title='设备型号管理', business_type=BusinessType.DELETE)
async def delete_device(
    request: Request,
    device_id: Annotated[int, Path(description='设备ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    delete_result = await DeviceService.delete_device_services(query_db, device_id)
    logger.info(delete_result.message)

    return ResponseUtil.success(msg=delete_result.message)


@device_controller.put(
    '/status/{device_id}/{status}',
    summary='修改设备型号状态接口',
    description='用于修改设备型号状态',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('device:model:edit')],
)
@Log(title='设备型号管理', business_type=BusinessType.UPDATE)
async def update_device_status(
    request: Request,
    device_id: Annotated[int, Path(description='设备ID')],
    status: Annotated[str, Path(description='设备状态(0正常 1离线 2故障)')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    update_result = await DeviceService.update_device_status_services(query_db, device_id, status)
    logger.info(update_result.message)

    return ResponseUtil.success(msg=update_result.message)


device_group_controller = APIRouterPro(
    prefix='/device/group', order_num=11, tags=['设备管理-设备分组'], dependencies=[PreAuthDependency()]
)


@device_group_controller.get(
    '/list',
    summary='获取设备分组列表接口',
    description='用于获取设备分组列表',
    response_model=DataResponseModel[list[DeviceGroupModel]],
    dependencies=[UserInterfaceAuthDependency('device:group:list')],
)
async def get_device_group_list(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    group_name: Annotated[str | None, Query(description='分组名称')] = None,
    status: Annotated[str | None, Query(description='状态')] = None,
) -> Response:
    group_list = await DeviceGroupService.get_device_group_list_services(
        query_db, group_name, status
    )
    logger.info('获取设备分组列表成功')

    return ResponseUtil.success(data=group_list)


@device_group_controller.get(
    '/tree',
    summary='获取设备分组树接口',
    description='用于获取设备分组树',
    response_model=DataResponseModel[list[DeviceGroupTreeModel]],
    dependencies=[UserInterfaceAuthDependency('device:group:list')],
)
async def get_device_group_tree(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    group_tree = await DeviceGroupService.get_device_group_tree_services(query_db)
    logger.info('获取设备分组树成功')

    return ResponseUtil.success(data=group_tree)


@device_group_controller.post(
    '/add',
    summary='新增设备分组接口',
    description='用于新增设备分组',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('device:group:add')],
)
@Log(title='设备分组管理', business_type=BusinessType.INSERT)
@ValidateFields(validate_model='device_group_add')
async def add_device_group(
    request: Request,
    group_add: DeviceGroupAddModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    add_result = await DeviceGroupService.add_device_group_services(query_db, group_add)
    logger.info(add_result.message)

    return ResponseUtil.success(msg=add_result.message)


@device_group_controller.put(
    '/edit',
    summary='编辑设备分组接口',
    description='用于编辑设备分组',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('device:group:edit')],
)
@Log(title='设备分组管理', business_type=BusinessType.UPDATE)
@ValidateFields(validate_model='device_group_edit')
async def edit_device_group(
    request: Request,
    group_edit: DeviceGroupEditModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    edit_result = await DeviceGroupService.edit_device_group_services(query_db, group_edit)
    logger.info(edit_result.message)

    return ResponseUtil.success(msg=edit_result.message)


@device_group_controller.delete(
    '/delete/{group_id}',
    summary='删除设备分组接口',
    description='用于删除设备分组',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('device:group:remove')],
)
@Log(title='设备分组管理', business_type=BusinessType.DELETE)
async def delete_device_group(
    request: Request,
    group_id: Annotated[int, Path(description='分组ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    delete_result = await DeviceGroupService.delete_device_group_services(query_db, group_id)
    logger.info(delete_result.message)

    return ResponseUtil.success(msg=delete_result.message)


@device_group_controller.get(
    '/device/list/{group_id}',
    summary='获取分组下的设备列表接口',
    description='用于获取分组下的设备列表',
    response_model=DataResponseModel[list[DeviceModel]],
    dependencies=[UserInterfaceAuthDependency('device:group:list')],
)
async def get_group_device_list(
    request: Request,
    group_id: Annotated[int, Path(description='分组ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    device_list = await DeviceGroupService.get_group_device_list_services(query_db, group_id)
    logger.info(f'获取分组{group_id}下的设备列表成功')

    return ResponseUtil.success(data=device_list)


@device_group_controller.post(
    '/device/add',
    summary='向分组添加设备接口',
    description='用于向分组添加设备',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('device:group:edit')],
)
@Log(title='设备分组管理', business_type=BusinessType.UPDATE)
async def add_group_device(
    request: Request,
    group_rel: DeviceGroupRelModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    add_result = await DeviceGroupService.add_group_device_services(query_db, group_rel)
    logger.info(add_result.message)

    return ResponseUtil.success(msg=add_result.message)


@device_group_controller.delete(
    '/device/remove',
    summary='从分组移除设备接口',
    description='用于从分组移除设备',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('device:group:edit')],
)
@Log(title='设备分组管理', business_type=BusinessType.UPDATE)
async def remove_group_device(
    request: Request,
    group_rel: DeviceGroupRelModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    remove_result = await DeviceGroupService.remove_group_device_services(query_db, group_rel)
    logger.info(remove_result.message)

    return ResponseUtil.success(msg=remove_result.message)
