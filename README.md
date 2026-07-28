<div align="center">

# Nexus

</div>

一个用于学习 AI 开发的项目仓库，包含 LangChain、向量数据库、RAG 技术等实践代码。

## 项目结构

```
Nexus/
├── Agent/                    # 智能代理模块
│   ├── agent_middleware.py   # Agent中间件处理
│   ├── agent_stream.py       # Agent流式响应
│   └── agent_test.py         # Agent测试
├── Rag/                      # RAG核心模块
│   └── vector_store.py       # 向量存储服务
├── Rag_data/                 # RAG数据处理模块
│   ├── app_file_uploader.py  # 文件上传应用
│   ├── app_qa.py             # QA问答应用
│   ├── config_data.py        # 数据配置
│   ├── file_history_store.py # 对话历史存储
│   ├── knowledge_base.py     # 知识库管理
│   ├── rag.py                # RAG服务主入口
│   ├── run_app.py            # Streamlit应用启动器
│   └── vector_stores.py      # 向量存储接口
├── Test/                     # 测试模块
│   ├── Test_API_KEY.py       # API Key测试
│   ├── chat_history.py       # 对话历史测试
│   ├── chat_model.py         # 聊天模型测试
│   ├── cosine_similarity.py  # 余弦相似度计算
│   ├── embeddings_model.py   # 嵌入模型测试
│   ├── prompt_template.py    # 提示词模板测试
│   └── streaming_output.py   # 流式输出测试
├── config/                   # 配置文件目录
│   ├── agent.yml             # Agent配置
│   ├── chroma.yml            # Chroma向量数据库配置
│   ├── prompts.yml           # 提示词配置
│   └── rag.yml               # RAG系统配置
├── data/                     # 数据目录
│   ├── external/             # 外部数据
│   └── *.txt/pdf             # 知识库文档
├── model/                    # 模型工厂
│   └── factory.py            # 聊天模型和嵌入模型工厂
├── prompts/                  # 提示词模板
│   ├── main_prompt.txt       # 主提示词
│   ├── rag_prompt.txt        # RAG提示词
│   └── report_prompt.txt     # 报告提示词
├── utils/                    # 工具模块
│   ├── config_handler.py     # 配置文件加载
│   ├── file_handler.py       # 文件处理工具
│   ├── logger_handler.py     # 日志处理工具
│   ├── path_tools.py         # 路径处理工具
│   └── prompt_loader.py      # 提示词加载工具
├── .gitignore
├── README.md
├── requirements.txt          # 项目依赖
└── 提示词工程.md             # 提示词工程学习文档
```

## 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\Activate.ps1

# 使用requirements.txt安装依赖
pip install -r requirements.txt
```

## 配置说明

### API Key 配置

在项目根目录创建 `.env` 文件，配置你的 DashScope API Key：

```env
DASHSCOPE_API_KEY=your_api_key_here
```

### 配置文件

- `config/rag.yml`: RAG系统配置（聊天模型、嵌入模型名称）
- `config/chroma.yml`: Chroma向量数据库配置（集合名称、持久化路径、文档切分参数）
- `config/prompts.yml`: 提示词模板配置
- `config/agent.yml`: Agent配置

## 使用说明

### 运行单个Python文件

使用项目虚拟环境运行单个Python文件：

```bash
# 运行向量存储服务
venv\Scripts\python.exe Rag\vector_store.py

# 运行RAG服务
venv\Scripts\python.exe Rag_data\rag.py

# 运行Agent流式响应
venv\Scripts\python.exe Agent\agent_stream.py
```

### 启动Streamlit应用

```bash
# 方法一：通过run_app.py（自动切换虚拟环境）
python Rag_data/run_app.py

# 方法二：直接使用streamlit（需先激活虚拟环境）
venv\Scripts\Activate.ps1  # PowerShell
venv\Scripts\activate.bat  # CMD
streamlit run Rag_data/app_file_uploader.py --browser.gatherUsageStats=false --server.headless=true
```

## 技术栈

- Python 3.x
- LangChain（Runnable链、RAG检索、消息历史）
- DashScope（阿里云通义千问）
- ChromaDB（向量数据库）
- Streamlit（Web应用框架）

## 注意事项

- 请保护好你的 API Key，不要提交到代码仓库
- `.env` 文件已添加到 `.gitignore`，不会被提交
- 向量数据库文件（`chroma_db/`）已添加到 `.gitignore`
- 建议使用项目虚拟环境运行代码，避免依赖冲突