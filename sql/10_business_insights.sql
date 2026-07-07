/*
=============================================================
Bangalore Cost of Living Analysis
10 - Business Insights
Author : Bhuvan S M
=============================================================
*/

-------------------------------------------------------------
-- 1. Top 10 Expensive Localities
-------------------------------------------------------------
SELECT Locality,
ROUND(AVG(Price_INR),2) AS Avg_Cost
FROM cost_of_living
GROUP BY Locality
ORDER BY Avg_Cost DESC
LIMIT 10;

-------------------------------------------------------------
-- 2. Top 10 Affordable Localities
-------------------------------------------------------------
SELECT Locality,
ROUND(AVG(Price_INR),2) AS Avg_Cost
FROM cost_of_living
GROUP BY Locality
ORDER BY Avg_Cost
LIMIT 10;

-------------------------------------------------------------
-- 3. Highest Average Rent
-------------------------------------------------------------
SELECT Locality,
ROUND(AVG(Price_INR),2) AS Avg_Rent
FROM cost_of_living
WHERE Category='rent'
GROUP BY Locality
ORDER BY Avg_Rent DESC
LIMIT 10;

-------------------------------------------------------------
-- 4. Cheapest Rent
-------------------------------------------------------------
SELECT Locality,
ROUND(AVG(Price_INR),2) Avg_Rent
FROM cost_of_living
WHERE Category='rent'
GROUP BY Locality
ORDER BY Avg_Rent
LIMIT 10;

-------------------------------------------------------------
-- 5. Swiggy vs Zomato
-------------------------------------------------------------
SELECT Provider,
ROUND(AVG(Price_INR),2) Avg_Delivery
FROM cost_of_living
WHERE Category='delivery_app'
GROUP BY Provider;

-------------------------------------------------------------
-- 6. Ola vs Uber
-------------------------------------------------------------
SELECT Provider,
ROUND(AVG(Price_INR),2) Avg_Fare
FROM cost_of_living
WHERE Category='auto_fare'
GROUP BY Provider;

-------------------------------------------------------------
-- 7. Grocery Providers
-------------------------------------------------------------
SELECT Provider,
ROUND(AVG(Price_INR),2) Avg_Grocery
FROM cost_of_living
WHERE Category='grocery'
GROUP BY Provider;

-------------------------------------------------------------
-- 8. Internet Providers
-------------------------------------------------------------
SELECT Provider,
ROUND(AVG(Price_INR),2) Avg_Internet
FROM cost_of_living
WHERE Category='internet'
GROUP BY Provider;

-------------------------------------------------------------
-- 9. Gym Providers
-------------------------------------------------------------
SELECT Provider,
ROUND(AVG(Price_INR),2) Avg_Gym
FROM cost_of_living
WHERE Category='gym'
GROUP BY Provider;

-------------------------------------------------------------
-- 10. Category Spending
-------------------------------------------------------------
SELECT Category,
ROUND(SUM(Price_INR),2) Total_Spending
FROM cost_of_living
GROUP BY Category
ORDER BY Total_Spending DESC;

-------------------------------------------------------------
-- 11. Provider Records
-------------------------------------------------------------
SELECT Provider,
COUNT(*) Total_Records
FROM cost_of_living
GROUP BY Provider
ORDER BY Total_Records DESC;

-------------------------------------------------------------
-- 12. Category Records
-------------------------------------------------------------
SELECT Category,
COUNT(*) Records
FROM cost_of_living
GROUP BY Category
ORDER BY Records DESC;