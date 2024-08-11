<template>
  <v-container fluid>
    <v-row v-if="!isFileUploaded">
      <v-col cols="12">
        <UploadFile @file-uploaded="handleFileUploaded" />
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col cols="3">
        <SubtitlesList />
      </v-col>
      <v-col cols="9">
        <v-row>
          <v-col cols="12">
            <VideoPlayer />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
  import { useSubtitlesStore } from '@/stores/subtitlesStore'
  import { ref } from 'vue'
  import SubtitlesList from './SubtitlesList.vue'
  import VideoPlayer from './VideoPlayer.vue'

  import UploadFile from './UploadFile.vue'

  const isFileUploaded = ref(false)
  const subtitlesStore = useSubtitlesStore()

  const handleFileUploaded = jsonData => {
    isFileUploaded.value = true

    jsonData.forEach(item => {
      subtitlesStore.addSubtitle(item.text, item.start, item.end)
    })
  }
</script>
