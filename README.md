# party

An AI storytelling engine for party games — generates illustrated, narrated stories on demand.

## What's here

- `backend/app/main.py` — the FastAPI service.
- `backend/app/ai/` — the generation pipeline:
  - `story_generation.py`, `story_generator.py` — narrative generation
  - `image_client.py`, `image_generation.py` — illustration
  - `text_to_speech.py`, `tts_client.py` — narration
  - `openrouter_client.py` — model routing
  - `cost_optimizer.py`, `ai_costs.json` — per-call cost tracking and model selection by budget
  - `quality_checker.py` — output validation before anything reaches a player
- `backend/REAL_AI_DEPLOYMENT_GUIDE.md` — deployment notes for running against live models rather than mocks.

## Status

The generation pipeline is built and cost-aware, which is the interesting part. Root-level documents (`AGENTS_README.md`, `LESSONS_LEARNED.md`, `CUSTOMER_DELIVERY_COMPLETE.md`) describe the multi-agent process used to build it, not the product itself. Several `fix_*.sed` and `fix_*.py` scripts in `backend/` are one-off repair scripts from that process and can be deleted.
