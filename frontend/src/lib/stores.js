import { writable } from 'svelte/store'
import languages from '../languages/languages.json'

export const currentLanguage = writable(languages[0])
let _currentLanguage
currentLanguage.subscribe((value) => (_currentLanguage = value))

async function loadWords(code) {
  return (await import(`../languages/${code}/words.json`)).default
}

function randInt(min, max) {
  return Math.floor(Math.random() * (max - min)) + min
}

async function getRandomWord() {
  let words = await loadWords(_currentLanguage.code)
  return words[randInt(0, words.length - 1)]
}

export const currentWord = writable(await getRandomWord())

export async function randomize(previousWord) {
  let nextWord = await getRandomWord()
  while (nextWord === previousWord) {
    nextWord = getRandomWord()
  }
  currentWord.set(nextWord)
}

export async function setLanguage(languageCode) {
  languages.forEach((value) => {
    if (value.code === languageCode) {
      currentLanguage.set(value)
    }
  })
  currentWord.set(await getRandomWord())
}
