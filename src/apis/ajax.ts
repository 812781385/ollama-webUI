import axios from 'axios'

const instance = axios.create({
  baseURL: import.meta.env.VITE_APP_AXIOS_BASE_URL
})

/**
 * 请求拦截
 */
instance.interceptors.request.use((config) => {
  const { method, params } = config
  // 附带鉴权的token
  const headers: any = {
    token: localStorage.getItem('token')
  }
  // 不缓存get请求
  if (method === 'get') {
    headers['Cache-Control'] = 'no-cache'
  }
  // delete请求参数放入body中
  if (method === 'delete') {
    headers['Content-type'] = 'application/json;'
    Object.assign(config, {
      data: params,
      params: {}
    })
  }

  return {
    ...config,
    headers
  }
})

/**
 * 响应拦截
 */
instance.interceptors.response.use((v) => {
  if (v.data?.code === 401) {
    localStorage.removeItem('token')
    return v.data
  }
  if (v.status === 200) {
    return v.data
  }
  return Promise.reject(v)
})

export default instance
