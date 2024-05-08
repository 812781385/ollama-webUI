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

export default {
  postChat,
  getTags,
  pullModel,
  deleteModel
}
