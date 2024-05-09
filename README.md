# ollama-webUI
*自由化的ollama webUI界面。*

## 功能
1. 流式聊天：本地化存储，上下文流式的聊天。
2. 模型管理：拉取模型、删除模型、切换聊天模型。
3. 主题切换：暗黑/明亮主题切换，适配PC与移动端。
4. 界面信息修改：可修改界面信息如：logo、用户头像名称等
5. RAG配置：可配置向量数据库或提示模版
 
## 安装cliet
- `git clone https://github.com/812781385/ollama-webUI.git`
- `cd ./client`
- `pnpm i`
- `npm run dev`
- `修改.env 里的VITE_APP_AXIOS_BASE_URL 为自己的ip地址`

## 安装serve
- `cd serve`
- `npm i   // 需要安装egg-init`
- `npm run dev`

## 安装ollama
- 访问官网地址：`https://ollama.com/download`，选择适合自己系统。（如果你是linux，安装过程可能很慢。先更新curl）
- 启动服务：`ollama serve`，(如果发现端口被占用，可能是默认开机启动状态，macos和windows先关闭ollama，linux使用命令`service ollama stop`)
- 关闭服务： `command + C`，(如果你是linux使用`service ollama stop`)
- 后台启用：`nohup ollama serve > log.txt 2>&1 &`

## 安装chroma（如果你需要使用RAG请安装chroma数据库，参见 https://docs.trychroma.com/getting-started）
-  `chroma run // 启动数据库服务` 


视频演示
[![Watch the video](https://my-mahjong.oss-cn-nanjing.aliyuncs.com/aiartImg/ollama-webUI.mp4)](https://my-mahjong.oss-cn-nanjing.aliyuncs.com/aiartImg/ollama-webUI.mp4)
