import { render, screen } from '@testing-library/svelte';
import Header from '$lib/components/Header.svelte';

it('renders the header', () => {
  render(Header);
  expect(screen.getByText('AI Storyteller')).toBeInTheDocument();
});