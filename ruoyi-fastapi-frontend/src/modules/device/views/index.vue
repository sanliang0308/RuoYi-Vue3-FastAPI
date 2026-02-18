<template>
  <div class="app-container">
    <el-form v-show="showSearch" ref="queryFormRef" :model="queryParams" :inline="true" label-width="68px">
      <el-form-item label="设备名称" prop="deviceName">
        <el-input
          v-model="queryParams.deviceName"
          placeholder="请输入设备名称"
          clearable
          style="width: 200px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="设备编码" prop="deviceCode">
        <el-input
          v-model="queryParams.deviceCode"
          placeholder="请输入设备编码"
          clearable
          style="width: 200px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="设备类型" prop="deviceType">
        <el-input
          v-model="queryParams.deviceType"
          placeholder="请输入设备类型"
          clearable
          style="width: 200px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="请选择状态" clearable style="width: 200px">
          <el-option label="正常" value="0" />
          <el-option label="离线" value="1" />
          <el-option label="故障" value="2" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          v-hasPermi="['device:model:add']"
          type="primary"
          plain
          icon="Plus"
          @click="handleAdd"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          v-hasPermi="['device:model:edit']"
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          v-hasPermi="['device:model:remove']"
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
        >删除</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList" />
    </el-row>

    <el-table v-loading="loading" :data="deviceList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="设备ID" align="center" prop="deviceId" width="80" />
      <el-table-column label="设备名称" align="center" prop="deviceName" :show-overflow-tooltip="true" />
      <el-table-column label="设备编码" align="center" prop="deviceCode" :show-overflow-tooltip="true" />
      <el-table-column label="设备类型" align="center" prop="deviceType" />
      <el-table-column label="设备型号" align="center" prop="deviceModel" :show-overflow-tooltip="true" />
      <el-table-column label="状态" align="center" prop="status" width="100">
        <template #default="scope">
          <el-switch
            v-model="scope.row.status"
            active-value="0"
            inactive-value="1"
            @change="handleStatusChange(scope.row)"
          />
        </template>
      </el-table-column>
      <el-table-column label="IP地址" align="center" prop="ipAddress" />
      <el-table-column label="MAC地址" align="center" prop="macAddress" />
      <el-table-column label="设备位置" align="center" prop="location" :show-overflow-tooltip="true" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width" width="180">
        <template #default="scope">
          <el-button
            v-hasPermi="['device:model:edit']"
            link
            type="primary"
            icon="Edit"
            @click="handleUpdate(scope.row)"
          >修改</el-button>
          <el-button
            v-hasPermi="['device:model:remove']"
            link
            type="primary"
            icon="Delete"
            @click="handleDelete(scope.row)"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total > 0"
      v-model:page="queryParams.pageNum"
      v-model:limit="queryParams.pageSize"
      :total="total"
      @pagination="getList"
    />

    <el-dialog v-model="open" :title="title" width="700px" append-to-body>
      <el-form ref="deviceFormRef" :model="form" :rules="rules" label-width="100px">
        <el-row>
          <el-col :span="12">
            <el-form-item label="设备名称" prop="deviceName">
              <el-input v-model="form.deviceName" placeholder="请输入设备名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="设备编码" prop="deviceCode">
              <el-input v-model="form.deviceCode" placeholder="请输入设备编码" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="设备类型" prop="deviceType">
              <el-input v-model="form.deviceType" placeholder="请输入设备类型" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="设备型号" prop="deviceModel">
              <el-input v-model="form.deviceModel" placeholder="请输入设备型号" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="设备状态" prop="status">
              <el-select v-model="form.status" placeholder="请选择设备状态" style="width: 100%">
                <el-option label="正常" value="0" />
                <el-option label="离线" value="1" />
                <el-option label="故障" value="2" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="IP地址" prop="ipAddress">
              <el-input v-model="form.ipAddress" placeholder="请输入IP地址" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="MAC地址" prop="macAddress">
              <el-input v-model="form.macAddress" placeholder="请输入MAC地址" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="设备位置" prop="location">
              <el-input v-model="form.location" placeholder="请输入设备位置" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="制造商" prop="manufacturer">
              <el-input v-model="form.manufacturer" placeholder="请输入制造商" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="供应商" prop="supplier">
              <el-input v-model="form.supplier" placeholder="请输入供应商" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form-item label="备注" prop="remark">
              <el-input v-model="form.remark" type="textarea" placeholder="请输入备注" :rows="3" />
            </el-form-item>
          </el-col>
        </el-row>
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

<script setup>
import { ref, reactive, toRefs, getCurrentInstance } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { deviceApi } from '@/modules/device/api'

const { proxy } = getCurrentInstance()
const api = deviceApi()

const deviceList = ref([])
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
    deviceName: undefined,
    deviceCode: undefined,
    deviceType: undefined,
    status: undefined
  },
  rules: {
    deviceName: [{ required: true, message: '设备名称不能为空', trigger: 'blur' }],
    deviceCode: [{ required: true, message: '设备编码不能为空', trigger: 'blur' }],
    deviceType: [{ required: true, message: '设备类型不能为空', trigger: 'blur' }],
    deviceModel: [{ required: true, message: '设备型号不能为空', trigger: 'blur' }],
    status: [{ required: true, message: '设备状态不能为空', trigger: 'change' }]
  }
})

const { queryParams, form, rules } = toRefs(data)

function getList() {
  loading.value = true
  api.getList(queryParams.value).then(response => {
    deviceList.value = response.rows
    total.value = response.total
    loading.value = false
  })
}

function cancel() {
  open.value = false
  reset()
}

function reset() {
  form.value = {
    deviceId: undefined,
    deviceName: undefined,
    deviceCode: undefined,
    deviceType: undefined,
    deviceModel: undefined,
    status: '0',
    ipAddress: undefined,
    macAddress: undefined,
    location: undefined,
    manufacturer: undefined,
    supplier: undefined,
    remark: undefined
  }
  if (proxy.$refs['deviceFormRef']) {
    proxy.$refs['deviceFormRef'].resetFields()
  }
}

function handleQuery() {
  queryParams.value.pageNum = 1
  getList()
}

function resetQuery() {
  if (proxy.$refs['queryFormRef']) {
    proxy.$refs['queryFormRef'].resetFields()
  }
  handleQuery()
}

function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.deviceId)
  single.value = selection.length !== 1
  multiple.value = !selection.length
}

function handleAdd() {
  reset()
  open.value = true
  title.value = '添加设备型号'
}

function handleUpdate(row) {
  reset()
  const deviceId = row.deviceId || ids.value[0]
  api.getInfo(deviceId).then(response => {
    form.value = response.data
    open.value = true
    title.value = '修改设备型号'
  })
}

function submitForm() {
  proxy.$refs['deviceFormRef'].validate(valid => {
    if (valid) {
      if (form.value.deviceId) {
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

function handleDelete(row) {
  const deviceIds = row.deviceId || ids.value
  proxy.$modal.confirm('是否确认删除设备编号为"' + deviceIds + '"的数据项？').then(function() {
    return api.delete(deviceIds)
  }).then(() => {
    getList()
    proxy.$modal.msgSuccess('删除成功')
  }).catch(() => {})
}

function handleStatusChange(row) {
  const text = row.status === '0' ? '启用' : '停用'
  proxy.$modal.confirm('确认要"' + text + '""' + row.deviceName + '"设备吗？').then(function() {
    return api.changeStatus(row.deviceId, row.status)
  }).then(() => {
    proxy.$modal.msgSuccess(text + '成功')
  }).catch(function() {
    row.status = row.status === '0' ? '1' : '0'
  })
}

getList()
</script>

<style scoped>
.mb8 {
  margin-bottom: 8px;
}
</style>
