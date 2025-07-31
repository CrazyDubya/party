# Cheapest/Free Model Comparison Across Inference Providers

This report compares the cheapest or free models/plans offered by various LLM inference providers, including their pricing, context window, cache support, output size limit, and rate limits.

## Table 1: Cheapest/Free Models from Direct Inference Providers

| Provider | Model Name | Context Window (Tokens) | Cost per 1M Input Tokens | Cost per 1M Output Tokens | Cache Support | Output Size Limit | Rate Limits (RPM/TPM) | Notes |
|---|---|---|---|---|---|---|---|---|
| **OpenAI** | GPT-3.5 Turbo | Varies | $0.50 | $1.50 | Yes (Automatic Prompt Caching) | Varies | Varies by account/usage | Cheapest paid model. |
| **xAI / Grok** | Grok 3 Mini | 131,072 | $0.30 | $0.50 | Yes (Input Token Caching) | Not explicitly mentioned | Varies by tier/feature | Cheapest paid model. Basic (Free) tier for Grok 3 also available. |
| **Google Gemini** | Free Tier | Varies | Free | Free | Yes (Explicit & Implicit) | Not explicitly mentioned | 5 RPM, 1M TPM, 25 RPD (for Gemini 2.5 Pro) | Free tier for testing. |
| **Anthropic** | Claude 3 Haiku | 200,000 (up to 500k enterprise) | Varies | Varies | Yes (Prompt Caching) | Not explicitly mentioned | Varies by model/tier | Cheapest paid model. |
| **OpenRouter** | Mistral 7B (example) | Varies | Free | Free | Yes (Prompt Caching) | Varies | Not explicitly detailed | Many free models available. |
| **Groq** | Llama 3.1 8B Instant | 128,000 | $0.05 | $0.08 | Not explicitly mentioned | Not explicitly mentioned | Varies by tier/model | Cheapest paid model. Free tier also available. |
| **Hyperbolic AI** | Llama 3.1 8B (BF16) | Varies | $0.1 | $0.1 | Not explicitly mentioned | Not explicitly mentioned | Basic: 60 RPM | Cheapest paid model. |
| **Novita AI** | DeepSeek R1 0528 Qwen3 8B | Varies | $0.06 | $0.09 | Not explicitly mentioned | Not explicitly mentioned | Varies by model/type | Cheapest paid LLM. |
| **Fireworks AI** | Entry-tier models (<4B params) | Varies | $0.10 | $0.10 | Not explicitly mentioned | Not explicitly mentioned | 600 RPM (serverless) | Cheapest paid models. |
| **Hugging Face Inference Endpoints** | Free Tier (CPU) | Varies by model | N/A (Instance-based) | N/A (Instance-based) | Not explicitly mentioned | Varies by model | Varies by tier/instance | Free tier for inference, instance-based. Lowest cost CPU instance: $0.03/hour. |

## Table 2: Cheapest/Free Plans from LLM Gateways / Management Platforms

| Provider | Plan Name | Cost | Rate Limits (RPM/TPM) | Notes |
|---|---|---|---|---|
| **LiteLLM** | Open-source library/proxy | Free | Configurable (tpm, rpm, parallel requests) | Free to use, self-hosted. |
| **Eden AI** | Starter Plan | Free (with $10 credit) | 60 API calls/min | Free tier for testing. |
| **Kong AI Gateway** | Open-source version | Free | Configurable (token-based, HTTP requests) | Free to use, self-hosted. |
| **Taam Cloud** | Basic Plan | Varies (pay-as-you-go) | 1000 RPM | Lowest cost plan. |

## Analysis

### Direct Inference Providers
*   **Free Tiers:** Google Gemini, OpenRouter, Groq, and Hugging Face Inference Endpoints offer free tiers or free models, making them excellent for initial experimentation and development without immediate cost. These free options often come with specific rate limits.
*   **Cheapest Paid Models:** For paid usage, models like Groq's Llama 3.1 8B Instant and Hyperbolic AI's Llama 3.1 8B (BF16) offer extremely competitive per-token pricing, especially for open-source models. OpenAI's GPT-3.5 Turbo provides a cost-effective entry into their proprietary models.
*   **Instance-Based vs. Token-Based:** Hugging Face Inference Endpoints stand out with their instance-based pricing. While there's no direct token cost, the hourly rate of the chosen compute instance determines the cost. This can be highly cost-effective for consistent, high-volume workloads where the model is constantly in use.

### LLM Gateways / Management Platforms
*   **Free Tools:** LiteLLM and Kong AI Gateway offer free, open-source solutions for managing LLM API calls, including rate limiting and cost tracking. These are valuable for developers who want to build their own LLM orchestration layer.
*   **Free Tiers with Credits:** Eden AI provides a free Starter Plan with initial credits, allowing users to test their unified API and access various AI services.
*   **Value Proposition:** These platforms primarily offer value through cost optimization, improved reliability (e.g., fallbacks), and simplified integration with multiple underlying LLM providers, rather than offering their own cheapest models.

### Key Considerations for Choosing a Cheapest/Free Option
*   **Use Case:** For simple, low-volume tasks, free tiers or very cheap token-based models are ideal. For continuous, high-volume workloads, instance-based pricing might be more economical.
*   **Model Capabilities:** Free or cheapest models often have limitations in terms of context window, performance, or advanced capabilities compared to their more expensive counterparts.
*   **Self-Hosting vs. Managed Service:** Open-source gateways offer flexibility but require self-hosting. Managed services provide convenience but may have subscription fees.
*   **Rate Limits:** Always consider the rate limits associated with free or cheapest tiers, as they can significantly impact the scalability of your application.

This comparison provides a clear overview of the most cost-effective options available across the LLM inference provider landscape.