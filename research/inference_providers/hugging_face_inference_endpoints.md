# Hugging Face Inference Endpoints

## Overview
Hugging Face Inference Endpoints provide a hosted solution for deploying and serving a wide range of open-source Large Language Models (LLMs) and other AI models. Their pricing is based on the compute instance selected and its active running time, offering a different cost model compared to token-based systems.

## Models Offered
| Model Name | Context Window (Tokens) | Cost per 1M Input Tokens | Cost per 1M Output Tokens | Cache Support | Output Size Limit | Notes |
|---|---|---|---|---|---|---|
| (Vast array of open-source models) | Varies by model | N/A (Instance-based pricing) | N/A (Instance-based pricing) | Not explicitly mentioned | Varies by model | Hugging Face hosts a massive collection of open-source models. Users deploy specific models to their Inference Endpoints. |

## Key Features
*   **API Endpoints:** Dedicated API endpoints for deployed models.
*   **Pricing Model:** Hourly or per-minute pricing based on the selected compute instance (CPU, GPU, or Accelerator). No separate charge for context window tokens. Example rates: 1 vCPU, 2GB memory AWS Intel Sapphire Rapids CPU instance starts at $0.03/hour. GPU instances range from $0.6 to $45/hour.
*   **Caching:** Not explicitly mentioned in the search results for Inference Endpoints.
*   **Rate Limits:** Vary by tier (Free, Pro, Dedicated). Free tier limits are not explicitly published but are generally a few hundred RPM, with a 10GB max model size. Pro plan offers higher limits. Dedicated endpoints have virtually unlimited usage. Limits are subject to change.
*   **Supported Modalities:** Text, Image, Audio, and other modalities supported by the vast array of models on Hugging Face.
*   **Developer Tools/SDKs:** Integrates with the Hugging Face ecosystem (Transformers library, Hub).
*   **Unique Selling Propositions:** Unparalleled access to a diverse range of open-source models, flexible instance-based pricing, managed deployment, and scaling.

## Pros & Cons
*   **Pros:**
    *   Unparalleled access to a diverse range of open-source models.
    *   Predictable costs for consistent workloads (fixed hourly/minute rate).
    *   Managed deployment and scaling of models.
*   **Cons:**
    *   Less cost-effective for intermittent or low-volume usage compared to pay-per-token models.
    *   Requires managing instance types and scaling.
    *   Specific details on caching and output size limits are not readily available in the search results.

## Links
*   [Official Website (Inference Endpoints)](https://huggingface.co/inference-endpoints)
*   [Pricing Page](https://huggingface.co/pricing#inference-endpoints)