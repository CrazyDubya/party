# Summary Report: GPU Rental Providers

## Introduction
This report summarizes the research conducted on various GPU rental providers, focusing on their offerings, pricing models, GPU types, and infrastructure ownership. The goal was to identify top providers and compare them based on a predefined schema.

## Categorization of Providers by Infrastructure Model

### Providers Owning Infrastructure
These providers own and operate their own data centers and GPU hardware, offering direct access to their resources.

*   **Lambda Labs**
*   **Amazon Web Services (AWS)**
*   **Google Cloud Platform (GCP)**
*   **Microsoft Azure**
*   **Oracle Cloud Infrastructure (OCI)**
*   **CoreWeave**
*   **E2E Cloud**

### Aggregators / Resellers
These platforms act as marketplaces, aggregating GPU resources from various independent hosts or data centers.

*   **Runpod** (also has own Secure Cloud)
*   **Vast.ai**
*   **TensorDock**

## Comparison Table: GPU Rental Providers

| Provider | Infrastructure Model | Key GPU Types Offered | On-Demand Price (per hour, Example) | Spot Price (per hour, Example) | Billing Granularity | Notes |
|---|---|---|---|---|---|---|
| **Lambda Labs** | Owns | H100, A100, A10, RTX 6000 Ada | ~$1.10 (A100) | Not explicitly mentioned | Per minute | Specialized for AI/ML; no egress fees. |
| **AWS** | Owns | H100, A100, L40S, L4, A10G | Varies | Up to 90% off On-Demand | Per hour/second | Extensive range; global presence. |
| **GCP** | Owns | H100, L4, A100, T4, V100 | Varies | 60-91% off On-Demand | Per second | Large context; multimodal. |
| **Azure** | Owns | H100, A100, L40S, RTX A6000 Ada | Varies | Up to 90% off Pay-as-you-go | Per second | Extensive range; global presence. |
| **OCI** | Owns | H100, A100, A10, V100, P100 | Varies | Available | Not explicitly detailed | Offers Bare Metal; high-performance networking. |
| **CoreWeave** | Owns | H100, A100, L40S, L4, RTX PRO 6000 | Varies | Not offered (On-demand competitive with spot) | Not explicitly detailed | Optimized for GPU-intensive workloads; Kubernetes-native. |
| **E2E Cloud** | Owns | H200, H100, A100, L40S, L4 | Varies | Varies (supply/demand) | Per hour | Primarily in India; pre-configured ML environments. |
| **Runpod** | Owns & Aggregator | H200, B200, H100, A100, RTX 4090 | ~$3.99 (H200) | Up to 50% cheaper | Per second | Flexible pricing; global distributed network. |
| **Vast.ai** | Aggregator | H200, H100, RTX 4090, RTX 3090, A100 | Varies | Varies (bidding system) | Per second | Highly cost-effective for interruptible workloads. |
| **TensorDock** | Aggregator | H100, RTX 4090, A100, RTX A6000 | From $2.25 (H100) | Varies (bidding system) | Per second | Competitive pricing; wide selection of GPUs. |

## Key Takeaways

1.  **Infrastructure Ownership Matters:** Providers owning their infrastructure (e.g., AWS, GCP, Lambda Labs, CoreWeave) generally offer more consistent performance, dedicated support, and deeper integration with their cloud ecosystems. Aggregators (e.g., Vast.ai, TensorDock) often provide more competitive spot pricing and a wider variety of GPU hardware, but with potentially less predictable availability and support.
2.  **Spot Instances for Cost Savings:** Spot instances (or interruptible instances) are a common offering across many providers, providing significant cost reductions (up to 90% off on-demand) for fault-tolerant or batch workloads. However, they come with the risk of preemption.
3.  **Diverse GPU Offerings:** The market offers a wide range of NVIDIA GPUs, from consumer-grade (e.g., RTX 4090) to high-end data center GPUs (e.g., H100, A100, H200, Blackwell). The choice depends on the specific workload requirements and budget.
4.  **Flexible Pricing Models:** Billing granularity varies from per-second to per-hour. Many providers offer various pricing models, including on-demand, reserved, and spot, to cater to different usage patterns and commitment levels.
5.  **Specialization:** Some providers specialize in specific niches (e.g., Lambda Labs and CoreWeave for AI/ML workloads, E2E Cloud for the Indian market), offering optimized environments and services.
6.  **Transparency Varies:** While many providers aim for transparent pricing, obtaining exact, real-time pricing for all GPU types and configurations across all regions can require navigating complex pricing pages or direct inquiry.

This research provides a comprehensive overview of the GPU rental market, highlighting key considerations for selecting a provider based on infrastructure needs, budget, and workload characteristics.