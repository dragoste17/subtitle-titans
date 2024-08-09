import { defineStore } from 'pinia'

export const useSubtitlesStore = defineStore('subtitles', {
  state: () => ({
    subtitles: [],
  }),
  actions: {
    addSubtitle (text = '', inTime = '00:00:00', outTime = '00:02:00') {
      this.subtitles.push({ text, inTime, outTime })
    },
    deleteSubtitle (index) {
      this.subtitles.splice(index, 1)
    },
  },
})
