<template>
  <v-container fluid>
    <v-row>
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
  import SubtitlesList from './SubtitlesList.vue'
  import VideoPlayer from './VideoPlayer.vue'
</script>
