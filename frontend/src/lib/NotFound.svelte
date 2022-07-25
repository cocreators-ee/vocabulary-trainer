<script>
  import { Link } from 'carbon-components-svelte'

  import 'carbon-components-svelte/css/g10.css'
  import 'carbon-components-svelte/css/all.css'
</script>

<main>
  <h2>404 Not Found</h2>
  <div class="home-redirect">
    <Link class="home-link" href="/">Try starting from the beginning...</Link>
  </div>
</main>

<style>
  :global(.translate-button) {
    padding: 1rem 2.5rem;
  }

  h2 {
    font-weight: 700;
    font-size: 2.5rem;
    text-transform: capitalize;
    text-align: center;
  }

  :global(.home-link) {
    font-size: 1.3rem;
  }

  .home-redirect {
    margin: 0 auto;
    margin: 2rem 0;
    display: flex;
    justify-content: center;
    font-size: 2rem;
  }

  main {
    padding: 1rem;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
</style>
