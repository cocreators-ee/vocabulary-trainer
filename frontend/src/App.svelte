<script>
  import Router from 'svelte-spa-router'
  import { Link } from 'carbon-components-svelte'
  import { routes } from './routes'
</script>

<div class="container">
  <nav><Link class="lang">Estonian</Link></nav>

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

  :global(.lang) {
    color: #000;
    text-decoration: underline;
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

  nav {
    display: flex;
    margin-left: auto;
  }

  @media only screen and (min-width: 60rem) {
    .container {
      min-width: 45rem;
      margin: 0 auto;
    }
  }
</style>
