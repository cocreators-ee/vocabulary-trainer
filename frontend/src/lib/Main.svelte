<script>
  import Button from './Button.svelte'
  import { SkeletonPlaceholder } from 'carbon-components-svelte'

  import 'carbon-components-svelte/css/g10.css'
  import 'carbon-components-svelte/css/all.css'
</script>

<main>
  <h2 class="heading">Tere</h2>
  <div class="placeholder">
    <SkeletonPlaceholder style="height: 8rem;  width: 14rem;" />
  </div>

  <Button />
</main>

<style>
  .heading {
    font-weight: 700;
    font-size: 3rem;
  }

  .placeholder {
    margin: 0 auto;
    margin: 2rem 0;
    display: flex;
    justify-content: center;
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
