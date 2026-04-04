<!--
文件名：DocumentPreview.vue
功能描述：文档预览组件。混排展示文档内容和插入的插图。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] 接收 props: illustratedDocument (IllustratedDocument 对象)
- [ ] 按 sections 顺序渲染文档内容：
      - HEADING -> <h1>~<h6> 标签
      - PARAGRAPH -> <p> 标签
      - LIST -> <ul><li> 标签
      - CODE -> <pre><code> 标签
      - BLOCKQUOTE -> <blockquote> 标签
- [ ] 每个 section 后检查是否有对应插图，如有则插入 IllustrationCard
- [ ] 整体使用 prose 样式（Tailwind Typography 或自定义）
-->

<script setup lang="ts">
// TODO: 定义 props
</script>

<template>
  <div class="prose max-w-none">
    <p class="text-gray-400 text-center py-8">文档内容将在此展示</p>
  </div>
</template>
