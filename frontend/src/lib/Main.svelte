<script>
  import { Button } from 'carbon-components-svelte'
  import { SkeletonPlaceholder } from 'carbon-components-svelte'
  import { currentWord, randomize } from './stores'

  import 'carbon-components-svelte/css/g10.css'
  import 'carbon-components-svelte/css/all.css'

  let makeVisible = false

  function showTranslation() {
    makeVisible = !makeVisible
  }

  function nextWord() {
    randomize($currentWord.source)
    showTranslation()
  }

  function handleKeydown(event) {
    if (event.key === 'Enter' || event.code === 'Space') {
      if (makeVisible) {
        nextWord()
      } else {
        showTranslation()
      }
    }
  }
</script>

<svelte:window on:keydown={handleKeydown} />
<main>
  <h2>{$currentWord.source}</h2>
  <div class="placeholder">
    {#if makeVisible}
      <p>{$currentWord.translations[0].word}</p>
    {:else}
      <button on:click={showTranslation}>
        <SkeletonPlaceholder style="height: 8rem;  width: 14rem;" />
      </button>
    {/if}
  </div>

  {#if makeVisible}
    <Button kind="primary" class="translate-button" on:click={nextWord}
      >Next word
    </Button>
  {:else}
    <Button kind="primary" class="translate-button" on:click={showTranslation}
      >Show translation
    </Button>
  {/if}
</main>

<style>
  :global(.translate-button) {
    padding: 1rem 2.5rem;
  }

  button {
    border: none;
  }

  h2 {
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
