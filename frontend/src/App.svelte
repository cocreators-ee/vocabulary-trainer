<script>
  import Router from 'svelte-spa-router'
  import { Link } from 'carbon-components-svelte'
  import { routes } from './routes'
  import LanguageSelector from './lib/LanguageSelector.svelte'

  import 'carbon-components-svelte/css/all.css'
  import 'carbon-components-svelte/css/g10.css'
</script>

<div class="container">
  <LanguageSelector />
  <div class="content">
    <Router {routes} />
  </div>
  <footer>
    <p>Vocabulary trainer</p>
    <p>Copyright @ 2022 Henry Elmest</p>
    <p>
      <Link href="https://github.com/cocreators-ee/vocabulary-trainer">Github</Link>
    </p>
  </footer>
</div>

<style>
  :global(html, body, #app) {
    display: flex;
    flex: 1;
    flex-direction: column;
    width: 100%;
    height: 100%;
    background-color: white;
  }

  .container {
    display: flex;
    flex: 1;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 1rem;
  }

  .content {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  footer {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: auto;
  }

  @media only screen and (min-width: 60rem) {
    .container {
      min-width: 45rem;
      margin: 0 auto;
    }
  }
</style>
