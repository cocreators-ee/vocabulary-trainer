import Main from './lib/Main.svelte'
import Home from './lib/Home.svelte'
import NotFound from './lib/NotFound.svelte'
export const routes = {
  '/': Home,
  '/:lang/': Main,
  '*': NotFound,
}
