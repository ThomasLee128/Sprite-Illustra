<!--
文件名：PreviewView.vue
功能描述：插图预览与调整页面。展示处理结果，允许用户：
         - 查看文档内容和插入的插图
         - 删除不需要的插图
         - 重新生成不满意的插图（可修改 prompt）
         - 调整插图位置
作者：Claude Code
创建时间：2026-04-04
后续开发：Trea
TODO：
- [ ] 页面加载时获取 taskId，调用 documentStore.fetchResult(taskId)
- [ ] 渲染文档内容：按 sections 顺序展示标题、段落等
- [ ] 在对应位置插入 IllustrationCard 组件展示插图
- [ ] IllustrationCard 操作按钮：删除、重新生成、编辑 prompt
- [ ] 拖拽调整插图位置（可选，MVP 阶段可用上下箭头）
- [ ] 底部"导出文档"按钮 -> 跳转到 /export/{taskId}
- [ ] 使用 DocumentPreview 组件整合文档和插图的混排展示
-->

<script setup lang="ts">
// TODO: 导入 stores 和 router
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-900">预览与调整</h1>
      <button class="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors">
        导出文档
      </button>
    </div>

    <!-- 文档预览区 -->
    <div class="bg-white rounded-lg shadow p-8">
      <!-- TODO: DocumentPreview 组件，混排展示文档内容和插图 -->
      <div class="prose max-w-none">
        <p class="text-gray-400 text-center py-12">文档预览区域（待实现）</p>
      </div>
    </div>
  </div>
</template>
