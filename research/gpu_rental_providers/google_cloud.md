# Google Cloud Platform (GCP)

## Overview
Google Cloud offers a comprehensive suite of GPU instances designed to accelerate various compute-intensive workloads, including AI, machine learning, and high-performance computing. They provide a diverse range of NVIDIA GPUs with flexible pricing models, including on-demand, committed use discounts, and spot VMs.

## Infrastructure Model
*   **Owns Infrastructure:** Yes - Google operates its own global data centers and provides a vast cloud infrastructure.
*   **Aggregator/Reseller:** No

## GPU Offerings & Pricing
| GPU Type | Preferred/Popular | On-Demand Price (per hour) | Spot Price (per hour) | Notes |
|---|---|---|---|---|
| NVIDIA H100 (SXM and PCIe) | Yes | Varies | 60-91% off On-Demand | High-performance for training. |
| NVIDIA L4 | Yes | Varies | 60-91% off On-Demand | Cost-optimized inference, graphics. |
| NVIDIA A100 (40GB and 80GB) | Yes | Varies | 60-91% off On-Demand | Popular for training and HPC. |
| NVIDIA T4 | Yes | Varies | 60-91% off On-Demand | Cost-effective AI inference. |
| NVIDIA V100 | No | Varies | 60-91% off On-Demand | |
| NVIDIA P100 | No | Varies | 60-91% off On-Demand | |
| NVIDIA P4 | No | Varies | 60-91% off On-Demand | |
| NVIDIA GB200, B200 | Yes | Varies | 60-91% off On-Demand | Latest generation. |

## Key Features
*   **Pricing Model:** On-Demand, Sustained Use Discounts (SUDs), Committed Use Discounts (CUDs), Spot VMs (60-91% off On-Demand).
*   **Billing Granularity:** Per second.
*   **Instance Types:** Virtual machines.
*   **Storage Options:** Persistent Disk, Local SSD.
*   **Networking:** High-bandwidth networking.
*   **Software Environment:** Integration with Compute Engine, GKE, Dataproc, Vertex AI, Cloud Run.
*   **Geographic Regions:** Global presence with many regions.
*   **Support:** Various support plans available.

## Pros & Cons
*   **Pros:**
    *   Extensive range of GPU instances and configurations.
    *   Flexible pricing models, including significant savings with Spot VMs and CUDs.
    *   Global infrastructure with high availability.
    *   Integrated with a vast ecosystem of Google Cloud services.
*   **Cons:**
    *   Pricing can be complex due to many options.
    *   Spot VMs can be interrupted.

## Links
*   [Official Website](https://cloud.google.com/gpu)
*   [Pricing Page](https://cloud.google.com/compute/gpus-pricing)
*   [Documentation](https://cloud.google.com/compute/docs/gpus)