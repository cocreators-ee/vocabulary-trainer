import et from '../languages/et/words.json'
import fi from '../languages/fi/words.json'
import { writable } from 'svelte/store'
import languages from '../languages/languages.json'

const words = {
  et,
  fi,
}

export const currentLanguage = writable(languages[0])
let _currentLanguage
currentLanguage.subscribe((value) => (_currentLanguage = value))

function randInt(min, max) {
  return Math.floor(Math.random() * (max - min)) + min
}

function getRandomWord() {
  return words[_currentLanguage.code][
    randInt(0, words[_currentLanguage.code].length - 1)
  ]
}

export const currentWord = writable(getRandomWord())

export function randomize(previousWord) {
  let nextWord = getRandomWord()
  while (nextWord === previousWord) {
    nextWord = getRandomWord()
  }
  currentWord.set(nextWord)
}

export function setLanguage(languageCode) {
  languages.forEach((value) => {
    if (value.code === languageCode) {
      currentLanguage.set(value)
    }
  })
  currentWord.set(getRandomWord())
}
