# AI Context Pack: Commerce Insights

Generated from OpenMetadata at `2026-10-23T20:51:02.067879+00:00`.

This artifact is grounded in governed metadata. It contains no source rows or customer values.

## dim_customers

Governed customer dimension for digital commerce analytics.

- FQN: `digital_commerce_postgres.chinook.marts.dim_customers`
- Domains: DigitalCommerce
- Owners: CommerceAnalytics
- Tags: Commerce.Customer, DbtTags.certified_candidate, DbtTags.digital_commerce, Tier.Tier1

| Column | Type | Description |
| --- | --- | --- |
| `customer_id` | `integer` | Stable customer key. |
| `customer_name` | `text` | Customer display name. |
| `company_name` | `text` |  |
| `email` | `text` | Customer contact email. |
| `city` | `text` |  |
| `state` | `text` |  |
| `country` | `text` | Customer country. |
| `postal_code` | `text` |  |
| `support_rep_id` | `integer` |  |

## dim_products

Governed digital product dimension combining tracks, albums, artists, and genres.

- FQN: `digital_commerce_postgres.chinook.marts.dim_products`
- Domains: DigitalCommerce
- Owners: CommerceAnalytics
- Tags: Commerce.DigitalProduct, DbtTags.certified_candidate, DbtTags.digital_commerce, Tier.Tier2

| Column | Type | Description |
| --- | --- | --- |
| `product_id` | `integer` | Stable digital product key. |
| `product_name` | `text` | Commercial track title. |
| `album_title` | `text` |  |
| `artist_name` | `text` |  |
| `genre_name` | `text` |  |
| `composer` | `character varying(220)` |  |
| `duration_ms` | `integer` |  |
| `list_price` | `numeric(12,2)` | Catalog unit price in the source currency. |

## fct_sales

Line-level digital commerce sales fact used as the governed analytical backbone.

- FQN: `digital_commerce_postgres.chinook.marts.fct_sales`
- Domains: DigitalCommerce
- Owners: CommerceAnalytics
- Tags: Commerce.Order, Commerce.Revenue, DbtTags.certified_candidate, DbtTags.digital_commerce, Tier.Tier1

| Column | Type | Description |
| --- | --- | --- |
| `sale_line_id` | `integer` | Stable order-line key. |
| `invoice_id` | `integer` |  |
| `customer_id` | `integer` |  |
| `product_id` | `integer` |  |
| `invoice_at` | `timestamp without time zone` |  |
| `sale_date` | `date` |  |
| `sale_month` | `date` |  |
| `billing_country` | `text` |  |
| `billing_state` | `text` |  |
| `billing_city` | `text` |  |
| `unit_price` | `numeric(12,2)` |  |
| `quantity` | `integer` |  |
| `revenue` | `numeric(12,2)` | Quantity multiplied by the realized unit price. |

## mart_customer_360

Customer-level commercial behavior and lifetime value metrics.

- FQN: `digital_commerce_postgres.chinook.marts.mart_customer_360`
- Domains: DigitalCommerce
- Owners: CommerceAnalytics
- Tags: Commerce.CustomerLifetimeValue, DbtTags.certified_candidate, DbtTags.digital_commerce, Tier.Tier1

| Column | Type | Description |
| --- | --- | --- |
| `customer_id` | `integer` |  |
| `customer_name` | `text` |  |
| `company_name` | `text` |  |
| `country` | `text` |  |
| `state` | `text` |  |
| `city` | `text` |  |
| `first_purchase_at` | `timestamp without time zone` |  |
| `latest_purchase_at` | `timestamp without time zone` |  |
| `order_count` | `bigint` |  |
| `units_purchased` | `bigint` |  |
| `lifetime_value` | `numeric(14,2)` | Total realized revenue attributed to a customer. |
| `average_order_value` | `numeric(14,2)` |  |

## mart_sales_performance

Monthly sales performance by billing country.

- FQN: `digital_commerce_postgres.chinook.marts.mart_sales_performance`
- Domains: DigitalCommerce
- Owners: CommerceAnalytics
- Tags: Commerce.Revenue, DbtTags.certified_candidate, DbtTags.digital_commerce, Tier.Tier1

| Column | Type | Description |
| --- | --- | --- |
| `sale_month` | `date` |  |
| `billing_country` | `text` |  |
| `order_count` | `bigint` |  |
| `active_customers` | `bigint` |  |
| `units_sold` | `bigint` |  |
| `revenue` | `numeric(14,2)` |  |
| `average_order_value` | `numeric(14,2)` |  |

## mart_catalog_performance

Product-level commercial performance across the complete digital catalog.

- FQN: `digital_commerce_postgres.chinook.marts.mart_catalog_performance`
- Domains: DigitalCommerce
- Owners: CommerceAnalytics
- Tags: Commerce.DigitalProduct, Commerce.Revenue, DbtTags.certified_candidate, DbtTags.digital_commerce, Tier.Tier2

| Column | Type | Description |
| --- | --- | --- |
| `product_id` | `integer` |  |
| `product_name` | `text` |  |
| `album_title` | `text` |  |
| `artist_name` | `text` |  |
| `genre_name` | `text` |  |
| `order_count` | `bigint` |  |
| `unique_customers` | `bigint` |  |
| `units_sold` | `bigint` |  |
| `revenue` | `numeric(14,2)` |  |

## mart_executive_kpis

Single-row executive summary of core digital commerce KPIs.

- FQN: `digital_commerce_postgres.chinook.marts.mart_executive_kpis`
- Domains: DigitalCommerce
- Owners: CommerceAnalytics
- Tags: Commerce.AverageOrderValue, Commerce.Revenue, DbtTags.certified_candidate, DbtTags.digital_commerce, Tier.Tier1

| Column | Type | Description |
| --- | --- | --- |
| `total_orders` | `bigint` |  |
| `total_customers` | `bigint` |  |
| `total_units_sold` | `bigint` |  |
| `total_revenue` | `numeric(14,2)` |  |
| `average_order_value` | `numeric(14,2)` |  |
| `reporting_period_start` | `timestamp without time zone` |  |
| `reporting_period_end` | `timestamp without time zone` |  |
