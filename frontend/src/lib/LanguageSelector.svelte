<script>
  import { Link } from 'carbon-components-svelte'
  import 'carbon-components-svelte/css/g10.css'
  import 'carbon-components-svelte/css/all.css'
  import { currentLanguage } from './stores'
</script>

<nav><Link class="lang">{$currentLanguage.name}</Link></nav>

<style>
  nav {
    display: flex;
    margin-left: auto;
  }
  :global(.lang) {
    color: #000;
    text-decoration: underline;
  }
</style>
