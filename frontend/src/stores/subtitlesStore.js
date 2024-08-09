import { defineStore } from 'pinia'

export const useSubtitlesStore = defineStore('subtitles', {
  state: () => ({
    subtitles: [],
  }),
  actions: {
    addSubtitle () {
      this.subtitles.push({ text: '', inTime: '', outTime: '' })
    },
    deleteSubtitle (index) {
      this.subtitles.splice(index, 1)
    },
  },
})
