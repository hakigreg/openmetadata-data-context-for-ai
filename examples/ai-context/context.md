# AI Context Pack: Commerce Insights

Generated from OpenMetadata at `2026-10-23T23:27:45.290728+00:00`.

This artifact is grounded in governed metadata. It contains no source rows or customer values.

## dim_customers

Governed customer dimension for digital commerce analytics.

- FQN: `digital_commerce_postgres.chinook.marts.dim_customers`
- Domains: DigitalCommerce
- Owners: CommerceAnalytics
- Tags: Commerce.Customer, DbtTags.certified_candidate, DbtTags.digital_commerce, Tier.Tier1

| Column | Type | Classification and terms | Description |
| --- | --- | --- | --- |
| `customer_id` | `integer` | Commerce.Customer.CustomerIdentifier, DataSensitivity.Confidential | Stable customer key. |
| `customer_name` | `text` | DataSensitivity.Confidential, DbtTags.personal_data | Customer display name. |
| `company_name` | `text` | None |  |
| `email` | `text` | DataSensitivity.Confidential, DbtTags.contact_data, DbtTags.personal_data | Customer contact email. |
| `city` | `text` | None |  |
| `state` | `text` | None |  |
| `country` | `text` | None | Customer country. |
| `postal_code` | `text` | None |  |
| `support_rep_id` | `integer` | None |  |

## dim_products

Governed digital product dimension combining tracks, albums, artists, and genres.

- FQN: `digital_commerce_postgres.chinook.marts.dim_products`
- Domains: DigitalCommerce
- Owners: CommerceAnalytics
- Tags: Commerce.DigitalProduct, DbtTags.certified_candidate, DbtTags.digital_commerce, Tier.Tier2

| Column | Type | Classification and terms | Description |
| --- | --- | --- | --- |
| `product_id` | `integer` | None | Stable digital product key. |
| `product_name` | `text` | None | Commercial track title. |
| `album_title` | `text` | None |  |
| `artist_name` | `text` | None |  |
| `genre_name` | `text` | None |  |
| `composer` | `character varying(220)` | None |  |
| `duration_ms` | `integer` | None |  |
| `list_price` | `numeric(12,2)` | None | Catalog unit price in the source currency. |

## fct_sales

Line-level digital commerce sales fact used as the governed analytical backbone.

- FQN: `digital_commerce_postgres.chinook.marts.fct_sales`
- Domains: DigitalCommerce
- Owners: CommerceAnalytics
- Tags: Commerce.Order, Commerce.Revenue, DbtTags.certified_candidate, DbtTags.digital_commerce, Tier.Tier1

| Column | Type | Classification and terms | Description |
| --- | --- | --- | --- |
| `sale_line_id` | `integer` | None | Stable order-line key. |
| `invoice_id` | `integer` | None |  |
| `customer_id` | `integer` | DataSensitivity.Confidential |  |
| `product_id` | `integer` | None |  |
| `invoice_at` | `timestamp without time zone` | None |  |
| `sale_date` | `date` | None |  |
| `sale_month` | `date` | None |  |
| `billing_country` | `text` | None |  |
| `billing_state` | `text` | None |  |
| `billing_city` | `text` | None |  |
| `unit_price` | `numeric(12,2)` | None |  |
| `quantity` | `integer` | None |  |
| `revenue` | `numeric(12,2)` | Commerce.Revenue | Quantity multiplied by the realized unit price. |

## mart_customer_360

Customer-level commercial behavior and lifetime value metrics.

- FQN: `digital_commerce_postgres.chinook.marts.mart_customer_360`
- Domains: DigitalCommerce
- Owners: CommerceAnalytics
- Tags: Commerce.CustomerLifetimeValue, DbtTags.certified_candidate, DbtTags.digital_commerce, Tier.Tier1

| Column | Type | Classification and terms | Description |
| --- | --- | --- | --- |
| `customer_id` | `integer` | DataSensitivity.Confidential |  |
| `customer_name` | `text` | DataSensitivity.Confidential |  |
| `company_name` | `text` | None |  |
| `country` | `text` | None |  |
| `state` | `text` | None |  |
| `city` | `text` | None |  |
| `first_purchase_at` | `timestamp without time zone` | None |  |
| `latest_purchase_at` | `timestamp without time zone` | None |  |
| `order_count` | `bigint` | None |  |
| `units_purchased` | `bigint` | None |  |
| `lifetime_value` | `numeric(14,2)` | None | Total realized revenue attributed to a customer. |
| `average_order_value` | `numeric(14,2)` | None |  |

## mart_sales_performance

Monthly sales performance by billing country.

- FQN: `digital_commerce_postgres.chinook.marts.mart_sales_performance`
- Domains: DigitalCommerce
- Owners: CommerceAnalytics
- Tags: Commerce.Revenue, DbtTags.certified_candidate, DbtTags.digital_commerce, Tier.Tier1

| Column | Type | Classification and terms | Description |
| --- | --- | --- | --- |
| `sale_month` | `date` | None |  |
| `billing_country` | `text` | None |  |
| `order_count` | `bigint` | None |  |
| `active_customers` | `bigint` | None |  |
| `units_sold` | `bigint` | None |  |
| `revenue` | `numeric(14,2)` | None |  |
| `average_order_value` | `numeric(14,2)` | None |  |

## mart_catalog_performance

Product-level commercial performance across the complete digital catalog.

- FQN: `digital_commerce_postgres.chinook.marts.mart_catalog_performance`
- Domains: DigitalCommerce
- Owners: CommerceAnalytics
- Tags: Commerce.DigitalProduct, Commerce.Revenue, DbtTags.certified_candidate, DbtTags.digital_commerce, Tier.Tier2

| Column | Type | Classification and terms | Description |
| --- | --- | --- | --- |
| `product_id` | `integer` | None |  |
| `product_name` | `text` | None |  |
| `album_title` | `text` | None |  |
| `artist_name` | `text` | None |  |
| `genre_name` | `text` | None |  |
| `order_count` | `bigint` | None |  |
| `unique_customers` | `bigint` | None |  |
| `units_sold` | `bigint` | None |  |
| `revenue` | `numeric(14,2)` | None |  |

## mart_executive_kpis

Single-row executive summary of core digital commerce KPIs.

- FQN: `digital_commerce_postgres.chinook.marts.mart_executive_kpis`
- Domains: DigitalCommerce
- Owners: CommerceAnalytics
- Tags: Commerce.AverageOrderValue, Commerce.Revenue, DbtTags.certified_candidate, DbtTags.digital_commerce, Tier.Tier1

| Column | Type | Classification and terms | Description |
| --- | --- | --- | --- |
| `total_orders` | `bigint` | None |  |
| `total_customers` | `bigint` | None |  |
| `total_units_sold` | `bigint` | None |  |
| `total_revenue` | `numeric(14,2)` | None |  |
| `average_order_value` | `numeric(14,2)` | None |  |
| `reporting_period_start` | `timestamp without time zone` | None |  |
| `reporting_period_end` | `timestamp without time zone` | None |  |
