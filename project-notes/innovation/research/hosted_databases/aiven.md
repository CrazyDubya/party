# Aiven

## Overview
Aiven offers a cloud-native platform providing fully managed services for various open-source data technologies, including popular databases and streaming services. They aim for transparent, all-inclusive hourly billing across major cloud providers.

## Database Types Supported
*   PostgreSQL
*   MySQL
*   Apache Kafka
*   Redis (now Valkey)
*   OpenSearch (formerly Elasticsearch)
*   Apache Cassandra
*   Apache Flink
*   ClickHouse
*   M3 (for metrics)
*   Grafana (for observability)
*   AlloyDB Omni

## Pricing Model
*   **General Model:** Hourly billing, all-inclusive, tiered plans (Startup, Business, Professional). Free plan available.
*   **Key Cost Factors:** Dedicated VMs, CPU, RAM, storage, cloud provider, region.
*   **Example Pricing:**
    *   **Free Plan:** Single node, 1 CPU, 1 GB RAM, 5 GB disk storage (for PostgreSQL and MySQL). Limited features.
    *   **Startup Plan (Kafka example):** Starts from $290/month, 3 dedicated VMs, 2 CPU/VM, 2-4 GB RAM/VM, 90 GB total storage.

## Key Features
*   **Managed Service:** Yes (fully managed).
*   **Scalability:** Supports scaling of resources to meet growing demands.
*   **High Availability & Durability:** Built-in automatic failover, cross-region replication, zero downtime during maintenance.
*   **Security:** Encryption (at rest and in transit), secure connections, access controls, automated security updates, various compliance certifications.
*   **Backup & Restore:** Automatic backups.
*   **Monitoring & Alerting:** Integrates with monitoring systems (AWS CloudWatch, DataDog, Prometheus).
*   **Multi-Cloud/Hybrid Support:** Deploy services across AWS, Google Cloud, and Microsoft Azure.
*   **Developer Experience:** Web console, CLI, API, Terraform provider, Kubernetes operator.

## Pros & Cons
*   **Pros:**
    *   Wide range of fully managed open-source data technologies.
    *   Transparent, all-inclusive hourly billing.
    *   Multi-cloud deployment options, avoiding vendor lock-in.
    *   Strong focus on security and compliance.
    *   Good developer tooling.
*   **Cons:**
    *   Free plan has significant limitations.
    *   Pricing can be complex due to many service types and configurations.

## Links
*   [Official Website](https://aiven.io/)
*   [Pricing Page](https://aiven.io/pricing)
*   [Documentation](https://aiven.io/docs)