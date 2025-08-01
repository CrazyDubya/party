# LiteLLM

## Overview
LiteLLM is an open-source library and proxy server that simplifies interaction with over 100 Large Language Models (LLMs) from various providers through a single, consistent API. It focuses on cost tracking, context window management, and providing a unified interface for LLM operations.

## Models Offered
LiteLLM itself does not offer models directly. It provides a unified interface to over 100 LLMs from various providers (e.g., OpenAI, Anthropic, Google, Cohere, etc.). It tracks `max_tokens`, `input_cost_per_token`, and `output_cost_per_token` for all integrated models.

## Key Features
*   **API Endpoints:** Single, consistent API for 100+ LLMs, OpenAI-compatible.
*   **Pricing Model:** Free to use (open-source). Provides tools for cost tracking (per token, per second) and customizable pricing for underlying LLMs.
*   **Caching:** Offers prompt caching as a feature of its Proxy Server (LLM Gateway).
*   **Rate Limits:** Supports setting limits based on Tokens per Minute (tpm), Requests per Minute (rpm), and max parallel requests. Limits can be applied per model, per API key, per user/team, or per project. Configurable via `config.yaml` or API endpoints.
*   **Supported Modalities:** Dependent on the underlying LLM providers it integrates with.
*   **Developer Tools/SDKs:** Python SDK, Proxy Server (LLM Gateway).
*   **Unique Selling Propositions:** Unified API for many LLMs, cost tracking and management, context window management with fallbacks, load balancing, OpenAI standards alignment.

## Pros & Cons
*   **Pros:**
    *   Simplifies integration with a vast number of LLMs.
    *   Excellent cost tracking and management features.
    *   Open-source and free to use.
    *   Helps manage context windows and provides fallbacks.
*   **Cons:**
    *   Does not provide its own inference; relies on external LLM providers.
    *   Requires self-hosting for the Proxy Server.

## Links
*   [Official Website](https://litellm.ai/)
*   [Pricing/Cost Tracking Documentation](https://litellm.ai/docs/observability/cost_tracking)
*   [Models and Max Tokens](https://litellm.ai/docs/providers/azure#get-max-tokens-for-a-model)