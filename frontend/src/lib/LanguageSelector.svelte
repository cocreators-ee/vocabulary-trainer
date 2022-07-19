<script>
  import { Button, Link, Modal, Select, SelectItem } from 'carbon-components-svelte'
  import { each } from 'svelte/internal'
  import { currentLanguage, setLanguage } from './stores'
  import languages from '../languages/languages.json'
  import 'carbon-components-svelte/css/g10.css'
  import 'carbon-components-svelte/css/all.css'

  let selected
  let _currentLanguage
  $: {
    _currentLanguage = $currentLanguage.code
  }

  export let modalOpen = false

  function openModal() {
    modalOpen = true
    selected = _currentLanguage
  }

  function closeModal() {
    modalOpen = false
  }
  function onSecondaryClick() {
    closeModal()
  }

  function onPrimaryClick() {
    closeModal()
    setLanguage(selected)
  }
</script>

<nav><Link on:click={openModal} class="lang">{$currentLanguage.name}</Link></nav>

<Modal
  modalHeading="Choose language"
  primaryButtonText="Confirm"
  secondaryButtonText="Cancel"
  open={modalOpen}
  on:close={closeModal}
  on:click:button--primary={onPrimaryClick}
  on:click:button--secondary={onSecondaryClick}
>
  <Select labelText="Language" bind:selected>
    {#each languages as language}
      <SelectItem value={language.code} text={language.name} />
    {/each}
  </Select>
</Modal>

<style>
  :global(.lang) {
    color: #000;
    text-decoration: underline;
    cursor: pointer;
  }

  nav {
    display: flex;
    margin-left: auto;
  }
</style>
