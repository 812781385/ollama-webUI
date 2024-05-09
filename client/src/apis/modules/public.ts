import ajax from '../ajax'

/**
 * 流式聊天
 * @param params 参数
 * @param onDownloadProgress 下载进度回调
 */
function postChat(params: any, onDownloadProgress: any): Promise<{ num: number }> {
  return ajax.post('/chat', params, { onDownloadProgress })
}

/**
 * 本地模型列表
 */
function getTags(): Promise<{ num: number }> {
  return ajax.post('/tags')
}

/**
 * 拉取模型
 * @param name 模型名称，参考ollama官网
 * @param onDownloadProgress 下载进度回调
 */
function pullModel(name: string, onDownloadProgress: any): Promise<{ num: number }> {
  return ajax.post('/pull', { name }, { onDownloadProgress })
}

/**
 * 删除模型
 * @param name 模型名称，参考ollama官网
 * @param onDownloadProgress 下载进度回调
 */
function deleteModel(name: string): Promise<{ num: number }> {
  return ajax.post('/delete', { name })
}

/**
 * 向chroma添加数据
 */
function addData(dataList: string[]): Promise<{ num: number }> {
  return ajax.post('/addData', { dataList })
}

/**
 * 删除数据
 */
function deleteCollection(): Promise<{ num: number }> {
  return ajax.post('/deleteCollection')
}

export default {
  postChat,
  getTags,
  pullModel,
  deleteModel,
  addData,
  deleteCollection
}
