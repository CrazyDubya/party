# Google Cloud Databases

## Overview
Google Cloud offers a comprehensive portfolio of fully managed database services, encompassing both relational and non-relational (NoSQL) options. These services are designed for scalability, high availability, and integration with the broader Google Cloud ecosystem, catering to diverse application needs.

## Database Types Supported
*   **Relational:** Cloud SQL (MySQL, PostgreSQL, SQL Server), Cloud Spanner (globally distributed), AlloyDB (PostgreSQL-compatible)
*   **Non-Relational (NoSQL):** Cloud Firestore (document), Cloud Bigtable (wide-column), Cloud Memorystore (in-memory), Firebase Realtime Database (NoSQL for mobile)

## Pricing Model
*   **General Model:** Pay-as-you-go. Discounts available for sustained use (SUDs) and committed use (CUDs). Free tiers for some services.
*   **Key Cost Factors:**
    *   **Cloud SQL:** CPU, memory, licensing (SQL Server), storage (SSD/HDD), network egress.
    *   **Cloud Spanner:** Compute capacity (processing units/nodes), database storage, backup storage, network bandwidth.
    *   **Cloud Firestore:** Document reads/writes/deletes, stored data, network bandwidth.
    *   **Cloud Bigtable:** Nodes, storage (SSD/HDD), network bandwidth.
*   **Example Pricing:** Varies significantly by service and configuration. Free quotas available for Cloud Firestore.

## Key Features
*   **Managed Service:** Yes (fully managed for all services).
*   **Scalability:** Horizontal and vertical scaling, global distribution (Cloud Spanner, Cloud Firestore), auto-scaling for some services.
*   **High Availability & Durability:** Multi-region replication, automated backups, point-in-time recovery, ACID compliance (relational).
*   **Security:** Encryption, IAM, network isolation.
*   **Backup & Restore:** Automated backups, PITR for some services.
*   **Monitoring & Alerting:** Integrated with Google Cloud Monitoring.
*   **Multi-Cloud/Hybrid Support:** GCP-native, but can integrate with hybrid environments.
*   **Developer Experience:** SDKs, CLIs, various APIs (SQL, NoSQL), integration with Firebase.

## Pros & Cons
*   **Pros:**
    *   Comprehensive range of managed database services for various workloads.
    *   Strong offerings for globally distributed and highly scalable databases (Spanner, Firestore).
    *   Deep integration with Google Cloud's AI/ML and analytics services.
    *   Flexible pricing with various discount options.
*   **Cons:**
    *   Pricing can be complex due to the diversity of services and billing components.
    *   Learning curve for new users to understand the optimal service for their needs.

## Links
*   [Official Website](https://cloud.google.com/products/databases)
*   [Pricing Page](https://cloud.google.com/sql/pricing) (Example for Cloud SQL, pricing varies by service)
*   [Documentation](https://cloud.google.com/docs/databases)