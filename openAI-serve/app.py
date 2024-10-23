import json, re
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from tqdm import tqdm
from openai import OpenAI

gtp4o_token = '你的access token'

# 服务接口
app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def create_stream_chat():
  endpoint = "https://models.inference.ai.azure.com"
  model_name = "gpt-4o"
  llm_client = OpenAI(
    base_url=endpoint,
    api_key=gtp4o_token,
  )

  request_data = request.get_json()
  messages = request_data.get('messages', [])
  id = request_data.get('id', 0)

  def generate(messages, id):
    response = llm_client.chat.completions.create(
      messages=messages,
      model=model_name,
      stream=True
    )

    res = {
      'id': id,
      'text': ''
    }
    for update in response:
      delta_content = getattr(update.choices[0].delta, 'content', None)
      if delta_content is not None:
          res['text'] += delta_content
          print(delta_content)
          yield json.dumps(res, ensure_ascii=False) + '\n'
      else:
          print("No content in delta")
          

  generator = generate(messages, id)
  return Response(generator, content_type='text/event-stream')

@app.route('/tags', methods=['POST'])
def get_tags():
  data = {
    'code': 0,
    'data': [{
      'model': 'gpt-4o',
      'name': 'gpt-4o'
    }]
  }
  return jsonify(data)
  
@app.route('/pull', methods=['POST'])
def pull_model():
  data = {
    'code': 200,
  }
  return jsonify(data)

@app.route('/delete', methods=['POST'])
def delet_model():
  data = {
    'code': 200,
  }
  return jsonify(data)

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=7001)