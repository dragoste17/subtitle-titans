<template>
  <v-container>
    <v-row v-for="(subtitle, index) in subtitles" :key="index" class="my-2">
      <v-col cols="6">
        <v-text-field v-model="subtitle.text" label="Subtitle Text" />
      </v-col>
      <v-col cols="3">
        <v-text-field v-model="subtitle.inTime" label="In (00:00:00)" />
        <v-text-field v-model="subtitle.outTime" label="Out (00:00:00)" />
      </v-col>
      <v-col class="d-flex align-center" cols="1">
        <v-btn color="error" icon @click="deleteSubtitle(index)">
          <v-icon>mdi-delete</v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <v-btn color="primary" @click="addSubtitle">+ Add New Subtitles Line</v-btn>
  </v-container>
</template>

<script setup>
  import { useSubtitlesStore } from '@/stores/subtitlesStore'

  const subtitlesStore = useSubtitlesStore()
  const subtitles = subtitlesStore.subtitles

  const addSubtitle = () => {
    subtitlesStore.addSubtitle()
  }

  const deleteSubtitle = index => {
    subtitlesStore.deleteSubtitle(index)
  }
</script>
