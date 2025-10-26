import { redirect } from "@sveltejs/kit"
import languages from "$languages/languages.json"
import { setLanguage } from "$lib/stores.js"

export const prerender = true
export const ssr = true

export function entries() {
  const datas = []
  languages.forEach((language) => {
    datas.push({ lang: language.code })
  })
  return datas
}

export async function load({ url, params }) {
  const language = params.lang
  const isValidLanguage = languages.some((lang) => lang.code === language)
  if (!isValidLanguage) {
    await redirect(307, "/")
  }

  await setLanguage(language)

  return {
    language: language,
  }
}
