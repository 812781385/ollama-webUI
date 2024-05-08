import type { App } from 'vue'

// 完整引入
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'

export default function mountElementUI(app: App<Element>) {
  app.use(ElementPlus, { locale: zhCn })
}
