function generateRandom6DigitInteger() {
  // 定义最大和最小可能的6位数（不包括0）
  const minPossible = 10000
  const maxPossible = 99999

  // 使用Math.random()生成一个介于0到1之间的随机小数
  const randomDecimal = Math.random()

  // 将这个随机小数乘以最大值和最小值之间的范围，得到一个整数值
  const randomInteger = Math.floor(randomDecimal * (maxPossible - minPossible)) + minPossible

  // 返回生成的6位数随机整数
  return randomInteger
}

function copyText(idName: string, callback: any) {
  window.getSelection()?.removeAllRanges()
  const range = document.createRange()
  // 选中需要复制的节点
  range.selectNode(document.getElementById(idName))
  // 执行选中元素
  window.getSelection()?.addRange(range)
  // 执行 copy 操作
  const successful = document.execCommand('copy')
  if (successful) {
    callback()
  }
  // 移除选中的元素
  window.getSelection()?.removeAllRanges()
}

export {
  generateRandom6DigitInteger,
  copyText
}
