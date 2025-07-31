<script>
  import Header from '$lib/components/Header.svelte';
  import Footer from '$lib/components/Footer.svelte';
  import StoryPlayer from '$lib/components/StoryPlayer.svelte';

  // This will be loaded from the backend in a later milestone
  let generatedStory = {
    title: `Story: Mock Story`,
    chapters: [
      {
        id: 1,
        text: "Chapter 1: The story begins... (This is a mock story for development)",
        choices: [
          { id: 'a', text: 'Continue forward', next: 2 },
          { id: 'b', text: 'Look around', next: 3 }
        ]
      }
    ]
  };
</script>

<Header />

<main>
  <StoryPlayer {generatedStory} />
</main>

<Footer />
