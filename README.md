# 智灵智能插图 (Sprite Illustra)

## 项目背景

作为一名拥有十年投资经验、最近投身 AI 创业的从业者，从上一个 [llm-api-detector](https://github.com/ThomasLee128/llm-api-detector) 项目（一个大模型检测系统，现已增加聚合站一键检测功能）开始接触 vibecoding。

我们智灵 AI 同时运营着[智灵 AI](https://serverless.datastone.cn/)——一个 GPU 分时租赁平台和[智灵 API](https://api.spiritgpu.com/)——一个 API 聚合站点。我坚定认为将自己作为平台使用者去深度使用自己产品才是最佳的产品改进方式。

所以有了我的人生中第二个 vibecoding 项目——智灵智能插图 (Sprite Illustra)，一个可以在纯文字文件里快速插入 AI 插图的应用。该应用完全按照我的使用需求开发（我是一个经常以文章形式进行输出但懒于配图的熟练键盘手），使用 Claude Code（Claude opus 4.6）模型进行架构搭建，使用 Trae 进行代码填充与后续调整。重在通过不同 vibecoding 工具的配合，达到对于稍复杂项目好钢花在刀刃上的优化，以降低开发成本。

## 项目概述

AI 驱动的文档智能配图工具。上传纯文字文档，AI 自动分析内容并在合适位置插入精美插图。

## 功能

- **文档解析**：支持 .txt、.md、.docx、.pdf 格式
- **AI 内容分析**：智能识别适合插图的位置，生成图片描述
- **AI 图片生成**：调用图片生成模型自动生成配图
- **多格式导出**：Word、Markdown、HTML（PDF 需额外配置）
- **预览与调整**：支持预览、删除、重新生成插图
- **一键PPT模式**：生成适合PPT演示的图文页面
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

## 使用教程

### 1. 配置 API（首次使用）

1. 点击页面顶部的"设置"标签
2. 填入您的 OpenAI 兼容 API 的 Base URL 和 API Key
3. 点击"拉取模型"按钮
4. 等待模型列表加载完成

### 2. 上传文档

1. 在首页拖拽文件到上传区域，或点击选择文件
2. 支持的格式：.txt、.md、.docx、.pdf
3. 文件大小限制：最大 50MB

### 3. 选择 AI 模型

1. **文案理解模型**：选择用于分析文档内容的文本模型
2. **图片生成模型**：选择用于生成插图的图片模型

### 4. 选择插图风格

提供以下风格选项：
- 🎨 扁平矢量：简洁现代的矢量插画
- 📷 写实风格：真实照片风格
- 🎨 水彩风格：水彩画效果
- ✏️ 素描风格：手绘线稿效果
- 🎭 卡通风格：卡通漫画风格
- ⚙️ 科技示意：科技/示意图风格
- 📊 PPT模式：生成适合PPT演示的图文页面

### 5. 开始处理

1. 点击"开始智能配图"按钮
2. 等待 AI 分析文档内容（第一阶段）
3. 查看预览：AI 会建议在哪些位置插入插图

### 6. 预览与确认

1. 预览页面会显示文档内容和计划的插图位置
2. 可以在此阶段修改或删除不需要的插图
3. 确认无误后点击"确认预览，开始生成"

### 7. 等待图片生成

1. AI 会根据描述自动生成插图
2. 进度条会显示当前生成进度
3. 生成完成后自动跳转到预览页面

### 8. 调整与优化

在预览页面可以对插图进行调整：
- **删除**：移除不需要的插图
- **重新生成**：对不满意的插图重新生成（可修改 prompt）
- **移动位置**：调整插图的位置（上下箭头）

### 9. 导出文档

1. 点击"导出文档"按钮
2. 选择导出格式：
   - Word (.docx)：适合继续编辑和打印
   - Markdown (.md)：适合技术文档和博客发布
   - HTML：适合网页展示，独立可用
3. 等待导出完成后自动下载

## 插图风格说明

### 普通插图模式
- 智能选择 3~8 个最有价值的位置插入插图
- 插图与文字内容混排，不影响阅读
- 适合制作技术文档、教程、博客等

### PPT模式
- 每一段内容都生成一张独立的PPT页面
- 包含完整的段落内容、清晰的排版、专业的配色
- 用户可以直接把图片插入PPT当讲解页面使用

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

---

# Sprite Illustra

## Project Background

As a professional with ten years of investment experience who has recently ventured into AI entrepreneurship, I started using vibecoding from my last project, [llm-api-detector](https://github.com/ThomasLee128/llm-api-detector) - a large model detection system that now includes one-click detection for API aggregators.

Our company, Spirit AI, operates both [Spirit AI](https://serverless.datastone.cn/) - a GPU time-sharing rental platform, and [Spirit API](https://api.spiritgpu.com/) - an API aggregator site. I firmly believe that deeply using our own products as platform users is the best way to improve them.

Hence came my second vibecoding project in life - Sprite Illustra, an application that can quickly insert AI illustrations into plain text documents. This application was developed entirely according to my usage needs (I'm a skilled typist who often produces content in article form but is lazy about adding illustrations), using Claude Code (Claude opus 4.6) for architecture design and Trae for code implementation and subsequent adjustments. The focus is on optimizing moderately complex projects through the collaboration of different vibecoding tools to reduce development costs.

## Project Overview

AI-powered document intelligent illustration tool. Upload plain text documents, and AI automatically analyzes content and inserts beautiful illustrations at appropriate positions.

## Features

- **Document Parsing**: Support .txt, .md, .docx, .pdf formats
- **AI Content Analysis**: Intelligently identify suitable positions for illustrations, generate image descriptions
- **AI Image Generation**: Call image generation models to automatically generate illustrations
- **Multi-format Export**: Word, Markdown, HTML (PDF requires additional configuration)
- **Preview and Adjustment**: Support preview, delete, regenerate illustrations
- **One-click PPT Mode**: Generate text-image pages suitable for PPT presentations
- **API Aggregator Integration**: One-click to fetch text and image model lists

## Technology Stack

- **Backend**: Python FastAPI + httpx
- **Frontend**: Vue 3 + TypeScript + Vite + Tailwind CSS + Pinia
- **AI Interface**: OpenAI compatible API (supports New API / One API aggregators)

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
# Visit http://localhost:8000/docs for API documentation
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# Visit http://localhost:5173
```

## Usage Guide

### 1. Configure API (First Time)

1. Click the "Settings" tab at the top of the page
2. Fill in your OpenAI compatible API Base URL and API Key
3. Click the "Fetch Models" button
4. Wait for the model list to load

### 2. Upload Document

1. Drag a file to the upload area on the homepage, or click to select a file
2. Supported formats: .txt, .md, .docx, .pdf
3. File size limit: Maximum 50MB

### 3. Select AI Models

1. **Text Understanding Model**: Select the text model for analyzing document content
2. **Image Generation Model**: Select the image model for generating illustrations

### 4. Select Illustration Style

The following style options are available:
- 🎨 Flat Vector: Clean modern vector illustrations
- 📷 Realistic: Authentic photo style
- 🎨 Watercolor: Watercolor painting effect
- ✏️ Sketch: Hand-drawn line art effect
- 🎭 Cartoon: Cartoon and comic style
- ⚙️ Tech Diagram: Technology/diagram style
- 📊 PPT Mode: Generate text-image pages suitable for PPT presentations

### 5. Start Processing

1. Click the "Start Intelligent Illustration" button
2. Wait for AI to analyze document content (Phase 1)
3. View preview: AI will suggest where to insert illustrations

### 6. Preview and Confirm

1. The preview page will show document content and planned illustration positions
2. You can modify or delete unwanted illustrations at this stage
3. Click "Confirm Preview, Start Generation" when satisfied

### 7. Wait for Image Generation

1. AI will automatically generate illustrations based on descriptions
2. Progress bar will show current generation progress
3. Automatically redirect to preview page when generation is complete

### 8. Adjust and Optimize

You can adjust illustrations on the preview page:
- **Delete**: Remove unwanted illustrations
- **Regenerate**: Regenerate unsatisfactory illustrations (can modify prompt)
- **Move Position**: Adjust illustration position (up/down arrows)

### 9. Export Document

1. Click the "Export Document" button
2. Select export format:
   - Word (.docx): Suitable for further editing and printing
   - Markdown (.md): Suitable for technical documents and blog publishing
   - HTML: Suitable for web display, standalone use
3. Wait for export to complete and automatically download

## Illustration Style Guide

### Normal Illustration Mode
- Intelligently select 3~8 most valuable positions to insert illustrations
- Illustrations are mixed with text content without affecting readability
- Suitable for creating technical documents, tutorials, blogs, etc.

### PPT Mode
- Generate an independent PPT page for each paragraph of content
- Includes complete paragraph content, clear layout, professional color scheme
- Users can directly insert images into PPT as presentation pages

## Project Structure

```
├── backend/
│   ├── main.py              # FastAPI entry
│   ├── config.py            # Configuration management
│   ├── api/                 # API routes
│   ├── schemas/             # Data models
│   ├── services/            # Business logic
│   ├── parsers/             # Document parsers (plugin-based)
│   ├── exporters/           # Document exporters (plugin-based)
│   └── core/                # Core utilities
└── frontend/
    └── src/
        ├── views/           # Page components
        ├── components/      # Common components
        ├── stores/          # Pinia state management
        └── api/             # API call wrappers
```

## Development Notes

This project is developed using the vibecoding pattern:
- **Claude Code**: Responsible for architecture design and skeleton building
- **Trea**: Responsible for code implementation and feature development

Each file has detailed TODO comments at the top describing the specific features that need to be implemented.
