## 使用免费的gpt-4o
*说明：使用的是github提供的Azure OpenAI的服务，可以无限薅羊毛*
- [地址](https://github.com/marketplace/models/azure-openai/gpt-4o)
- 进入后点击 右上角“Get API key”按钮
- 点击“Get developer key”
- 选择Beta版本“Generate new token”
- 然后授权进入，“token name”随便取，例如：gpt4，然后点击最下面的“Generate token”按钮
- 这时候会得到一个access token，复制到`./app.py的gtp4o_token变量中`
- 启动服务`python app.py`
