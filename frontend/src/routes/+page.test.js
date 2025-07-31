import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/svelte';
import Page from './+page.svelte';

describe('Story Generation Page', () => {
	it('renders the main heading', () => {
		render(Page);
		expect(screen.getByText('AI Storytelling Engine')).toBeTruthy();
	});

	it('renders the story form', () => {
		render(Page);
		expect(screen.getByLabelText('Story Premise *')).toBeTruthy();
		expect(screen.getByLabelText('Mood')).toBeTruthy();
		expect(screen.getByLabelText('Number of Characters')).toBeTruthy();
	});

	it('has generate button initially enabled when premise is filled', () => {
		render(Page);
		const button = screen.getByRole('button', { name: /generate story/i });
		expect(button).toBeTruthy();
	});
});