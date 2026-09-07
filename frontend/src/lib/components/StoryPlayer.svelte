<script>
  export let story = {
    text: "Default story text",
    choices: [],
    image: "https://via.placeholder.com/500x200",
  };
</script>

<div class="story-player">
  {#if story.image}
    <img src={story.image} alt="Story illustration" />
  {/if}
  <p>{story.text}</p>
  <div class="choices">
    {#each story.choices || [] as choice}
      <button class="choice-btn">{choice}</button>
    {/each}
  </div>
</div>

<style>
  img {
    max-width: 100%;
  }

  .choices {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
  }

  .choice-btn {
    padding: 0.5rem 1rem;
    border: 1px solid #ccc;
    background: white;
    cursor: pointer;
  }
</style>
