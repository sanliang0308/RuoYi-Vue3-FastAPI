from datetime import datetime, date
from typing import Literal, List, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank, Size, Xss

from exceptions.exception import ModelValidatorException


class DeviceBaseModel(BaseModel):
    """
    设备基础模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    device_name: str | None = Field(default=None, description='设备名称')
    device_code: str | None = Field(default=None, description='设备编码')
    device_type: str | None = Field(default=None, description='设备类型')
    device_model: str | None = Field(default=None, description='设备型号')
    status: Literal['0', '1', '2'] | None = Field(default='0', description='设备状态(0正常 1离线 2故障)')
    ip_address: str | None = Field(default=None, description='IP地址')
    mac_address: str | None = Field(default=None, description='MAC地址')
    location: str | None = Field(default=None, description='设备位置')
    manufacturer: str | None = Field(default=None, description='制造商')
    supplier: str | None = Field(default=None, description='供应商')
    purchase_date: date | None = Field(default=None, description='购买日期')
    warranty_end_date: date | None = Field(default=None, description='保修截止日期')
    department_id: int | None = Field(default=None, description='所属部门ID')
    user_id: int | None = Field(default=None, description='负责人ID')
    remark: str | None = Field(default=None, description='备注')

    @Xss(field_name='device_name', message='设备名称不能包含脚本字符')
    @NotBlank(field_name='device_name', message='设备名称不能为空')
    @Size(field_name='device_name', min_length=0, max_length=64, message='设备名称长度不能超过64个字符')
    def get_device_name(self) -> str | None:
        return self.device_name

    @Xss(field_name='device_code', message='设备编码不能包含脚本字符')
    @NotBlank(field_name='device_code', message='设备编码不能为空')
    @Size(field_name='device_code', min_length=0, max_length=64, message='设备编码长度不能超过64个字符')
    def get_device_code(self) -> str | None:
        return self.device_code

    @Xss(field_name='device_type', message='设备类型不能包含脚本字符')
    @NotBlank(field_name='device_type', message='设备类型不能为空')
    @Size(field_name='device_type', min_length=0, max_length=32, message='设备类型长度不能超过32个字符')
    def get_device_type(self) -> str | None:
        return self.device_type

    @Xss(field_name='device_model', message='设备型号不能包含脚本字符')
    @NotBlank(field_name='device_model', message='设备型号不能为空')
    @Size(field_name='device_model', min_length=0, max_length=64, message='设备型号长度不能超过64个字符')
    def get_device_model(self) -> str | None:
        return self.device_model


class DeviceModel(DeviceBaseModel):
    """
    设备表对应pydantic模型
    """

    device_id: int | None = Field(default=None, description='设备ID')
    department_name: str | None = Field(default=None, description='部门名称')
    user_name: str | None = Field(default=None, description='负责人名称')
    create_by: str | None = Field(default=None, description='创建者')
    create_time: datetime | None = Field(default=None, description='创建时间')
    update_by: str | None = Field(default=None, description='更新者')
    update_time: datetime | None = Field(default=None, description='更新时间')


class DeviceQueryModel(BaseModel):
    """
    设备查询模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    device_name: str | None = Field(default=None, description='设备名称')
    device_code: str | None = Field(default=None, description='设备编码')
    device_type: str | None = Field(default=None, description='设备类型')
    status: Literal['0', '1', '2'] | None = Field(default=None, description='设备状态')
    department_id: int | None = Field(default=None, description='部门ID')
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeviceAddModel(DeviceBaseModel):
    """
    添加设备模型
    """
    pass


class DeviceEditModel(DeviceBaseModel):
    """
    编辑设备模型
    """

    device_id: int | None = Field(default=None, description='设备ID')


class DeviceGroupBaseModel(BaseModel):
    """
    设备分组基础模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    group_name: str | None = Field(default=None, description='分组名称')
    parent_id: int | None = Field(default=0, description='父分组ID')
    order_num: int | None = Field(default=0, description='显示顺序')
    status: Literal['0', '1'] | None = Field(default='0', description='状态(0正常 1停用)')
    remark: str | None = Field(default=None, description='备注')

    @Xss(field_name='group_name', message='分组名称不能包含脚本字符')
    @NotBlank(field_name='group_name', message='分组名称不能为空')
    @Size(field_name='group_name', min_length=0, max_length=64, message='分组名称长度不能超过64个字符')
    def get_group_name(self) -> str | None:
        return self.group_name


class DeviceGroupModel(DeviceGroupBaseModel):
    """
    设备分组表对应pydantic模型
    """

    group_id: int | None = Field(default=None, description='分组ID')
    create_by: str | None = Field(default=None, description='创建者')
    create_time: datetime | None = Field(default=None, description='创建时间')
    update_by: str | None = Field(default=None, description='更新者')
    update_time: datetime | None = Field(default=None, description='更新时间')


class DeviceGroupTreeModel(BaseModel):
    """
    设备分组树模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    value: int = Field(..., description='分组ID')
    label: str = Field(..., description='分组名称')
    children: List['DeviceGroupTreeModel'] | None = Field(default=None, description='子分组')


class DeviceGroupAddModel(DeviceGroupBaseModel):
    """
    添加设备分组模型
    """
    pass


class DeviceGroupEditModel(DeviceGroupBaseModel):
    """
    编辑设备分组模型
    """

    group_id: int | None = Field(default=None, description='分组ID')


class DeviceGroupRelModel(BaseModel):
    """
    设备分组关联模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    group_id: int = Field(..., description='分组ID')
    device_ids: List[int] = Field(..., description='设备ID列表')
