# Microsoft Azure

## Overview
Microsoft Azure offers a variety of GPU-enabled Virtual Machines (VMs) designed for compute and graphics-intensive workloads such as AI, machine learning, deep learning, and high-performance computing. They provide a wide range of NVIDIA and AMD GPUs with flexible pricing models, including pay-as-you-go, reserved instances, and spot instances.

## Infrastructure Model
*   **Owns Infrastructure:** Yes - Microsoft operates its own global data centers and provides a vast cloud infrastructure.
*   **Aggregator/Reseller:** No

## GPU Offerings & Pricing
| GPU Type | Preferred/Popular | On-Demand Price (per hour) | Spot Price (per hour) | Notes |
|---|---|---|---|---|
| NVIDIA H100 | Yes | Varies | Up to 90% off Pay-as-you-go | Best for AI training and large language models. |
| NVIDIA A100 (80GB) | Yes | Varies | Up to 90% off Pay-as-you-go | Suited for high-performance computing and deep learning. |
| NVIDIA L40S | Yes | Varies | Up to 90% off Pay-as-you-go | Good for generative AI, rendering, and virtualization. |
| NVIDIA RTX A6000 Ada | Yes | Varies | Up to 90% off Pay-as-you-go | Excellent for CAD and professional graphics. |
| NVIDIA V100 | No | Varies | Up to 90% off Pay-as-you-go | |
| NVIDIA T4 | No | Varies | Up to 90% off Pay-as-you-go | Suitable for ML inference and light workloads. |
| NVIDIA M60 | No | Varies | Up to 90% off Pay-as-you-go | |
| AMD MI25 | No | Varies | Up to 90% off Pay-as-you-go | Used in NVv4 series for GPU-accelerated graphics. |

## Key Features
*   **Pricing Model:** Pay-as-you-go, Reserved Instances, Azure Savings Plan for Compute, Spot Instances (up to 90% off).
*   **Billing Granularity:** Per second for running VMs.
*   **Instance Types:** Virtual machines.
*   **Storage Options:** Azure Managed Disks.
*   **Networking:** High-throughput networking.
*   **Software Environment:** Supports various images with pre-installed ML frameworks.
*   **Geographic Regions:** Global presence with many regions.
*   **Support:** Various support plans available.

## Pros & Cons
*   **Pros:**
    *   Extensive range of GPU instances and configurations.
    *   Flexible pricing models, including significant savings with Spot Instances and Reserved Instances.
    *   Global infrastructure with high availability.
    *   Integrated with a vast ecosystem of Azure services.
*   **Cons:**
    *   Pricing can be complex due to many options.
    *   Spot instances can be interrupted.

## Links
*   [Official Website](https://azure.microsoft.com/en-us/products/virtual-machines/g-series)
*   [Pricing Page](https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/) (General VM pricing, GPU VM pricing varies by region and type)
*   [Spot Instances](https://azure.microsoft.com/en-us/pricing/details/virtual-machines/spot/)