/*
=============================================================
Bangalore Cost of Living Analysis
07 - Category Analysis

Author : Bhuvan S M
=============================================================
*/

-------------------------------------------------------------
-- 1. Overall Category Statistics
-------------------------------------------------------------
SELECT
    Category,
    COUNT(*) AS Total_Records,
    ROUND(AVG(Price_INR),2) AS Average_Price,
    MIN(Price_INR) AS Minimum_Price,
    MAX(Price_INR) AS Maximum_Price,
    ROUND(SUM(Price_INR),2) AS Total_Spending
FROM cost_of_living
GROUP BY Category
ORDER BY Average_Price DESC;

-------------------------------------------------------------
-- 2. Rent by Locality
-------------------------------------------------------------
SELECT
    Locality,
    ROUND(AVG(Price_INR),2) AS Average_Rent
FROM cost_of_living
WHERE Category='rent'
GROUP BY Locality
ORDER BY Average_Rent DESC;

-------------------------------------------------------------
-- 3. Grocery by Locality
-------------------------------------------------------------
SELECT
    Locality,
    ROUND(AVG(Price_INR),2) AS Average_Grocery
FROM cost_of_living
WHERE Category='grocery'
GROUP BY Locality
ORDER BY Average_Grocery DESC;

-------------------------------------------------------------
-- 4. Delivery App Comparison
-------------------------------------------------------------
SELECT
    Provider,
    ROUND(AVG(Price_INR),2) AS Average_Delivery
FROM cost_of_living
WHERE Category='delivery_app'
GROUP BY Provider
ORDER BY Average_Delivery DESC;

-------------------------------------------------------------
-- 5. Auto Fare Comparison
-------------------------------------------------------------
SELECT
    Provider,
    ROUND(AVG(Price_INR),2) AS Average_Fare
FROM cost_of_living
WHERE Category='auto_fare'
GROUP BY Provider;

-------------------------------------------------------------
-- 6. Internet Providers
-------------------------------------------------------------
SELECT
    Provider,
    ROUND(AVG(Price_INR),2) AS Average_Internet
FROM cost_of_living
WHERE Category='internet'
GROUP BY Provider
ORDER BY Average_Internet DESC;

-------------------------------------------------------------
-- 7. Gym Comparison
-------------------------------------------------------------
SELECT
    Provider,
    ROUND(AVG(Price_INR),2) AS Average_Gym
FROM cost_of_living
WHERE Category='gym'
GROUP BY Provider
ORDER BY Average_Gym DESC;

-------------------------------------------------------------
-- 8. Electricity Bills
-------------------------------------------------------------
SELECT
    Locality,
    ROUND(AVG(Price_INR),2) AS Average_Bill
FROM cost_of_living
WHERE Category='electricity'
GROUP BY Locality
ORDER BY Average_Bill DESC;

-------------------------------------------------------------
-- 9. Fuel Cost
-------------------------------------------------------------
SELECT
    Locality,
    ROUND(AVG(Price_INR),2) AS Average_Fuel
FROM cost_of_living
WHERE Category='fuel'
GROUP BY Locality
ORDER BY Average_Fuel DESC;

-------------------------------------------------------------
-- 10. Metro Fare
-------------------------------------------------------------
SELECT
    Locality,
    ROUND(AVG(Price_INR),2) AS Average_Metro
FROM cost_of_living
WHERE Category='metro'
GROUP BY Locality
ORDER BY Average_Metro DESC;

-------------------------------------------------------------
-- 11. BMTC Fare
-------------------------------------------------------------
SELECT
    Locality,
    ROUND(AVG(Price_INR),2) AS Average_BMTC
FROM cost_of_living
WHERE Category='bmtc'
GROUP BY Locality
ORDER BY Average_BMTC DESC;

-------------------------------------------------------------
-- 12. Highest Average Category
-------------------------------------------------------------
SELECT
    Category,
    ROUND(AVG(Price_INR),2) AS Average_Price
FROM cost_of_living
GROUP BY Category
ORDER BY Average_Price DESC
LIMIT 5;

-------------------------------------------------------------
-- 13. Lowest Average Category
-------------------------------------------------------------
SELECT
    Category,
    ROUND(AVG(Price_INR),2) AS Average_Price
FROM cost_of_living
GROUP BY Category
ORDER BY Average_Price ASC
LIMIT 5;

-------------------------------------------------------------
-- 14. Category-wise Provider Count
-------------------------------------------------------------
SELECT
    Category,
    COUNT(DISTINCT Provider) AS Providers
FROM cost_of_living
GROUP BY Category;

-------------------------------------------------------------
-- 15. Records by Category
-------------------------------------------------------------
SELECT
    Category,
    COUNT(*) AS Records
FROM cost_of_living
GROUP BY Category
ORDER BY Records DESC;