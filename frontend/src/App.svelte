<script>
  import Main from './lib/Main.svelte'
  import { Link } from 'carbon-components-svelte'
</script>

<div class="container">
  <nav><Link class="lang">Estonian</Link></nav>

  <div class="content">
    <Main />
  </div>
  <footer>
    <p>Vocabulary trainer</p>
    <p>Copyright @ 2022 Henry Elmest</p>
    <Link href="https://github.com/cocreators-ee/vocabulary-trainer"><p>Github</p></Link
    >
  </footer>
</div>

<style>
  footer {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: auto;
  }
  :global(html, body, #app) {
    display: flex;
    flex: 1;
    flex-direction: column;
    width: 100%;
    height: 100%;
    background-color: white;
  }
  :root {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu,
      Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  }
  .content {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .container {
    display: flex;
    flex: 1;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 1rem;
  }

  nav {
    display: flex;
    margin-left: auto;
  }

  :global(.lang) {
    color: #000;
    text-decoration: underline;
  }

  @media only screen and (min-width: 60rem) {
    .container {
      min-width: 45rem;
      margin: 0 auto;
    }
  }
</style>
