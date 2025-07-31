# CockroachDB

## Overview
CockroachDB is a distributed SQL database designed for cloud applications, emphasizing resilience, scalability, and strong consistency. It is PostgreSQL-compatible and offers various pricing tiers to suit different workload requirements.

## Database Types Supported
*   Distributed SQL (relational)
*   PostgreSQL-compatible

## Pricing Model
*   **General Model:** Usage-based pricing with free and paid tiers.
*   **Key Cost Factors:** Compute (Request Units or vCPU hours), storage (GiB-hour), data transfer.
*   **Example Pricing:**
    *   **Basic (formerly Serverless):** Free tier of 50 million Request Units (RUs) and 10 GiB of storage per month. Scales to zero.
    *   **Standard:** Provisioned compute with instant scaling, on-demand storage.
    *   **Advanced:** High-scale applications with sophisticated security and compliance needs, unlimited scaling.
    *   **Self-Hosted:** Enterprise license, support, and features for on-premises or private cloud deployments.

## Key Features
*   **Managed Service:** Yes (for Basic, Standard, Advanced plans).
*   **Scalability:** Effortless horizontal scaling, add nodes without disruption.
*   **High Availability & Durability:** Designed for continuous operation during failures (node, AZ, region), automated repair, Raft consensus for data integrity, automatic failover.
*   **Security:** Enterprise-grade security, IP allowlist, CMEK.
*   **Backup & Restore:** Managed backups (charged based on storage rates).
*   **Monitoring & Alerting:** Metrics/log export to Datadog (for Standard+ plans).
*   **Multi-Cloud/Hybrid Support:** Multi-region support across AWS, GCP, and Azure (for Advanced plan).
*   **Developer Experience:** SQL API, command-line interface (SQL shell), PostgreSQL compatibility, Change Data Capture (CDC).

## Pros & Cons
*   **Pros:**
    *   Highly scalable and resilient distributed SQL database.
    *   Strong consistency and ACID transactions.
    *   PostgreSQL compatibility for easy migration.
    *   Multi-region deployments for global applications.
    *   Generous free tier.
*   **Cons:**
    *   Pricing can be complex with RU-based billing.
    *   Advanced features and multi-cloud support are in higher tiers.

## Links
*   [Official Website](https://www.cockroachlabs.com/)
*   [Pricing Page](https://www.cockroachlabs.com/pricing/)
*   [Documentation](https://www.cockroachlabs.com/docs/)