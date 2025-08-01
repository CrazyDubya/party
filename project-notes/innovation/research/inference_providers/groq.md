# Groq

## Overview
Groq is a direct inference provider known for its custom-built Language Processing Units (LPUs) that deliver high-speed and low-latency inference for large language models. They offer a "tokens-as-a-service" pricing model with detailed costs per million tokens for various models.

## Models Offered
| Model Name | Context Window (Tokens) | Cost per 1M Input Tokens | Cost per 1M Output Tokens | Cache Support | Output Size Limit | Notes |
|---|---|---|---|---|---|---|
| Kimi K2 1T | 128,000 | $1.00 | $3.00 | Not explicitly mentioned | Not explicitly mentioned | |
| Llama 4 Scout (17Bx16E) | 128,000 | $0.11 | $0.34 | Not explicitly mentioned | Not explicitly mentioned | |
| Llama 4 Maverick (17Bx128E) | 128,000 | $0.20 | $0.60 | Not explicitly mentioned | Not explicitly mentioned | |
| Llama Guard 4 12B | 128,000 | $0.20 | $0.20 | Not explicitly mentioned | Not explicitly mentioned | |
| DeepSeek R1 Distill Llama 70B | 128,000 | $0.75 | $0.99 | Not explicitly mentioned | Not explicitly mentioned | |
| Qwen3 32B | 131,000 | $0.29 | $0.59 | Not explicitly mentioned | Not explicitly mentioned | |
| Mistral Saba 24B | 32,000 | $0.79 | $0.79 | Not explicitly mentioned | Not explicitly mentioned | |
| Llama 3.3 70B Versatile | 128,000 | $0.59 | $0.79 | Not explicitly mentioned | Not explicitly mentioned | |
| Llama 3.1 8B Instant | 128,000 | $0.05 | $0.08 | Not explicitly mentioned | Not explicitly mentioned | |
| Llama 3 70B | 8,000 | $0.59 | $0.79 | Not explicitly mentioned | Not explicitly mentioned | |
| Llama 3 8B | 8,000 | $0.05 | $0.08 | Not explicitly mentioned | Not explicitly mentioned | |
| Gemma 2 9B | 8,000 | $0.20 | $0.20 | Not explicitly mentioned | Not explicitly mentioned | |
| Llama Guard 3 8B | 8,000 | $0.20 | $0.20 | Not explicitly mentioned | Not explicitly mentioned | |

## Key Features
*   **API Endpoints:** Unified API for LLMs.
*   **Pricing Model:** "Tokens-as-a-service" per million tokens. Also offers per-hour pricing for on-demand compute. Batch API for 50% lower cost. Free tier available.
*   **Caching:** Not explicitly mentioned in the search results.
*   **Rate Limits:** Measured in Requests per Minute (RPM), Tokens per Minute (TPM), compute time, and concurrent usage caps. Applied at the organization level and can vary per model. Different API endpoints may have distinct rate limit configurations. Users can access specific limits on the Groq console and can request higher limits.
*   **Supported Modalities:** Primarily text-based LLMs.
*   **Developer Tools/SDKs:** Not explicitly mentioned, but a unified API implies ease of integration.
*   **Unique Selling Propositions:** High-speed, low-latency inference due to custom LPU hardware.

## Pros & Cons
*   **Pros:**
    *   Extremely fast inference speeds.
    *   Competitive pricing for token usage.
    *   Offers a wide range of models with varying capabilities.
*   **Cons:**
    *   Limited to models optimized for their LPU architecture.
    *   Specific details on caching and output size limits are not readily available in the search results.

## Links
*   [Official Website](https://groq.com/)
*   [Pricing Page](https://groq.com/pricing)