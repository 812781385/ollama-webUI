// 固定的响应格式
interface BaseResponse<T = any> {
  code: number
  errMsg: string
  data: T
}

type ResponseData<T = any> = Promise<BaseResponse<T>>
