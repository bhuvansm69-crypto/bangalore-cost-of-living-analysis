/*
=============================================================
Bangalore Cost of Living Analysis
03 - Provider Analysis

Author : Bhuvan S M
=============================================================
*/

-------------------------------------------------------------
-- 1. Average Price by Provider
-------------------------------------------------------------
SELECT
    Provider,
    ROUND(AVG(Price_INR),2) AS Average_Price
FROM cost_of_living
GROUP BY Provider
ORDER BY Average_Price DESC;

-------------------------------------------------------------
-- 2. Swiggy vs Zomato
-------------------------------------------------------------
SELECT
    Provider,
    COUNT(*) AS Orders,
    ROUND(AVG(Price_INR),2) AS Average_Price,
    MIN(Price_INR) AS Minimum,
    MAX(Price_INR) AS Maximum
FROM cost_of_living
WHERE Provider IN ('Swiggy','Zomato')
GROUP BY Provider;

-------------------------------------------------------------
-- 3. Ola vs Uber
-------------------------------------------------------------
SELECT
    Provider,
    COUNT(*) AS Trips,
    ROUND(AVG(Price_INR),2) AS Average_Fare
FROM cost_of_living
WHERE Provider IN ('Ola','Uber')
GROUP BY Provider;

-------------------------------------------------------------
-- 4. NoBroker vs 99acres
-------------------------------------------------------------
SELECT
    Provider,
    ROUND(AVG(Price_INR),2) AS Average_Rent
FROM cost_of_living
WHERE Provider IN ('NoBroker','99acres')
GROUP BY Provider;

-------------------------------------------------------------
-- 5. Internet Providers
-------------------------------------------------------------
SELECT
    Provider,
    ROUND(AVG(Price_INR),2) AS Average_Internet_Cost
FROM cost_of_living
WHERE Provider IN ('ACT','Airtel','JioFiber')
GROUP BY Provider
ORDER BY Average_Internet_Cost DESC;

-------------------------------------------------------------
-- 6. Grocery Providers
-------------------------------------------------------------
SELECT
    Provider,
    ROUND(AVG(Price_INR),2) AS Average_Grocery_Cost
FROM cost_of_living
WHERE Provider IN ('DMart','BigBasket','Blinkit')
GROUP BY Provider
ORDER BY Average_Grocery_Cost DESC;

-------------------------------------------------------------
-- 7. Gym Providers
-------------------------------------------------------------
SELECT
    Provider,
    ROUND(AVG(Price_INR),2) AS Average_Gym_Cost
FROM cost_of_living
WHERE Provider IN ('Cult','Local Gym')
GROUP BY Provider;

-------------------------------------------------------------
-- 8. Provider-wise Total Records
-------------------------------------------------------------
SELECT
    Provider,
    COUNT(*) AS Total_Records
FROM cost_of_living
GROUP BY Provider
ORDER BY Total_Records DESC;

-------------------------------------------------------------
-- 9. Provider-wise Category Distribution
-------------------------------------------------------------
SELECT
    Provider,
    Category,
    COUNT(*) AS Records
FROM cost_of_living
GROUP BY Provider, Category
ORDER BY Provider, Category;

-------------------------------------------------------------
-- 10. Highest Average Provider Cost
-------------------------------------------------------------
SELECT
    Provider,
    ROUND(AVG(Price_INR),2) AS Average_Cost
FROM cost_of_living
GROUP BY Provider
ORDER BY Average_Cost DESC
LIMIT 5;

-------------------------------------------------------------
-- 11. Lowest Average Provider Cost
-------------------------------------------------------------
SELECT
    Provider,
    ROUND(AVG(Price_INR),2) AS Average_Cost
FROM cost_of_living
GROUP BY Provider
ORDER BY Average_Cost ASC
LIMIT 5;

-------------------------------------------------------------
-- 12. Provider Performance Summary
-------------------------------------------------------------
SELECT
    Provider,
    COUNT(*) AS Records,
    ROUND(AVG(Price_INR),2) AS Avg_Price,
    ROUND(MIN(Price_INR),2) AS Min_Price,
    ROUND(MAX(Price_INR),2) AS Max_Price
FROM cost_of_living
GROUP BY Provider
ORDER BY Avg_Price DESC;