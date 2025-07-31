# Vast.ai

## Overview
Vast.ai is a GPU cloud marketplace that connects users with a global network of GPU providers. It offers highly cost-effective access to a wide range of NVIDIA GPUs through a bidding system for interruptible instances, as well as on-demand and reserved options.

## Infrastructure Model
*   **Owns Infrastructure:** No
*   **Aggregator/Reseller:** Yes - Vast.ai operates as a marketplace, aggregating GPUs from individual hobbyists to large data centers.

## GPU Offerings & Pricing
| GPU Type | Preferred/Popular | On-Demand Price (per hour) | Spot Price (per hour) | Notes |
|---|---|---|---|---|
| NVIDIA H200 | Yes | Varies | Varies (bidding system) | Latest generation. |
| NVIDIA H100 (SXM, NVL, PCIe) | Yes | Varies | Varies (bidding system) | High-performance. |
| NVIDIA RTX 4090 | Yes | Varies | Varies (bidding system) | Popular consumer-grade. |
| NVIDIA RTX 3090 | Yes | Varies | Varies (bidding system) | Popular consumer-grade. |
| NVIDIA A100 (SXM4, PCIe) | Yes | Varies | Varies (bidding system) | Popular for AI/ML. |
| NVIDIA RTX 6000 Ada | Yes | Varies | Varies (bidding system) | |
| NVIDIA L40S | Yes | Varies | Varies (bidding system) | |
| NVIDIA A40 | No | Varies | Varies (bidding system) | |
| NVIDIA Tesla V100 | No | Varies | Varies (bidding system) | |
| NVIDIA RTX 2080 Ti | No | Varies | Varies (bidding system) | |
| NVIDIA GTX 1080 Ti | No | Varies | Varies (bidding system) | |

## Key Features
*   **Pricing Model:** On-Demand, Reserved Instances (up to 50% off), Interruptible Instances (Spot Instances) with a bidding system. Billed per second.
*   **Billing Granularity:** Per second.
*   **Instance Types:** Linux Docker instances (containers).
*   **Storage Options:** Local SSD, network storage, object storage.
*   **Networking:** Not explicitly detailed, but supports SSH, Jupyter, and APIs.
*   **Software Environment:** Supports prebuilt templates (PyTorch, NVIDIA CUDA, TensorFlow, Ubuntu) and custom images.
*   **Geographic Regions:** Global presence with hosts in various regions worldwide.
*   **Support:** Community, enterprise options with dedicated support.

## Pros & Cons
*   **Pros:**
    *   Highly cost-effective, especially for interruptible workloads through bidding system.
    *   Wide range of NVIDIA GPUs, including latest models.
    *   Globally distributed network.
    *   Flexible billing with per-second granularity.
    *   Transparent, real-time pricing.
*   **Cons:**
    *   Interruptible instances carry the risk of preemption.
    *   Pricing can fluctuate based on market demand.

## Links
*   [Official Website](https://vast.ai/)
*   [Pricing Page](https://vast.ai/pricing)
*   [Documentation](https://vast.ai/docs)