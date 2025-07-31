# TensorDock

## Overview
TensorDock is a GPU cloud marketplace that offers on-demand access to a variety of GPU models for AI, machine learning, rendering, and cloud gaming workloads. It operates on a marketplace model where independent hosts provide GPU resources, contributing to its competitive pricing.

## Infrastructure Model
*   **Owns Infrastructure:** No
*   **Aggregator/Reseller:** Yes - TensorDock operates as a marketplace, aggregating GPUs from independent hosts.

## GPU Offerings & Pricing
| GPU Type | Preferred/Popular | On-Demand Price (per hour) | Spot Price (per hour) | Notes |
|---|---|---|---|---|
| NVIDIA HGX H100 SXM5 (80GB) | Yes | From $2.25 | Varies (bidding system) | |
| NVIDIA RTX 4090 (24GB) | Yes | From $0.35 | Varies (bidding system) | |
| NVIDIA A100 SXM4 (80GB) | Yes | Varies | Varies (bidding system) | |
| NVIDIA RTX A6000 (48GB) | Yes | Varies | Varies (bidding system) | |
| NVIDIA RTX 3090 (24GB) | Yes | Varies | Varies (bidding system) | |
| NVIDIA RTX 5090 (32GB) | Yes | Varies | Varies (bidding system) | |
| NVIDIA RTX 5000 ADA (32GB) | Yes | Varies | Varies (bidding system) | |
| NVIDIA RTX PRO 6000 (96GB) | Yes | Varies | Varies (bidding system) | |
| NVIDIA V100 (32GB) | No | Varies | Varies (bidding system) | |
| NVIDIA L40 (48GB) | No | Varies | Varies (bidding system) | |

## Key Features
*   **Pricing Model:** Pay-as-you-go (billed per second, no minimums), Spot Instances (beta, bidding system, interruptible), Marketplace model.
*   **Billing Granularity:** Per second.
*   **Instance Types:** Virtual machines.
*   **Storage Options:** Not explicitly detailed, but storage costs are separate.
*   **Networking:** Not explicitly detailed.
*   **Software Environment:** Supports Docker, full OS control, pre-configured OS images with drivers and ML frameworks.
*   **Geographic Regions:** Global and scalable, over 100 locations across 20+ countries.
*   **Support:** Not explicitly detailed.

## Pros & Cons
*   **Pros:**
    *   Highly competitive pricing due to marketplace model.
    *   Wide selection of GPUs, including high-end models.
    *   Flexible pay-as-you-go billing.
    *   Global presence.
*   **Cons:**
    *   Spot instances are in beta and interruptible.
    *   Reliability can vary due to independent hosts (some hardware might be converted mining rigs).

## Links
*   [Official Website](https://tensordock.com/)
*   [Pricing Page](https://tensordock.com/pricing)
*   [Documentation](https://tensordock.com/docs)