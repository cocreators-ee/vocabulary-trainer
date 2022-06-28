<script>
  import Counter from './lib/Counter.svelte'
  import { Grid, Row, Column } from 'carbon-components-svelte'
  import { Link } from 'carbon-components-svelte'
  import { Select, SelectItem } from 'carbon-components-svelte'
  import { Loading } from 'carbon-components-svelte'
  import { SkeletonPlaceholder } from 'carbon-components-svelte'
  import Layout from './lib/Layout.svelte'

  import 'carbon-components-svelte/css/g10.css'
  import 'carbon-components-svelte/css/all.css'
</script>

<Layout>
  <main>
    <h1><strong>Tere!</strong></h1>
    <div class="placeholder">
      <SkeletonPlaceholder />
    </div>

    <Counter />
  </main>
</Layout>

<style>
  h2 {
    margin: 3rem 0;
  }
  .placeholder {
    margin: 0 auto;
  }

  main {
    text-align: center;
    padding: 1em;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
  }

  img {
    height: 16rem;
    width: 16rem;
  }
</style>
