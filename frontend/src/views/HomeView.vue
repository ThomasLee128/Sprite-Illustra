<!--
文件名：HomeView.vue
功能描述：首页 - 文档上传页面。用户在此上传文档、选择模型和风格，启动处理。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] 实现文件上传区域（拖拽上传 + 点击上传）
      - 使用 FileUploader 组件
      - 支持 .txt, .md, .docx, .pdf
      - 显示文件大小限制提示（50MB）
- [ ] 实现模型选择区域
      - 使用 ModelSelector 组件选择文本模型和图片模型
      - 如果模型列表为空，提示用户先去设置页面配置
- [ ] 实现风格选择（flat/realistic/watercolor/sketch/cartoon/tech）
      - 卡片式 UI，每种风格配示意图标
- [ ] 实现"开始处理"按钮
      - 验证：已选文件 + 已选模型
      - 调用 uploadDocument -> startProcessing
      - 跳转到 /process/{taskId}
-->

<script setup lang="ts">
// TODO: 导入 stores 和 router
</script>

<template>
  <div class="space-y-8">
    <!-- 页面标题 -->
    <div class="text-center">
      <h1 class="text-3xl font-bold text-gray-900">智灵智能插图</h1>
      <p class="mt-2 text-gray-500">上传文档，AI 自动在合适的位置插入精美配图</p>
    </div>

    <!-- 文件上传区 -->
    <div class="bg-white rounded-lg shadow p-6">
      <h2 class="text-lg font-semibold text-gray-800 mb-4">1. 上传文档</h2>
      <!-- TODO: FileUploader 组件 -->
      <div class="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-indigo-400 transition-colors cursor-pointer">
        <p class="text-gray-400">拖拽文件到此处，或点击选择文件</p>
        <p class="text-sm text-gray-300 mt-2">支持 .txt .md .docx .pdf（最大 50MB）</p>
      </div>
    </div>

    <!-- 模型选择区 -->
    <div class="bg-white rounded-lg shadow p-6">
      <h2 class="text-lg font-semibold text-gray-800 mb-4">2. 选择 AI 模型</h2>
      <!-- TODO: ModelSelector 组件 x 2（文本模型 + 图片模型） -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">文案理解模型</label>
          <select class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm">
            <option>请先在设置页面拉取模型列表</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">图片生成模型</label>
          <select class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm">
            <option>请先在设置页面拉取模型列表</option>
          </select>
        </div>
      </div>
    </div>

    <!-- 风格选择区 -->
    <div class="bg-white rounded-lg shadow p-6">
      <h2 class="text-lg font-semibold text-gray-800 mb-4">3. 选择插图风格</h2>
      <!-- TODO: 风格卡片网格，点击切换选中状态 -->
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        <div class="border-2 border-indigo-500 rounded-lg p-3 text-center cursor-pointer bg-indigo-50">
          <div class="text-2xl mb-1">🎨</div>
          <div class="text-sm font-medium">扁平矢量</div>
        </div>
        <div class="border border-gray-200 rounded-lg p-3 text-center cursor-pointer hover:border-indigo-300">
          <div class="text-2xl mb-1">📷</div>
          <div class="text-sm font-medium">写实风格</div>
        </div>
        <div class="border border-gray-200 rounded-lg p-3 text-center cursor-pointer hover:border-indigo-300">
          <div class="text-2xl mb-1">💧</div>
          <div class="text-sm font-medium">水彩风格</div>
        </div>
        <div class="border border-gray-200 rounded-lg p-3 text-center cursor-pointer hover:border-indigo-300">
          <div class="text-2xl mb-1">✏️</div>
          <div class="text-sm font-medium">素描线稿</div>
        </div>
        <div class="border border-gray-200 rounded-lg p-3 text-center cursor-pointer hover:border-indigo-300">
          <div class="text-2xl mb-1">🎪</div>
          <div class="text-sm font-medium">卡通风格</div>
        </div>
        <div class="border border-gray-200 rounded-lg p-3 text-center cursor-pointer hover:border-indigo-300">
          <div class="text-2xl mb-1">⚙️</div>
          <div class="text-sm font-medium">科技示意</div>
        </div>
      </div>
    </div>

    <!-- 开始按钮 -->
    <div class="text-center">
      <button class="bg-indigo-600 text-white px-8 py-3 rounded-lg text-lg font-medium hover:bg-indigo-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed">
        开始智能配图
      </button>
    </div>
  </div>
</template>
