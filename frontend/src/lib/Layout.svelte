<div class="container">
  <nav><u> Estonian </u></nav>

  <div class="content">
    <slot />
  </div>
  <footer>
    <p>Vocabulary trainer</p>
    <p>Copyright @ 2022 Henry Elmest</p>
    <a href="https://github.com/cocreators-ee/vocabulary-trainer" target="_blank"
      ><p>github</p></a
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
  }
  :root {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu,
      Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  }
  .content {
    flex: 1;
  }

  .container {
    display: flex;
    flex: 1;
    flex-direction: column;
    max-width: 768px;
    margin: 0 auto;
    text-align: right;
  }
</style>
