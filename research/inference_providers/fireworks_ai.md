# Fireworks AI

## Overview
Fireworks AI is a generative inference platform known for its fast model APIs. They offer serverless inference and training for various LLMs, image generation, and speech-to-text, with a usage-based pricing model primarily determined by token usage or inference steps.

## Models Offered
| Model Name | Context Window (Tokens) | Cost per 1M Input Tokens | Cost per 1M Output Tokens | Cache Support | Output Size Limit | Notes |
|---|---|---|---|---|---|---|
| Entry-tier models (<4B params) | Varies | $0.10 | $0.10 | Not explicitly mentioned | Not explicitly mentioned | |
| Mid-tier models (4B-16B params) | Varies | $0.20 | $0.20 | Not explicitly mentioned | Not explicitly mentioned | |
| High-end models (>16B params) | Varies | Up to $0.90-$1.20 | Up to $0.90-$1.20 | Not explicitly mentioned | Not explicitly mentioned | |
| Mixtral | Varies | Tiered rates | Tiered rates | Not explicitly mentioned | Not explicitly mentioned | Mixture of Experts (MoE) model. |
| DBRX | Varies | Tiered rates | Tiered rates | Not explicitly mentioned | Not explicitly mentioned | Mixture of Experts (MoE) model. |
| FireLLaVA-13B | Varies | Varies | Varies | Not explicitly mentioned | Not explicitly mentioned | |
| Llama 4 Scout | 10,000,000 | Varies | Varies | Not explicitly mentioned | Not explicitly mentioned | Industry-leading context window. |

## Key Features
*   **API Endpoints:** Fast model APIs for generative inference.
*   **Pricing Model:** Usage-based, per million tokens for text models (tiered by parameter size). Image generation priced per inference step (e.g., $0.0039 per image at 30 steps). Speech-to-Text also available. Batch API offers 40% cost reduction. On-demand GPU deployments priced per GPU second.
*   **Caching:** Not explicitly mentioned in the search results.
*   **Rate Limits:** Default of 600 Requests Per Minute (RPM) for all serverless models. Business tier users can receive custom, higher limits. Dedicated deployments do not have predefined rate limits.
*   **Supported Modalities:** Text (LLMs), Image Generation, Speech-to-Text.
*   **Developer Tools/SDKs:** Not explicitly mentioned.
*   **Unique Selling Propositions:** High-performance and fast model APIs, competitive pricing, Batch API for cost savings, serverless serving of fine-tuned models with no extra cost, large context windows for some models.

## Pros & Cons
*   **Pros:**
    *   High-performance and fast model APIs.
    *   Transparent tiered pricing.
    *   Cost-effective for large-scale tasks with Batch API.
    *   No extra cost for serving fine-tuned models.
    *   Supports multimodal AI.
*   **Cons:**
    *   Specific details on caching and output size limits are not readily available in the search results.

## Links
*   [Official Website](https://fireworks.ai/)
*   [Pricing Page](https://fireworks.ai/pricing)