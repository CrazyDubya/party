# Microsoft Azure AI Speech

## Overview
Microsoft Azure AI Speech provides Text-to-Speech (TTS) services using AI models to produce natural-sounding voices. It operates on a pay-as-you-go model, with various voice types (Standard, Neural, Custom) and supports commercial usage.

## Models/Technology Used
*   Proprietary AI models for TTS.

## Voice Quality
Natural-sounding voices.

## Language Support
Not explicitly detailed in search results, but implies broad support.

## Voice Options
Standard, Neural, Custom voices.

## Custom Voice/Cloning
Yes, custom voice creation from recordings (Custom Neural Voices).

## SSML Support
Yes, for controlling pitch, speed, and emphasis.

## Emotional/Speaking Styles
Not explicitly detailed in search results.

## API Availability
Yes.

## SDKs/Libraries
Not explicitly detailed in search results.

## Streaming Support
Yes (real-time synthesis).

## Output Formats
Not explicitly detailed in search results.

## Pricing Model
*   **General Model:** Pay-as-you-go, billed per character. Free (F0) Tier available.
*   **Key Cost Factors:** Characters processed, voice type (Standard, Neural, Custom), training compute hours (for Custom Neural Voices), endpoint hosting.
*   **Example Pricing:**
    *   **Free (F0) Tier:** 0.5 million characters/month for Neural voices, 5 million characters/month for Standard/Custom voices.
    *   **Standard TTS:** $4 per 1 million characters.
    *   **Neural TTS:** $16 per 1 million characters (real-time/batch), $100 per 1 million characters (long audio).
    *   **Custom TTS:** $6 per 1 million characters + endpoint hosting fee.
    *   **Custom Neural Voices:** $52 per compute hour (training) + character costs + endpoint hosting.

## Commercial Usage Rights
*   Yes, can be used for commercial purposes. Users are not required to seek permission or pay royalties for generated output.

## Limits & Rate Completions
*   **Free Tier Limits:** 0.5 million characters/month (Neural), 5 million characters/month (Standard/Custom). 20 transactions per 60 seconds.
*   **Paid Tier Limits:** Character limits based on usage.
*   **Rate Limits (API):**
    *   Real-time TTS (Standard S0 Tier): Default 200 transactions per second (TPS), adjustable up to 1000 TPS.
    *   Real-time TTS (Free F0 Tier): Non-adjustable 20 transactions per 60 seconds.
    *   Rate limits can be increased via support request.
*   **Completion Time/Speed:** Synthesis rate automatically scales with requests.

## Key Features
*   **Text-to-Speech Capabilities:** Natural-sounding voice generation.
*   **API Access:** Yes.
*   **Customization:** Custom voice creation, SSML support.
*   **Upscaling/Enhancement:** Not explicitly detailed.
*   **Editing Tools:** Not explicitly detailed.
*   **Integrations:** Designed for enterprise-level businesses and integration within Microsoft ecosystem.
*   **Community/Sharing:** Not explicitly detailed.

## Pros & Cons
*   **Pros:**
    *   High-quality, natural-sounding voices.
    *   Flexible pricing with free tiers.
    *   Custom voice creation.
    *   Scalable synthesis rate.
    *   Commercial usage permitted.
*   **Cons:**
    *   Pricing can be complex due to various voice types and usage scenarios.
    *   Long audio creation is significantly more expensive.

## Links
*   [Official Website](https://azure.microsoft.com/en-us/services/ai-services/text-to-speech/)
*   [Pricing Page](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/speech-services/)
*   [Documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/text-to-speech)