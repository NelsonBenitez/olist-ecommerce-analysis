-- 04_metrics.sql
-- Key business KPIs.

-- 1. Revenue by month
SELECT
    DATE_TRUNC('month', order_purchase_timestamp) AS month,
    COUNT(DISTINCT order_id)                       AS orders,
    ROUND(SUM(payment_value), 2)                   AS revenue,
    ROUND(AVG(payment_value), 2)                   AS avg_order_value
FROM master
WHERE order_status = 'delivered'
GROUP BY 1
ORDER BY 1;

-- 2. Top 10 product categories by revenue
SELECT
    category_english,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(price), 2)     AS revenue,
    ROUND(AVG(review_score), 2) AS avg_review
FROM master
WHERE order_status = 'delivered'
  AND category_english IS NOT NULL
GROUP BY category_english
ORDER BY revenue DESC
LIMIT 10;

-- 3. Delivery delay vs review score
SELECT
    review_score,
    COUNT(*)                              AS orders,
    ROUND(AVG(delivery_delay_days), 1)   AS avg_delay_days,
    ROUND(SUM(CASE WHEN delivery_delay_days > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS late_pct
FROM master
WHERE order_status = 'delivered'
  AND review_score IS NOT NULL
  AND delivery_delay_days IS NOT NULL
GROUP BY review_score
ORDER BY review_score;

-- 4. Revenue by state (for geo map)
SELECT
    customer_state,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(payment_value), 2) AS revenue
FROM master
WHERE order_status = 'delivered'
GROUP BY customer_state
ORDER BY revenue DESC;
