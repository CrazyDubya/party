import { render, screen } from '@testing-library/svelte';
import StoryPlayer from '$lib/components/StoryPlayer.svelte';

it('renders the story player', () => {
  const story = {
    title: 'Test Story',
    chapters: [
      {
        id: 1,
        text: 'Chapter 1',
        choices: [
          { id: 'a', text: 'Choice A' },
          { id: 'b', text: 'Choice B' },
        ],
      },
    ],
  };
  render(StoryPlayer, { generatedStory: story });
  expect(screen.getByText('Test Story')).toBeInTheDocument();
  expect(screen.getByText('Chapter 1')).toBeInTheDocument();
  expect(screen.getByText('Choice A')).toBeInTheDocument();
  expect(screen.getByText('Choice B')).toBeInTheDocument();
});