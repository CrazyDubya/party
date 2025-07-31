# Azure Cosmos DB

## Overview
Azure Cosmos DB is Microsoft's globally distributed, multi-model database service designed for high availability, scalability, and low-latency access to data for modern applications. It supports various NoSQL data models and a PostgreSQL API.

## Database Types Supported
*   SQL API (Document DB - JSON)
*   MongoDB API (Document DB - BSON)
*   Cassandra API (Column-family)
*   Gremlin API (Graph)
*   Table API (Key-value)
*   PostgreSQL API (Relational)

## Pricing Model
*   **General Model:** Based on compute (Request Units per second - RU/s or vCores), storage (GB), and bandwidth. Offers Provisioned Throughput, Autoscale Provisioned Throughput, and Serverless options.
*   **Key Cost Factors:** RU/s, storage (GB), data transfer.
*   **Example Pricing:**
    *   **Free Tier:** First 1000 RU/s and 25 GB storage free for the lifetime of the account.
    *   **Serverless:** Consumption-based (pay only for RUs consumed).
    *   **Reserved Capacity:** Up to 30% savings for 1 or 3-year commitments.

## Key Features
*   **Managed Service:** Yes (fully managed).
*   **Scalability:** Elastic scalability, automatically scales storage and throughput.
*   **High Availability & Durability:** Global distribution with multi-region writes, 99.999% read/write availability, automatic failover.
*   **Security:** Enterprise-grade security, encryption, network isolation (VPC peering), authentication, access control.
*   **Backup & Restore:** Not explicitly detailed in search results, but implied for a managed service.
*   **Monitoring & Alerting:** Built-in monitoring.
*   **Multi-Cloud/Hybrid Support:** Azure-native, but multi-region capabilities.
*   **Developer Experience:** Multi-model APIs, SDKs, Change Feed for event-driven architectures.

## Pros & Cons
*   **Pros:**
    *   Globally distributed with multi-region write capabilities.
    *   Multi-model support with various APIs.
    *   Guaranteed low latency and high availability.
    *   Elastic scalability.
    *   Generous free tier.
*   **Cons:**
    *   Pricing can be complex due to RU/s model.
    *   Tied to Azure ecosystem.

## Links
*   [Official Website](https://azure.microsoft.com/en-us/services/cosmos-db/)
*   [Pricing Page](https://azure.microsoft.com/en-us/pricing/details/cosmos-db/)
*   [Documentation](https://docs.microsoft.com/en-us/azure/cosmos-db/)