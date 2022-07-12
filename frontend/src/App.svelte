<script>
  import Main from './lib/Main.svelte'
  import { Link } from 'carbon-components-svelte'
  import LanguageSelector from './lib/LanguageSelector.svelte'
</script>

<div class="container">
  <LanguageSelector />
  <div class="content">
    <Main />
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
  :root {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu,
      Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  }
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
