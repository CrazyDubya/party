# Kong AI Gateway

## Overview
Kong AI Gateway is an open-source and enterprise-grade LLM gateway that helps manage, optimize, and secure interactions with various Large Language Model (LLM) providers. It offers features like prompt compression, semantic caching, and AI rate limiting to reduce costs and improve efficiency.

## Models Offered
| Model Name | Context Window (Tokens) | Cost per 1M Input Tokens | Cost per 1M Output Tokens | Cache Support | Output Size Limit | Notes |
|---|---|---|---|---|---|---|
| (Kong AI Gateway does not offer models directly) | Varies by underlying provider | Varies by underlying provider | Varies by underlying provider | Yes (Semantic Caching) | Varies by underlying provider | Kong AI Gateway integrates with various LLM providers (e.g., OpenAI, Azure AI, AWS Bedrock, GCP Vertex). It helps manage costs and usage for these external models. |

## Key Features
*   **API Endpoints:** Acts as an LLM Gateway, sitting in front of various AI models.
*   **Pricing Model:** Open-source version is free. Enterprise features are part of the broader Kong Konnect platform, with pricing based on factors like gateway services, API requests, and advanced features. Specific AI Gateway pricing is related to "Unique LLMs proxied by AI plugins measured hourly, enforced monthly."
*   **Caching:** Semantic caching to prevent redundant LLM calls.
*   **Rate Limits:** Advanced token-based rate limiting for AI workloads via the "AI Rate Limiting Advanced" plugin (Enterprise). Can be used with standard HTTP request rate limiting. Supports local, cluster, and Redis strategies. Provides client feedback headers.
*   **Supported Modalities:** Dependent on the underlying LLM providers it integrates with.
*   **Developer Tools/SDKs:** Integrates with the Kong ecosystem.
*   **Unique Selling Propositions:** Prompt compression (up to 5x cost reduction), semantic caching, AI rate limiting, centralized management of AI prompt contexts, open-source option.

## Pros & Cons
*   **Pros:**
    *   Powerful features for cost optimization (compression, caching).
    *   Robust management and security features for LLM interactions.
    *   Open-source option available.
    *   Integrates with a wide range of LLM providers.
*   **Cons:**
    *   Does not provide its own LLM inference; relies on external providers.
    *   Enterprise features require a broader Kong Konnect subscription, which can be complex in pricing.

## Links
*   [Official Website](https://konghq.com/ai-gateway)
*   [Pricing (Kong Konnect)](https://konghq.com/kong-konnect-pricing)