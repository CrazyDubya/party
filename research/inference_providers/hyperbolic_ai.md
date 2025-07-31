# Hyperbolic AI

## Overview
Hyperbolic AI offers an inference service with competitive token-based pricing for various AI models, including LLMs, image generation, and text-to-speech. They provide both serverless inference and dedicated GPU instances for custom model hosting, aiming to be a cost-effective solution.

## Models Offered
| Model Name | Context Window (Tokens) | Cost per 1M Input Tokens | Cost per 1M Output Tokens | Cache Support | Output Size Limit | Notes |
|---|---|---|---|---|---|---|
| Llama 3.1 8B (BF16) | Varies | $0.1 | $0.1 | Not explicitly mentioned | Not explicitly mentioned | |
| Llama 3.1 70B (BF16) | Varies | $0.4 | $0.4 | Not explicitly mentioned | Not explicitly mentioned | |
| Llama 3.1 405B (BF16) | Varies | $4 | $4 | Not explicitly mentioned | Not explicitly mentioned | |
| Llama 3 70B (BF16) | Varies | $0.4 | $0.4 | Not explicitly mentioned | Not explicitly mentioned | |
| Llama 3.2 3B (BF16) | Varies | $0.1 | $0.1 | Not explicitly mentioned | Not explicitly mentioned | |
| Llama 3.3 70B (BF16) | Varies | $0.4 | $0.4 | Not explicitly mentioned | Not explicitly mentioned | |
| Qwen 2.5 72B (BF16) | Varies | $0.4 | $0.4 | Not explicitly mentioned | Not explicitly mentioned | |
| Qwen 2.5 Coder 32B (BF16) | Varies | $0.2 | $0.2 | Not explicitly mentioned | Not explicitly mentioned | |
| Qwen 2.5 VL 7B Instruct (BF16) | Varies | $0.2 | $0.2 | Not explicitly mentioned | Not explicitly mentioned | |
| Qwen 2.5 VL 72B Instruct (BF16) | Varies | $0.6 | $0.6 | Not explicitly mentioned | Not explicitly mentioned | |
| Qwen 3 Coder 480B A35B (FP8) | Varies | $2 | $2 | Not explicitly mentioned | Not explicitly mentioned | |
| Qwen 3 235B A22B (FP8) | Varies | $0.4 | $0.4 | Not explicitly mentioned | Not explicitly mentioned | |
| Qwen 3 235B A22B Instruct 2507 | Varies | $2 | $2 | Not explicitly mentioned | Not explicitly mentioned | |
| Pixtral 12B (BF16) | Varies | $0.1 | $0.1 | Not explicitly mentioned | Not explicitly mentioned | |
| DeepSeek-V2.5 | Varies | $2.00 | $2.00 | Not explicitly mentioned | Not explicitly mentioned | |
| Hermes-3-70B | Varies | $0.40 | $0.40 | Not explicitly mentioned | Not explicitly mentioned | |

## Key Features
*   **API Endpoints:** Offers inference services.
*   **Pricing Model:** Token-based pricing per 1 million tokens for serverless inference. Also offers hourly hosting fees for dedicated GPU instances (e.g., H100 SXM: $3.20/hr, RTX 4090: $0.50/hr). Image generation ($0.01/image) and Text-to-Speech ($5.00 per 1M characters) also available. Pay-as-you-go with no hidden fees.
*   **Caching:** Not explicitly mentioned in the search results.
*   **Rate Limits:** Vary by service tier (Basic: 60 RPM; Pro: 600 RPM; Enterprise: Custom/Unlimited) and specific model (e.g., Llama 3.1 405B: 5 RPM Basic, 120 RPM Pro). IP address limit of 600 RPM.
*   **Supported Modalities:** Text (LLMs), Image Generation, Text-to-Speech.
*   **Developer Tools/SDKs:** Not explicitly mentioned.
*   **Unique Selling Propositions:** Cost-effective (claims 3-10x less expensive than competitors), dedicated GPU instances for custom hosting, multimodal offerings.

## Pros & Cons
*   **Pros:**
    *   Competitive pricing for inference.
    *   Offers dedicated instances for more control and optimization.
    *   Flexible pay-as-you-go model.
    *   Multimodal capabilities.
*   **Cons:**
    *   Specific details on caching and output size limits for LLMs are not readily available in the search results.

## Links
*   [Official Website](https://hyperbolic.ai/)
*   [Pricing Page](https://hyperbolic.ai/pricing)