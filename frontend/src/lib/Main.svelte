<script>
  import { Button } from 'carbon-components-svelte'
  import { SkeletonPlaceholder } from 'carbon-components-svelte'
  import { currentWord, randomize, setLanguage } from './stores'
  import languages from '../languages/languages.json'
  import NotFound from './NotFound.svelte'

  export let params
  const isValidLanguage = languages.some((lang) => lang.code === params.lang)

  $: {
    setLanguage(params.lang)
  }
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
{#if isValidLanguage}
  <main>
    <h2>{$currentWord.source}</h2>
    <div class="placeholder">
      {#if isTranslationVisible}
        <div class="translations">
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
      <Button on:click={nextWord}>Next word</Button>
    {:else}
      <Button on:click={showTranslation}>Show translation</Button>
    {/if}
  </main>
{:else}
  <NotFound />
{/if}

<style>
  :global(.bx--btn.bx--btn--primary) {
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
    height: 8rem;
    max-width: 40rem;
    margin: 2rem auto;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .translations {
    text-align: center;
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
    display: inline-block;
    margin-bottom: 8px;
  }
</style>
