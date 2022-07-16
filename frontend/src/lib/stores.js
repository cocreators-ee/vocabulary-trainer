import { writable } from 'svelte/store'
import languages from '../languages/languages.json'

let wordCache
let cachedLanguage

async function getWords() {
  if (cachedLanguage !== _currentLanguage.code) {
    wordCache = (await import(`../languages/${_currentLanguage.code}/words.json`))
      .default
    cachedLanguage = _currentLanguage.code
  }
  return wordCache
}

export const currentLanguage = writable(languages[0])
let _currentLanguage
currentLanguage.subscribe(async (value) => {
  _currentLanguage = value
  await getWords()
})

function randInt(min, max) {
  return Math.floor(Math.random() * (max - min)) + min
}

function getRandomWord() {
  return wordCache[randInt(0, wordCache.length - 1)]
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
