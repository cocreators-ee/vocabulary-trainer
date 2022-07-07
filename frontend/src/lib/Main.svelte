<script>
  import { Button } from 'carbon-components-svelte'
  import { SkeletonPlaceholder } from 'carbon-components-svelte'
  import { currentWord, skipNext } from './stores'
  import { onDestroy } from 'svelte'

  import 'carbon-components-svelte/css/g10.css'
  import 'carbon-components-svelte/css/all.css'

  let skeleton = { show: false }

  function toggleTranslation() {
    skeleton.show = !skeleton.show
  }

  function nextWords() {
    skipNext()
    skeleton.show = !skeleton.show
  }

  function handleKeydown(event) {
    if (skeleton.show) {
      nextWords()
    } else {
      if (event.key === 'Enter' || event.code === 'Space') {
        skeleton.show = !skeleton.show
      }
    }
  }

  let word
  let translation

  const unsubscribe = currentWord.subscribe((value) => {
    word = value.source
    translation = value.translations[0].word
  })

  onDestroy(unsubscribe)
</script>

<svelte:window on:keydown={handleKeydown} />
<main>
  <h2 class="heading">{word}</h2>
  <div class="placeholder">
    {#if skeleton.show}
      <p>{translation}</p>
    {:else}
      <button on:click={toggleTranslation}>
        <SkeletonPlaceholder style="height: 8rem;  width: 14rem;" />
      </button>
    {/if}
  </div>

  {#if skeleton.show}
    <Button kind="primary" class="translate-button" on:click={nextWords}
      >Next word
    </Button>
  {:else}
    <Button kind="primary" class="translate-button" on:click={toggleTranslation}
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
