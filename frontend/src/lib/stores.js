import { writable } from 'svelte/store'
import languages from '../languages/languages.json'

let wordCache
let cachedLanguage

export const currentLanguage = writable(languages[0])
let _currentLanguage
currentLanguage.subscribe(async (value) => {
  _currentLanguage = value
  await getWords()
})

async function getWords() {
  if (cachedLanguage !== _currentLanguage.code) {
    wordCache = (await import(`../languages/${_currentLanguage.code}/words.json`))
      .default
    cachedLanguage = _currentLanguage.code
  }
  return wordCache
}

function randInt(min, max) {
  return Math.floor(Math.random() * (max - min)) + min
}

async function getRandomWord() {
  let words = await getWords()
  return words[randInt(0, words.length - 1)]
}

const NO_WORD = { source: '', translations: [] }
export const currentWord = writable(NO_WORD)

async function init() {
  currentWord.set(await getRandomWord())
}

init()

export async function randomize(previousWord) {
  let nextWord = await getRandomWord()
  while (nextWord === previousWord) {
    nextWord = await getRandomWord()
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
