<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
import { CirclePlus, Delete, Moon, Operation, Sunny, UserFilled } from '@element-plus/icons-vue'
import { useDark, useToggle } from '@vueuse/core'
import { ElMessage } from 'element-plus'
import { useUserInfoStore } from '@/store'
import { publicApi } from '@/apis/index'

interface Props {
  modelValue?: boolean
  tages: any
}
const props = withDefaults(defineProps<Props>(), {
  modelValue: true,
  tages: []
})
const emit = defineEmits(['update:modelValue', 'update:tages'])

const userInfoStore = useUserInfoStore()
const userInfo = computed(() => userInfoStore.getUserInfo)
const chatAiConfig = computed(() => userInfoStore.getChatAiConfig)
const isDark = useDark({
  selector: 'html',
  valueDark: 'dark',
  valueLight: 'light'
})
const toggleDark = useToggle(isDark)

const modelName = ref('')
const deleteLoading = ref(false)
const deleteModelName = ref('')
const pullProgress = ref(0)
const dialogVisible = ref(false)
const formUserInfo = reactive({
  name: '',
  avtar: '',
  aiAvtar: '',
  logo: '',
  logoName: '',
  language: '简体中文',
  Topic: 'dark'
})
const formChatAiConfig = reactive({
  model: '',
  rag: '0',
  system: '',
  chromadb: ''
})

function handleCance() {
  emit('update:modelValue', false)
}

function handleToggleDark(status: boolean) {
  status && toggleDark()
}

function handleSave() {
  userInfoStore.updateUserInfo(formUserInfo)
  userInfoStore.updateChatAiConfig(formChatAiConfig)
  handleCance()
}

function onDownloadProgress(event: any) {
  const xhr = event.target

  // ollama run qwen:0.5b
  const { responseText } = xhr

  try {
    const test = responseText.split('\n')
    test.forEach((item: any) => {
      if (item.length) {
        const itemObj = JSON.parse(item)
        if (itemObj.completed && itemObj.total) {
          const percentage = (itemObj.completed / itemObj.total * 100).toFixed(2)
          percentage && (pullProgress.value = Number.parseFloat(percentage))
        }
      }
    })
  }
  catch (err) {
    pullProgress.value = 0
  }
}

async function handlePullModel() {
  pullProgress.value = 0.1
  await publicApi.pullModel(modelName.value, onDownloadProgress)
  ElMessage({ message: '模型拉取完成！', type: 'success' })

  const tagesRes = await publicApi.getTags()
  emit('update:tages', tagesRes.data ? tagesRes.data : [])
}

async function handleDeleteModel() {
  console.log(deleteModelName.value)
  deleteLoading.value = true
  const res = await publicApi.deleteModel(deleteModelName.value)
  console.log(res)

  if (res.code !== 200) {
    ElMessage({ message: '呀，出错了！', type: 'error' })
    return
  }
  const tagesRes = await publicApi.getTags()
  emit('update:tages', tagesRes.data ? tagesRes.data : [])

  ElMessage({ message: `模型: ${deleteModelName.value} 已删除！`, type: 'success' })
  deleteLoading.value = false
  deleteModelName.value = ''
}

function isMobile() {
  return window.innerWidth < 768
}

function handleClearChat() {
  userInfoStore.clearChatList()
  ElMessage({ message: '聊天记录已删除', type: 'success' })
}

function init() {
  for (const key in userInfo.value) {
    formUserInfo[key] = userInfo.value[key]
  }
  for (const key in chatAiConfig.value) {
    formChatAiConfig[key] = chatAiConfig.value[key]
  }
}

watch(() => props.modelValue, (state) => {
  dialogVisible.value = state
  init()
}, { immediate: true })
</script>

<template>
  <el-dialog
    v-model="dialogVisible"
    :width="isMobile() ? '90%' : '50%'"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    :show-close="false" draggable
  >
    <el-tabs class="demo-tabs">
      <el-tab-pane>
        <template #label>
          <span class="custom-tabs-label">
            <el-icon><UserFilled /></el-icon>
            <span>&nbsp;用户信息</span>
          </span>
        </template>
        <div class="content">
          <div class="row">
            <span class="row-label">应用名称</span>
            <el-input v-model="formUserInfo.logo" class="row-input" placeholder="图片地址或文字" clearable />
          </div>
          <div class="row">
            <span class="row-label">应用头像</span>
            <el-input v-model="formUserInfo.aiAvtar" class="row-input" placeholder="AI应用头像地址" clearable />
          </div>
          <div class="row">
            <span class="row-label">应用描述</span>
            <el-input v-model="formUserInfo.logoName" class="row-input" placeholder="应用名称" clearable />
          </div>
          <div class="row">
            <span class="row-label">用户名称</span>
            <el-input v-model="formUserInfo.name" class="row-input" placeholder="你的名称" clearable />
          </div>
          <div class="row">
            <span class="row-label">用户头像</span>
            <el-input v-model="formUserInfo.avtar" class="row-input" placeholder="你的头像地址" clearable />
          </div>
          <div class="row">
            <span class="row-label">清空聊天记录</span>
            <el-popconfirm
              confirm-button-text="是"
              cancel-button-text="否"
              icon-color="#F56C6C"
              title="确定删除?"
              @confirm="handleClearChat"
            >
              <template #reference>
                <el-button type="danger" :icon="Delete" />
              </template>
            </el-popconfirm>
          </div>
        </div>
      </el-tab-pane>

      <el-tab-pane>
        <template #label>
          <span class="custom-tabs-label">
            <el-icon><Operation /></el-icon>
            <span>&nbsp;配置</span>
          </span>
        </template>
        <div class="content">
          <div class="row">
            <span class="row-label">会话模型</span>
            <el-select v-model="formChatAiConfig.model" class="row-input" placeholder="当前模型">
              <el-option v-for="item in props.tages" :key="item.name" :label="item.name" :value="item.name" />
            </el-select>
          </div>
          <div class="row">
            <span class="row-label">拉取新模型</span>
            <div v-if="pullProgress" class="progress">
              <el-progress :text-inside="true" :stroke-width="18" :percentage="pullProgress" striped striped-flow size="small" />
            </div>
            <template v-else>
              <el-input v-model="modelName" class="row-input row-input-short" placeholder="输入新模型的name" clearable />
              &nbsp;
              <el-button type="primary" :icon="CirclePlus" :disabled="!modelName" @click="handlePullModel" />
            </template>
          </div>
          <div class="row">
            <span class="row-label">删除模型</span>
            <el-select v-model="deleteModelName" class="row-input row-input-short" placeholder="选择要删除的模型">
              <el-option v-for="item in props.tages" :key="item.name" :label="item.name" :value="item.name" />
            </el-select>
            &nbsp;
            <el-popconfirm
              confirm-button-text="是"
              cancel-button-text="否"
              icon-color="#F56C6C"
              title="确定删除?"
              @confirm="handleDeleteModel"
            >
              <template #reference>
                <el-button type="danger" :icon="Delete" :loading="deleteLoading" :disabled="!deleteModelName" />
              </template>
            </el-popconfirm>
          </div>

          <div class="row">
            <span class="row-label">system提示词</span>
            <el-input v-model="formChatAiConfig.system" type="textarea" class="row-input" placeholder="system提示词" clearable />
          </div>
          <div class="row">
            <span class="row-label">RAG开关</span>
            <el-select v-model="formChatAiConfig.rag" class="row-input" placeholder="当前模型">
              <el-option label="开" value="1" />
              <el-option label="关" value="0" />
            </el-select>
          </div>
          <div class="row">
            <span class="row-label">主题</span>
            <el-button :type="isDark ? 'info' : 'primary'" :icon="Sunny" size="small" circle @click="handleToggleDark(isDark)" />
            <el-button :type="isDark ? 'primary' : 'info'" :icon="Moon" size="small" circle @click="handleToggleDark(!isDark)" />
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleCance">
          取消
        </el-button>
        <el-button type="primary" @click="handleSave">
          确定
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped lang="scss">
.content {
  padding: 0 20px;
  padding-bottom: 40px;
  .row {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    margin-top: 20px;
    .row-label {
      display: inline-block;
      width: 100px;
    }
    .row-input {
      width: calc(100% - 200px);
    }
    .row-input-short {
      width: calc(100% - 250px);
    }
    .row-btn {
      margin-left: 10px;
    }
    .progress {
      width: calc(100% - 200px);
    }
  }

}
@media screen and (max-width: 750px) {
  .row-input {
    width: calc(100% - 100px)!important;
  }
  .progress {
    width: calc(100% - 100px)!important;
  }
}
</style>

<style>
.el-dialog__header {
  height: 10px!important;
  padding: 0!important;
  padding-bottom: 0!important;
}
.el-dialog__body {
  padding: 0 10px!important;
}
</style>
