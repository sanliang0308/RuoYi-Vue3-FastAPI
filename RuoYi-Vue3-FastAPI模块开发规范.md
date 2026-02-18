# RuoYi-Vue3-FastAPI 模块开发规范

> 基于 module_ai 模块提炼的标准规范

---

## 一、项目架构概览

```
RuoYi-Vue3-FastAPI/
├── ruoyi-fastapi-backend/          # 后端服务 (FastAPI)
│   ├── common/                      # 公共模块
│   ├── module_ai/                   # AI模块 (规范模板)
│   ├── module_admin/                # 系统管理模块
│   ├── module_device/               # 设备管理模块
│   └── ...
├── ruoyi-fastapi-frontend/         # 前端界面 (Vue3)
│   ├── src/api/                    # API接口定义
│   ├── src/views/                   # 页面视图
│   └── ...
```

---

## 二、后端模块标准结构

每个业务模块应遵循以下目录结构：

```
module_xxx/
├── controller/                      # 控制器层 (API入口)
│   ├── xxx_controller.py
│   └── xxx_controller.py
├── dao/                             # 数据访问层 (数据库操作)
│   ├── xxx_dao.py
│   └── xxx_dao.py
├── entity/
│   ├── do/                          # 数据库实体 (SQLAlchemy Model)
│   │   └── xxx_do.py
│   └── vo/                          # 视图对象 (Pydantic Model)
│       ├── xxx_vo.py
│       └── xxx_vo.py
└── service/                         # 业务逻辑层
    ├── xxx_service.py
    └── xxx_service.py
```

---

## 三、后端开发规范

### 3.1 DO层 (Database Object)

**文件命名**: `{模块名}_do.py`

**命名规范**:
- 类名: PascalCase，如 `AiModels`
- 表名: 蛇形小写，如 `ai_models`
- 字段名: 蛇形小写，如 `model_id`

**示例**:
```python
from datetime import datetime
from sqlalchemy import CHAR, BigInteger, Column, DateTime, Integer, String
from config.database import Base
from config.env import DataBaseConfig
from utils.common_util import SqlalchemyUtil

class AiModels(Base):
    """
    AI模型表
    """

    __tablename__ = 'ai_models'
    __table_args__ = {'comment': 'AI模型表'}

    model_id = Column(BigInteger, primary_key=True, nullable=False,
                       autoincrement=True, comment='模型主键')
    model_code = Column(String(100), nullable=False, comment='模型编码')
    model_name = Column(String(100), nullable=True,
                        server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type),
                        comment='模型名称')
    provider = Column(String(50), nullable=False, comment='提供商')
    status = Column(CHAR(1), default='0', comment='状态')
    user_id = Column(BigInteger, nullable=True, comment='用户ID')
    dept_id = Column(BigInteger, nullable=True, comment='部门ID')
    create_by = Column(String(64), nullable=True, default='', comment='创建者')
    create_time = Column(DateTime, nullable=True, default=datetime.now, comment='创建时间')
    update_by = Column(String(64), nullable=True, default='', comment='更新者')
    update_time = Column(DateTime, nullable=True, default=datetime.now, comment='更新时间')
    remark = Column(String(500), nullable=True, comment='备注')
```

**字段规范**:
| 字段类型 | 使用类型 | 说明 |
|---------|---------|------|
| 主键 | BigInteger | 自增主键 |
| 状态/开关 | CHAR(1) | '0'-正常/启用, '1'-禁用 |
| 排序 | Integer | 用于列表排序 |
| 时间 | DateTime | 配合 default=datetime.now |
| 文本 | String(length) | 指定长度 |
| 大文本 | String(500+) | 用于备注等 |

### 3.2 VO层 (View Object)

**文件命名**: `{模块名}_vo.py`

**命名规范**:
- 类名: PascalCase + Model，如 `AiModelModel`
- 字段别名: 驼峰命名，如 `modelCode` → `model_code`

**示例**:
```python
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank, Size

class AiModelModel(BaseModel):
    """
    AI模型表对应pydantic模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    model_id: int | None = Field(default=None, description='模型主键')
    model_code: str | None = Field(default=None, description='模型编码')
    model_name: str | None = Field(default=None, description='模型名称')
    provider: str | None = Field(default=None, description='提供商')
    model_sort: int | None = Field(default=None, description='显示顺序')
    api_key: str | None = Field(default=None, description='API Key')
    status: Literal['0', '1'] | None = Field(default=None, description='模型状态')

    @NotBlank(field_name='model_code', message='模型编码不能为空')
    def get_model_code(self) -> str | None:
        return self.model_code

class AiModelPageQueryModel(AiModelModel):
    """
    AI模型管理分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')

class DeleteAiModelModel(BaseModel):
    """
    删除AI模型模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    model_ids: str = Field(description='需要删除的模型主键')
```

**验证注解**:
- `@NotBlank`: 字符串不能为空
- `@Size`: 字符串长度限制

### 3.3 DAO层 (Data Access Object)

**文件命名**: `{模块名}_dao.py`

**命名规范**:
- 类名: PascalCase + Dao，如 `AiModelDao`
- 方法名: 蛇形小写 + _dao 后缀

**示例**:
```python
from typing import Any
from sqlalchemy import ColumnElement, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from common.vo import PageModel
from module_ai.entity.do.ai_model_do import AiModels
from module_ai.entity.vo.ai_model_vo import AiModelModel, AiModelPageQueryModel
from utils.page_util import PageUtil

class AiModelDao:
    """
    AI模型管理数据库操作层
    """

    @classmethod
    async def get_ai_model_detail_by_id(cls, db: AsyncSession, model_id: int) -> AiModels | None:
        """根据AI模型id获取AI模型详细信息"""
        ai_model_info = (await db.execute(
            select(AiModels).where(AiModels.model_id == model_id)
        )).scalars().first()
        return ai_model_info

    @classmethod
    async def get_ai_model_list(
        cls, db: AsyncSession, query_object: AiModelPageQueryModel,
        data_scope_sql: ColumnElement, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """根据查询参数获取AI模型列表信息"""
        query = (
            select(AiModels)
            .where(
                AiModels.model_id == query_object.model_id if query_object.model_id else True,
                AiModels.model_name.like(f'%{query_object.model_name}%')
                    if query_object.model_name else True,
                AiModels.status == query_object.status if query_object.status else True,
                data_scope_sql,
            )
            .order_by(AiModels.model_sort)
        )
        ai_model_list = await PageUtil.paginate(
            db, query, query_object.page_num, query_object.page_size, is_page
        )
        return ai_model_list

    @classmethod
    async def add_ai_model_dao(cls, db: AsyncSession, ai_model: AiModelModel) -> AiModels:
        """新增AI模型数据库操作"""
        db_model = AiModels(**ai_model.model_dump(exclude_unset=True))
        db.add(db_model)
        await db.flush()
        return db_model

    @classmethod
    async def edit_ai_model_dao(cls, db: AsyncSession, ai_model: dict) -> None:
        """编辑AI模型数据库操作"""
        await db.execute(update(AiModels), [ai_model])

    @classmethod
    async def delete_ai_model_dao(cls, db: AsyncSession, ai_model: AiModelModel) -> None:
        """删除AI模型数据库操作"""
        await db.execute(delete(AiModels).where(AiModels.model_id.in_([ai_model.model_id])))
```

**DAO方法命名规范**:
| 操作 | 方法命名 | 示例 |
|-----|---------|------|
| 详情 | get_xxx_detail_by_id | `get_ai_model_detail_by_id` |
| 列表 | get_xxx_list | `get_ai_model_list` |
| 新增 | add_xxx_dao | `add_ai_model_dao` |
| 编辑 | edit_xxx_dao | `edit_ai_model_dao` |
| 删除 | delete_xxx_dao | `delete_ai_model_dao` |

### 3.4 Service层

**文件命名**: `{模块名}_service.py`

**命名规范**:
- 类名: PascalCase + Service，如 `AiModelService`
- 方法名: 蛇形小写 + _services 后缀

**示例**:
```python
from typing import Any
from sqlalchemy import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
from common.vo import CrudResponseModel, PageModel
from exceptions.exception import ServiceException
from module_ai.dao.ai_model_dao import AiModelDao
from module_ai.entity.vo.ai_model_vo import AiModelModel, AiModelPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.crypto_util import CryptoUtil

class AiModelService:
    """
    AI模型管理服务层
    """

    @classmethod
    async def get_ai_model_list_services(
        cls, query_db: AsyncSession, query_object: AiModelPageQueryModel,
        data_scope_sql: ColumnElement, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """获取AI模型列表信息service"""
        ai_model_list_result = await AiModelDao.get_ai_model_list(
            query_db, query_object, data_scope_sql, is_page
        )
        rows = ai_model_list_result.rows if isinstance(ai_model_list_result, PageModel) else ai_model_list_result

        # 敏感信息脱敏
        for row in rows:
            if 'apiKey' in row:
                row['apiKey'] = '********' * 3

        return ai_model_list_result

    @classmethod
    async def check_ai_model_data_scope_services(
        cls, query_db: AsyncSession, model_id: int, data_scope_sql: ColumnElement
    ) -> CrudResponseModel:
        """校验用户是否有AI模型数据权限"""
        ai_models = await AiModelDao.get_ai_model_list(
            query_db, AiModelModel(modelId=model_id), data_scope_sql, is_page=False
        )
        if ai_models:
            return CrudResponseModel(is_success=True, message='校验通过')
        raise ServiceException(message='没有权限访问AI模型数据')

    @classmethod
    async def add_ai_model_services(cls, query_db: AsyncSession,
                                    page_object: AiModelModel) -> CrudResponseModel:
        """新增AI模型信息service"""
        try:
            # 敏感信息加密
            if page_object.api_key:
                page_object.api_key = CryptoUtil.encrypt(page_object.api_key)
            await AiModelDao.add_ai_model_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_ai_model_services(cls, query_db: AsyncSession,
                                    page_object: AiModelModel) -> CrudResponseModel:
        """编辑AI模型信息service"""
        edit_ai_model = page_object.model_dump(exclude_unset=True)
        if page_object.api_key:
            # 保留原密钥或更新密钥
            if page_object.api_key == '********' * 3:
                if 'api_key' in edit_ai_model:
                    del edit_ai_model['api_key']
            else:
                edit_ai_model['api_key'] = CryptoUtil.encrypt(page_object.api_key)

        ai_model_info = await cls.ai_model_detail_services(query_db, page_object.model_id)
        if ai_model_info.model_id:
            try:
                await AiModelDao.edit_ai_model_dao(query_db, edit_ai_model)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='修改成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='AI模型不存在')

    @classmethod
    async def delete_ai_model_services(
        cls, query_db: AsyncSession, page_object: DeleteAiModelModel
    ) -> CrudResponseModel:
        """删除AI模型信息service"""
        if page_object.model_ids:
            model_id_list = page_object.model_ids.split(',')
            try:
                for model_id in model_id_list:
                    await AiModelDao.delete_ai_model_dao(query_db, AiModelModel(modelId=model_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入AI模型id为空')

    @classmethod
    async def ai_model_detail_services(cls, query_db: AsyncSession,
                                      model_id: int) -> AiModelModel:
        """获取AI模型详细信息service"""
        ai_model = await AiModelDao.get_ai_model_detail_by_id(query_db, model_id=model_id)
        result = AiModelModel(**CamelCaseUtil.transform_result(ai_model)) if ai_model else AiModelModel()

        # 脱敏
        if result.api_key:
            result.api_key = '********' * 3

        return result
```

**Service方法命名规范**:
| 操作 | 方法命名 | 返回类型 |
|-----|---------|---------|
| 列表 | get_xxx_list_services | PageModel / list |
| 详情 | get_xxx_detail_services | VO Model |
| 新增 | add_xxx_services | CrudResponseModel |
| 编辑 | edit_xxx_services | CrudResponseModel |
| 删除 | delete_xxx_services | CrudResponseModel |
| 校验 | check_xxx_data_scope_services | CrudResponseModel |

### 3.5 Controller层

**文件命名**: `{模块名}_controller.py`

**命名规范**:
- 路由前缀: 蛇形小写，如 `/ai/model`
- 依赖注入: 使用 Annotated 语法

**示例**:
```python
from datetime import datetime
from typing import Annotated
from fastapi import Path, Query, Request, Response
from pydantic_validation_decorator import ValidateFields
from sqlalchemy import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
from common.annotation.log_annotation import Log
from common.aspect.data_scope import DataScopeDependency
from common.aspect.db_seesion import DBSessionDependency
from common.aspect.interface_auth import UserInterfaceAuthDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.enums import BusinessType
from common.router import APIRouterPro
from common.vo import DataResponseModel, PageResponseModel, ResponseBaseModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_ai.entity.do.ai_model_do import AiModels
from module_ai.entity.vo.ai_model_vo import AiModelModel, AiModelPageQueryModel, DeleteAiModelModel
from module_ai.service.ai_model_service import AiModelService
from utils.log_util import logger
from utils.response_util import ResponseUtil

ai_model_controller = APIRouterPro(
    prefix='/ai/model', order_num=18, tags=['AI管理-模型管理'], dependencies=[PreAuthDependency()]
)

@ai_model_controller.get(
    '/list',
    summary='获取AI模型分页列表接口',
    description='用于获取AI模型分页列表',
    response_model=PageResponseModel[AiModelModel],
    dependencies=[UserInterfaceAuthDependency('ai:model:list')],
)
async def get_ai_model_list(
    request: Request,
    ai_model_page_query: Annotated[AiModelPageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    data_scope_sql: Annotated[ColumnElement, DataScopeDependency(AiModels)],
) -> Response:
    result = await AiModelService.get_ai_model_list_services(
        query_db, ai_model_page_query, data_scope_sql, is_page=True
    )
    logger.info('获取成功')
    return ResponseUtil.success(model_content=result)

@ai_model_controller.post(
    '',
    summary='新增AI模型接口',
    description='用于新增AI模型',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('ai:model:add')],
)
@ValidateFields(validate_model='add_ai_model')
@Log(title='AI模型管理', business_type=BusinessType.INSERT)
async def add_ai_model(
    request: Request,
    add_ai_model: AiModelModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    add_ai_model.user_id = current_user.user.user_id
    add_ai_model.dept_id = current_user.user.dept_id
    add_ai_model.create_by = current_user.user.user_name
    add_ai_model.create_time = datetime.now()
    add_ai_model.update_by = current_user.user.user_name
    add_ai_model.update_time = datetime.now()
    result = await AiModelService.add_ai_model_services(query_db, add_ai_model)
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message)

@ai_model_controller.put(
    '',
    summary='编辑AI模型接口',
    description='用于编辑AI模型',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('ai:model:edit')],
)
@ValidateFields(validate_model='edit_ai_model')
@Log(title='AI模型管理', business_type=BusinessType.UPDATE)
async def edit_ai_model(
    request: Request,
    edit_ai_model: AiModelModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
    data_scope_sql: Annotated[ColumnElement, DataScopeDependency(AiModels)],
) -> Response:
    if not current_user.user.admin:
        await AiModelService.check_ai_model_data_scope_services(
            query_db, edit_ai_model.model_id, data_scope_sql
        )
    edit_ai_model.update_by = current_user.user.user_name
    edit_ai_model.update_time = datetime.now()
    result = await AiModelService.edit_ai_model_services(query_db, edit_ai_model)
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message)

@ai_model_controller.delete(
    '/{model_ids}',
    summary='删除AI模型接口',
    description='用于删除AI模型',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('ai:model:remove')],
)
@Log(title='AI模型管理', business_type=BusinessType.DELETE)
async def delete_ai_model(
    request: Request,
    model_ids: Annotated[str, Path(description='需要删除的模型ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
    data_scope_sql: Annotated[ColumnElement, DataScopeDependency(AiModels)],
) -> Response:
    model_id_list = model_ids.split(',')
    for model_id in model_id_list:
        if not current_user.user.admin:
            await AiModelService.check_ai_model_data_scope_services(
                query_db, int(model_id), data_scope_sql
            )
    delete_ai_model = DeleteAiModelModel(modelIds=model_ids)
    result = await AiModelService.delete_ai_model_services(query_db, delete_ai_model)
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message)
```

**API路由规范**:
| 方法 | 路径 | 功能 | 权限标识 |
|-----|------|-----|---------|
| GET | /list | 分页列表 | xxx:xxx:list |
| GET | /all | 不分页列表 | - |
| GET | /{id} | 详情 | xxx:xxx:query |
| POST | / | 新增 | xxx:xxx:add |
| PUT | / | 编辑 | xxx:xxx:edit |
| DELETE | /{ids} | 删除 | xxx:xxx:remove |

---

## 四、前端模块化开发规范（推荐）

### 4.1 模块目录结构

推荐将 API 和 Views 放在统一的 `modules` 目录下：

```
ruoyi-fastapi-frontend/
├── src/
│   ├── modules/                      # 模块目录
│   │   ├── ai/                      # AI模块
│   │   │   ├── api/                 # AI模块API
│   │   │   │   └── model.js         # 模型管理API
│   │   │   └── views/               # AI模块页面
│   │   │       ├── model/
│   │   │       │   └── index.vue    # 模型管理页面
│   │   │       └── chat/
│   │   │           ├── index.vue    # 对话页面
│   │   │           └── components/
│   │   │               └── AiMessage.vue
│   │   └── device/                  # 设备模块
│   │       ├── api/
│   │       │   └── device.js        # 设备API
│   │       └── views/
│   │           ├── index.vue         # 设备列表
│   │           └── group/
│   │               └── index.vue    # 设备分组
│   ├── api/                         # 公共API目录（可选）
│   └── views/                       # 公共视图目录（可选）
│       ├── dashboard/
│       └── system/
```

### 4.2 API文件规范

**推荐方式：工厂函数模式**

**文件路径**: `src/modules/{模块名}/api/{功能名}.js`

```javascript
import request from '@/utils/request'

/**
 * AI模型管理 API
 */
export function aiModelApi() {
  return {
    // 获取分页列表
    getList: (params) => {
      return request({
        url: '/ai/model/list',
        method: 'get',
        params
      })
    },
    // 获取所有模型（不分页）
    getAll: () => {
      return request({
        url: '/ai/model/all',
        method: 'get'
      })
    },
    // 获取详情
    getInfo: (modelId) => {
      return request({
        url: `/ai/model/${modelId}`,
        method: 'get'
      })
    },
    // 新增
    add: (data) => {
      return request({
        url: '/ai/model',
        method: 'post',
        data
      })
    },
    // 编辑
    edit: (data) => {
      return request({
        url: '/ai/model',
        method: 'put',
        data
      })
    },
    // 删除
    delete: (modelIds) => {
      return request({
        url: `/ai/model/${modelIds}`,
        method: 'delete'
      })
    }
  }
}

/**
 * AI对话 API
 */
export function aiChatApi() {
  return {
    // 发送消息（流式）
    sendMessage: (data) => {
      return request({
        url: '/ai/chat/send',
        method: 'post',
        data,
        responseType: 'stream'
      })
    },
    // 获取会话列表
    getSessionList: () => {
      return request({
        url: '/ai/chat/session/list',
        method: 'get'
      })
    },
    // 获取配置
    getConfig: () => {
      return request({
        url: '/ai/chat/config',
        method: 'get'
      })
    },
    // 保存配置
    saveConfig: (data) => {
      return request({
        url: '/ai/chat/config',
        method: 'put',
        data
      })
    }
  }
}
```

**使用方式**:
```javascript
import { aiModelApi } from '@/modules/ai/api/model'

const api = aiModelApi()
api.getList(queryParams).then(response => {
  // 处理响应
})
```

### 4.3 视图文件规范

**文件路径**: `src/modules/{模块名}/views/{功能}/index.vue`

```vue
<template>
  <div class="app-container">
    <!-- 搜索表单 -->
    <el-form v-show="showSearch" ref="queryFormRef" :model="queryParams" :inline="true" label-width="68px">
      <el-form-item label="模型编码" prop="modelCode">
        <el-input v-model="queryParams.modelCode" placeholder="请输入模型编码" clearable style="width: 200px" @keyup.enter="handleQuery" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 操作按钮 -->
    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button type="primary" plain icon="Plus" @click="handleAdd" v-hasPermi="['ai:model:add']">新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="success" plain icon="Edit" :disabled="single" @click="handleUpdate" v-hasPermi="['ai:model:edit']">修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="danger" plain icon="Delete" :disabled="multiple" @click="handleDelete" v-hasPermi="['ai:model:remove']">删除</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList" />
    </el-row>

    <!-- 数据表格 -->
    <el-table v-loading="loading" :data="modelList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="模型ID" align="center" prop="modelId" width="80" />
      <el-table-column label="模型编码" align="center" prop="modelCode" />
      <el-table-column label="提供商" align="center" prop="provider" />
      <el-table-column label="状态" align="center" prop="status">
        <template #default="scope">
          <dict-tag :options="sys_normal_disable" :value="scope.row.status" />
        </template>
      </el-table-column>
      <el-table-column label="创建时间" align="center" prop="createTime" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.createTime) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="180" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['ai:model:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['ai:model:remove']">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <pagination v-show="total > 0" :total="total" v-model:page="queryParams.pageNum" v-model:limit="queryParams.pageSize" @pagination="getList" />

    <!-- 添加/编辑对话框 -->
    <el-dialog :title="title" v-model="open" width="700px" append-to-body>
      <el-form ref="modelFormRef" :model="form" :rules="rules" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="模型编码" prop="modelCode">
              <el-input v-model="form.modelCode" placeholder="请输入模型编码" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="模型名称" prop="modelName">
              <el-input v-model="form.modelName" placeholder="请输入模型名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <!-- 更多表单项... -->
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="AiModel">
import { aiModelApi } from '@/modules/ai/api/model'

const { proxy } = getCurrentInstance()
const { sys_normal_disable } = proxy.useDict('sys_normal_disable')

// API实例
const api = aiModelApi()

// 响应式数据
const modelList = ref([])
const open = ref(false)
const loading = ref(true)
const showSearch = ref(true)
const ids = ref([])
const single = ref(true)
const multiple = ref(true)
const total = ref(0)
const title = ref('')

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    modelCode: undefined,
    provider: undefined,
    status: undefined
  },
  rules: {
    modelCode: [{ required: true, message: '模型编码不能为空', trigger: 'blur' }],
    provider: [{ required: true, message: '提供商不能为空', trigger: 'change' }]
  }
})

const { queryParams, form, rules } = toRefs(data)

/** 查询列表 */
function getList() {
  loading.value = true
  api.getList(queryParams.value).then(response => {
    modelList.value = response.rows
    total.value = response.total
    loading.value = false
  })
}

/** 重置 */
function reset() {
  form.value = {
    modelId: undefined,
    modelCode: undefined,
    modelName: undefined,
    provider: undefined,
    modelSort: 0,
    status: '0',
    remark: undefined
  }
  proxy.$refs.modelFormRef?.resetFields()
}

/** 搜索 */
function handleQuery() {
  queryParams.value.pageNum = 1
  getList()
}

/** 重置搜索 */
function resetQuery() {
  proxy.$refs.queryFormRef?.resetFields()
  handleQuery()
}

/** 选择变化 */
function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.modelId)
  single.value = selection.length !== 1
  multiple.value = !selection.length
}

/** 新增 */
function handleAdd() {
  reset()
  open.value = true
  title.value = '添加模型'
}

/** 修改 */
function handleUpdate(row) {
  reset()
  const modelId = row.modelId || ids.value[0]
  api.getInfo(modelId).then(response => {
    form.value = response.data
    open.value = true
    title.value = '修改模型'
  })
}

/** 提交 */
function submitForm() {
  proxy.$refs.modelFormRef.validate(valid => {
    if (valid) {
      if (form.value.modelId) {
        api.edit(form.value).then(() => {
          proxy.$modal.msgSuccess('修改成功')
          open.value = false
          getList()
        })
      } else {
        api.add(form.value).then(() => {
          proxy.$modal.msgSuccess('新增成功')
          open.value = false
          getList()
        })
      }
    }
  })
}

/** 删除 */
function handleDelete(row) {
  const modelIds = row.modelId || ids.value
  proxy.$modal.confirm(`是否确认删除模型编号为"${modelIds}"的数据项？`).then(() => {
    return api.delete(modelIds)
  }).then(() => {
    getList()
    proxy.$modal.msgSuccess('删除成功')
  }).catch(() => {})
}

/** 取消 */
function cancel() {
  open.value = false
  reset()
}

// 初始化
getList()
</script>
```

### 4.4 动态路由配置

由于模块化结构使用 `src/modules/` 目录，需要在路由配置中正确引用：

#### 4.4.1 静态路由配置

在 `src/router/index.js` 中配置：

```javascript
// 静态路由配置
export const constantRoutes = [
  // ... 其他静态路由
]

// 模块化静态路由
export const moduleRoutes = [
  {
    path: '/ai/model',
    component: Layout,
    hidden: false,
    meta: { title: '模型管理', icon: 'user' },
    children: [
      {
        path: 'index',
        component: () => import('@/modules/ai/views/model/index.vue'),
        name: 'AiModel',
        meta: { title: '模型管理', icon: 'user', affix: true }
      }
    ]
  },
  {
    path: '/ai/chat',
    component: Layout,
    hidden: false,
    meta: { title: 'AI对话', icon: 'message' },
    children: [
      {
        path: 'index',
        component: () => import('@/modules/ai/views/chat/index.vue'),
        name: 'AiChat',
        meta: { title: 'AI对话', icon: 'message' }
      }
    ]
  }
]
```

#### 4.4.2 动态路由加载

如果需要从后端动态获取菜单并加载模块：

```javascript
// src/store/modules/user.js
import { moduleRoutes } from '@/router'

// 生成菜单树时，映射组件路径
function generateRoutes(routes, baseUrl = '/modules') {
  return routes.map(route => {
    const tmp = { ...route }
    if (tmp.children) {
      tmp.children = generateRoutes(tmp.children, baseUrl)
    } else {
      // 动态组件路径映射
      const componentPathMap = {
        'ai/model/index': () => import('@/modules/ai/views/model/index.vue'),
        'ai/chat/index': () => import('@/modules/ai/views/chat/index.vue'),
        'device/index': () => import('@/modules/device/views/index.vue'),
        'device/group/index': () => import('@/modules/device/views/group/index.vue')
      }
      const modulePath = `${tmp.path.replace('/', '')}/index`
      if (componentPathMap[modulePath]) {
        tmp.component = componentPathMap[modulePath]
      }
    }
    return tmp
  })
}

// 使用
function filterAsyncRoutes(routes) {
  const res = []
  routes.forEach(route => {
    const tmp = { ...route }
    if (tmp.component) {
      // 布局组件
      if (tmp.component === 'Layout') {
        tmp.component = Layout
      } else {
        // 模块化组件路径映射
        const componentMap = {
          'ai/model': () => import('@/modules/ai/views/model/index.vue'),
          'ai/chat': () => import('@/modules/ai/views/chat/index.vue'),
          'device': () => import('@/modules/device/views/index.vue'),
          'device/group': () => import('@/modules/device/views/group/index.vue')
        }
        const key = tmp.path.replace('/', '')
        if (componentMap[key]) {
          tmp.component = componentMap[key]
        }
      }
    }
    if (tmp.children) {
      tmp.children = filterAsyncRoutes(tmp.children)
    }
    res.push(tmp)
  })
  return res
}
```

### 4.5 组件规范

模块内组件统一放在 `components` 目录：

```
src/modules/ai/
├── api/
│   └── model.js
├── views/
│   ├── model/
│   │   └── index.vue
│   └── chat/
│       ├── index.vue
│       └── components/
│           ├── AiMessage.vue       # AI消息组件
│           └── ChatInput.vue       # 输入框组件
└── components/
    └── index.js                     # 统一导出
```

**组件统一导出** `components/index.js`:
```javascript
import AiMessage from './chat/components/AiMessage.vue'
import ChatInput from './chat/components/ChatInput.vue'

export default {
  install(app) {
    app.component('AiMessage', AiMessage)
    app.component('ChatInput', ChatInput)
  }
}
```

在 `main.js` 中注册：
```javascript
import aiComponents from '@/modules/ai/components'
app.use(aiComponents)
```

---

## 五、通用规范

### 5.1 命名规范

| 类型 | 规范 | 示例 |
|-----|------|------|
| Python类 | PascalCase | `AiModelService`, `AiModels` |
| Python变量/函数 | 蛇形小写 | `get_ai_model_list_services` |
| Python常量 | 全大写蛇形 | `MAX_CONNECTIONS` |
| 数据库字段 | 蛇形小写 | `model_id`, `create_time` |
| API请求参数 | 驼峰 | `modelCode`, `pageNum` |
| 前端变量 | 驼峰 | `modelList`, `queryParams` |
| 权限标识 | 冒号分隔 | `ai:model:list`, `ai:model:add` |

### 5.2 API响应格式

**成功响应**:
```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {}
}
```

**分页响应**:
```json
{
  "code": 200,
  "msg": "查询成功",
  "rows": [],
  "total": 0
}
```

### 5.3 状态码规范

| 值 | 说明 |
|---|------|
| '0' | 正常/启用 |
| '1' | 禁用/停用 |
| 'Y' | 是 |
| 'N' | 否 |

### 5.4 敏感信息处理

```python
# 后端脱敏
for row in rows:
    if 'apiKey' in row:
        row['apiKey'] = '********' * 3

# 前端密码输入
<el-input v-model="form.apiKey" type="password" placeholder="请输入API Key" />
```

### 5.5 日志规范

```python
from utils.log_util import logger

# Service层日志
logger.info('获取成功')
logger.info(f'获取model_id为{model_id}的信息成功')

# Controller层日志
logger.info(add_ai_model_result.message)
```

---

## 六、模块注册

在 `app.py` 中注册模块路由：

```python
from fastapi import FastAPI
from module_ai.controller.ai_model_controller import ai_model_controller
from module_ai.controller.ai_chat_controller import ai_chat_controller

app = FastAPI()

# 注册AI模块
app.include_router(ai_model_controller, prefix='/prod-api', tags=['AI管理'])
app.include_router(ai_chat_controller, prefix='/prod-api', tags=['AI管理'])
```

---

## 七、快速参考表

### 7.1 后端文件命名参考

| 层级 | 文件命名 | 类名示例 | 说明 |
|-----|---------|---------|------|
| DO | `xxx_do.py` | `XxxModels` | 数据库实体 |
| VO | `xxx_vo.py` | `XxxModel` | Pydantic模型 |
| DAO | `xxx_dao.py` | `XxxDao` | 数据访问层 |
| Service | `xxx_service.py` | `XxxService` | 业务逻辑层 |
| Controller | `xxx_controller.py` | - | API控制器 |

### 7.2 后端方法命名参考

| 层级 | 操作 | 方法命名示例 |
|-----|-----|-------------|
| DAO | 详情 | `get_xxx_detail_by_id` |
| DAO | 列表 | `get_xxx_list` |
| DAO | 新增 | `add_xxx_dao` |
| DAO | 编辑 | `edit_xxx_dao` |
| DAO | 删除 | `delete_xxx_dao` |
| Service | 列表 | `get_xxx_list_services` |
| Service | 详情 | `get_xxx_detail_services` |
| Service | 新增 | `add_xxx_services` |
| Service | 编辑 | `edit_xxx_services` |
| Service | 删除 | `delete_xxx_services` |
| Service | 校验 | `check_xxx_data_scope_services` |

### 7.3 前端文件命名参考

| 类型 | 文件路径 | 函数/组件名 | 说明 |
|-----|---------|-----------|------|
| API | `modules/ai/api/model.js` | `aiModelApi()` | 模型管理API工厂函数 |
| View | `modules/ai/views/model/index.vue` | `<script setup name="AiModel">` | 模型管理页面 |

### 7.4 前端API方法参考

| 操作 | 函数命名 | 使用示例 |
|-----|---------|---------|
| 列表 | `getList(params)` | `api.getList(queryParams)` |
| 所有 | `getAll()` | `api.getAll()` |
| 详情 | `getInfo(id)` | `api.getInfo(modelId)` |
| 新增 | `add(data)` | `api.add(formData)` |
| 编辑 | `edit(data)` | `api.edit(formData)` |
| 删除 | `delete(ids)` | `api.delete(modelIds)` |

### 7.5 权限标识参考

| 模块 | 操作 | 权限标识 |
|-----|-----|---------|
| ai | 列表 | `ai:model:list` |
| ai | 查询 | `ai:model:query` |
| ai | 新增 | `ai:model:add` |
| ai | 编辑 | `ai:model:edit` |
| ai | 删除 | `ai:model:remove` |
| device | 列表 | `device:list` |
| device | 新增 | `device:add` |
| device | 编辑 | `device:edit` |
| device | 删除 | `device:remove` |

### 7.6 API路由参考

| 方法 | 路径 | 功能 |
|-----|------|-----|
| GET | `/xxx/list` | 分页列表 |
| GET | `/xxx/all` | 不分页列表 |
| GET | `/xxx/{id}` | 详情 |
| POST | `/xxx` | 新增 |
| PUT | `/xxx` | 编辑 |
| DELETE | `/xxx/{ids}` | 删除 |
