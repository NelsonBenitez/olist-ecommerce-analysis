-- 01_schema_joins.sql
-- Master joined view combining the core Olist tables.
-- Run this in DuckDB or SQLite after importing CSVs.

CREATE OR REPLACE VIEW master AS
SELECT
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_approved_at,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,

    -- Delivery delay in days (positive = late)
    DATEDIFF('day',
        o.order_estimated_delivery_date,
        o.order_delivered_customer_date
    ) AS delivery_delay_days,

    oi.product_id,
    oi.seller_id,
    oi.price,
    oi.freight_value,
    oi.price + oi.freight_value AS order_total,

    p.payment_type,
    p.payment_installments,
    p.payment_value,

    r.review_score,
    r.review_creation_date,

    pr.product_category_name,
    ct.product_category_name_english AS category_english,

    c.customer_city,
    c.customer_state,

    s.seller_city,
    s.seller_state

FROM orders o
LEFT JOIN order_items oi   ON o.order_id  = oi.order_id
LEFT JOIN payments    p    ON o.order_id  = p.order_id
LEFT JOIN reviews     r    ON o.order_id  = r.order_id
LEFT JOIN products    pr   ON oi.product_id = pr.product_id
LEFT JOIN category_t  ct   ON pr.product_category_name = ct.product_category_name
LEFT JOIN customers   c    ON o.customer_id = c.customer_id
LEFT JOIN sellers     s    ON oi.seller_id  = s.seller_id;
