# 智灵智能插图

AI 驱动的文档智能配图工具。上传纯文字文档，AI 自动分析内容并在合适位置插入精美插图。

## 功能

- **文档解析**：支持 .txt、.md、.docx、.pdf 格式
- **AI 内容分析**：智能识别适合插图的位置，生成图片描述
- **AI 图片生成**：调用图片生成模型自动生成配图
- **多格式导出**：Word、PDF、Markdown、HTML
- **API 聚合站集成**：一键拉取文本和图片模型列表

## 技术栈

- **后端**：Python FastAPI + httpx
- **前端**：Vue 3 + TypeScript + Vite + Tailwind CSS + Pinia
- **AI 接口**：OpenAI 兼容 API（支持 New API / One API 聚合站）

## 快速开始

### 后端

```bash
cd backend
pip install -r requirements.txt
python main.py
# 访问 http://localhost:8000/docs 查看 API 文档
```

### 前端

```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:5173
```

## 项目结构

```
├── backend/
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置管理
│   ├── api/                 # API 路由
│   ├── schemas/             # 数据模型
│   ├── services/            # 业务逻辑
│   ├── parsers/             # 文档解析器（插件式）
│   ├── exporters/           # 文档导出器（插件式）
│   └── core/                # 核心工具
└── frontend/
    └── src/
        ├── views/           # 页面组件
        ├── components/      # 通用组件
        ├── stores/          # Pinia 状态管理
        └── api/             # API 调用封装
```

## 开发说明

本项目采用 vibecoding 模式开发：
- **Claude Code**：负责架构设计和骨架搭建
- **Trea**：负责代码填充和功能实现

每个文件顶部都有详细的 TODO 注释，描述了需要实现的具体功能。
