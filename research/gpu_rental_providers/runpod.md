# Runpod

## Overview
Runpod offers a flexible and competitive GPU cloud computing platform designed for AI and machine learning workloads. They provide a wide range of NVIDIA GPUs with pay-by-the-minute billing, including spot instance options, across a globally distributed network.

## Infrastructure Model
*   **Owns Infrastructure:** Yes (for Secure Cloud) - They operate their own data centers for Secure Cloud offerings.
*   **Aggregator/Reseller:** Yes (for Community Cloud) - They act as a marketplace for GPUs from various providers.

## GPU Offerings & Pricing
| GPU Type | Preferred/Popular | On-Demand Price (per hour) | Spot Price (per hour) | Notes |
|---|---|---|---|---|
| NVIDIA H200 | Yes | ~$3.99 | Varies (up to 50% cheaper) | High-performance. |
| NVIDIA B200 | Yes | ~$5.99 | Varies (up to 50% cheaper) | High-performance. |
| NVIDIA H100 (PCIe and SXM) | Yes | ~$2.39 (PCIe), ~$2.69 (SXM) | Varies (up to 50% cheaper) | |
| NVIDIA A100 (PCIe and SXM) | Yes | ~$1.64 (PCIe), ~$1.74 (SXM) | Varies (up to 50% cheaper) | |
| NVIDIA RTX 3090 | Yes | ~$0.46 | Varies (up to 50% cheaper) | Popular consumer-grade. |
| NVIDIA RTX 4090 | Yes | ~$0.69 | Varies (up to 50% cheaper) | Popular consumer-grade. |
| NVIDIA RTX 6000 Ada | Yes | ~$0.77 | Varies (up to 50% cheaper) | |
| NVIDIA L40S | Yes | ~$0.86 | Varies (up to 50% cheaper) | |
| NVIDIA A40 | No | ~$0.40 | Varies (up to 50% cheaper) | |
| NVIDIA RTX A6000 | No | ~$0.49 | Varies (up to 50% cheaper) | |
| NVIDIA L4 | No | ~$0.43 | Varies (up to 50% cheaper) | |
| NVIDIA RTX A5000 | No | ~$0.27 | Varies (up to 50% cheaper) | |

## Key Features
*   **Pricing Model:** Pay-as-you-go (billed by the second), Spot instances (up to 50% cheaper), Serverless (pay only while code runs).
*   **Billing Granularity:** Per second.
*   **Instance Types:** Pods (dedicated GPU instances), Serverless.
*   **Storage Options:** Persistent and temporary storage, network volumes.
*   **Networking:** Globally distributed network.
*   **Software Environment:** Containerized workloads (Docker), customizable environments.
*   **Geographic Regions:** Globally distributed network across more than 30 regions.
*   **Support:** Not explicitly detailed in search results.

## Pros & Cons
*   **Pros:**
    *   Highly flexible pricing with pay-by-the-minute and spot options.
    *   Wide range of NVIDIA GPUs, including latest models.
    *   Globally distributed network for high availability.
    *   Supports both community marketplace and secure dedicated cloud.
    *   No hidden fees for data transfer.
*   **Cons:**
    *   Spot instances can be interrupted.

## Links
*   [Official Website](https://www.runpod.io/)
*   [Pricing Page](https://www.runpod.io/gpu-cloud/pricing)
*   [Documentation](https://docs.runpod.io/)