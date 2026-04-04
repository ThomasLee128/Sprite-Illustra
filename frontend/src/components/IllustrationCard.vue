<!--
文件名：IllustrationCard.vue
功能描述：单张插图卡片组件。展示 AI 生成的插图和相关操作。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] 接收 props: illustration (IllustrationItem 对象)
- [ ] 展示插图图片（img 标签，src 指向 /api/images/{filename}）
- [ ] 展示中文描述和英文 prompt
- [ ] 操作按钮行：
      - 重新生成（弹出对话框可修改 prompt）
      - 删除（确认对话框）
      - 上移/下移（调整位置）
- [ ] 加载中状态（generating 时显示骨架屏/loading 动画）
- [ ] 失败状态（显示错误信息和重试按钮）
Emits: regenerate(id, prompt?), remove(id), move(id, direction)
-->

<script setup lang="ts">
// TODO: 定义 props 和 emits
</script>

<template>
  <div class="border border-gray-200 rounded-lg overflow-hidden bg-white">
    <!-- 图片区 -->
    <div class="aspect-video bg-gray-100 flex items-center justify-center">
      <span class="text-gray-300">插图预览</span>
    </div>
    <!-- 信息和操作 -->
    <div class="p-3 space-y-2">
      <p class="text-sm text-gray-600">插图描述</p>
      <div class="flex space-x-2">
        <button class="text-xs text-indigo-600 hover:underline">重新生成</button>
        <button class="text-xs text-red-500 hover:underline">删除</button>
      </div>
    </div>
  </div>
</template>
