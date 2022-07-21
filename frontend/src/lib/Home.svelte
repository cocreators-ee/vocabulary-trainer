<script>
  import { replace } from 'svelte-spa-router'
  import languages from '../languages/languages.json'

  replace(`/${languages[0].code}/`)
</script>
