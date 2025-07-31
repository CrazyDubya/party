<script>
  export let isGenerating = false;
  export let premise = '';
  export let mood = '';
  export let characters = '';
</script>

<form on:submit|preventDefault>
  <div class="input-group">
    <label for="premise">Story Premise *</label>
    <input id="premise" type="text" bind:value={premise} placeholder="e.g., A cyberpunk detective story" required />
  </div>

  <div class="input-group">
    <label for="mood">Mood</label>
    <input id="mood" type="text" bind:value={mood} placeholder="e.g., gritty, mysterious, upbeat" />
  </div>

  <div class="input-group">
    <label for="characters">Number of Characters</label>
    <input id="characters" type="text" bind:value={characters} placeholder="e.g., 3 characters" />
  </div>

  <button type="submit" disabled={isGenerating || !premise.trim()}>
    {isGenerating ? 'Generating Story...' : 'Generate Story'}
  </button>
</form>