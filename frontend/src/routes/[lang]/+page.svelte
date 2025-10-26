<script>
  import {Button} from 'carbon-components-svelte'
  import {SkeletonPlaceholder} from 'carbon-components-svelte'
  import {aiInfo, currentWord, currentLanguage, randomize, setLanguage} from '$lib/stores'
  import {page} from '$app/state'
  import AI from "$assets/ai.svg?url"

  let {params} = $props()

  $effect(async () => {
    let word = undefined
    if (page.url.hash.length > 0) {
      word = decodeURIComponent(page.url.hash.substring(1))
    }

    await setLanguage(params.lang, word)
  })

  $effect(async () => {
    if (typeof window !== "undefined" && $currentWord.source !== undefined && $currentWord.source !== "") {
      const newHash = `#${$currentWord.source}`
      if (window.location.hash !== newHash) {
        window.location.hash = newHash
      }
    }
  })

  let isTranslationVisible = $state(false)

  function showTranslation() {
    isTranslationVisible = true

    // Track word reveals in Plausible analytics when possible
    if (typeof plausible !== "undefined") {
      plausible('reveal')
    }
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

  function ekssUrl(word) {
    const url = new URL("https://arhiiv.eki.ee/dict/ekss/index.cgi?F=M")
    url.searchParams.set("Q", word)
    return url.toString()
  }

  function wiktionaryUrl(word) {
    const url = new URL("https://en.wiktionary.org/wiki/")
    url.pathname += encodeURIComponent(word)
    url.hash = `#${$currentLanguage.name}`
    return url.toString()
  }

  function githubIssueUrl(language, word) {
    const url = new URL("https://github.com/cocreators-ee/vocabulary-trainer/issues/new")
    url.searchParams.set("title", `Problem with the ${language} word ${word}`)
    return url.toString()
  }
</script>

<svelte:window on:keydown={handleKeydown}/>
<main>
  <h2>{$currentWord.source}</h2>
  <div class="info-container">
    <div class="placeholder">
      {#if isTranslationVisible}
        <h3>Machine translation</h3>
        <div class="translations">
          {#each $currentWord.translations as {word}}
            <span class="word">{word}</span><span class="separator">, </span>
          {/each}
        </div>
        {#if params.lang === "et"}
          <a target="_blank" rel="noopener" href={ekssUrl($currentWord.source)}>EKSS dictionary</a>
        {/if}
        <a target="_blank" rel="noopener" href={wiktionaryUrl($currentWord.source)}>Wiktionary</a>

        <div class="warning">
          <h4>WARNING</h4>
          <p class="note">
            As always with machine translation, these answers are often missing context, may be incompete, and sometimes just incorrect. Verify use from e.g. dictionaries when in doubt.
          </p>
        </div>
      {:else}
        <button onclick={showTranslation}>
          <SkeletonPlaceholder style="height: 12rem; width: 18rem;"/>
        </button>
      {/if}
    </div>
    <div class="ai-info" class:left={isTranslationVisible}>
      {#if isTranslationVisible}
        <h3><img src={AI} class="ai-icon" alt="" /> AI analysis</h3>
        {#if $aiInfo !== undefined}
          <h4>Translations</h4>
          <div class="ai-translations">
            {#each $aiInfo.translation as word}
              <span class="word">{word}</span><span class="separator">, </span>
            {/each}
          </div>

          <h4>Example sentences</h4>
          <div class="Examples">
            <ul>
              {#each $aiInfo.sentences as sentence}
                <li>{sentence}</li>
              {/each}
            </ul>
          </div>

          <h4>Additional information</h4>
          <p>{$aiInfo.context}</p>

          <div class="warning">
            <h4>WARNING</h4>
            <p class="note">
              As always with "AI", these answers are often wrong and it may e.g. have imagined the word was in English and gave answers based on the English word instead.
            </p>
            <p>Claimed confidence: {$aiInfo.confidence}</p>
          </div>
        {:else}
          <div class="no-ai-info">
            <p>No AI info available at this time.</p>
          </div>
        {/if}
      {:else}
        <button onclick={showTranslation}>
          <SkeletonPlaceholder style="height: 30rem; width: 25rem;"/>
        </button>
      {/if}
    </div>
  </div>

  {#if isTranslationVisible}
    <Button onclick={nextWord}>Next word</Button>

    <a target="_blank" rel="noopener" class="report" href={githubIssueUrl($currentLanguage.name, $currentWord.source)}>Report issue</a>
  {:else}
    <Button onclick={showTranslation}>Show translation</Button>
  {/if}
</main>

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

  h3 {
    font-weight: 600;
    font-size: 1.5rem;
    display: flex;
    flex-direction: row;
    gap: 0.5rem;
  }

  h4 {
    font-weight: 500;
    font-size: 1.25rem;
    margin: 1rem 0 0.5rem 0;
  }

  .ai-icon {
    width: 2rem;
    height: 2rem;
  }

  .info-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin: 2rem 0 1rem 0;
  }

  .ai-info, .placeholder {
    border: 1px solid #ddd;
    background-color: #eee;
    padding: 2rem;
    max-width: 40rem;
    width: 40vw;
    margin: 2rem auto;
    min-height: 35rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    justify-content: center;
    align-items: center;
  }

  .ai-info.left {
    align-items: flex-start;
  }

  .no-ai-info {
    margin: 1rem 0;
  }

  .placeholder {
    height: 8rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .translations {
    text-align: center;
    margin-bottom: 1rem;
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
    background-color: #dde;
    padding: 0 8px;
    display: inline-block;
    margin-bottom: 8px;
  }

  ul, li {
    margin: 0 0 0 0.5rem;
    list-style: disc;
  }

  li, p {
    font-weight: 400;
    font-size: 1rem;
    line-height: 1.1;
  }

  .warning {
    margin-top: 1rem;
    border: 1px solid #c4a679;
    background-color: #ffe2b0;
    padding: 0.5rem 0.75rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .warning h4 {
    margin-top: 0;
  }

  .note {
    font-style: italic;
  }

  a.report {
    margin-top: 1rem;
  }

  @media (max-width: 1080px) {
    .info-container {
      display: flex;
      flex-direction: column;
    }

    .placeholder, .ai-info {
      width: 100%;
      margin: 0;
      padding: 0.75rem;
    }

    main {
      margin-bottom: 5rem;
      padding: 0;
    }
  }
</style>
