<script>
  /**
   * @typedef {{ id?: string, text: string, next?: number }} StoryChoice
   * @typedef {{
   *   text?: string,
   *   choices?: Array<string | StoryChoice>,
   *   image?: string,
   *   title?: string,
   *   chapters?: Array<{
   *     id?: number,
   *     text: string,
   *     choices?: Array<string | StoryChoice>
   *   }>
   * }} Story
   */

  /** @type {Story} */
  export let story = {
    text: "Default story text",
    choices: [],
    image: "https://via.placeholder.com/500x200",
  };

  $: chapter = story.chapters?.[0];
  $: displayText = story.text ?? chapter?.text ?? "";
  $: displayChoices = story.choices ?? chapter?.choices ?? [];
  $: displayImage = story.image ?? "";
</script>

<div class="story-player">
  {#if displayImage}
    <img src={displayImage} alt="Story illustration" />
  {/if}
  <p>{displayText}</p>
  <div class="choices">
    {#each displayChoices as choice}
      <button class="choice-btn">
        {typeof choice === "string" ? choice : choice.text}
      </button>
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
