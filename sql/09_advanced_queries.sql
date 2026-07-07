/*
=============================================================
Bangalore Cost of Living Analysis
09 - Advanced Queries (SQLite Compatible)

Author : Bhuvan S M
=============================================================
*/

-------------------------------------------------------------
-- 1. Dataset Summary
-------------------------------------------------------------
SELECT
    COUNT(*) AS Total_Records,
    COUNT(DISTINCT Locality) AS Total_Localities,
    COUNT(DISTINCT Category) AS Total_Categories,
    COUNT(DISTINCT Provider) AS Total_Providers,
    ROUND(AVG(Price_INR),2) AS Average_Price
FROM cost_of_living;

-------------------------------------------------------------
-- 2. Top 10 Most Expensive Localities
-------------------------------------------------------------
SELECT
    Locality,
    ROUND(AVG(Price_INR),2) AS Average_Cost
FROM cost_of_living
GROUP BY Locality
ORDER BY Average_Cost DESC
LIMIT 10;

-------------------------------------------------------------
-- 3. Top 10 Cheapest Localities
-------------------------------------------------------------
SELECT
    Locality,
    ROUND(AVG(Price_INR),2) AS Average_Cost
FROM cost_of_living
GROUP BY Locality
ORDER BY Average_Cost ASC
LIMIT 10;

-------------------------------------------------------------
-- 4. Localities Above Overall Average
-------------------------------------------------------------
SELECT
    Locality,
    ROUND(AVG(Price_INR),2) AS Average_Cost
FROM cost_of_living
GROUP BY Locality
HAVING AVG(Price_INR) >
(
    SELECT AVG(Price_INR)
    FROM cost_of_living
)
ORDER BY Average_Cost DESC;

-------------------------------------------------------------
-- 5. Provider Statistics
-------------------------------------------------------------
SELECT
    Provider,
    COUNT(*) AS Records,
    ROUND(AVG(Price_INR),2) AS Average_Price,
    MIN(Price_INR) AS Minimum,
    MAX(Price_INR) AS Maximum
FROM cost_of_living
GROUP BY Provider
ORDER BY Average_Price DESC;

-------------------------------------------------------------
-- 6. Category Statistics
-------------------------------------------------------------
SELECT
    Category,
    COUNT(*) AS Records,
    ROUND(AVG(Price_INR),2) AS Average_Price,
    MIN(Price_INR) AS Minimum,
    MAX(Price_INR) AS Maximum
FROM cost_of_living
GROUP BY Category
ORDER BY Average_Price DESC;

-------------------------------------------------------------
-- 7. Cost Classification
-------------------------------------------------------------
SELECT
    Locality,
    ROUND(AVG(Price_INR),2) AS Average_Cost,

    CASE
        WHEN AVG(Price_INR) >= 15000 THEN 'Very Expensive'
        WHEN AVG(Price_INR) >= 8000 THEN 'Expensive'
        WHEN AVG(Price_INR) >= 3000 THEN 'Moderate'
        ELSE 'Affordable'
    END AS Cost_Level

FROM cost_of_living
GROUP BY Locality
ORDER BY Average_Cost DESC;

-------------------------------------------------------------
-- 8. Highest Price per Category
-------------------------------------------------------------
SELECT
    Category,
    MAX(Price_INR) AS Highest_Price
FROM cost_of_living
GROUP BY Category
ORDER BY Highest_Price DESC;

-------------------------------------------------------------
-- 9. Lowest Price per Category
-------------------------------------------------------------
SELECT
    Category,
    MIN(Price_INR) AS Lowest_Price
FROM cost_of_living
GROUP BY Category
ORDER BY Lowest_Price ASC;

-------------------------------------------------------------
-- 10. Average Price by Locality and Category
-------------------------------------------------------------
SELECT
    Locality,
    Category,
    ROUND(AVG(Price_INR),2) AS Average_Price
FROM cost_of_living
GROUP BY Locality, Category
ORDER BY Locality, Category;

-------------------------------------------------------------
-- 11. Provider Count per Category
-------------------------------------------------------------
SELECT
    Category,
    COUNT(DISTINCT Provider) AS Provider_Count
FROM cost_of_living
GROUP BY Category
ORDER BY Provider_Count DESC;

-------------------------------------------------------------
-- 12. Duplicate Record Check
-------------------------------------------------------------
SELECT
    Timestamp,
    Locality,
    Category,
    Provider,
    COUNT(*) AS Duplicate_Count
FROM cost_of_living
GROUP BY Timestamp, Locality, Category, Provider
HAVING COUNT(*) > 1;

-------------------------------------------------------------
-- 13. Price Range by Category
-------------------------------------------------------------
SELECT
    Category,
    MIN(Price_INR) AS Minimum_Price,
    MAX(Price_INR) AS Maximum_Price,
    MAX(Price_INR)-MIN(Price_INR) AS Price_Range
FROM cost_of_living
GROUP BY Category
ORDER BY Price_Range DESC;

-------------------------------------------------------------
-- 14. Average Cost by Provider
-------------------------------------------------------------
SELECT
    Provider,
    ROUND(AVG(Price_INR),2) AS Average_Cost
FROM cost_of_living
GROUP BY Provider
ORDER BY Average_Cost DESC;

-------------------------------------------------------------
-- 15. Total Spending by Category
-------------------------------------------------------------
SELECT
    Category,
    ROUND(SUM(Price_INR),2) AS Total_Spending
FROM cost_of_living
GROUP BY Category
ORDER BY Total_Spending DESC;

-------------------------------------------------------------
-- 16. Monthly Average Cost
-------------------------------------------------------------
SELECT
    substr(Timestamp,1,7) AS Month,
    ROUND(AVG(Price_INR),2) AS Average_Cost
FROM cost_of_living
GROUP BY Month
ORDER BY Month;

-------------------------------------------------------------
-- 17. Monthly Record Count
-------------------------------------------------------------
SELECT
    substr(Timestamp,1,7) AS Month,
    COUNT(*) AS Records
FROM cost_of_living
GROUP BY Month
ORDER BY Month;

-------------------------------------------------------------
-- 18. Localities with Rent Above Average Rent
-------------------------------------------------------------
SELECT
    Locality,
    ROUND(AVG(Price_INR),2) AS Average_Rent
FROM cost_of_living
WHERE Category='rent'
GROUP BY Locality
HAVING AVG(Price_INR) >
(
    SELECT AVG(Price_INR)
    FROM cost_of_living
    WHERE Category='rent'
)
ORDER BY Average_Rent DESC;

-------------------------------------------------------------
-- 19. Provider Performance
-------------------------------------------------------------
SELECT
    Provider,
    COUNT(*) AS Total_Records,
    ROUND(AVG(Price_INR),2) AS Average_Price
FROM cost_of_living
GROUP BY Provider
HAVING COUNT(*) > 100
ORDER BY Total_Records DESC;

-------------------------------------------------------------
-- 20. Final Project Summary
-------------------------------------------------------------
SELECT
    COUNT(*) AS Total_Records,
    COUNT(DISTINCT Locality) AS Localities,
    COUNT(DISTINCT Category) AS Categories,
    COUNT(DISTINCT Provider) AS Providers,
    ROUND(AVG(Price_INR),2) AS Average_Price,
    ROUND(SUM(Price_INR),2) AS Total_Value
FROM cost_of_living;