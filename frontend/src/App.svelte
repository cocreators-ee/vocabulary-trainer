<script>
  import logo from './assets/svelte.png'
  import Counter from './lib/Counter.svelte'
  import { Grid, Row, Column } from 'carbon-components-svelte'
  import { Link } from 'carbon-components-svelte'
  import { Select, SelectItem } from 'carbon-components-svelte'
  import { Loading } from 'carbon-components-svelte'
  import { SkeletonPlaceholder } from 'carbon-components-svelte'

  import 'carbon-components-svelte/css/g10.css'
  import 'carbon-components-svelte/css/all.css'
</script>

<main>
  <h2><strong>Tere!</strong></h2>

  <script>
    import { SkeletonPlaceholder } from 'carbon-components-svelte'
  </script>

  <SkeletonPlaceholder />

  <Counter />
  <p>Vocabulary trainer</p>
  <p>Copyright @ 2022</p>
</main>

<style>
  :root {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu,
      Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  }

  main {
    text-align: center;
    padding: 1em;
    margin: 0 auto;
  }

  img {
    height: 16rem;
    width: 16rem;
  }

  h1 {
    color: #ff3e00;
    text-transform: uppercase;
    font-size: 4rem;
    font-weight: 100;
    line-height: 1.1;
    margin: 2rem auto;
    max-width: 14rem;
  }

  p {
    max-width: 14rem;
    margin: 1rem auto;
    line-height: 1.35;
  }

  @media (min-width: 480px) {
    h1 {
      max-width: none;
    }

    p {
      max-width: none;
    }
  }
</style>
