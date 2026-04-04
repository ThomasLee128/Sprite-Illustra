<!--
文件名：ModelSelector.vue
功能描述：模型选择下拉框组件。展示可用模型列表，支持搜索和选择。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] 接收 props: models (ModelInfo[]), modelValue (选中的模型ID), label (标签文字),
      placeholder (占位文字)
- [ ] 渲染 select 下拉框，option 展示模型 ID
- [ ] 支持搜索过滤（输入关键词过滤模型列表）
- [ ] 空列表时显示提示信息
- [ ] emit('update:modelValue', modelId) 实现 v-model
-->

<script setup lang="ts">
// TODO: 定义 props 和 emits
</script>

<template>
  <div>
    <label class="block text-sm font-medium text-gray-700 mb-1">{{ '模型选择' }}</label>
    <select class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500">
      <option value="">请选择模型</option>
    </select>
  </div>
</template>
