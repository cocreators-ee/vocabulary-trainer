import { writable } from "svelte/store"
import languages from "$languages/languages.json"

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
    wordCache = (await import(`$languages/${_currentLanguage.code}/words.json`)).default
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

const NO_WORD = { source: "", translations: [] }
export const currentWord = writable(NO_WORD)
export const aiInfo = writable(undefined)

async function init() {
  currentWord.set(await getRandomWord())
}

init()

async function tryLoadAIInfo(sourceWord) {
  aiInfo.set(undefined)
  try {
    const aiInfoContents = (await import(`$languages/${_currentLanguage.code}/ai/${sourceWord}.json`)).default
    aiInfo.set(aiInfoContents)
  } catch (e) {
    console.log(`Failed to load AI info for word ${sourceWord}`)
  }
}

async function setCurrentWord(word) {
  currentWord.set(word)
  await tryLoadAIInfo(word.source)
}

async function getWord(sourceWord) {
  const words = await getWords()
  for (const word of words) {
    if (word.source === sourceWord) {
      return word
    }
  }

  throw new Error(`Failed to find source word ${sourceWord}`)
}

export async function randomize(previousWord) {
  let nextWord = await getRandomWord()
  while (nextWord === previousWord) {
    nextWord = await getRandomWord()
  }
  await setCurrentWord(nextWord)
}

export async function setLanguage(languageCode, word) {
  languages.forEach((value) => {
    if (value.code === languageCode) {
      currentLanguage.set(value)
    }
  })
  if (word !== undefined) {
    await setCurrentWord(await getWord(word))
  } else {
    await setCurrentWord(await getRandomWord())
  }
}
