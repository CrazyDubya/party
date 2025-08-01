# Anthropic

## Overview
Anthropic is an AI safety and research company that develops large language models, most notably the Claude series. Their API provides access to these models with a pay-as-you-go, token-based pricing model, and offers a Prompt Caching feature for cost and latency optimization.

## Models Offered
| Model Name | Context Window (Tokens) | Cost per 1M Input Tokens | Cost per 1M Output Tokens | Cache Support | Output Size Limit | Notes |
|---|---|---|---|---|---|---|
| Claude 3.5 Sonnet | 200,000 (up to 500k enterprise) | $3.00 | Varies | Yes (Prompt Caching) | Not explicitly mentioned | |
| Claude 3 Haiku | 200,000 (up to 500k enterprise) | Varies | Varies | Yes (Prompt Caching) | Not explicitly mentioned | |
| Claude 3 Opus | 200,000 (up to 500k enterprise) | Varies | Varies | Yes (Prompt Caching) | Not explicitly mentioned | |

## Key Features
*   **API Endpoints:** RESTful API.
*   **Pricing Model:** Pay-as-you-go, token-based. Different models have distinct pricing for input and output tokens.
*   **Caching:** Prompt Caching available.
    *   **Writing to cache:** 25% higher than base input token price.
    *   **Reading from cache:** 10% of base input token price.
    *   Can achieve up to 90% cost reduction and 85% latency improvement for long, repetitive prompts.
*   **Rate Limits:** Enforced at the organization and workspace level. Measured in Requests Per Minute (RPM), Input Tokens Per Minute (ITPM), and Output Tokens Per Minute (OTPM). Vary by model class and usage tier (e.g., Tier 1, Tier 2). Free and Pro users have daily/weekly message limits. Exceeding limits results in a 429 error with a `retry-after` header.
*   **Supported Modalities:** Primarily text-based LLMs.
*   **Developer Tools/SDKs:** Not explicitly mentioned, but an API implies ease of integration.
*   **Unique Selling Propositions:** Focus on AI safety, large context windows, detailed pricing for prompt caching.

## Pros & Cons
*   **Pros:**
    *   Access to Claude models with large context windows.
    *   Explicit pricing for prompt caching, offering significant cost savings for specific use cases.
    *   Strong focus on AI safety.
*   **Cons:**
    *   Caching has a cost for writing to the cache.
    *   Specific details on output size limits are not readily available.

## Links
*   [Official Website](https://www.anthropic.com/)
*   [Pricing Page](https://www.anthropic.com/api)