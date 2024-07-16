<script setup lang="ts">
import { computed, onMounted, provide, ref } from 'vue'
import { RouterView } from 'vue-router'
import { ChatDotSquare, Delete, EditPen, Select, Setting, UserFilled } from '@element-plus/icons-vue'
import { generateRandom6DigitInteger } from './utils/util'
import SetChat from '@/components/setChat.vue'
import { useUserInfoStore } from '@/store'
import { chatAiConfigDefault, userInfoDefault } from '@/config'
import { publicApi } from '@/apis/index'

interface ChatITem {
  id: number
  name: string
  messages: any[]
}

const userInfoStore = useUserInfoStore()
const userInfo = computed(() => userInfoStore.getUserInfo)
const chatList = computed(() => userInfoStore.getChatList)
const activeChat = computed(() => userInfoStore.getActiveChat)
const chatAiConfig = computed(() => userInfoStore.getChatAiConfig)

const visibleErr = ref(false)
const dialogVisible = ref(false)
const editIng = ref('')
const tages: any = ref([])

async function init() {
  const tagesRes = await publicApi.getTags()

  tages.value = tagesRes.data ? tagesRes.data : []
  if (tages.value.length) {
    visibleErr.value = false
  }
  else {
    visibleErr.value = true
    return
  }
  if (!userInfo.value.name) {
    userInfoStore.updateUserInfo(userInfoDefault)
    userInfoStore.updateChatAiConfig({ ...chatAiConfigDefault, model: tages.value[0].name })
  }

  if (userInfoStore.getChatList.length < 1) {
    handleAddChat()
  }
}

function handleAddChat() {
  editIng.value = ''
  const chatItem: ChatITem = {
    id: generateRandom6DigitInteger(),
    name: 'New chat',
    messages: [
      { role: 'system', content: chatAiConfig.value.system }
    ]
  }
  userInfoStore.updateChatList(chatItem)
  userInfoStore.selectChatItem(chatItem)
}
function handleChatItem(item: ChatITem) {
  if (activeChat.value === item.id) {
    return
  }
  editIng.value = ''
  userInfoStore.selectChatItem(item)
}
function handleDeleteChat(item: ChatITem) {
  editIng.value = ''
  userInfoStore.deleteChatItem(item)
  if (activeChat.value === item.id && chatList.value.length) {
    userInfoStore.selectChatItem(chatList.value[0])
  }
}
function handleSet() {
  dialogVisible.value = true
}
function handleEdit(item: ChatITem) {
  editIng.value = item.name
}
function handleSave(item: ChatITem) {
  item.name = editIng.value
  userInfoStore.updateChatList(item)
  editIng.value = ''
}

onMounted(init)
provide('handleAddChat', handleAddChat)
</script>

<template>
  <div v-loading="visibleErr" element-loading-text="暂无模型，请先去服务器安装模型后再来使用！" class="common-layout dark">
    <el-container>
      <el-header>
        <div class="logo">
          <div class="img-text">
            {{ userInfo.logo }}
          </div>
          <div>{{ userInfo.logoName }}</div>
        </div>
        <div class="settings">
          <div class="left">
            <div class="img">
              <img :src="userInfo.avtar" alt="avtar">
            </div>
            <div>&emsp;{{ userInfo.name }}</div>
          </div>
          <div class="right">
            <el-icon size="22" @click="handleSet">
              <Setting />
            </el-icon>
          </div>
        </div>
      </el-header>
      <el-container>
        <el-aside class="custom-aside">
          <div class="logo">
            <div class="img-text">
              {{ userInfo.logo }}
            </div>
            <div>{{ userInfo.logoName }}</div>
          </div>
          <div class="add-btn" @click="handleAddChat">
            New chat
          </div>
          <div class="chat-list">
            <div
              v-for="item in chatList" :key="item.id" class="chat-item"
              :class="[activeChat === item.id ? 'chat-item-active' : '']" @click="handleChatItem(item)"
            >
              <el-input
                v-if="activeChat === item.id && editIng" v-model="editIng" class="chat-name"
                autofocus
                placeholder="Please input" size="small"
              />
              <template v-else>
                <el-icon>
                  <ChatDotSquare />
                </el-icon>
                &nbsp;
                <span class="chat-name">{{ item.name }}</span>
              </template>

              <template v-if="activeChat === item.id">
                <template v-if="editIng.length">
                  &emsp;<el-icon @click="handleSave(item)">
                    <Select />
                  </el-icon>
                </template>
                <template v-else>
                  &emsp;
                  <el-icon @click.stop="handleEdit(item)">
                    <EditPen />
                  </el-icon>
                  &nbsp;
                  <el-popconfirm
                    confirm-button-text="是" cancel-button-text="否" icon-color="#626AEF" title="确定删除?"
                    @confirm="handleDeleteChat(item)"
                  >
                    <template #reference>
                      <el-icon>
                        <Delete />
                      </el-icon>
                    </template>
                  </el-popconfirm>
                </template>
              </template>
            </div>
          </div>
          <div class="settings">
            <div class="left">
              <div class="img">
                <el-image
                  style="width: 100%"
                  :src="userInfo.avtar"
                  :zoom-rate="1.2"
                  :max-scale="7"
                  :min-scale="0.2"
                  :preview-src-list="[userInfo.avtar]"
                  :initial-index="0"
                  fit="cover"
                />
                <!-- <img :src="userInfo.avtar" alt="avtar"> -->
              </div>
              <div>&emsp;{{ userInfo.name }}</div>
            </div>
            <div class="right">
              <el-icon size="22" @click="handleSet">
                <Setting />
              </el-icon>
            </div>
          </div>
        </el-aside>
        <el-main class="custom-main">
          <RouterView />
        </el-main>
      </el-container>
    </el-container>
  </div>
  <SetChat v-model="dialogVisible" v-model:tages="tages" />
</template>

<style scoped lang="scss">
.el-input__wrapper {
  border: none !important;
}

.common-layout {
  width: 100vw;
  height: 100vh;
  overflow: hidden;

  .el-aside {
    height: 100vh;
    width: 200px;
    background: var(--vt-c-black-side);
    padding: 0 10px;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    flex-direction: column;
    position: relative;
    border-right: 1px solid var(--side-border-color);

    .logo {
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--vt-c-text-dark-1);
      font-weight: bold;
      width: 100%;
      font-family: fantasy;
      margin-top: 30px;

      .img-text {
        background-image: linear-gradient(to right, #2579ce, #16c0c1);
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
        font-size: 32px;
        font-weight: 800;
        padding-bottom: 0;
        line-height: 43px;
        height: 33px;
        display: inline-block;
        overflow: hidden;
        padding-right: 10px;
      }
    }

    .add-btn {
      border: 0.5px dashed var(--vt-c-text-dark-1);
      color: var(--vt-c-text-dark-1);
      line-height: 30px;
      margin-top: 30px;
      width: 130px;
      border-radius: 4px;
      text-align: center;
      user-select: none;
    }

    .add-btn:hover {
      color: #66b1ff;
      border-color: #66b1ff;
      cursor: pointer;
    }

    .chat-list {
      margin-top: 10px;
      height: calc(100% - 200px);
      width: 150px;
      overflow-y: scroll;
      box-sizing: border-box;
      padding: 10px;
      border-radius: 4px;

      .chat-item {
        border: 0.5px solid var(--vt-c-divider-dark-1);
        color: var(--vt-c-text-dark-1);
        line-height: 30px;
        margin-bottom: 10px;
        width: 100%;
        border-radius: 4px;
        text-align: center;
        display: flex;
        justify-content: flex-start;
        align-items: center;
        padding: 0 10px;
        font-size: 12px;

        .chat-name {
          width: 160px;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          user-select: none;
          text-align: left;
        }
      }

      .chat-item-active {
        color: #66b1ff;
        border-color: #66b1ff;
      }

      .chat-item:hover {
        color: #3375b9;
        border: 0.5px dashed #3375b9;
        cursor: pointer;
      }
    }

    .settings {
      color: var(--vt-c-text-dark-1);
      border-top: 0.5px solid var(--vt-c-divider-dark-1);
      width: 100%;
      height: 60px;
      position: absolute;
      left: 0;
      bottom: 0;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 13px;

      .left {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 13px;

        >div {
          width: 90px;
          font-weight: bold;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }

        .img {
          width: 40px;
          height: 40px;
          border-radius: 50%;
          overflow: hidden;

          img {
            width: 100%;
          }
        }
      }

      .right {
        height: 33px;
        width: 33px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
      }
    }
  }
}

.custom-tabs-label {
  display: flex;
  justify-content: center;
  align-items: center
}

.custom-main {
  background: var(--color-background);
  padding: 0;
}

@media screen and (min-width: 750px) {
  .el-header {
    display: none;
  }
}

@media screen and (max-width: 750px) {
  .el-aside {
    display: none!important;
  }
  .el-header {
    padding: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--vt-c-divider-dark-1);
    background-color: var(--vt-c-black-side-border);
    .logo {
      display: flex;
      align-items: center;
      justify-content: flex-start;
      .img-text {
        background-image: linear-gradient(to right, #2579ce, #16c0c1);
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
        font-size: 32px;
        font-weight: 800;
        display: inline-block;
        overflow: hidden;
        padding-right: 10px;
      }
    }
    .settings {
      color: var(--vt-c-text-dark-1);
      border-top: 0.5px solid var(--vt-c-divider-dark-1);
      height: 60px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 13px;

      .left {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 13px;

        >div {
          max-width: 100px;
          font-weight: bold;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }

        .img {
          width: 26px;
          height: 26px;
          border-radius: 50%;
          overflow: hidden;

          img {
            width: 100%;
          }
        }
      }

      .right {
        height: 20px;
        width: 20px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        padding-left: 10px;
      }
    }
  }
}
</style>
