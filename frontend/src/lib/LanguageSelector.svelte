<script>
  import { Link, Modal, Select, SelectItem } from 'carbon-components-svelte'
  import { currentLanguage } from './stores'
  import languages from '$languages/languages.json'
  import 'carbon-components-svelte/css/g10.css'
  import 'carbon-components-svelte/css/all.css'
  import {goto} from "$app/navigation";

  let selected

  export let modalOpen = false

  function openModal() {
    modalOpen = true
    selected = $currentLanguage.code
  }

  function closeModal() {
    modalOpen = false
  }

  function onSecondaryClick() {
    closeModal()
  }

  function onPrimaryClick() {
    closeModal()
    goto(`/${selected}/`)
  }
</script>

<nav><Link onclick={openModal} class="lang">{$currentLanguage.name}</Link></nav>

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
