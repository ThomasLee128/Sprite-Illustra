<!--
文件名：SettingsView.vue
功能描述：API 聚合站设置页面。用户在此配置 API URL 和 Key，
         一键拉取模型列表，选择默认模型。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] 页面加载时调用 settingsStore.fetchSettings() 填充表单
- [ ] 实现表单：API 聚合站 URL 输入框、API Key 输入框（密码类型，带显示/隐藏切换）
- [ ] 实现"保存设置"按钮 -> settingsStore.saveSettings()
- [ ] 实现"一键拉取模型"按钮 -> settingsStore.pullModels()
      - 拉取中显示 loading 动画
      - 拉取成功后展示模型列表（分文本模型和图片模型两列）
      - 拉取失败显示错误提示
- [ ] 模型列表展示：表格形式，显示模型 ID 和提供者
- [ ] 默认模型选择：下拉框选择默认文本模型和图片模型
- [ ] 保存默认模型选择
-->

<script setup lang="ts">
// TODO: 导入 useSettingsStore, onMounted, ref
</script>

<template>
  <div class="max-w-3xl mx-auto space-y-8">
    <h1 class="text-2xl font-bold text-gray-900">API 设置</h1>

    <!-- API 配置表单 -->
    <div class="bg-white rounded-lg shadow p-6 space-y-4">
      <h2 class="text-lg font-semibold text-gray-800">聚合站配置</h2>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">API 聚合站 URL</label>
        <input
          type="url"
          placeholder="https://api.spiritgpu.com"
          class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
        />
        <p class="text-xs text-gray-400 mt-1">支持 New API / One API 等 OpenAI 兼容聚合服务</p>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">API Key</label>
        <div class="relative">
          <input
            type="password"
            placeholder="sk-..."
            class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
      </div>

      <div class="flex space-x-3">
        <button class="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm hover:bg-indigo-700 transition-colors">
          保存设置
        </button>
        <button class="bg-white border border-indigo-600 text-indigo-600 px-4 py-2 rounded-md text-sm hover:bg-indigo-50 transition-colors">
          一键拉取模型
        </button>
      </div>
    </div>

    <!-- 模型列表 -->
    <div class="bg-white rounded-lg shadow p-6 space-y-4">
      <h2 class="text-lg font-semibold text-gray-800">可用模型</h2>

      <!-- 文本模型 -->
      <div>
        <h3 class="text-sm font-medium text-gray-600 mb-2">文案理解模型（文本）</h3>
        <div class="bg-gray-50 rounded-md p-4 text-center text-gray-400 text-sm">
          请先拉取模型列表
        </div>
      </div>

      <!-- 图片模型 -->
      <div>
        <h3 class="text-sm font-medium text-gray-600 mb-2">图片生成模型</h3>
        <div class="bg-gray-50 rounded-md p-4 text-center text-gray-400 text-sm">
          请先拉取模型列表
        </div>
      </div>

      <!-- 默认模型选择 -->
      <div class="border-t pt-4">
        <h3 class="text-sm font-medium text-gray-600 mb-3">默认模型</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-xs text-gray-500 mb-1">默认文本模型</label>
            <select class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm">
              <option>暂无可选模型</option>
            </select>
          </div>
          <div>
            <label class="block text-xs text-gray-500 mb-1">默认图片模型</label>
            <select class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm">
              <option>暂无可选模型</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
