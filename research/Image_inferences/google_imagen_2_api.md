# Google Imagen 2 API (via Vertex AI)

## Overview
Google Imagen 2 API, delivered through Google Cloud's Vertex AI, leverages Google's AI capabilities to produce high-quality images from text prompts. It offers a token-based pricing model for image generation and supports commercial usage with an indemnification commitment.

## Models/Technology Used
*   Imagen 2
*   Gemini API (for image generation capabilities within Vertex AI)

## Pricing Model
*   **General Model:** Pay-as-you-go, token-based for image output, query-based for chat interactions. Free trial credits available.
*   **Key Cost Factors:** Tokens consumed per image, number of queries.
*   **Example Pricing:**
    *   Image output (up to 1024x1024): ~$0.039 per image (calculated based on 1290 tokens/image at $30 per 1M tokens).
    *   Batch Mode requests: 50% of interactive requests.

## Commercial Usage Rights
*   Yes, commercial use is supported. Google provides an indemnification commitment for Imagen on Vertex AI.

## Limits & Rate Completions
*   **Free Tier Limits:** Free trial with $300 in credits.
*   **Paid Tier Limits:** Rate limits vary by project's usage tier.
*   **Rate Limits (API):** Measured in Requests per Minute (RPM), Tokens per Minute (TPM), and Images per Minute (IPM). Online inference requests have a quota of 30,000 RPM per region. Some models use Dynamic Shared Quota (DSQ) with no predefined fixed quotas. Preview models may have more restrictive limits.
*   **Completion Time/Speed:** Not explicitly detailed in search results.

## Key Features
*   **Image Generation Capabilities:** Text-to-image.
*   **API Access:** Yes (via Vertex AI).
*   **Customization:** Text prompts.
*   **Upscaling/Enhancement:** Not explicitly detailed.
*   **Editing Tools:** Not explicitly detailed.
*   **Integrations:** Integrated with Google Cloud's Vertex AI platform.
*   **Community/Sharing:** Not explicitly detailed.

## Pros & Cons
*   **Pros:**
    *   High-quality image generation.
    *   Commercial usage supported with indemnification.
    *   Integration with Google Cloud ecosystem.
    *   Flexible pricing with batch mode discounts.
*   **Cons:**
    *   Specific IPM rate limits are not explicitly listed for all models.
    *   Pricing can be complex due to token-based and query-based components.

## Links
*   [Official Website](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/imagen)
*   [Pricing Page](https://cloud.google.com/vertex-ai/pricing#imagen)
*   [Documentation](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/imagen)