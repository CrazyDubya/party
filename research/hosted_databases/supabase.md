# Supabase

## Overview
Supabase is an open-source Firebase alternative that provides a hosted PostgreSQL database and a suite of features designed to simplify application development, including real-time capabilities, authentication, storage, and edge functions.

## Database Types Supported
*   PostgreSQL (core offering)
*   Supports various PostgreSQL data types (e.g., Date, Time, Int, Varchar, Jsonb, Uuid)

## Pricing Model
*   **General Model:** Tiered pricing (Free, Pro, Team, Enterprise) with usage-based billing for overages.
*   **Key Cost Factors:** Database storage, file storage, database egress, monthly active users (MAUs), Edge Function invocations, compute.
*   **Example Pricing:**
    *   **Free Tier:** 2 projects, 500 MB DB storage, 1 GB file storage, 50 MB DB egress/day, 10,000 MAUs, 1,000 Edge Function invocations/day.
    *   **Pro Tier:** Starts from $25/month. Includes 100,000 MAUs, 8 GB DB space, 250 GB bandwidth, 100 GB file storage.
    *   **Team Tier:** Starts from $599/month. Includes all Pro features plus custom limits, advanced security, priority support.
    *   **Enterprise Plan:** Custom pricing for large-scale needs.

## Key Features
*   **Managed Service:** Yes
*   **Scalability:** Horizontal and vertical scaling, auto-scaling for some components.
*   **High Availability & Durability:** Daily backups, point-in-time recovery.
*   **Security:** Data encryption (at rest and in transit), 2FA, SQL injection prevention, rate limiting, Row Level Security (RLS).
*   **Backup & Restore:** Automated daily backups, 7-day (Pro) or 14-day (Team) log retention.
*   **Monitoring & Alerting:** Supabase Studio dashboard for monitoring API usage and project settings.
*   **Multi-Cloud/Hybrid Support:** Primarily hosted on AWS, but aims for cloud-agnostic approach.
*   **Developer Experience:** Auto-generated RESTful and GraphQL APIs, client libraries for various frameworks, built-in SQL editor, Supabase Studio dashboard.

## Pros & Cons
*   **Pros:**
    *   Open-source friendly with a full PostgreSQL database.
    *   Comprehensive suite of features (BaaS).
    *   Generous free tier for development.
    *   Real-time capabilities.
    *   Automatic API generation.
*   **Cons:**
    *   Primarily focused on PostgreSQL, less diverse database types compared to some other DBaaS.
    *   Overage costs can add up for high usage.

## Links
*   [Official Website](https://supabase.com/)
*   [Pricing Page](https://supabase.com/pricing)
*   [Documentation](https://supabase.com/docs)