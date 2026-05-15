-- 02_funnel.sql
-- Sales funnel: count of orders at each status stage.

SELECT
    order_status,
    COUNT(*) AS order_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct_of_total
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;

-- Funnel in logical sequence
SELECT
    stage,
    order_count,
    ROUND(order_count * 100.0 / LAG(order_count) OVER (ORDER BY step_num), 1) AS conversion_pct
FROM (
    VALUES
        (1, 'Placed',    (SELECT COUNT(*) FROM orders)),
        (2, 'Approved',  (SELECT COUNT(*) FROM orders WHERE order_approved_at IS NOT NULL)),
        (3, 'Shipped',   (SELECT COUNT(*) FROM orders WHERE order_delivered_carrier_date IS NOT NULL)),
        (4, 'Delivered', (SELECT COUNT(*) FROM orders WHERE order_status = 'delivered')),
        (5, 'Reviewed',  (SELECT COUNT(*) FROM reviews WHERE review_score IS NOT NULL))
) AS t(step_num, stage, order_count);
