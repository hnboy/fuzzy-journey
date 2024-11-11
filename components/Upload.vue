i<template>
  <div>
    <input type="file" @change="uploadFile" />
  </div>
</template>

<script>
import axios from 'axios';

export default {
  methods: {
    async uploadFile(event) {
      const file = event.target.files[0];
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post('/upload/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      this.$emit('fileUploaded', response.data.file_id);
    },
  },
};
</script>

