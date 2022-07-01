<script>
  import Main from './lib/Main.svelte'
  import { Link } from 'carbon-components-svelte'
</script>

<div class="container">
  <nav><u> Estonian </u></nav>

  <div class="content">
    <Main />
  </div>
  <footer>
    <p>Vocabulary trainer</p>
    <p>Copyright @ 2022 Henry Elmest</p>
    <Link href="https://github.com/cocreators-ee/vocabulary-trainer"
      ><h4>Github</h4></Link
    >
  </footer>
</div>

<style>
  footer {
    text-align: center;
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
  }

  @media only screen and (min-width: 900px) {
    .container {
      max-width: 768px;
      margin: 0 auto;
    }
  }
  .container {
    display: flex;
    flex: 1;
    flex-direction: column;
    text-align: right;
  }
</style>
