<script>
  import {Link} from 'carbon-components-svelte'
  import LanguageSelector from '../lib/LanguageSelector.svelte'
  import 'carbon-components-svelte/css/all.css'
  import 'carbon-components-svelte/css/g10.css'

  let {children} = $props()
</script>

<div class="container">
  <LanguageSelector/>
  <div class="content">
    {@render children()}
  </div>
  <footer>
    <p>Vocabulary trainer</p>
    <p>Copyright @ 2022 Henry Elmest, 2025 Cocreators OÜ</p>
    <p>
      <Link target="_blank" rel="noopener" href="https://github.com/cocreators-ee/vocabulary-trainer">
        GitHub
      </Link>
    </p>
    <p>
      We use the privacy-respecting
      <Link href="https://plausible.io/privacy" target="_blank" rel="noopener">
        Plausible Analytics
      </Link>
      to measure usage of this site. You can view the
      <Link href="https://plausible.io/vocabulary-trainer.cocreators.ee" target="_blank" rel="noopener">
        statistics
      </Link>
      yourself.
    </p>
    <p>
      This project has been made possible thanks to support from
      <Link href="https://cocreators.ee" target="_blank" rel="noopener">Cocreators OÜ</Link>.
      You can help us continue our open source work by supporting us on
      <Link href="https://www.buymeacoffee.com/cocreators" target="_blank" rel="noopener">Buy me a coffee</Link>.
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

  footer p {
    font-size: var(--cds-body-short-01-font-size, 0.875rem);
  }

  @media only screen and (min-width: 60rem) {
    .container {
      min-width: 45rem;
      margin: 0 auto;
    }
  }
</style>
