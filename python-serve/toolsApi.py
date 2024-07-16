import requests
import pytz
from bs4 import BeautifulSoup

# 创建北京时区对象（等同于东八区）
bj_tz = pytz.timezone('Asia/Shanghai')

# 调用起飞机场和降落机场的气象信息
def get_ZSAM_info(args):
  base_url = 'http://www.hbt7.com/hbinfo/app/common/search/ZSAM'
  headers = {
      'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
      'x-requested-with': 'XMLHttpRequest',
  }
  response = requests.get(base_url, headers=headers)
  html_content = response.text
  soup = BeautifulSoup(html_content, 'html.parser')

  panel_inverse_elements = soup.select('.panel-inverse')

  result = []
  # 遍历所有找到的元素并打印文本内容
  for index, panel_inverse_element in enumerate(panel_inverse_elements):
    title_element = panel_inverse_element.find('h4', class_='panel-title')
    title_text = title_element.text

    stationinfo_element = panel_inverse_element.find('div', class_='panel-body')
    if index !=0 and stationinfo_element:
      
      if title_text == '机场报文':
        li_elements = stationinfo_element.find_all('li')
        stationinfo_text = ''
        for li_element in li_elements:
          li_text = li_element.text.strip().strip().replace('\n', ' ')
          stationinfo_text += f'{li_text}   '
      else:
        stationinfo_text = stationinfo_element.text
        stationinfo_text =  stationinfo_text.strip().replace('\n', ',').replace('\t', '').replace('\r', '').replace('\xa0', ' ').replace(',,', '')
      item = {
        'name': title_text,
        'content': stationinfo_text
      }
      result.append(item)
  return str(result)

def get_weather(args):
  city=args['city']
  return f"{city}的天气目前多云，温度26度，湿度20，空气优"
