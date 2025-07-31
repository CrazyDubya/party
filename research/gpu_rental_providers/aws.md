# Amazon Web Services (AWS)

## Overview
AWS offers a comprehensive suite of EC2 GPU instances designed for compute-intensive workloads like machine learning, AI, and scientific simulations. They provide a wide range of NVIDIA GPUs with flexible pricing models, including on-demand, reserved, and spot instances.

## Infrastructure Model
*   **Owns Infrastructure:** Yes - AWS operates its own global data centers and provides a vast cloud infrastructure.
*   **Aggregator/Reseller:** No

## GPU Offerings & Pricing
| GPU Type | Preferred/Popular | On-Demand Price (per hour) | Spot Price (per hour) | Notes |
|---|---|---|---|---|
| NVIDIA H100 (P5 instances) | Yes | Varies | Up to 90% off On-Demand | High-performance for training. |
| NVIDIA A100 (P4 instances) | Yes | Varies | Up to 90% off On-Demand | Popular for training and inference. |
| NVIDIA L40S (G6e instances) | Yes | Varies | Up to 90% off On-Demand | Optimized for graphics and inference. |
| NVIDIA L4 (G6 instances) | Yes | Varies | Up to 90% off On-Demand | Optimized for graphics and inference. |
| NVIDIA A10G (G5 instances) | Yes | Varies | Up to 90% off On-Demand | Optimized for graphics and inference. |
| NVIDIA V100 (P3 instances) | No | Varies | Up to 90% off On-Demand | |
| NVIDIA T4 (G4dn instances) | No | Varies | Up to 90% off On-Demand | |
| NVIDIA M60 (G3 instances) | No | Varies | Up to 90% off On-Demand | |
| NVIDIA Kepler K80 (P2 instances) | No | Varies | Up to 90% off On-Demand | Older generation. |
| NVIDIA Blackwell (P6-B200, P6e-GB200) | Yes | Varies | Up to 90% off On-Demand | Latest generation. |
| AMD Radeon Pro V520 (G4ad instances) | No | Varies | Up to 90% off On-Demand | |

## Key Features
*   **Pricing Model:** On-Demand, Savings Plans (up to 72% off), Spot Instances (up to 90% off), Reserved Instances, Capacity Blocks for ML, Dedicated Hosts.
*   **Billing Granularity:** Per hour or per second for On-Demand.
*   **Instance Types:** Virtual machines.
*   **Storage Options:** EBS (Elastic Block Store), Instance Store.
*   **Networking:** Elastic Fabric Adapter (EFA), GPUDirect RDMA for distributed workloads.
*   **Software Environment:** Supports various AMIs with pre-installed ML frameworks.
*   **Geographic Regions:** Global presence with many regions and Availability Zones.
*   **Support:** Various support plans available.

## Pros & Cons
*   **Pros:**
    *   Extensive range of GPU instances and configurations.
    *   Highly flexible pricing models, including significant savings with Spot Instances and Savings Plans.
    *   Global infrastructure with high availability.
    *   Integrated with a vast ecosystem of AWS services.
*   **Cons:**
    *   Pricing can be complex due to many options.
    *   Spot instances can be interrupted.

## Links
*   [Official Website](https://aws.amazon.com/ec2/instance-types/gpu/)
*   [Pricing Page](https://aws.amazon.com/ec2/pricing/on-demand/) (General EC2 pricing, GPU instance pricing varies by region and type)
*   [Spot Instances](https://aws.amazon.com/ec2/spot/)