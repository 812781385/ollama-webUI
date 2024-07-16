const userInfoDefault = {
  name: '小虎',
  avtar: 'https://my-mahjong.oss-cn-nanjing.aliyuncs.com/aiartImg/111.png',
  aiAvtar: 'https://my-mahjong.oss-cn-nanjing.aliyuncs.com/aiartImg/mmexport1711704584738.jpg',
  logo: 'ollama',
  logoName: 'chatAi',
  language: '简体中文',
  Topic: 'dark'
}
const chatAiConfigDefault = {
  model: '',
  rag: '0',
  system: '### 你好！有什么我可以帮助你的吗？\n 作为你的智能伙伴，我既能写文案、想点子，又能陪你聊天、答疑解惑。', // system提示词
  chromadb: '',
  ragList: '我的名字叫小虎;我的家乡来自安徽的'
}

export {
  userInfoDefault,
  chatAiConfigDefault
}
