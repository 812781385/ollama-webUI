import ollama, json, re
from flask import Flask, request, Response, jsonify
from qwen_agent.llm import get_chat_model
from toolsApi import get_ZSAM_info, get_weather
from flask_cors import CORS
from tqdm import tqdm

ollama_url = 'http://127.0.0.1:11434/v1'

# 工具配置
tools = [
  {
    "name": "get_weather",
    "description": "获取城市天气",
    "parameters": {
      "type": "object",
      "properties": {
        "city": {
          "type": "string",
          "description": "城市地区city, " "例如： 厦门",
        }
      },
      "required": ["city"],
    },
  },
  {
    "name": "get_ZSAM_info",
    "description": "查询机场附近的气象",
    "parameters": {
      "type": "object",
      "properties": {},
      "required": [],
    },
  },
]
available_functions = {
  'get_ZSAM_info': get_ZSAM_info,
  'get_weather': get_weather,
}

# 服务接口
app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def create_stream_chat():
  request_data = request.get_json()
  messages = request_data.get('messages', [])
  id = request_data.get('id', 0)
  model = request_data.get('model', 'qwen:14b')

  llm_client = get_chat_model({
    'model': model,
    'model_server': ollama_url,
    'generate_cfg': {
      'top_p': 0.8
    }
  })

  print('新问题：', messages)
 
  def generate(llm_client, messages, id):
    print('---------第一轮message列表.....')
    print(json.dumps(messages, indent=2, ensure_ascii=False))
    response = llm_client.chat(
      messages=messages,  
      functions=tools,
      stream=True
    )

    pending_function_call = None
    pending_arguments = ""
    res_stream = []
    for res_stream in response:
        if 'function_call' in res_stream[0]:
          if pending_function_call is None:
            pending_function_call = res_stream[0]['function_call']['name']
          pending_arguments = res_stream[0]['function_call']['arguments']

          # 检查参数是否完整,如果能转换为json说明完整
          print('-----pending_arguments--', pending_arguments)
          try:
            json.loads(pending_arguments)
          except json.JSONDecodeError:
            # 参数不完整，跳过本次循环
            continue

          messages.append(res_stream[0])
          function_name = messages[-1]['function_call']['name']
          function_to_call = available_functions.get(function_name)

          print('------function_name', function_name)
          if function_to_call:
            function_args = json.loads(messages[-1]['function_call']['arguments'])
            print('------function_args', function_args)
            function_response = function_to_call(function_args)
          else:
            function_response = "在available_functions中找不到可用的函数"
          print('------接口返回-------')
          print(json.dumps(function_response, indent=2, ensure_ascii=False))

          messages.append({
            'role': 'function',
            'name': function_name,
            'content': function_response,
          })
          print('--------第二轮messages-------')
          print(json.dumps(messages, indent=2, ensure_ascii=False))
          updated_response = llm_client.chat(
            messages=messages,
            stream=True
          )

          for newres_stream in updated_response:
            truncated_text = f"{json.dumps(newres_stream, indent=2, ensure_ascii=False)[:200 - 3]}..."
            print(truncated_text)
            new_content = newres_stream[0]['content']
            res = {
              'id': id,
              'function_call': res_stream[0],
              'function_response': function_response,
              'text': re.sub(r'^[:\s]+', '', new_content)
            }
            yield json.dumps(res, ensure_ascii=False) + '\n'
               
        else:
          res = {
            'id': id,
            'text': res_stream[0]['content']
          }
        yield json.dumps(res, ensure_ascii=False) + '\n'

  generator = generate(llm_client, messages, id)
  return Response(generator, content_type='text/event-stream')

@app.route('/tags', methods=['POST'])
def get_tags():
  response = ollama.list()
  print(response)
  data = {
    'code': 0,
    'data': response['models']
  }
  return jsonify(data)
  
    
@app.route('/pull', methods=['POST'])
def pull_model():
  request_data = request.get_json()
  model = request_data.get('name')
  def generate():
    current_digest, bars = '', {}
    for progress in ollama.pull(model, stream=True):
      digest = progress.get('digest', '')
      
      if digest != current_digest and current_digest in bars:
        bars[current_digest].close()

      if digest not in bars and (total := progress.get('total')):
        bars[digest] = tqdm(total=total, desc=f'pulling {digest[7:19]}', unit='B', unit_scale=True)

      if completed := progress.get('completed'):
        bars[digest].update(completed - bars[digest].n)

      current_digest = digest

      yield json.dumps(progress, ensure_ascii=False) + '\n'
      if progress['status']=='success':
        yield 'OK\n'
        return
  return Response(generate(), content_type='text/event-stream')

@app.route('/delete', methods=['POST'])
def delet_model():
  request_data = request.get_json()
  model = request_data.get('name')
  response = ollama.delete(model)
  print(response)
  data = {
    'code': 200,
  }
  return jsonify(data)

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=7010)