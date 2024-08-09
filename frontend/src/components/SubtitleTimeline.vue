<!-- components/SubtitleTimeline.vue -->
<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <!-- Main timeline slider (disabled, for visual reference only) -->
        <v-slider
          v-model="timelinePosition"
          class="mb-5"
          disabled
          max="100"
          min="0"
          step="1"
          thumb-label="always"
          tick-size="4"
          ticks="always"
        />

        <!-- Subtitle chunks as chips -->
        <div class="subtitle-chunks">
          <div
            v-for="(subtitle, index) in subtitles"
            :key="index"
            class="subtitle-chip-container"
            :style="getChunkStyle(subtitle)"
            @click="selectSubtitle(index)"
          >
            <div class="subtitle-timing">
              <span>{{ formatTime(subtitle.inTime) }}</span>
              <span>{{ formatTime(subtitle.outTime) }}</span>
            </div>
            <v-chip
              class="subtitle-chip"
              color="primary"
              pill
            >
              {{ subtitle.text || `Subtitle ${index + 1}` }}
            </v-chip>
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
  const selectedSubtitle = ref(0)
  const timelinePosition = ref(0)

  // Assuming the total video duration in seconds
  const totalDuration = 100 // Replace with actual video duration

  const selectSubtitle = index => {
    selectedSubtitle.value = index
  }

  // Format time (in seconds) to hh:mm:ss
  const formatTime = seconds => {
    const h = Math.floor(seconds / 3600).toString().padStart(2, '0')
    const m = Math.floor((seconds % 3600) / 60).toString().padStart(2, '0')
    const s = Math.floor(seconds % 60).toString().padStart(2, '0')
    return `${h}:${m}:${s}`
  }

  // Dynamically calculate the width and position of each subtitle chunk
  const getChunkStyle = subtitle => {
    const chunkDuration = subtitle.outTime - subtitle.inTime
    const startPercentage = (subtitle.inTime / totalDuration) * 100
    const widthPercentage = (chunkDuration / totalDuration) * 100

    return {
      left: `${startPercentage}%`,
      width: `${widthPercentage}%`,
    }
  }
</script>

<style scoped>
.subtitle-chunks {
  position: relative;
  height: 40px;
  margin-bottom: 20px;
}

.subtitle-chip-container {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
}

.subtitle-timing {
  display: flex;
  justify-content: space-between;
  width: 100%;
  font-size: 12px;
  color: #555;
  margin-bottom: 4px;
}

.subtitle-chip {
  width: 100%;
  text-align: center;
}
</style>
