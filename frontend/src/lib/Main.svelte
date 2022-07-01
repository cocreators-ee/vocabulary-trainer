<script>
  import Counter from './Counter.svelte'
  import { SkeletonPlaceholder } from 'carbon-components-svelte'

  import 'carbon-components-svelte/css/g10.css'
  import 'carbon-components-svelte/css/all.css'
</script>

<main>
  <h1><strong>Tere</strong></h1>
  <div class="placeholder">
    <SkeletonPlaceholder
      style="height: 8em;  width: 14rem; margin-bottom: 25px; margin-top: 145px"
    />
  </div>

  <Counter />
</main>

<style>
  h1 {
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
</style>
