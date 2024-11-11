<template>
  <div>
    <h1>文件处理网站</h1>
    <Upload @fileUploaded="fileUploaded" />
    <View v-if="fileId" :fileId="fileId" />
    <Download v-if="fileId" :fileId="fileId" />
  </div>
</template>

<script>
import Upload from './components/Upload.vue';
import View from './components/View.vue';
import Download from './components/Download.vue';

export default {
  components: { Upload, View, Download },
  data() {
    return {
      fileId: null,
    };
  },
  methods: {
    fileUploaded(fileId) {
      this.fileId = fileId;
    },
  },
};
</script>

