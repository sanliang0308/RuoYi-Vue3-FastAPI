<template>
  <div>
    <AConfigProvider
      :theme="{
        algorithm: settingsStore.isDark
          ? theme.darkAlgorithm
          : theme.defaultAlgorithm,
      }"
    >
      <div class="pageHeaderContent">
        <div class="avatar">
          <a-avatar size="large" :src="currentUser.avatar" />
        </div>
        <div class="content">
          <div class="contentTitle">
            早安，
            {{ currentUser.name }}
            ，祝你开心每一天！
          </div>
          <div>{{ currentUser.title }} | {{ currentUser.department }}</div>
        </div>
        <div class="extraContent">
          <div class="statItem">
            <a-statistic title="设备总数" :value="deviceStats.total" />
          </div>
          <div class="statItem">
            <a-statistic title="在线设备" :value="deviceStats.online" value-style="color: #52c41a;" />
          </div>
          <div class="statItem">
            <a-statistic title="故障设备" :value="deviceStats.fault" value-style="color: #f5222d;" />
          </div>
        </div>
      </div>

      <div style="padding: 10px">
        <a-row :gutter="24">
          <a-col :xl="16" :lg="24" :md="24" :sm="24" :xs="24">
            <a-card
              class="deviceCard"
              :style="{ marginBottom: '24px' }"
              title="设备状态分布"
              :bordered="false"
              :loading="false"
              :body-style="{ padding: 0 }"
            >
              <div class="deviceOverview">
                <div class="overviewItem online">
                  <div class="icon">📱</div>
                  <div class="info">
                    <div class="count">{{ deviceStats.online }}</div>
                    <div class="label">在线设备</div>
                  </div>
                </div>
                <div class="overviewItem offline">
                  <div class="icon">📴</div>
                  <div class="info">
                    <div class="count">{{ deviceStats.offline }}</div>
                    <div class="label">离线设备</div>
                  </div>
                </div>
                <div class="overviewItem fault">
                  <div class="icon">⚠️</div>
                  <div class="info">
                    <div class="count">{{ deviceStats.fault }}</div>
                    <div class="label">故障设备</div>
                  </div>
                </div>
              </div>
            </a-card>
            <a-card
              :body-style="{ padding: 0 }"
              :bordered="false"
              class="activeCard"
              title="设备告警"
              :loading="false"
            >
              <a-list :data-source="deviceAlerts" class="activitiesList">
                <template #renderItem="{ item }">
                  <a-list-item :key="item.id">
                    <a-list-item-meta>
                      <template #title>
                        <span>
                          <a-tag :color="item.level === 'high' ? 'red' : item.level === 'medium' ? 'orange' : 'blue'">
                            {{ item.levelText }}
                          </a-tag>
                          <span class="alert-title">{{ item.title }}</span>
                        </span>
                      </template>
                      <template #avatar>
                        <a-avatar :style="{ backgroundColor: item.level === 'high' ? '#f56a00' : item.level === 'medium' ? '#7265e6' : '#1890ff' }">
                          {{ item.icon }}
                        </a-avatar>
                      </template>
                      <template #description>
                        <span class="alert-info">
                          <span>{{ item.deviceName }}</span>
                          <span class="datetime">{{ item.time }}</span>
                        </span>
                      </template>
                    </a-list-item-meta>
                  </a-list-item>
                </template>
              </a-list>
            </a-card>
          </a-col>
          <a-col :xl="8" :lg="24" :md="24" :sm="24" :xs="24">
            <a-card
              :style="{ marginBottom: '24px' }"
              title="设备类型分布"
              :bordered="false"
              :body-style="{ padding: 0 }"
            >
              <div class="deviceTypeChart">
                <div v-for="type in deviceTypes" :key="type.name" class="typeItem">
                  <span class="typeName">{{ type.name }}</span>
                  <a-progress 
                    :percent="type.percent" 
                    :stroke-color="type.color"
                    :show-info="false"
                    size="small"
                  />
                  <span class="typeCount">{{ type.count }}台</span>
                </div>
              </div>
            </a-card>
            <a-card
              :style="{ marginBottom: '24px' }"
              :bordered="false"
              title="快速操作"
            >
              <div class="quickActions">
                <a-button type="primary" block style="margin-bottom: 12px">
                  <template #icon><PlusOutlined /></template>
                  新增设备
                </a-button>
                <a-button block style="margin-bottom: 12px">
                  <template #icon><ToolOutlined /></template>
                  设备巡检
                </a-button>
                <a-button block style="margin-bottom: 12px">
                  <template #icon><FileSearchOutlined /></template>
                  设备查询
                </a-button>
                <a-button block>
                  <template #icon><ApartmentOutlined /></template>
                  设备分组
                </a-button>
              </div>
            </a-card>
          </a-col>
        </a-row>
      </div>
    </AConfigProvider>
  </div>
</template>

<script>
import {
  Progress,
  Row,
  Col,
  Card,
  List,
  ListItem,
  ListItemMeta,
  Avatar,
  Tag,
  Button,
  ConfigProvider,
  theme,
} from "ant-design-vue";
import "ant-design-vue/dist/reset.css";

export default {
  components: {
    AProgress: Progress,
    ARow: Row,
    ACol: Col,
    ACard: Card,
    AList: List,
    AListItem: ListItem,
    AListItemMeta: ListItemMeta,
    AAvatar: Avatar,
    ATag: Tag,
    AButton: Button,
    AConfigProvider: ConfigProvider,
  },
};
</script>

<script setup>
import { PlusOutlined, ToolOutlined, FileSearchOutlined, ApartmentOutlined } from "@ant-design/icons-vue";
import useSettingsStore from "@/store/modules/settings";

const settingsStore = useSettingsStore();

defineOptions({
  name: "DashBoard",
});

const currentUser = {
  avatar: "https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png",
  name: "管理员",
  userid: "00000001",
  title: "系统管理员",
  department: "设备管理部",
};

const deviceStats = {
  total: 128,
  online: 96,
  offline: 24,
  fault: 8,
};

const deviceAlerts = [
  {
    id: "alert-1",
    level: "high",
    levelText: "严重",
    icon: "⚠️",
    title: "设备温度过高",
    deviceName: "服务器-001",
    time: "5分钟前",
  },
  {
    id: "alert-2",
    level: "medium",
    levelText: "警告",
    icon: "📡",
    title: "网络连接不稳定",
    deviceName: "交换机-A3",
    time: "30分钟前",
  },
  {
    id: "alert-3",
    level: "low",
    levelText: "提示",
    icon: "🔄",
    title: "设备固件需要更新",
    deviceName: "摄像头-012",
    time: "2小时前",
  },
  {
    id: "alert-4",
    level: "medium",
    levelText: "警告",
    icon: "🔋",
    title: "备用电源电量低",
    deviceName: "UPS-002",
    time: "4小时前",
  },
];

const deviceTypes = [
  { name: "服务器", count: 32, percent: 75, color: "#1890ff" },
  { name: "网络设备", count: 28, percent: 65, color: "#52c41a" },
  { name: "摄像头", count: 45, percent: 85, color: "#722ed1" },
  { name: "传感器", count: 15, percent: 35, color: "#fa8c16" },
  { name: "其他", count: 8, percent: 15, color: "#8c8c8c" },
];
</script>

<style scoped lang="less">
.textOverflow() {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  word-break: break-all;
}

.clearfix() {
  zoom: 1;
  &::before,
  &::after {
    display: table;
    content: " ";
  }
  &::after {
    clear: both;
    height: 0;
    font-size: 0;
    visibility: hidden;
  }
}

.activitiesList {
  padding: 0 24px 8px 24px;
}

.alert-title {
  margin-left: 8px;
}

.alert-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.pageHeaderContent {
  display: flex;
  padding: 12px;
  margin-bottom: 24px;
  box-shadow: var(--el-box-shadow-light);
  .avatar {
    flex: 0 1 72px;
    & > span {
      display: block;
      width: 72px;
      height: 72px;
      border-radius: 72px;
    }
  }
  .content {
    position: relative;
    top: 4px;
    flex: 1 1 auto;
    margin-left: 24px;
    color: var(--el-text-color-secondary);
    line-height: 22px;
    .contentTitle {
      margin-bottom: 12px;
      color: var(--el-text-color-primary);
      font-weight: 500;
      font-size: 20px;
      line-height: 28px;
    }
  }
}

.extraContent {
  .clearfix();
  float: right;
  white-space: nowrap;
  .statItem {
    position: relative;
    display: inline-block;
    padding: 0 32px;
    > p:first-child {
      margin-bottom: 4px;
      color: var(--el-text-color-secondary);
      font-size: 14px;
      line-height: 22px;
    }
    > p {
      margin: 0;
      color: var(--el-text-color-primary);
      font-size: 30px;
      line-height: 38px;
      > span {
        color: var(--el-text-color-secondary);
        font-size: 20px;
      }
    }
    &::after {
      position: absolute;
      top: 8px;
      right: 0;
      width: 1px;
      height: 40px;
      background-color: var(--el-border-color);
      content: "";
    }
    &:last-child {
      padding-right: 0;
      &::after {
        display: none;
      }
    }
  }
}

.deviceOverview {
  display: flex;
  padding: 24px;
  .overviewItem {
    flex: 1;
    display: flex;
    align-items: center;
    padding: 16px;
    margin: 0 8px;
    border-radius: 8px;
    &.online {
      background: #f6ffed;
      .icon { font-size: 40px; }
      .count { color: #52c41a; }
    }
    &.offline {
      background: #f5f5f5;
      .icon { font-size: 40px; }
      .count { color: #8c8c8c; }
    }
    &.fault {
      background: #fff1f0;
      .icon { font-size: 40px; }
      .count { color: #f5222d; }
    }
    .info {
      margin-left: 16px;
      .count {
        font-size: 28px;
        font-weight: bold;
      }
      .label {
        color: var(--el-text-color-secondary);
        font-size: 14px;
      }
    }
  }
}

.deviceTypeChart {
  padding: 16px 24px;
  .typeItem {
    display: flex;
    align-items: center;
    margin-bottom: 12px;
    .typeName {
      width: 80px;
      color: var(--el-text-color-primary);
    }
    .typeCount {
      width: 60px;
      text-align: right;
      color: var(--el-text-color-secondary);
      font-size: 12px;
    }
  }
}

.quickActions {
  padding: 16px;
}

.datetime {
  color: var(--el-text-color-placeholder);
}

@media screen and (max-width: 1200px) and (min-width: 992px) {
  .activeCard {
    margin-bottom: 24px;
  }
}

@media screen and (max-width: 992px) {
  .activeCard {
    margin-bottom: 24px;
  }
}

@media screen and (max-width: 768px) {
  .extraContent {
    margin-left: -16px;
  }
}

@media screen and (max-width: 576px) {
  .pageHeaderContent {
    display: block;
    .content {
      margin-left: 0;
    }
  }
  .extraContent {
    .statItem {
      float: none;
    }
  }
}
</style>
