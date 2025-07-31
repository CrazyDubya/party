# Fauna

## Overview
Fauna is a distributed, serverless, document-relational database delivered as a cloud API. It combines the flexibility of a document model with relational querying capabilities, offering global distribution, ACID transactions, and a consumption-based pricing model.

## Database Types Supported
*   Document-Relational (JSON documents with relational querying)
*   Key-Value Store
*   Graph Database
*   OLTP (Online Transaction Processing)

## Pricing Model
*   **General Model:** Consumption-based (pay-as-you-go) with a generous daily free tier. Also offers fixed-price subscription tiers (e.g., Pro Plan).
*   **Key Cost Factors:** Read operations, write operations, storage, data transfer.
*   **Example Pricing:**
    *   **Free Tier:** Generous daily free tier, suitable for small applications. No credit card required to start.
    *   **Pro Plan:** $500/month (example for production workloads).

## Key Features
*   **Managed Service:** Yes (fully managed, serverless).
*   **Scalability:** Auto-scales, handles sharding and capacity planning automatically.
*   **High Availability & Durability:** Global distribution with automatic data replication for high availability and low latency across multiple regions. Distributed ACID transactions.
*   **Security:** Authentication, access providers, tokens, keys, authorization, roles, attribute-based access control (ABAC).
*   **Backup & Restore:** Supports data retention and history, allowing queries to access previous versions of documents.
*   **Monitoring & Alerting:** Not explicitly detailed in search results, but implied for a managed service.
*   **Multi-Cloud/Hybrid Support:** Delivered as a cloud API, with global distribution. Can be deployed on-premises (JAR, machine image, container).
*   **Developer Experience:** Fauna Query Language (FQL), native GraphQL API, web console, CLI, client libraries, integrations (e.g., Netlify).

## Pros & Cons
*   **Pros:**
    *   Serverless and fully managed, reducing operational overhead.
    *   Global distribution with low latency.
    *   Distributed ACID transactions for strong consistency.
    *   Multi-model support with flexible querying (FQL, GraphQL).
    *   Generous free tier.
*   **Cons:**
    *   Consumption-based pricing can be unpredictable for fluctuating workloads.
    *   FQL has a learning curve for new users.

## Links
*   [Official Website](https://fauna.com/)
*   [Pricing Page](https://fauna.com/pricing)
*   [Documentation](https://docs.fauna.com/)