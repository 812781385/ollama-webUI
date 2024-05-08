import CryptoJS from 'crypto-js'

interface Storage {
  value: any
  time: string | number
  expire: number
}

interface StorageConfig {
  prefix: string
  expire: number
  isEncrypt: boolean
}

export default class LocalStorageDataPlus {
  // 密钥 和 密钥偏移量
  private SECRET_KEY = CryptoJS.enc.Utf8.parse('3333e6e143439161')
  private SECRET_IV = CryptoJS.enc.Utf8.parse('e3bbe7e3ba84431a')

  private config: StorageConfig = {
    prefix: 'ollama_web_ui',
    expire: 1,
    isEncrypt: true
  }

  private static instance: LocalStorageDataPlus | null = null

  static getInstance() {
    if (!LocalStorageDataPlus.instance) {
      LocalStorageDataPlus.instance = new LocalStorageDataPlus()
    }
    return LocalStorageDataPlus.instance
  }

  // 添加后缀
  private autoAddPrefix(key: string) {
    const prefix = this.config.prefix ? `${this.config.prefix}_` : ''
    return prefix + key
  }

  // 移除已添加的前缀
  private autoRemovePrefix(key: string) {
    const len = this.config.prefix ? this.config.prefix.length + 1 : 0
    return key.substr(len)
  }

  /**
   * 加密方法
   * @param data
   * @returns {string}
   */
  private encrypt(data: any) {
    if (typeof data === 'object') {
      try {
        data = JSON.stringify(data)
      }
      catch (error) {
        // console.log("encrypt error:", error);
      }
    }
    const dataHex = CryptoJS.enc.Utf8.parse(data)
    const encrypted = CryptoJS.AES.encrypt(dataHex, this.SECRET_KEY, {
      iv: this.SECRET_IV,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7
    })
    return encrypted.ciphertext.toString()
  }

  /**
   * 解密方法
   * @param data
   * @returns {string}
   */
  private decrypt(data: any) {
    const encryptedHexStr = CryptoJS.enc.Hex.parse(data)
    const str = CryptoJS.enc.Base64.stringify(encryptedHexStr)
    const decrypt = CryptoJS.AES.decrypt(str, this.SECRET_KEY, {
      iv: this.SECRET_IV,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7
    })
    const decryptedStr = decrypt.toString(CryptoJS.enc.Utf8)
    return decryptedStr.toString()
  }

  // 设置 setStorage
  setStorage(key: string, value: any, expire = 0) {
    if (value === '' || value === null || value === undefined) {
      value = null
    }
    if (isNaN(expire) || expire < 0)
      throw new Error('Expire must be a number')
    expire = (expire || this.config.expire) * 1000
    const data: Storage = {
      value, // 存储值
      time: Date.now(), // 存值时间戳
      expire // 过期时间
    }

    const encryptString = this.config.isEncrypt ? this.encrypt(JSON.stringify(data)) : JSON.stringify(data)
    window.localStorage.setItem(this.autoAddPrefix(key), encryptString)
  }

  // 获取 getStorage
  getStorage(key: string) {
    key = this.autoAddPrefix(key)
    // key 不存在判断

    if (!window.localStorage.getItem(key) || JSON.stringify(window.localStorage.getItem(key)) === 'null') {
      return null
    }
    // 优化 持续使用中续期
    const storage = this.config.isEncrypt ? JSON.parse(this.decrypt(window.localStorage.getItem(key))) : JSON.parse(window.localStorage.getItem(key)!)
    const nowTime = Date.now()
    // 过期删除
    if (storage.expire && storage.expire < (nowTime - storage.time)) {
      this.removeStorage(key)
      return null
    }
    else {
      // 未过期期间被调用 则自动续期 进行保活
      // this.setStorage(this.autoRemovePrefix(key), storage.value);
      return storage.value
    }
  }

  // 是否存在 hasStorage
  hasStorage(key: string) {
    key = this.autoAddPrefix(key)
    const arr = this.getStorageAll().filter((item: any) => {
      return item.key === key
    })
    return !!arr.length
  }

  // 获取所有key
  getStorageKeys() {
    const items = this.getStorageAll()
    const keys = []
    for (let index = 0; index < items.length; index++) {
      keys.push(items[index].key)
    }
    return keys
  }

  // 根据索引获取key
  getStorageForIndex(index: number) {
    return window.localStorage.key(index)
  }

  // 获取localStorage长度
  getStorageLength() {
    return window.localStorage.length
  }

  // 获取全部 getAllStorage
  getStorageAll() {
    const len = window.localStorage.length // 获取长度
    const arr = [] // 定义数据集
    for (let i = 0; i < len; i++) {
      // 获取key 索引从0开始
      const getKey = window.localStorage.key(i)
      // 获取key对应的值
      const getVal = window.localStorage.getItem(getKey || '')
      // 放进数组
      arr[i] = { key: getKey, val: getVal }
    }
    return arr
  }

  // 删除 removeStorage
  removeStorage(key: string) {
    const reg = new RegExp(this.config.prefix)
    if (reg.test(key)) {
      key = this.autoRemovePrefix(key)
    }
    window.localStorage.removeItem(this.autoAddPrefix(key))
  }

  // 清空 clearStorage
  clearStorage() {
    window.localStorage.clear()
  }
}
