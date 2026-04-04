<!--
文件名：ProgressTracker.vue
功能描述：进度追踪组件。展示任务处理的阶段进度条和状态信息。
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] 接收 props: phase, progress (0~1), message, illustrationCount, completedCount
- [ ] 渲染多阶段进度指示器（解析 -> 分析 -> 生图 -> 完成）
      - 已完成阶段显示绿色勾
      - 当前阶段显示蓝色动画
      - 未开始阶段显示灰色
- [ ] 渲染总进度条（百分比 + 动画过渡）
- [ ] 生图阶段显示 "第 N/M 张" 计数
- [ ] 失败状态显示红色错误信息
-->

<script setup lang="ts">
// TODO: 定义 props
</script>

<template>
  <div class="space-y-4">
    <div class="w-full bg-gray-200 rounded-full h-3">
      <div class="bg-indigo-600 h-3 rounded-full transition-all duration-500" style="width: 0%"></div>
    </div>
    <p class="text-center text-gray-500 text-sm">等待中...</p>
  </div>
</template>
