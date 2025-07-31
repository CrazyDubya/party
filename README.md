# AI-Generated Immersive Storytelling Engine

A web/mobile application that generates playable, branching narratives in under 60 seconds with AI-powered text, audio, and visuals.

## Project Overview

This application allows users to input a story premise (e.g., "A cyberpunk detective story, gritty mood, 3 characters") and generates an immersive, interactive story with:
- Branching narrative paths (3-5 choices)
- AI-generated text (500-1000 words total)
- Text-to-speech audio snippets (<10s for key moments)
- AI-generated or stock visuals (one per chapter)
- Save/load functionality
- Shareable story links

## Tech Stack

### Frontend
- **Svelte** for web (lightweight, reactive)
- **SvelteKit** for mobile (PWA, no native apps)
- **Vitest** for testing (90% coverage requirement)

### Backend
- **Python with FastAPI** (async, handles AI orchestration)
- **pytest** for testing (90% coverage requirement)

### AI Services
- **Gemini Flash** via OpenRouter (primary narrative generation)
- **Claude Haiku** via OpenRouter (backup/consideration)
- **Grok/Llama 3** via xAI API (alternative option)
- **ElevenLabs** or similar for text-to-speech
- **Stable Diffusion** (local or API) for visuals
- **Unsplash** as fallback for images

### Storage
- **SQLite** for local story caching
- Optional user-controlled cloud sync (Dropbox API)

## Development Workflow

### Branch Structure
- **production**: Final, stable releases (tagged with semantic versioning)
- **staging**: Testing and pre-production validation
- **dev**: Active development and integration
- **feature/**: Individual feature branches (created from dev)
- **bugfix/**: Bug fix branches (created from dev)

### Workflow Rules
1. **No direct commits** to dev, staging, or production
2. All work happens on feature branches
3. **Pull Requests required** for all changes
4. **At least one review** required before merging
5. **Squash commits** on merge to maintain linear history
6. **Atomic commits** with clear, descriptive messages

### Code Standards
- **Prettier** for Svelte formatting
- **Black** for Python formatting
- **Descriptive commit messages** (e.g., "Add branching logic to story player")
- **Inline comments** and documentation
- **Swagger** for API documentation

## Milestones

### Milestone 1: Setup and Story Scaffold (Week 1 → dev)
- [x] Initialize repository with README and process documentation
- [ ] Create Svelte app shell with input form
- [ ] Build FastAPI backend with stub endpoints
- [ ] Set up testing frameworks (Vitest + pytest)
- [ ] Create wireframes and mockups (commit PNG files)
- [ ] Mock AI outputs to avoid early API costs

### Milestone 2: Core AI Story Generation (Week 3 → staging)
- [ ] Implement narrative generation with branching paths
- [ ] Integrate text-to-speech for audio snippets
- [ ] Add AI-generated/stock image integration
- [ ] Build interactive story player with choices
- [ ] Implement save/load functionality
- [ ] Ensure narrative consistency and human-like quality

### Milestone 3: Polish and Sharing (Week 5 → production)
- [ ] Implement story sharing via unique URLs
- [ ] Add offline mode with story caching
- [ ] Create user customization options for AI parameters
- [ ] Complete E2E testing on staging
- [ ] Manual UX testing for immersion
- [ ] Tag v1.0.0 with PWA link and demo video

## Performance Requirements
- **Story generation**: <60 seconds
- **App load time**: <2 seconds
- **Test coverage**: 90% minimum
- **No user tracking** (privacy-first approach)

## Project Structure
```
├── frontend/          # Svelte/SvelteKit application
│   ├── src/
│   ├── tests/
│   └── package.json
├── backend/           # FastAPI Python application
│   ├── app/
│   ├── tests/
│   └── requirements.txt
├── docs/              # Documentation and wireframes
├── .github/           # GitHub workflows and templates
└── README.md
```

## Getting Started

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Git

### Local Development
```bash
# Clone repository
git clone <repository-url>
cd ai-storytelling-engine

# Frontend setup
cd frontend
npm install
npm run dev

# Backend setup (in new terminal)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Run tests
npm test          # Frontend tests
pytest           # Backend tests
```

## API Documentation
Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

## Contributing
1. Create feature branch from `dev`
2. Make atomic commits with clear messages
3. Ensure 90% test coverage
4. Submit PR with description and screenshots
5. Get at least one review approval
6. Squash merge to maintain clean history

## Communication
- **GitHub Issues**: Tasks, bugs, and feature requests
- **GitHub Discussions**: Broader ideas and planning
- **PR Comments**: Code reviews and feedback
- **Commit messages**: Progress tracking

All communication stays within GitHub for transparency.

---

**Note**: This project prioritizes speed, creativity, and user privacy. Stories must feel human-generated, not like chatbot output. If the final product feels derivative or unintuitive, iteration is required.