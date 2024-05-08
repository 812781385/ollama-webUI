import { defineStore } from 'pinia'
import LocalStorageDataPlus from '../localStorageDataPlus'

interface ChatITem {
  id: number
  name: string
  messages: any[]
}

const useUserInfoStore = defineStore('userInfo', {
  state: () => ({
    activeChat: LocalStorageDataPlus.getInstance().getStorage('activeChat') || 0,
    userInfo: LocalStorageDataPlus.getInstance().getStorage('messageList') || '',
    chatAiConfig: LocalStorageDataPlus.getInstance().getStorage('chatAiConfig') || '',
    chatList: LocalStorageDataPlus.getInstance().getStorage('chatList') || ''
  }),
  getters: {
    getUserInfo: (state) => {
      return state.userInfo ? JSON.parse(state.userInfo) : {}
    },
    getChatAiConfig: (state) => {
      return state.chatAiConfig ? JSON.parse(state.chatAiConfig) : {}
    },
    getChatList: (state) => {
      return state.chatList ? JSON.parse(state.chatList) : []
    },
    getActiveChat: (state) => {
      return state.activeChat || 0
    }
  },
  actions: {
    updateUserInfo(userInfo: any) {
      const userInfoStr = JSON.stringify(userInfo)
      this.userInfo = userInfoStr
      LocalStorageDataPlus.getInstance().setStorage('messageList', this.userInfo, 60 * 60 * 24 * 365 * 1)
    },
    updateChatAiConfig(chatAiConfig: any) {
      const chatAiConfigStr = JSON.stringify(chatAiConfig)
      this.chatAiConfig = chatAiConfigStr
      LocalStorageDataPlus.getInstance().setStorage('chatAiConfig', this.chatAiConfig, 60 * 60 * 24 * 365 * 1)
    },
    updateChatList(chatItem: ChatITem) {
      const list = this.chatList ? JSON.parse(this.chatList) : []

      const hasChatItem = list.some((item: ChatITem) => {
        if (item.id === chatItem.id) {
          item.messages = chatItem.messages
          item.name = chatItem.name
          return true
        }
        return false
      })
      if (!hasChatItem) {
        list.unshift(chatItem)
      }

      const chatListStr = JSON.stringify(list)
      this.chatList = chatListStr
      LocalStorageDataPlus.getInstance().setStorage('chatList', this.chatList, 60 * 60 * 24 * 365 * 1)
    },
    clearChatList() {
      const chatListStr = JSON.stringify([])
      this.chatList = chatListStr
      LocalStorageDataPlus.getInstance().setStorage('chatList', this.chatList, 60 * 60 * 24 * 365 * 1)
    },
    deleteChatItem(chatItem: ChatITem) {
      const oldList = this.chatList ? JSON.parse(this.chatList) : []
      const list = <ChatITem[]>[]

      oldList.forEach((item: ChatITem) => {
        if (item.id !== chatItem.id) {
          list.push(item)
        }
      })

      const chatListStr = JSON.stringify(list)
      this.chatList = chatListStr
      LocalStorageDataPlus.getInstance().setStorage('chatList', this.chatList, 60 * 60 * 24 * 365 * 1)
    },
    selectChatItem(chatItem: ChatITem) {
      this.activeChat = chatItem.id
      LocalStorageDataPlus.getInstance().setStorage('activeChat', this.activeChat, 60 * 60 * 24 * 365 * 1)
    }
  }
})

export default useUserInfoStore
