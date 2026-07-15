# Nexus

一个用于学习 AI 开发的项目仓库，包含 OpenAI API、LangChain、向量数据库等技术的实践代码。

## 项目结构

```
Nexus/
├── Test/
│   ├── Test_API_KEY.py        # OpenAI API 测试（流式输出）
│   ├── chat_model.py          # 聊天模型初始化和基本调用
│   ├── prompt_template.py     # 提示词模板使用（零样本分类）
│   ├── embeddings_model.py    # 嵌入模型使用
│   ├── streaming_output.py    # 流式输出示例
│   └── cosine_similarity.py   # 余弦相似度计算
├── README.md
├── .gitignore
└── 提示词工程.md              # 提示词工程学习文档
```

## 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\Activate.ps1

# 安装依赖
pip install openai langchain langchain-community langchain-ollama langchain-openai dashscope chromadb
```

## 使用说明

1. **配置 API Key**：在代码中替换 `api_key` 参数为你的 API Key
2. **运行测试文件**：
   ```bash
   venv\Scripts\python.exe Test/chat_model.py
   ```

## 技术栈

- Python 3.x
- OpenAI API
- LangChain
- DashScope（阿里云）
- ChromaDB

## 注意事项

- 请保护好你的 API Key，不要提交到代码仓库
- 建议使用环境变量管理敏感信息
