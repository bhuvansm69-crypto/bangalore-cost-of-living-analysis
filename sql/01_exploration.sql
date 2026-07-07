/*
=============================================================
Bangalore Cost of Living Analysis
Phase 3.1 - Database Exploration
Author: Bhuvan S M
=============================================================
*/

-- ==========================================================
-- 1. Total Records
-- ==========================================================

SELECT COUNT(*) AS total_records
FROM cost_of_living;


-- ==========================================================
-- 2. Total Localities
-- ==========================================================

SELECT COUNT(DISTINCT Locality) AS total_localities
FROM cost_of_living;


-- ==========================================================
-- 3. Total Categories
-- ==========================================================

SELECT COUNT(DISTINCT Category) AS total_categories
FROM cost_of_living;


-- ==========================================================
-- 4. List All Categories
-- ==========================================================

SELECT DISTINCT Category
FROM cost_of_living
ORDER BY Category;


-- ==========================================================
-- 5. Total Providers
-- ==========================================================

SELECT COUNT(DISTINCT Provider) AS total_providers
FROM cost_of_living;


-- ==========================================================
-- 6. List Providers
-- ==========================================================

SELECT DISTINCT Provider
FROM cost_of_living
ORDER BY Provider;


-- ==========================================================
-- 7. Date Range
-- ==========================================================

SELECT
    MIN(Timestamp) AS start_date,
    MAX(Timestamp) AS end_date
FROM cost_of_living;


-- ==========================================================
-- 8. Price Statistics
-- ==========================================================

SELECT
    MIN(Price_INR) AS minimum_price,
    MAX(Price_INR) AS maximum_price,
    ROUND(AVG(Price_INR),2) AS average_price,
    ROUND(SUM(Price_INR),2) AS total_price
FROM cost_of_living;


-- ==========================================================
-- 9. Records Per Category
-- ==========================================================

SELECT
    Category,
    COUNT(*) AS total_records
FROM cost_of_living
GROUP BY Category
ORDER BY total_records DESC;


-- ==========================================================
-- 10. Records Per Locality
-- ==========================================================

SELECT
    Locality,
    COUNT(*) AS total_records
FROM cost_of_living
GROUP BY Locality
ORDER BY total_records DESC;


-- ==========================================================
-- 11. Records Per Provider
-- ==========================================================

SELECT
    Provider,
    COUNT(*) AS total_records
FROM cost_of_living
GROUP BY Provider
ORDER BY total_records DESC;


-- ==========================================================
-- 12. Preview Dataset
-- ==========================================================

SELECT *
FROM cost_of_living
LIMIT 20;