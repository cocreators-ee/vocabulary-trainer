<script>
  import { Button } from 'carbon-components-svelte'
  import { SkeletonPlaceholder } from 'carbon-components-svelte'
  import { currentWord, randomize } from './stores'

  import 'carbon-components-svelte/css/g10.css'
  import 'carbon-components-svelte/css/all.css'

  let isTranslationVisible = false

  function showTranslation() {
    isTranslationVisible = true
  }

  function nextWord() {
    randomize($currentWord.source)
    isTranslationVisible = false
  }

  function handleKeydown(event) {
    if (event.key === 'Enter' || event.code === 'Space') {
      if (isTranslationVisible) {
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
    {#if isTranslationVisible}
      {#each $currentWord.translations as { word }}
        <span>{word}</span>&nbsp;
      {/each}
    {:else}
      <button on:click={showTranslation}>
        <SkeletonPlaceholder style="height: 8rem;  width: 14rem;" />
      </button>
    {/if}
  </div>

  {#if isTranslationVisible}
    <Button kind="primary" class="translate-button" on:click={nextWord}>
      Next word
    </Button>
  {:else}
    <Button kind="primary" class="translate-button" on:click={showTranslation}>
      Show translation
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
    text-transform: capitalize;
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

  span {
    text-transform: capitalize;
  }

  span:not(:last-of-type)::after {
    content: ',';
  }
</style>
