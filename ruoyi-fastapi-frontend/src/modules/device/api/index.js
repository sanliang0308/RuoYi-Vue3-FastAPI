import request from '@/utils/request'

/**
 * 设备型号管理 API
 */
export function deviceApi() {
  return {
    getList: (params) => {
      return request({
        url: '/device/model/list',
        method: 'get',
        params
      })
    },
    getInfo: (deviceId) => {
      return request({
        url: `/device/model/get/${deviceId}`,
        method: 'get'
      })
    },
    add: (data) => {
      return request({
        url: '/device/model/add',
        method: 'post',
        data
      })
    },
    edit: (data) => {
      return request({
        url: '/device/model/edit',
        method: 'put',
        data
      })
    },
    delete: (deviceId) => {
      return request({
        url: `/device/model/delete/${deviceId}`,
        method: 'delete'
      })
    },
    changeStatus: (deviceId, status) => {
      return request({
        url: `/device/model/status/${deviceId}/${status}`,
        method: 'put'
      })
    }
  }
}

/**
 * 设备分组管理 API
 */
export function deviceGroupApi() {
  return {
    getList: (params) => {
      return request({
        url: '/device/group/list',
        method: 'get',
        params
      })
    },
    getTree: () => {
      return request({
        url: '/device/group/tree',
        method: 'get'
      })
    },
    add: (data) => {
      return request({
        url: '/device/group/add',
        method: 'post',
        data
      })
    },
    edit: (data) => {
      return request({
        url: '/device/group/edit',
        method: 'put',
        data
      })
    },
    delete: (groupId) => {
      return request({
        url: `/device/group/delete/${groupId}`,
        method: 'delete'
      })
    },
    getGroupDevices: (groupId) => {
      return request({
        url: `/device/group/device/list/${groupId}`,
        method: 'get'
      })
    },
    addGroupDevices: (data) => {
      return request({
        url: '/device/group/device/add',
        method: 'post',
        data
      })
    },
    removeGroupDevices: (data) => {
      return request({
        url: '/device/group/device/remove',
        method: 'delete',
        data
      })
    }
  }
}
