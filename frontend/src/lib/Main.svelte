<script>
  import Counter from './Counter.svelte'
  import { SkeletonPlaceholder } from 'carbon-components-svelte'

  import 'carbon-components-svelte/css/g10.css'
  import 'carbon-components-svelte/css/all.css'
</script>

<main>
  <h2><strong>Tere!</strong></h2>
  <div class="placeholder">
    <SkeletonPlaceholder />
  </div>

  <Counter />
</main>

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
