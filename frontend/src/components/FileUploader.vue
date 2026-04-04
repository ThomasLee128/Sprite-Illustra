<!--
文件名：FileUploader.vue
功能描述：文件上传组件。支持拖拽上传和点击选择，显示文件信息和格式验证。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] 实现拖拽上传（dragover/drop 事件）
- [ ] 实现点击选择（隐藏 input[type=file]，点击区域触发）
- [ ] 文件格式验证（.txt, .md, .docx, .pdf）
- [ ] 文件大小验证（<50MB）
- [ ] 选择后展示文件名、大小、格式图标
- [ ] emit('select', file) 向父组件传递选中的文件
- [ ] 支持清除已选文件
Props: accept (string[], 允许的扩展名), maxSize (number, 最大字节数)
Emits: select(file: File), clear()
-->

<script setup lang="ts">
// TODO: 实现组件逻辑
</script>

<template>
  <div class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-indigo-400 transition-colors cursor-pointer">
    <p class="text-gray-400">拖拽文件到此处，或点击选择文件</p>
    <p class="text-sm text-gray-300 mt-2">支持 .txt .md .docx .pdf（最大 50MB）</p>
  </div>
</template>
