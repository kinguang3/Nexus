<div align="center">

# Nexus

</div>

基于 LangChain + LangGraph 的智能客服项目，实现 RAG 检索增强生成、Agent 工具调用和多轮对话。

## 项目结构

```
Nexus/
├── agent/                     # Agent 智能体模块
│   ├── react_agent.py         # ReAct Agent 实现
│   └── tools/
│       ├── agent_tools.py     # Agent 工具集合（RAG检索、天气查询等）
│       └── middleware.py      # Agent 中间件（工具监控、提示词切换）
├── Rag/                       # RAG 核心模块
│   ├── vector_store.py        # 向量存储服务（Chroma）
│   └── rag_service.py         # RAG 总结服务
├── config/                    # 配置文件
│   ├── agent.yml              # Agent 配置
│   ├── chroma.yml             # Chroma 向量数据库配置
│   ├── prompts.yml            # 提示词路径配置
│   └── rag.yml                # RAG 模型配置
├── data/                      # 知识库数据
├── model/                     # 模型工厂
│   └── factory.py             # 聊天模型/嵌入模型工厂
├── prompts/                   # 提示词模板
├── utils/                     # 工具模块
│   ├── config_handler.py      # 配置文件加载
│   ├── file_handler.py        # 文件处理工具
│   ├── logger_handler.py      # 日志工具
│   ├── path_tools.py          # 路径工具
│   └── prompt_loader.py       # 提示词加载
├── app.py                     # Streamlit 应用入口
├── requirements.txt           # 依赖清单
└── 错误日志.md                # 错误记录（不提交到Git）
```

## 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\Activate.ps1  # PowerShell
venv\Scripts\activate.bat  # CMD

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 API Key

在项目根目录创建 `.env` 文件：

```env
DASHSCOPE_API_KEY=your_api_key_here
```

### 3. 运行服务

```bash
# 启动 Web 应用
$env:PYTHONPATH='d:\Nexus;d:\Nexus\utils'; venv\Scripts\streamlit.exe run app.py --browser.gatherUsageStats=false --server.headless=true

# 单独运行 Agent 测试
$env:PYTHONPATH='d:\Nexus;d:\Nexus\utils'; venv\Scripts\python.exe agent\react_agent.py

# 单独运行 RAG 服务
$env:PYTHONPATH='d:\Nexus;d:\Nexus\utils'; venv\Scripts\python.exe Rag\vector_store.py
```

## 核心架构

### Agent 流程

```
用户输入 → ReactAgent → 工具调用循环 → 最终回答
                ↓
          ┌─────┴─────┐
          ↓           ↓
     RAG 检索     外部工具
  (知识库搜索)  (天气/用户数据)
```

### RAG 流程

```
用户问题 → 向量检索 → 召回文档 → 提示词模板 → LLM 总结
```

### 中间件

- `monitor_tool`: 工具调用监控
- `log_agent_model`: 模型调用日志
- `report_prompt_switch`: 动态提示词切换

## 技术栈

- **Python 3.x**
- **LangChain / LangGraph**: Agent 框架
- **ChromaDB**: 向量数据库
- **Streamlit**: Web 应用框架

## 注意事项

### 环境配置
- Python 版本要求：3.10+
- 必须使用项目虚拟环境运行，避免依赖冲突
- 运行前需设置 `PYTHONPATH` 包含 `d:\Nexus` 和 `d:\Nexus\utils`

### API Key
- 必须配置 `.env` 文件中的 `DASHSCOPE_API_KEY`，否则所有模型调用将失败
- `.env` 文件已在 `.gitignore` 中，**切勿手动添加到Git**

### 向量数据库
- 首次运行 `vector_store.py` 会自动加载 `data/` 目录下的文档
- 文档处理记录保存在 `chroma_db/md5.txt`，已处理的文档会跳过
- 如需重新加载所有文档，请删除 `chroma_db/` 目录

### 运行问题排查
- `ModuleNotFoundError: No module named 'xxx'` → 检查 `PYTHONPATH` 是否正确设置
- `ValueError: Function must have a docstring` → 工具函数必须有docstring描述
- `KeyError: 'xxx'` → 检查 `config/` 目录下的YAML配置文件键名是否正确
- `400 InvalidParameter` → 检查模型名称是否正确（嵌入模型用 `text-embedding-v1`，不是 `qwen-plus`）

### 开发规范
- 新增工具函数必须添加中文docstring描述
- 修改配置文件后需同步检查代码中的键名引用
- 错误日志（`错误日志.md`）不提交到Git