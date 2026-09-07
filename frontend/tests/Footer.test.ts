import { render, screen } from "@testing-library/svelte";
import Footer from "$lib/components/Footer.svelte";

it("renders the footer", () => {
  render(Footer);
  expect(screen.getByText("© 2025 AI Storyteller")).toBeInTheDocument();
});
