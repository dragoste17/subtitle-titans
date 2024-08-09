<template>
  <v-footer app height="120">
    <v-container class="ma-0 fill-height" fluid>
      <v-row class="fill-height">
        <v-col class="py-0" cols="9" offset="3">
          <v-chip-group
            class="ml-6 fill-height"
            row
          >
            <!-- <v-chip
              v-for="(subtitle, index) in subtitles"
              :key="index"
              class="timeline-chip "
              :style="{ width: calculateChipWidth(subtitle) + '%', height: '90%' }"
            >
              <span class="subtitle-timing">
                {{ formatTime(subtitle.inTime) }} ~ {{ formatTime(subtitle.outTime) }}
              </span>
              <span class="justify-center align-center">
                {{ subtitle.text || `Subtitle ${index + 1}` }}
              </span>

            </v-chip> -->
            <v-chip
              v-for="(subtitle, index) in subtitles"
              :key="index"
              class="timeline-chip"
              :style="{ width: calculateChipWidth(subtitle) + '%', 'min-height': '90%' }"
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
          </v-chip-group>

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
    const milliseconds = Math.floor((timeInSeconds % 1) * 1000)
      .toString()
      .padStart(3, '0')
    return `${minutes}:${seconds}`
  }

  // Calculate chip width based on subtitle duration relative to total video duration
  const calculateChipWidth = subtitle => {
    const videoDuration = 15 // Assume a 60-second video; adjust as needed
    const duration = subtitle.outTime - subtitle.inTime
    return (duration / videoDuration) * 100
  }
</script>

<style scoped>
.subtitle-timing {
  justify-content: space-between;
  width: 100%;
  font-size: 12px;
  color: #b5adad;
  margin-bottom: 4px;
}

/*
.timeline-chip {
  margin: 2px 0;
  text-align: center;
  justify-content: center;

  color: white;
} */

.timeline-chip {
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

.subtitle-text {
  margin-top: 4px;
  white-space: normal;
  word-wrap: break-word;
  text-align: center;
}
</style>
