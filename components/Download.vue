<template>
  <div>
    <a :href="downloadUrl" download>下载处理结果</a>
  </div>
</template>

<script>
export default {
  props: ['fileId'],
  computed: {
    downloadUrl() {
      return `/download/${this.fileId}/`;
    },
  },
};
</script>

