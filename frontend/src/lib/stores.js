import et from '../languages/et/words.json'
import fi from '../languages/fi/words.json'
import { writable } from 'svelte/store'
import languages from '../languages/languages.json'

const words = {
  et,
  fi,
}

const currentLanguage = languages[0]

function randInt(min, max) {
  return Math.floor(Math.random() * (max - min)) + min
}

function getRandomWord() {
  return words[currentLanguage.code][randInt(0, words[currentLanguage.code].length - 1)]
}

export const currentWord = writable(getRandomWord())

export function randomize(previousWord) {
  let nextWord = getRandomWord()
  while (nextWord === previousWord) {
    nextWord = getRandomWord()
  }
  currentWord.set(nextWord)
}
