<script setup lang="ts">
import { computed, inject, nextTick, onMounted, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Delete, DocumentCopy, MoreFilled } from '@element-plus/icons-vue'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import mdKatex from '@traptitech/markdown-it-katex'
import { marked } from 'marked'
import { copyText } from '../utils/util'
import { useUserInfoStore } from '@/store'
import { publicApi } from '@/apis/index'

interface ChatITem {
  id: number
  name: string
  messages: any[]
}

const handleAddChat: any = inject('handleAddChat')

marked.setOptions({
  gfm: true,
  breaks: false
})
const userInfoStore = useUserInfoStore()
const chatAiConfig = computed(() => userInfoStore.getChatAiConfig)
const userInfo = computed(() => userInfoStore.getUserInfo)
const messageList = computed(() => {
  const chatItem = userInfoStore.getChatList.filter((item: ChatITem) => item.id === userInfoStore.getActiveChat)[0]
  return chatItem?.messages || []
})

const loading = ref(false)
const loadingChat = ref(true)
const listRef: any = ref(null)

const mdi = new MarkdownIt({
  linkify: true,
  highlight(code: any, language: any) {
    const validLang = !!(language && hljs.getLanguage(language))
    if (validLang) {
      const lang = language ?? ''
      return highlightBlock(hljs.highlight(lang, code, true).value, lang)
    }
    return highlightBlock(hljs.highlightAuto(code).value, '')
  }
})
mdi.use(mdKatex, { blockClass: 'katexmath-block rounded-md p-[10px]', errorColor: ' #cc0000' })
const inputValue = ref('')

function highlightBlock(str: string, lang?: string) {
  // return `<pre class="code-block-wrapper"><div class="code-block-header"><span class="code-block-header__lang">${lang}</span><span class="code-block-header__copy">copyCode</span></div><code class="hljs code-block-body ${lang}">${str}</code></pre>`
  return `<pre class="code-block-wrapper"><div class="code-block-header"><span class="code-block-header__lang">${lang}</span></div><code class="hljs code-block-body ${lang}">${str}</code></pre>`
}

function scrollToBottom() {
  if (listRef.value) {
    const ulElement = listRef.value
    ulElement.lastElementChild && ulElement.lastElementChild.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }
}

function onDownloadProgress(event: any) {
  const xhr = event.target
  const { responseText } = xhr
  const test = responseText.split('\n')
  let id = 0
  let text = ''

  test.forEach((item: any) => {
    if (item.length) {
      const itemObj = JSON.parse(item)
      id = itemObj.id
      // text += itemObj.text
      // text = itemObj.text

      // python服务端启用了qwen-agent的functioncall，它的底层是全量返回所以直接覆盖
      const baseURL = import.meta.env.VITE_APP_AXIOS_BASE_URL
      if (baseURL.indexOf('7010') !== -1) {
        text = itemObj.text
      } else {
        text += itemObj.text
      }
    }
  })

  const assistantPromt = { role: 'assistant', content: text }

  const chatItem = userInfoStore.getChatList.filter((item: ChatITem) => item.id === id)[0]
  chatItem.messages[chatItem.messages.length - 1] = messageList.value[messageList.value.length - 1] = assistantPromt
  userInfoStore.updateChatList(chatItem)
}

async function handlerSubmit(e?: any) {
  if (e && e.type !== 'click' && (e.keyCode !== 13 || e.isComposing)) {
    return
  }
  if (e && e.keyCode === 13 && e.shiftKey) {
    return
  }
  if (inputValue.value.trim() === '' || loading.value) {
    return
  }
  loading.value = true

  if (!messageList.value.length) {
    handleAddChat()
  }

  const chatItem = userInfoStore.getChatList.filter((item: ChatITem) => item.id === userInfoStore.getActiveChat)[0]
  chatItem.messages.push({ role: 'user', content: inputValue.value })
  chatItem.messages.push({ role: 'assistant', content: '正在输入...' })
  userInfoStore.updateChatList(chatItem)

  const params = JSON.parse(JSON.stringify(messageList.value))
  params.pop()
  inputValue.value = ''
  const model = chatAiConfig.value.model
  const rag = chatAiConfig.value.rag

  const apiParams = {
    id: chatItem.id,
    model,
    rag,
    messages: params
  }

  // params.slice(0, params.length).forEach

  console.log('请求参数：', params)
  const res = await publicApi.postChat(apiParams, onDownloadProgress)
  loading.value = false

  const test = res.split('\n')

  const lastPart = test[test.length - 2]

  console.log(lastPart)
  if (lastPart.length > 10) {
    const lastPartObj = JSON.parse(lastPart)
    console.log(lastPartObj)

    if (lastPartObj.function_call) {
      const chatItem = userInfoStore.getChatList.filter((item: ChatITem) => item.id === userInfoStore.getActiveChat)[0]
      const index = chatItem.messages.length - 1

      const functionPromt = {
        role: 'function',
        name: lastPartObj.function_call.function_call.name,
        content: lastPartObj.function_response
      }

      chatItem.messages.splice(index, 0, functionPromt)

      chatItem.messages.splice(index, 0, lastPartObj.function_call)
      // messageList.value.splice(index, 0, functionPromt)
      userInfoStore.updateChatList(chatItem)
    }
  }

  console.log(userInfoStore.getChatList.filter((item: ChatITem) => item.id === userInfoStore.getActiveChat)[0])
}

function hancleCopy(idName: string) {
  copyText(idName, () => {
    ElMessage({
      message: '复制成功！',
      type: 'success'
    })
  })
}

function handleDelete(index: number) {
  const chatItem = userInfoStore.getChatList.filter((item: ChatITem) => item.id === userInfoStore.getActiveChat)[0]
  chatItem.messages = chatItem.messages.slice(0, index).concat(chatItem.messages.slice(index + 1))
  userInfoStore.updateChatList(chatItem)
}

onMounted(async () => {
  loadingChat.value = false
  nextTick(() => {
    scrollToBottom()
  })
})

watch(() => messageList.value, () => {
  nextTick(() => {
    scrollToBottom()
  })
}, {
  deep: true
})
</script>

<template>
  <main class="home-page">
    <div v-loading="loadingChat" class="wrapper-home-page">
      <ul ref="listRef" class="content">
        <li v-for="(item, index) in messageList" :key="index" :class="[{ 'is-empty': item.hasOwnProperty('function_call') || item.role === 'function' }, `is-${item.role}`]">
          <div class="wrapper">
            <template v-if="item.role !== 'user'">
              <div class="user">
                <img :src="userInfo.aiAvtar" alt="ai">
              </div>
              <div :id="`assistant-answer${index}`" class="answer markdown-body" v-html="mdi.render(item.content)" />
              <div v-if="!loading || (index !== messageList.length - 1)" class="set-more">
                <el-popover
                  placement="left"
                  :width="60"
                  trigger="hover"
                >
                  <template #reference>
                    <el-icon class="user-set-icon" size="13">
                      <MoreFilled />
                    </el-icon>
                  </template>
                  <div class="set-more-tool">
                    <div @click="hancleCopy(`assistant-answer${index}`)">
                      <el-button :icon="DocumentCopy" size="small" text>
                        复制
                      </el-button>
                    </div>
                    <div @click="handleDelete(index)">
                      <el-button :icon="Delete" size="small" text>
                        删除
                      </el-button>
                    </div>
                  </div>
                </el-popover>
              </div>
            </template>
            <template v-else>
              <div class="set-more">
                <el-popover
                  placement="left"
                  :width="60"
                  trigger="hover"
                >
                  <template #reference>
                    <el-icon class="user-set-icon" size="13">
                      <MoreFilled />
                    </el-icon>
                  </template>
                  <div class="set-more-tool">
                    <div @click="hancleCopy(`user-answer${index}`)">
                      <el-button :icon="DocumentCopy" size="small" text>
                        复制
                      </el-button>
                    </div>
                    <div @click="handleDelete(index)">
                      <el-button :icon="Delete" size="small" text>
                        删除
                      </el-button>
                    </div>
                  </div>
                </el-popover>
              </div>
              <div :id="`user-answer${index}`" class="answer">
                {{ item.content }}
              </div>
              <div class="user">
                <img :src="userInfo.avtar" alt="">
              </div>
            </template>
          </div>
        </li>
      </ul>

      <div class="input-wi">
        <el-input
          v-model="inputValue" :rows="1" class="input" type="input" placeholder="有问题尽管问我..."
          @keydown.enter="handlerSubmit"
        />
        &emsp;
        <el-button
          :loading="loading" :disabled="inputValue.length < 1" type="primary"
          @click="handlerSubmit"
        >
          发送
        </el-button>
      </div>
    </div>
  </main>
</template>

<style lang="scss">
  @import url(@/styles/lib/md.scss);
  .el-popper {
    padding: 5px!important;
  }
  .el-popover.el-popper {
    min-width: 70px!important;
  }
  .set-more-tool {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }

  @media screen and (max-width: 750px) {
    .el-main {
      padding: 0!important;
    }
  }
</style>

<style scoped lang="scss">
@media screen and (min-width: 750px) {
  .content {
    height: calc(100vh - 80px);
  }
}

@media screen and (max-width: 750px) {
  .content {
    height: calc(100vh - 130px);
  }
}
.wrapper-home-page {
  height: calc(100vh - 0px);
  background-color: var(--vt-c-black-side-border);
}

.content {
  overflow-y: auto;
  padding-left: 10px;
  padding-right: 10px;
  box-sizing: border-box;

  li {
    display: flex;
    overflow: hidden;
    margin-top: 20px;

    .wrapper {
      width: 80%;
      padding: 10px;
      color: var(--vt-c-text-dark-3);

      .set-more {
        display: flex;
        justify-content: center;
        align-items: flex-end;
        padding-left: 5px;
        padding-right: 5px;
        box-sizing: border-box;
        display: flex;
        align-items: flex-start;
        padding-top: 10px;
        cursor: pointer;
        .user-set-icon {
          transform: rotate(90deg);
          color: var(--more-tool-color);
        }
      }

      .answer {
        border-radius: 8px;
        background-color: var(--vt-c-divider-light-1);
        padding: 10px 15px;
        margin: 0;
        max-width: calc(100% - 80px);
      }

      .user {
        display: flex;
        align-items: flex-end;
        overflow: hidden;
        width: 32px;
        height: 32px;
        border-radius: 50%;

        img {
          width: 100%;
        }

        span {
          padding-left: 10px;
          font-size: 12px;
          color: #3c3c3c;
        }
      }
    }
  }

  .is-user {
    display: flex;
    justify-content: flex-end;

    .wrapper {
      display: flex;
      justify-content: flex-end;
      .answer {
        background-color: #a1dc95;
        background-color: var(--vt-c-divider-light-1);
        margin-right: 10px;
        color: var(--vt-c-text-dark-3);
      }
    }
  }

  .is-system, .is-assistant {
    display: flex;
    justify-content: flex-start;

    .wrapper {
      display: flex;
      justify-content: flex-start;

      .answer {
        margin-left: 10px;
      }
    }
  }
  .is-empty {
    display: none;
  }
}

.input-wi {
  margin-top: 20px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  padding-left: 10px;
  padding-right: 10px;

  .input {
    width: 95%;
  }
}

@media screen and (max-width: 750px) {
  .content {
    padding: 0;
    background-color: var(--vt-c-black-side-border);
    li {
      .wrapper {
        width: 100%;
        padding: 0;
        color: #3c3c3c;
        .set-more {
          display: none;
        }
      }
    }
  }
}
</style>
