/*
=============================================================
Bangalore Cost of Living Analysis
02 - Locality Analysis

Author : Bhuvan S M
=============================================================
*/

-------------------------------------------------------------
-- 1. Average Cost by Locality
-------------------------------------------------------------
SELECT
    Locality,
    ROUND(AVG(Price_INR),2) AS Average_Cost
FROM cost_of_living
GROUP BY Locality
ORDER BY Average_Cost DESC;

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
-- 3. Top 10 Most Affordable Localities
-------------------------------------------------------------
SELECT
    Locality,
    ROUND(AVG(Price_INR),2) AS Average_Cost
FROM cost_of_living
GROUP BY Locality
ORDER BY Average_Cost ASC
LIMIT 10;

-------------------------------------------------------------
-- 4. Average Rent by Locality
-------------------------------------------------------------
SELECT
    Locality,
    ROUND(AVG(Price_INR),2) AS Average_Rent
FROM cost_of_living
WHERE Category='rent'
GROUP BY Locality
ORDER BY Average_Rent DESC;

-------------------------------------------------------------
-- 5. Average Grocery Cost by Locality
-------------------------------------------------------------
SELECT
    Locality,
    ROUND(AVG(Price_INR),2) AS Average_Grocery
FROM cost_of_living
WHERE Category='grocery'
GROUP BY Locality
ORDER BY Average_Grocery DESC;

-------------------------------------------------------------
-- 6. Average Food Delivery Cost
-------------------------------------------------------------
SELECT
    Locality,
    ROUND(AVG(Price_INR),2) AS Average_Delivery
FROM cost_of_living
WHERE Category='delivery_app'
GROUP BY Locality
ORDER BY Average_Delivery DESC;

-------------------------------------------------------------
-- 7. Average Auto Fare
-------------------------------------------------------------
SELECT
    Locality,
    ROUND(AVG(Price_INR),2) AS Average_Auto_Fare
FROM cost_of_living
WHERE Category='auto_fare'
GROUP BY Locality
ORDER BY Average_Auto_Fare DESC;

-------------------------------------------------------------
-- 8. Highest Recorded Price by Locality
-------------------------------------------------------------
SELECT
    Locality,
    MAX(Price_INR) AS Highest_Price
FROM cost_of_living
GROUP BY Locality
ORDER BY Highest_Price DESC;

-------------------------------------------------------------
-- 9. Lowest Recorded Price by Locality
-------------------------------------------------------------
SELECT
    Locality,
    MIN(Price_INR) AS Lowest_Price
FROM cost_of_living
GROUP BY Locality
ORDER BY Lowest_Price ASC;

-------------------------------------------------------------
-- 10. Total Records per Locality
-------------------------------------------------------------
SELECT
    Locality,
    COUNT(*) AS Total_Records
FROM cost_of_living
GROUP BY Locality
ORDER BY Total_Records DESC;

-------------------------------------------------------------
-- 11. Localities with Above Average Cost
-------------------------------------------------------------
SELECT
    Locality,
    ROUND(AVG(Price_INR),2) AS Avg_Cost
FROM cost_of_living
GROUP BY Locality
HAVING AVG(Price_INR) >
(
    SELECT AVG(Price_INR)
    FROM cost_of_living
)
ORDER BY Avg_Cost DESC;

-------------------------------------------------------------
-- 12. Category-wise Average Cost per Locality
-------------------------------------------------------------
SELECT
    Locality,
    Category,
    ROUND(AVG(Price_INR),2) AS Avg_Price
FROM cost_of_living
GROUP BY Locality, Category
ORDER BY Locality, Category;