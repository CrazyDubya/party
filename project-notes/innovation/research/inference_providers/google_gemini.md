# Google Gemini

## Overview
Google Gemini offers a family of powerful multimodal models accessible via API, designed for various tasks from text generation to complex reasoning. Their pricing is primarily token-based, with a focus on large context windows and cost optimization through caching.

## Models Offered
| Model Name | Context Window (Tokens) | Cost per 1M Input Tokens | Cost per 1M Output Tokens | Cache Support | Output Size Limit | Notes |
|---|---|---|---|---|---|---|
| Gemini 1.5 Pro | 1,000,000 (up to 2M) | Varies | Varies | Yes (Explicit & Implicit) | Not explicitly mentioned | |
| Gemini 1.5 Flash | 1,000,000 | Varies | Varies | Yes (Explicit & Implicit) | Not explicitly mentioned | |
| Gemini 2.0 Flash | Varies | Single price per input type | Single price per input type | Yes (Implicit) | Not explicitly mentioned | Optimized pricing, no short/long context distinction. |
| Gemini 2.0 Flash-Lite | Varies | Single price per input type | Single price per input type | Yes (Implicit) | Not explicitly mentioned | |
| Gemini 1.5 Flash-8B | Varies | Varies | Varies | Yes (Implicit) | Not explicitly mentioned | |

## Key Features
*   **API Endpoints:** RESTful API.
*   **Pricing Model:** Token-based (input, output, cached tokens). Free tier available. Charges for cached token storage duration.
*   **Caching:**
    *   **Explicit Caching:** Manually enabled, guarantees cost savings, configurable TTL.
    *   **Implicit Caching:** Automatically enabled for Gemini 2.5 models, applies cost savings if cache hit.
*   **Rate Limits:** Applied per project, vary by model and usage tier. Include Requests per Minute (RPM), Tokens per Minute (TPM), and Requests per Day (RPD). Example: Free tier for Gemini 2.5 Pro has 5 RPM, 1M TPM, 25 RPD. Users can upgrade to higher tiers for increased limits.
*   **Supported Modalities:** Multimodal (text, images, audio, video).
*   **Developer Tools/SDKs:** Official SDKs and integration with Google Cloud Vertex AI.
*   **Unique Selling Propositions:** Large context windows (up to 2M tokens), advanced multimodal capabilities, explicit and implicit caching for cost reduction.

## Pros & Cons
*   **Pros:**
    *   Very large context windows for complex tasks.
    *   Advanced multimodal capabilities.
    *   Sophisticated caching mechanisms for cost optimization.
    *   Free tier for testing.
*   **Cons:**
    *   Cost for cached token storage.
    *   Pricing can be complex due to various models and caching nuances.

## Links
*   [Official Website](https://gemini.google.com/api)
*   [Pricing Page](https://ai.google.dev/pricing)