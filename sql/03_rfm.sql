-- 03_rfm.sql
-- RFM scoring using SQL window functions.

WITH snapshot AS (
    SELECT MAX(order_purchase_timestamp) + INTERVAL '1 day' AS ref_date
    FROM orders
    WHERE order_status = 'delivered'
),
base AS (
    SELECT
        o.customer_id,
        MAX(o.order_purchase_timestamp) AS last_purchase,
        COUNT(DISTINCT o.order_id)       AS frequency,
        SUM(p.payment_value)             AS monetary
    FROM orders o
    JOIN payments p ON o.order_id = p.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY o.customer_id
),
rfm AS (
    SELECT
        b.customer_id,
        DATEDIFF('day', b.last_purchase, s.ref_date) AS recency,
        b.frequency,
        b.monetary,
        NTILE(5) OVER (ORDER BY DATEDIFF('day', b.last_purchase, s.ref_date) DESC) AS r_score,
        NTILE(5) OVER (ORDER BY b.frequency ASC)  AS f_score,
        NTILE(5) OVER (ORDER BY b.monetary ASC)   AS m_score
    FROM base b, snapshot s
)
SELECT
    customer_id,
    recency,
    frequency,
    ROUND(monetary, 2) AS monetary,
    r_score,
    f_score,
    m_score,
    r_score * 100 + f_score * 10 + m_score AS rfm_score,
    CASE
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
        WHEN f_score >= 4 AND m_score >= 3                  THEN 'Loyal'
        WHEN r_score >= 3 AND f_score <= 3                  THEN 'Potential Loyalist'
        WHEN r_score >= 4 AND f_score = 1                   THEN 'New Customers'
        WHEN r_score <= 2 AND f_score >= 3                  THEN 'At Risk'
        WHEN r_score = 1 AND f_score = 1                    THEN 'Lost'
        ELSE 'Other'
    END AS segment
FROM rfm
ORDER BY rfm_score DESC;
