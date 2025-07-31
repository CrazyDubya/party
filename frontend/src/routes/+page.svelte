<script>
	// Story premise input form - Milestone 1 scaffold
	let premise = '';
	let mood = '';
	let characters = '';
	let isGenerating = false;
	let generatedStory = null;

	async function generateStory() {
		if (!premise.trim()) return;
		
		isGenerating = true;
		try {
			// TODO: Replace with actual API call in Milestone 2
			// Mock story generation for now
			await new Promise(resolve => setTimeout(resolve, 2000));
			
			generatedStory = {
				title: `Story: ${premise}`,
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
		} catch (error) {
			console.error('Story generation failed:', error);
		} finally {
			isGenerating = false;
		}
	}
</script>

<main>
	<h1>AI Storytelling Engine</h1>
	<p>Generate immersive, interactive stories in under 60 seconds</p>

	{#if !generatedStory}
		<form on:submit|preventDefault={generateStory} class="story-form">
			<div class="input-group">
				<label for="premise">Story Premise *</label>
				<input 
					id="premise"
					type="text" 
					bind:value={premise} 
					placeholder="e.g., A cyberpunk detective story"
					required
				/>
			</div>

			<div class="input-group">
				<label for="mood">Mood</label>
				<input 
					id="mood"
					type="text" 
					bind:value={mood} 
					placeholder="e.g., gritty, mysterious, upbeat"
				/>
			</div>

			<div class="input-group">
				<label for="characters">Number of Characters</label>
				<input 
					id="characters"
					type="text" 
					bind:value={characters} 
					placeholder="e.g., 3 characters"
				/>
			</div>

			<button type="submit" disabled={isGenerating || !premise.trim()}>
				{isGenerating ? 'Generating Story...' : 'Generate Story'}
			</button>
		</form>
	{:else}
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
</main>

<style>
	main {
		max-width: 800px;
		margin: 0 auto;
		padding: 2rem;
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
	}

	h1 {
		color: #333;
		text-align: center;
		margin-bottom: 0.5rem;
	}

	p {
		text-align: center;
		color: #666;
		margin-bottom: 2rem;
	}

	.story-form {
		background: #f9f9f9;
		padding: 2rem;
		border-radius: 8px;
		box-shadow: 0 2px 10px rgba(0,0,0,0.1);
	}

	.input-group {
		margin-bottom: 1.5rem;
	}

	label {
		display: block;
		margin-bottom: 0.5rem;
		font-weight: 600;
		color: #333;
	}

	input {
		width: 100%;
		padding: 0.75rem;
		border: 1px solid #ddd;
		border-radius: 4px;
		font-size: 1rem;
	}

	input:focus {
		outline: none;
		border-color: #007acc;
		box-shadow: 0 0 0 2px rgba(0,122,204,0.2);
	}

	button {
		background: #007acc;
		color: white;
		border: none;
		padding: 0.75rem 1.5rem;
		border-radius: 4px;
		font-size: 1rem;
		cursor: pointer;
		transition: background 0.2s;
	}

	button:hover:not(:disabled) {
		background: #005a9e;
	}

	button:disabled {
		background: #ccc;
		cursor: not-allowed;
	}

	.story-display {
		background: #f9f9f9;
		padding: 2rem;
		border-radius: 8px;
		box-shadow: 0 2px 10px rgba(0,0,0,0.1);
	}

	.chapter {
		margin-bottom: 2rem;
	}

	.choices {
		display: flex;
		gap: 1rem;
		flex-wrap: wrap;
	}

	.choice-btn {
		background: #28a745;
		flex: 1;
		min-width: 200px;
	}

	.choice-btn:hover {
		background: #218838;
	}
</style>