const { Controller } = require('egg');
const { Ollama } = require('ollama');
const { ChromaClient } = require('chromadb');

class ChatController extends Controller {

  // 列出本地模型
  async getTags() {
    const { ctx } = this;
    const ollama = new Ollama();
    const res = await ollama.list();
    ctx.body = {
      data: res.models,
      code: 200,
    };
  }

  // 删除模型
  async deleteModel() {
    const { ctx } = this;
    const { request } = ctx;
    const { name } = request.body;
    const ollama = new Ollama();
    const res = await ollama.delete({ model: name });
    ctx.body = {
      data: res.models,
      code: 200,
    };
  }

  // 拉取新模型
  async pullModel() {
    const { ctx } = this;
    const { request } = ctx;
    const { name } = request.body;

    ctx.set({
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      Connection: 'keep-alive',
    });

    const ollama = new Ollama();
    const response = await ollama.pull({ model: name, stream: true });
    ctx.status = 200;
    ctx.flushHeaders();

    for await (const part of response) {
      if (part.done) {
        ctx.res.end();
        return;
      }

      ctx.res.write(JSON.stringify(part) + '\n');
    }

    ctx.res.on('close', () => {
      console.log('连接断开');
    });
  }

  // 流式聊天
  async createStreamChat() {
    const { ctx } = this;
    const { request } = ctx;
    const { messages, id = 0, rag = '1', model = 'qwen:14b' } = request.body;
    const prompt = messages[messages.length - 1].content;
    ctx.set({
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      Connection: 'keep-alive',
    });

    const ollama = new Ollama();

    const data = [];
    // 使用rag，需要先安装chroma数据库
    if (rag === '1') {
      const client = new ChromaClient();
      const collection = await client.getOrCreateCollection({ name: 'rag' });

      const promptResponse = await ollama.embeddings({ prompt, model: 'mxbai-embed-large' });
      const results = await collection.query({
        queryEmbeddings: [ promptResponse.embedding ],
        nResults: 10,
      });
      results.distances[0].forEach((item, index) => {
        if (item < 50) {
          data.push(results.documents[0][index]);
        }
      });
    }

    const newMessages = JSON.parse(JSON.stringify(messages));
    newMessages[newMessages.length - 1] = {
      role: 'user',
      content: data.length ? `${data}.\n ${prompt}` : prompt,
    };

    const response = await ollama.chat({
      model,
      messages: newMessages,
      stream: true,
    });
    ctx.status = 200;
    ctx.flushHeaders();

    for await (const part of response) {
      if (part.done) {
        ctx.res.end();
        return;
      }
      const text = part.message.content;
      if (id) {
        ctx.res.write(JSON.stringify({ id, text }) + '\n');
      } else {
        ctx.res.write(text);
      }
    }

    ctx.res.on('close', () => {
      console.log('连接断开');
    });
  }

  // 添加数据到chaoma
  async addDataForDB() {
    const { ctx } = this;
    const { request } = ctx;
    const tests = [ '小虎的家乡来自安徽的，喜欢写代码和看书' ];
    const { dataList = tests } = request.body;

    const ollama = new Ollama();
    const client = new ChromaClient();
    const collection = await client.getOrCreateCollection({ name: 'rag' });

    // 添加数据
    for (let i = 0; i < dataList.length; i++) {
      const response = await ollama.embeddings({ model: 'mxbai-embed-large', prompt: dataList[i] });
      const embedding = response.embedding;
      await collection.add({
        ids: [ String(i) ],
        embeddings: [ embedding ],
        documents: [ dataList[i] ],
      });
    }

    ctx.body = {
      data: 'ok',
      code: 200,
    };
  }

  // 删除chaoma集合
  async deleteCollection() {
    const { ctx } = this;
    const client = new ChromaClient();
    const res = await client.deleteCollection({ name: 'rag' });
    ctx.body = {
      data: res,
      code: 200,
    };
  }

}

module.exports = ChatController;
