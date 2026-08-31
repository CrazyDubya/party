# party

An AI storytelling engine. The backend generates stories with illustrations and narration.

## What's here

- `backend/app/main.py` — the FastAPI service.
- `backend/app/ai/` — the generation pipeline. From the modules' own docstrings:
  - `cost_optimizer.py` — "cost tracking and optimization for AI API usage with budget management and model selection based on complexity". Costs are recorded in `ai_costs.json`.
  - `quality_checker.py` — "ensures generated stories meet quality standards and feel human-authored, not AI-generated. Includes validation, content filtering, and quality metrics."
  - `story_generation.py`, `story_generator.py` — narrative generation.
  - `image_client.py`, `image_generation.py` — illustration.
  - `text_to_speech.py`, `tts_client.py` — narration.
  - `openrouter_client.py` — model routing.
- `backend/REAL_AI_DEPLOYMENT_GUIDE.md` — notes on running against live models rather than mocks.

## Housekeeping

`backend/` contains several one-off repair scripts from development — `fix_await.sed`, `fix_indent.sed`, `fix_indent2.sed`, `fix_indent3.sed`, `fix_runware_models.py` — and an `image_client.py.bak`. None are part of the application.

Root-level documents (`AGENTS_README.md`, `LESSONS_LEARNED.md`, `CUSTOMER_DELIVERY_COMPLETE.md`, `BRANCH_CLEANUP_COMPLETE.md`) describe the multi-agent process used to build this, not the product.
