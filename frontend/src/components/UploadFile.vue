<template>
  <v-card>
    <v-card-title>Upload File</v-card-title>
    <v-card-subtitle>Select a file to upload</v-card-subtitle>
    <v-card-actions>
      <v-file-input
        v-model="file"
        accept="audio/mp3"
        label="Choose file"
        prepend-icon="mdi-file-mp3"
      />
      <v-btn
        color="primary"
        :disabled="!file"
        @click="uploadFile"
      >
        Upload File
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
  import { ref } from 'vue'
  import axios from 'axios'

  const file = ref(null)

  const uploadFile = async () => {
    if (!file.value) {
      alert('No file selected.')
      return
    }

    const formData = new FormData()
    formData.append('file', file.value)

    try {
      axios.defaults.baseURL = 'http://localhost:8000/';
      await axios.post('upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      // Emit event when the file is successfully uploaded
      emit('file-uploaded')
    } catch (error) {
      console.error('Error uploading file:', error)
      alert('Error uploading file.')
    }
  }
</script>

<style scoped>
/* Add your styles here */
</style>
