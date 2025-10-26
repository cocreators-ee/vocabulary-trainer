<script>
  import {browser} from '$app/environment';
</script>

<div class="stats">
  <div style="font-size: 14px; padding-bottom: 14px;">
    Stats powered by <a target="_blank" style="color: #4F46E5; text-decoration: underline;"
                        href="https://plausible.io">Plausible Analytics</a>
  </div>

  <iframe plausible-embed
          title="Visitor analytics"
          src="https://plausible.io/vocabulary-trainer.cocreators.ee?embed=true&theme=system" scrolling="no"
          frameborder="0" loading="lazy"
          style="width: 1px; min-width: 100%; height: 1600px; color-scheme: auto;"></iframe>

  {#if browser}
    <script async src="https://plausible.io/js/embed.host.js"></script>
  {/if}

  <div class="back">
    <a href="/">Back to vocabulary trainer</a>
  </div>
</div>

<style>
  .stats {
    margin: 5rem 0;
    min-width: 80vw;
    width: 100%;
  }

  .back {
    margin: 2rem 0;
  }
</style>
