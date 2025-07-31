# Oracle Cloud Infrastructure (OCI)

## Overview
OCI offers a range of GPU instances designed for hardware-accelerated workloads such as AI training, machine learning, and HPC. They provide NVIDIA and AMD GPUs in both Virtual Machine (VM) and Bare Metal (BM) configurations, with flexible pricing models including spot instances.

## Infrastructure Model
*   **Owns Infrastructure:** Yes - Oracle operates its own global data centers and provides a vast cloud infrastructure.
*   **Aggregator/Reseller:** No

## GPU Offerings & Pricing
| GPU Type | Preferred/Popular | On-Demand Price (per hour) | Spot Price (per hour) | Notes |
|---|---|---|---|---|
| NVIDIA H100 (BM.GPU.H100) | Yes | Varies | Available | Latest generation, high-performance. |
| NVIDIA A100 (BM.GPU4, BM.GPU.A100-v2) | Yes | Varies | Available | Popular for AI/ML training and HPC. |
| NVIDIA A10 (VM.GPU.A10, BM.GPU.A10) | Yes | Varies | Available | |
| NVIDIA Tesla V100 (VM.GPU3, BM.GPU3) | No | Varies | Available | |
| NVIDIA Tesla P100 (VM.GPU2, BM.GPU2) | No | Varies | Available | |
| NVIDIA H200 | Yes | Varies | Available | Newer generation. |
| NVIDIA Blackwell B200 | Yes | Varies | Available | Latest generation. |
| AMD Instinct MI300X | Yes | Varies | Available | |

## Key Features
*   **Pricing Model:** Pay-as-you-go, Spot Instances, and longer-term commitment options.
*   **Billing Granularity:** Not explicitly detailed in search results, but implied to be granular (e.g., per hour).
*   **Instance Types:** Virtual Machine (VM) and Bare Metal (BM). Bare Metal offers direct access to hardware.
*   **Storage Options:** Not explicitly detailed in search results.
*   **Networking:** High-performance networking, including RDMA-based cluster networking. OCI Supercluster for massive scale.
*   **Software Environment:** Not explicitly detailed in search results, but supports common ML frameworks.
*   **Geographic Regions:** Global presence.
*   **Support:** Various support plans available.

## Pros & Cons
*   **Pros:**
    *   Offers both VM and Bare Metal GPU instances.
    *   Access to latest NVIDIA and AMD GPUs.
    *   Flexible pricing models, including spot instances.
    *   High-performance networking for large-scale workloads.
*   **Cons:**
    *   Specific pricing for all GPU types and regions requires deeper investigation on their website.

## Links
*   [Official Website](https://www.oracle.com/cloud/compute/gpu/)
*   [Pricing Page](https://www.oracle.com/cloud/price-list.html) (General OCI price list, GPU pricing varies)
*   [Documentation](https://docs.oracle.com/en-us/iaas/Content/Compute/References/gpu-compute.htm)