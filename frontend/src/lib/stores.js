import words from '../languages/et/words.json'
import { writable } from 'svelte/store'

function randInt(min, max) {
  return Math.floor(Math.random() * (max - min)) + min
}

function getRandomWord() {
  return words[randInt(0, words.length - 1)]
}

export const currentWord = writable(getRandomWord())
