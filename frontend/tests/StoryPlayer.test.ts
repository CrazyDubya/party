import { render, screen } from '@testing-library/svelte';
import StoryPlayer from '$lib/components/StoryPlayer.svelte';

it('renders the story player', () => {
  const story = {
    text: 'A cyberpunk detective walks through neon-lit streets.',
    choices: ['Follow the suspect', 'Check the alley', 'Call for backup'],
    image: 'https://example.com/cyberpunk.jpg'
  };
  render(StoryPlayer, { story: story });
  expect(screen.getByText('A cyberpunk detective walks through neon-lit streets.')).toBeInTheDocument();
  expect(screen.getByText('Follow the suspect')).toBeInTheDocument();
  expect(screen.getByText('Check the alley')).toBeInTheDocument();
  expect(screen.getByText('Call for backup')).toBeInTheDocument();
});