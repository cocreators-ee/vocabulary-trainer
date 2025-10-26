import languages from "$languages/languages.json"
import { redirect } from "@sveltejs/kit"

export async function load() {
  return redirect(307, `/${languages[0].code}/`)
}
