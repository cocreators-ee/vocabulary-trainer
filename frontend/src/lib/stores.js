import { writable } from 'svelte/store'
import languages from '../languages/languages.json'

let words = [
  {
    source: 'tere',
    translations: [
      {
        word: 'Hi',
        tag: 'NOUN',
      },
    ],
  },
]

async function loadWords() {
  return (await import(`../languages/${_currentLanguage.code}/words.json`)).default
}

export const currentLanguage = writable(languages[0])
let _currentLanguage
currentLanguage.subscribe(async (value) => {
  _currentLanguage = value
  words = await loadWords()
})

function randInt(min, max) {
  return Math.floor(Math.random() * (max - min)) + min
}

function getRandomWord() {
  return words[randInt(0, words.length - 1)]
}

export const currentWord = writable(getRandomWord())

export function randomize(previousWord) {
  let nextWord = getRandomWord()
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
  currentWord.set(getRandomWord())
}
