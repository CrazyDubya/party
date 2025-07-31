# Cloudflare

## Overview
Cloudflare is a global network that provides a wide range of cloud services, including security, performance, and developer tools. While traditionally known for CDN and DDoS protection, they have expanded into serverless compute (Workers), object storage (R2), and AI/ML offerings, focusing on edge computing.

## Core Services & Pricing Model
| Service Category | Key Offerings | Pricing Model (General) | Notes |
|---|---|---|---|---|
| **Compute** | Cloudflare Workers (Serverless Functions), Cloudflare Pages | Usage-based (requests, CPU time). Free tier (100k requests/day, 400k GB-seconds CPU/day). Paid plan starts at $5/month. | Edge computing, JavaScript/WebAssembly. |
| **Storage** | R2 Storage (Object Storage) | Usage-based (per GB-month, Class A/B operations). No egress fees. | S3-compatible, designed for cost-effectiveness. |
| **Networking** | CDN, DNS, Load Balancing, Argo Smart Routing, Magic Transit, Magic WAN, Magic Firewall | Tiered plans (Free, Pro, Business, Enterprise) for core services. Usage-based or add-on pricing for advanced features. | Global network, performance optimization, security. |
| **Databases** | KV storage, Durable Objects (part of Workers) | Usage-based (reads, writes, storage). | Key-value store and strongly consistent storage for Workers. |
| **AI/ML** | Workers AI, Pay-Per-Crawl | Workers AI: $0.011 per 1,000 "Neurons" (GPU compute). Free allocation (10,000 Neurons/day). Pay-Per-Crawl: Monetization/blocking for AI crawlers. | AI inference at the edge. |

## Key Features
*   **Global Infrastructure:** Massive global network with data centers in over 300 cities.
*   **Security:** DDoS protection, WAF, Bot Management, Zero Trust security.
*   **Management & Governance:** Analytics, logging, API for programmatic control.
*   **Developer Tools:** Workers CLI, API, integrations with Git.
*   **Ecosystem & Marketplace:** Integrations with various platforms and services.
*   **Hybrid Cloud Capabilities:** Not their primary focus, but can integrate with existing cloud infrastructure.

## Pros & Cons
*   **Pros:**
    *   Strong focus on edge computing, leading to low latency.
    *   Generous free tiers for many services.
    *   No egress fees for R2 storage.
    *   Comprehensive security features.
    *   Developer-friendly serverless platform.
*   **Cons:**
    *   Less comprehensive traditional IaaS offerings compared to hyperscalers.
    *   Pricing can become complex with many add-ons.
    *   Database offerings are more specialized (KV, Durable Objects) rather than traditional relational/NoSQL.

## Links
*   [Official Website](https://www.cloudflare.com/)
*   [Pricing Page](https://www.cloudflare.com/plans/pricing/)
*   [Developer Platform Pricing](https://developers.cloudflare.com/workers/platform/pricing/)