<script>
  import Header from "$lib/components/Header.svelte";
  import Footer from "$lib/components/Footer.svelte";
  import StoryInputForm from "$lib/components/StoryInputForm.svelte";
  import StoryPlayer from "$lib/components/StoryPlayer.svelte";

  /** @typedef {{ id: string, text: string, next: number }} GeneratedChoice */
  /** @typedef {{ id: number, text: string, choices: GeneratedChoice[] }} GeneratedChapter */
  /** @typedef {{ title: string, chapters: GeneratedChapter[] }} GeneratedStory */

  let premise = "";
  let mood = "";
  let characters = "";
  let isGenerating = false;
  /** @type {GeneratedStory | null} */
  let generatedStory = null;

  async function generateStory() {
    if (!premise.trim()) return;

    isGenerating = true;
    try {
      // Mock story generation
      await new Promise((resolve) => setTimeout(resolve, 2000));

      generatedStory = {
        title: `Story: ${premise}`,
        chapters: [
          {
            id: 1,
            text: "Chapter 1: The story begins... (This is a mock story for development)",
            choices: [
              { id: "a", text: "Continue forward", next: 2 },
              { id: "b", text: "Look around", next: 3 },
            ],
          },
        ],
      };
    } catch (error) {
      console.error("Story generation failed:", error);
    } finally {
      isGenerating = false;
    }
  }
</script>

<Header />

<main>
  {#if !generatedStory}
    <StoryInputForm
      bind:premise
      bind:mood
      bind:characters
      {isGenerating}
      on:submit={generateStory}
    />
  {:else}
    <StoryPlayer story={generatedStory} />
  {/if}
</main>

<Footer />
