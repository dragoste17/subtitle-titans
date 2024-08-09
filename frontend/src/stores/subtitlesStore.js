import { defineStore } from 'pinia'

export const useSubtitlesStore = defineStore('subtitles', {
  state: () => ({
    subtitles: [],
  }),
  actions: {
    addSubtitle (text = '', inTime = 0, outTime = 2) {
      this.subtitles.push({ text, inTime, outTime })
    },
    deleteSubtitle (index) {
      this.subtitles.splice(index, 1)
    },
    convertToSRT () {
      return this.subtitles.map((subtitle, index) => {
        const t1 = formatTime(subtitle.inTime)
        const t2 = formatTime(subtitle.outTime)
        const startTime = convertTimeFormat(t1)
        const endTime = convertTimeFormat(t2)
        return `${index + 1}\n${startTime} --> ${endTime}\n${subtitle.text}\n`
      }).join('\n')
    },
  },
})

const formatTime = timeInSeconds => {
  const minutes = Math.floor(timeInSeconds / 60).toString().padStart(2, '0')
  const seconds = Math.floor(timeInSeconds % 60).toString().padStart(2, '0')
  const milliseconds = Math.floor((timeInSeconds % 1) * 1000)
    .toString()
    .padStart(2, '0')
  return `${minutes}:${seconds}:${milliseconds}`
}

function convertTimeFormat(timeStr) {
  // Convert mm:ss:ms to hh:mm:ss,ms
  const [minutes, seconds, milliseconds] = timeStr.split(':').map(Number)
  const hours = Math.floor(minutes / 60)
  const min = minutes % 60
  const sec = Math.floor(seconds)
  const ms = Math.floor(milliseconds)

  return `${String(hours).padStart(2, '0')}:${String(min).padStart(2, '0')}:${String(sec).padStart(2, '0')},${String(ms).padStart(3, '0')}`
}
