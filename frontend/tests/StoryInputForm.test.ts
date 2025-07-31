import { render, screen } from '@testing-library/svelte';
import StoryInputForm from '$lib/components/StoryInputForm.svelte';

it('renders the story input form', () => {
  render(StoryInputForm, { premise: '', mood: '', characters: '' });
  expect(screen.getByPlaceholderText('e.g., A cyberpunk detective story')).toBeInTheDocument();
  expect(screen.getByPlaceholderText('e.g., gritty, mysterious, upbeat')).toBeInTheDocument();
  expect(screen.getByPlaceholderText('e.g., 3 characters')).toBeInTheDocument();
  expect(screen.getByText('Generate Story')).toBeInTheDocument();
});