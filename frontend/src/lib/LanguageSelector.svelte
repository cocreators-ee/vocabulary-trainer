<script>
  import { Link, Modal } from 'carbon-components-svelte'
  import 'carbon-components-svelte/css/g10.css'
  import 'carbon-components-svelte/css/all.css'
</script>

<nav><Link class="lang">Estonian</Link></nav>

<Modal open={true}>lalalal</Modal>

<style>
  nav {
    display: flex;
    margin-left: auto;
  }
  :global(.lang) {
    color: #000;
    text-decoration: underline;
  }
</style>
