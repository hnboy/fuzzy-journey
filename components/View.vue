<template>
  <div>
    <iframe :src="viewUrl" width="100%" height="500px"></iframe>
  </div>
</template>

<script>
export default {
  props: ['fileId'],
  computed: {
    viewUrl() {
      return `/view/${this.fileId}/index.html`;
    },
  },
};
</script>

