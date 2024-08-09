<template>
  <v-footer app height="120">
    <v-container class="ma-0 fill-height" fluid>
      <v-row class="fill-height">
        <v-col class="py-0" cols="12">
          <div class="timeline-container">
            <v-chip
              v-for="(subtitle, index) in subtitles"
              :key="index"
              class="timeline-chip"
              :style="{
                left: `${calculateChipPosition(subtitle.inTime)}%`,
                width: `${calculateChipWidth(subtitle)}%`,
                'min-height': '90%'
              }"
              variant="elevated"
            >
              <div class="chip-content">
                <span class="subtitle-timing">
                  {{ formatTime(subtitle.inTime) }} ~ {{ formatTime(subtitle.outTime) }}
                </span>
                <v-spacer />
                <span class="justify-center align-center subtitle-text">
                  {{ subtitle.text || `Subtitle ${index + 1}` }}
                </span>
              </div>
            </v-chip>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script setup>
  import { useSubtitlesStore } from '@/stores/subtitlesStore'

  const subtitlesStore = useSubtitlesStore()
  const subtitles = subtitlesStore.subtitles

  const formatTime = timeInSeconds => {
    const minutes = Math.floor(timeInSeconds / 60).toString().padStart(2, '0')
    const seconds = Math.floor(timeInSeconds % 60).toString().padStart(2, '0')
    return `${minutes}:${seconds}`
  }

  // Calculate chip width based on subtitle duration relative to total video duration
  const calculateChipWidth = subtitle => {
    const videoDuration = 15 // Assume a 15-second video; adjust as needed
    const duration = subtitle.outTime - subtitle.inTime
    return (duration / videoDuration) * 100
  }

  // Calculate chip position based on subtitle start time relative to total video duration
  const calculateChipPosition = inTime => {
    const videoDuration = 15 // Assume a 15-second video; adjust as needed
    return (inTime / videoDuration) * 100
  }
</script>

<style scoped>
.timeline-container {
  position: relative;
  height: 100%;
  overflow: hidden;
}

.timeline-chip {
  position: absolute;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #6200ea;
  text-align: center;
  padding: 8px;
  box-sizing: border-box;
}

.chip-content {
  width: 100%;
  word-wrap: break-word;
}

.subtitle-timing {
  justify-content: space-between;
  width: 100%;
  font-size: 12px;
  color: #b5adad;
  margin-bottom: 4px;
}

.subtitle-text {
  margin-top: 4px;
  white-space: normal;
  word-wrap: break-word;
  color: white;
  text-align: center;
}
</style>
