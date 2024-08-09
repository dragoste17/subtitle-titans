<!-- components/VideoPlayerWithSubtitles.vue -->
<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12">
        <div class="video-container">
          <!-- HTML5 Video Player -->
          <video
            ref="videoPlayer"
            class="video-player"
            controls
            @timeupdate="updateSubtitle"
          >
            <source src="/Users/lav-shinde/Downloads/PXL_20240809_031057196.TS.mp4" type="video/mp4">
            Your browser does not support the video tag.
          </video>

          <!-- Subtitles Overlay -->
          <div class="subtitles-overlay">
            <div v-if="currentSubtitle" class="subtitle-text">
              {{ currentSubtitle.text }}
            </div>
          </div>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
  import { ref } from 'vue'
  import { useSubtitlesStore } from '@/stores/subtitlesStore'

  const subtitlesStore = useSubtitlesStore()
  const subtitles = subtitlesStore.subtitles
  const currentSubtitle = ref(null)
  const videoPlayer = ref(null)

  const updateSubtitle = () => {
    const currentTime = videoPlayer.value.currentTime
    const subtitle = subtitles.find(
      s => currentTime >= s.inTime && currentTime <= s.outTime
    )
    currentSubtitle.value = subtitle || null
  }
</script>

<style scoped>
.video-container {
  position: relative;
  width: 100%;
  max-height: 500px;
  background-color: black;
}

.video-player {
  width: 100%;
  height: auto;
}

.subtitles-overlay {
  position: absolute;
  top: 180%;
  width: 100%;
  text-align: center;
  pointer-events: none;
  /* Allow clicks to pass through */
}

.subtitle-text {
  display: inline-block;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  font-size: 32px;
  padding: 5px 10px;
  border-radius: 5px;
}
</style>
