<script>
  import { onMount } from 'svelte'
  import { push, location } from 'svelte-spa-router'
  import { Button } from 'carbon-components-svelte'
  import { SkeletonPlaceholder } from 'carbon-components-svelte'
  import { currentWord, randomize } from './stores'
  import languages from '../languages/languages.json'

  import 'carbon-components-svelte/css/g10.css'
  import 'carbon-components-svelte/css/all.css'

  onMount(() => {
    if ($location === '/') {
      push(`/${languages[0].code}`)
    }
  })

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
      <div>
        {#each $currentWord.translations as { word }}
          <span class="word">{word}</span><span class="separator">, </span>
        {/each}
      </div>
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
    font-size: 1.35rem;
  }

  span.separator:last-of-type {
    display: none;
  }

  span.word {
    background-color: #eeeeee;
    padding: 0 8px;
  }
</style>
