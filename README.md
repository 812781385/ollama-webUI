# ollama-webUI
*自由化的ollama webUI界面。*

## 功能
1. 流式聊天：本地化存储，上下文流式的聊天。
2. 模型管理：拉取模型、删除模型、切换聊天模型。
3. 主题切换：暗黑/明亮主题切换，适配PC与移动端。
4. 界面信息修改：可修改界面信息如：logo、用户头像名称等
5. RAG配置：可配置向量数据库或提示模版
6. functioncall：又叫做工具调用，类似于openAI的functioncalling，使用qwen-agent模块，最好使用qwen32b及更大模型使用（目前只有python版本支持，nodejs可自行编码）
 
## 安装cliet
- `git clone https://github.com/812781385/ollama-webUI.git`
- `cd ./client`
- `pnpm i`
- `npm run dev`
- `修改.env 里的VITE_APP_AXIOS_BASE_URL 为自己的ip地址`

## serve有两个版本可以自己选择

## 1.安装nodejs版本serve
- `cd serve`
- `npm i   // 需要安装egg-init`
- `npm run dev`

## 2.安装python版本serve
- `cd python-serve`
- `pip install xxx // 安装所需依赖`
- `python app.py`

## 安装ollama
- 访问官网地址：`https://ollama.com/download`，选择适合自己系统。（如果你是linux，安装过程可能很慢。先更新curl）
- 启动服务：`ollama serve`，(如果发现端口被占用，可能是默认开机启动状态，macos和windows先关闭ollama，linux使用命令`service ollama stop`)
- 关闭服务： `command + C`，(如果你是linux使用`service ollama stop`)
- 后台启用：`nohup ollama serve > log.txt 2>&1 &`

## 安装chroma
- 如果你要使用RAG，请先安装chroma数据库，参见 https://docs.trychroma.com/getting-started
-  `chroma run // 启动数据库服务` 

### 演示
- 图片展示
<br>
<img src="https://my-mahjong.oss-cn-nanjing.aliyuncs.com/aiartImg/ollama1.png" width="500" height="300px" atl="图片描述" />
<img src="https://my-mahjong.oss-cn-nanjing.aliyuncs.com/aiartImg/ollama1.jpg" width="500" height="300px" atl="图片描述" />

- 视频演示
[![Watch the video](https://b23.tv/XNK0Sth)](https://b23.tv/XNK0Sth)
