<!-- components/SubtitlesList.vue -->
<template>
  <v-container>
    <v-row>
      <v-col>
        <v-list>
          <v-list-item
            v-for="(subtitle, index) in subtitles"
            :key="index"
          >
            <v-list-item-content>
              <v-text-field
                v-model="subtitle.text"
                dense
                label="Subtitle"
                @input="updateSubtitle(index, subtitle)"
              />
              <div class="time-fields">
                <!-- Editable Start Time -->
                <v-text-field
                  v-model="formattedInTimes[index]"
                  dense
                  label="Start Time"
                  @input="updateTime(index, 'inTime', formattedInTimes[index])"
                />
                <!-- Editable End Time -->
                <v-text-field
                  v-model="formattedOutTimes[index]"
                  dense
                  label="End Time"
                  @input="updateTime(index, 'outTime', formattedOutTimes[index])"
                />
              </div>
            </v-list-item-content>
            <v-list-item-action>
              <v-btn icon @click="deleteSubtitle(index)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </v-list-item-action>
          </v-list-item>
        </v-list>

        <v-btn class="mt-4" color="primary" @click="addSubtitle">
          Add New Subtitle
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
  import { ref, watch } from 'vue'
  import { useSubtitlesStore } from '@/stores/subtitlesStore'

  const subtitlesStore = useSubtitlesStore()
  const subtitles = subtitlesStore.subtitles

  const formattedInTimes = ref(subtitles.map(sub => formatTime(sub.inTime)))
  const formattedOutTimes = ref(subtitles.map(sub => formatTime(sub.outTime)))

  const addSubtitle = () => {
    if (subtitles.length === 0) {
      subtitlesStore.addSubtitle('', parseTime('00:00:000'), parseTime('00:02:000'))
      formattedInTimes.value.push(formatTime(0))
      formattedOutTimes.value.push(formatTime(2))
      return
    }

    const lastSubtitle = subtitles[subtitles.length - 1]
    subtitlesStore.addSubtitle('', lastSubtitle.outTime, lastSubtitle.outTime + 2)
    formattedInTimes.value.push(formatTime(lastSubtitle.outTime))
    formattedOutTimes.value.push(formatTime(lastSubtitle.outTime + 2))
  }

  const deleteSubtitle = index => {
    subtitlesStore.deleteSubtitle(index)
    formattedInTimes.value.splice(index, 1)
    formattedOutTimes.value.splice(index, 1)
  }

  const updateSubtitle = (index, subtitle) => {
    subtitlesStore.subtitles[index] = subtitle
  }

  const updateTime = (index, key, value) => {
    const seconds = parseTime(value)
    subtitlesStore.subtitles[index][key] = seconds

    // Update the formatted times array
    if (key === 'inTime') {
      formattedInTimes.value[index] = formatTime(seconds)
    } else if (key === 'outTime') {
      formattedOutTimes.value[index] = formatTime(seconds)
    }
  }

  // Convert time in seconds to mm:ss:ms format
  const formatTime = timeInSeconds => {
    const minutes = Math.floor(timeInSeconds / 60).toString().padStart(2, '0')
    const seconds = Math.floor(timeInSeconds % 60).toString().padStart(2, '0')
    const milliseconds = Math.floor((timeInSeconds % 1) * 1000)
      .toString()
      .padStart(3, '0')
    return `${minutes}:${seconds}:${milliseconds}`
  }

  // Convert time from mm:ss:ms format to seconds
  const parseTime = timeString => {
    const [minutes, seconds, milliseconds] = timeString.split(':').map(Number)
    return minutes * 60 + seconds + milliseconds / 1000
  }

  // Watch for changes in subtitles and update the formatted times
  watch(
    () => subtitles,
    newSubtitles => {
      formattedInTimes.value = newSubtitles.map(sub => formatTime(sub.inTime))
      formattedOutTimes.value = newSubtitles.map(sub => formatTime(sub.outTime))
    },
    { deep: true }
  )
</script>

<style scoped>
.time-fields {
  display: flex;
  gap: 10px;
}
</style>
