<script>
  export let generatedStory;
  export let isGenerating;
</script>

{#if generatedStory}
  <div class="story-display">
    <h2>{generatedStory.title}</h2>
    <div class="chapter">
      <p>{generatedStory.chapters[0].text}</p>
      <div class="choices">
        {#each generatedStory.chapters[0].choices as choice}
          <button class="choice-btn">{choice.text}</button>
        {/each}
      </div>
    </div>
    <button on:click={() => generatedStory = null}>Generate New Story</button>
  </div>
{/if}