# CoreWeave

## Overview
CoreWeave is a specialized cloud provider focusing on GPU-accelerated infrastructure for compute-intensive workloads like AI, machine learning, and VFX rendering. They offer a Kubernetes-native platform designed for high performance and efficiency, with flexible pricing for highly configurable instances.

## Infrastructure Model
*   **Owns Infrastructure:** Yes - CoreWeave operates its own data centers and provides bare metal servers.
*   **Aggregator/Reseller:** No

## GPU Offerings & Pricing
| GPU Type | Preferred/Popular | On-Demand Price (per hour) | Spot Price (per hour) | Notes |
|---|---|---|---|---|
| NVIDIA H100 (PCIe and SXM) | Yes | Varies | Not offered (On-demand competitive with spot) | Latest generation, high-performance. |
| NVIDIA A100 (80GB and 40GB, PCIe and NVLINK) | Yes | Varies | Not offered (On-demand competitive with spot) | Popular for AI/ML. |
| NVIDIA L40S | Yes | Varies | Not offered (On-demand competitive with spot) | |
| NVIDIA L4 | Yes | Varies | Not offered (On-demand competitive with spot) | |
| NVIDIA RTX PRO 6000 Blackwell Server Edition | Yes | Varies | Not offered (On-demand competitive with spot) | |
| NVIDIA H200 | Yes | Varies | Not offered (On-demand competitive with spot) | Newer generation. |
| NVIDIA Blackwell (B200, GH200, GB200 NVL72) | Yes | Varies | Not offered (On-demand competitive with spot) | Future/latest architectures. |
| NVIDIA A40 | No | Varies | Not offered (On-demand competitive with spot) | |
| NVIDIA Tesla V100 NVLINK | No | Varies | Not offered (On-demand competitive with spot) | |
| NVIDIA Quadro RTX 5000 | No | Varies | Not offered (On-demand competitive with spot) | |
| NVIDIA Quadro RTX 4000 | No | Varies | Not offered (On-demand competitive with spot) | |

## Key Features
*   **Pricing Model:** On-demand (highly configurable instances), Reserved instances. Claims to be up to 80% less expensive than generalized public clouds.
*   **Billing Granularity:** Not explicitly detailed in search results, but implied to be granular.
*   **Instance Types:** Bare metal servers, Kubernetes-native platform.
*   **Storage Options:** Object, File, and Block Storage services optimized for AI (up to 2 GB/s/GPU throughput).
*   **Networking:** High-performance networking.
*   **Software Environment:** Kubernetes-native architecture, supports Slurm on Kubernetes (SUNK).
*   **Geographic Regions:** United States and Europe (32 data centers in 2025).
*   **Support:** Not explicitly detailed in search results.

## Pros & Cons
*   **Pros:**
    *   Purpose-built and optimized for GPU-intensive AI/ML workloads.
    *   Competitive on-demand pricing, often comparable to other providers' spot rates.
    *   Access to latest NVIDIA GPUs.
    *   High-performance networking and storage.
    *   Kubernetes-native platform for easy scaling.
*   **Cons:**
    *   Does not offer traditional spot instances (though on-demand is competitive).
    *   More limited geographic regions compared to hyperscalers.

## Links
*   [Official Website](https://www.coreweave.com/)
*   [Pricing Page](https://www.coreweave.com/pricing)
*   [Documentation](https://docs.coreweave.com/)