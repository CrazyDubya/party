# TiDB

## Overview
TiDB is an open-source, cloud-native, distributed SQL database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads. It is MySQL compatible and designed for high availability, horizontal scalability, strong consistency, and high performance.

## Database Types Supported
*   Distributed SQL (NewSQL)
*   HTAP (Hybrid Transactional and Analytical Processing)
*   Supports MySQL data types (except SPATIAL)

## Pricing Model
*   **General Model:**
    *   **TiDB Cloud Serverless:** Pay-as-you-go consumption model (Request Units - RUs, storage). Free tier available.
    *   **TiDB Cloud Dedicated:** Node-based pricing (provisioned infrastructure, storage, backup, data transfer).
    *   **TiDB Self-Managed:** Free (open-source version) or costs depend on user's infrastructure.
*   **Key Cost Factors:** Request Units (RUs), row storage (GB), column storage (GB), instances, storage, backup, data transfer.
*   **Example Pricing:**
    *   **TiDB Cloud Serverless Free Tier:** 25 GB row storage, 25 GB column storage, 250 million RUs per month.
    *   **TiDB Cloud Serverless Overage:** $0.20 per GB for additional storage, $0.10 per 1 million RUs.

## Key Features
*   **Managed Service:** Yes (for TiDB Cloud Serverless and Dedicated).
*   **Scalability:** Horizontal scalability (separate compute and storage), can scale out by adding nodes without downtime.
*   **High Availability & Durability:** Distributed transactions with strong consistency (ACID compliant), Multi-Raft protocol for data availability and self-healing.
*   **Security:** Encryption, data schema, access control, authentication.
*   **Backup & Restore:** Tools for backup and restore.
*   **Monitoring & Alerting:** Not explicitly detailed in search results, but implied for a managed service.
*   **Multi-Cloud/Hybrid Support:** TiDB Cloud Dedicated available on AWS, Google Cloud, and Azure. TiDB Self-Managed can be deployed on public/private clouds or on-premise.
*   **Developer Experience:** MySQL compatibility, various open-source tools for data replication and migration (TiDB Data Migration, Backup & Restore, etc.).

## Pros & Cons
*   **Pros:**
    *   Horizontal scalability for both transactional and analytical workloads.
    *   MySQL compatibility simplifies migration.
    *   Strong consistency and high availability.
    *   Cloud-native design with Kubernetes support.
    *   Generous free tier for Serverless.
*   **Cons:**
    *   Complexity can be higher for self-managed deployments.
    *   Pricing for Dedicated tier is node-based, requiring provisioning.

## Links
*   [Official Website](https://pingcap.com/products/tidb-cloud/)
*   [Pricing Page](https://pingcap.com/products/tidb-cloud/pricing/)
*   [Documentation](https://docs.pingcap.com/tidb/stable)