import Main from './lib/Main.svelte'

export const routes = {
  '/': Main,
  '/:code': Main,
}
