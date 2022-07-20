import Main from './lib/Main.svelte'
import Home from './lib/Home.svelte'
export const routes = {
  '/': Home,
  '/:lang/': Main,
}
