/*
=============================================================
Bangalore Cost of Living Analysis
11 - Dashboard Queries
Author : Bhuvan S M
=============================================================
*/

-------------------------------------------------------------
-- Dashboard 1
-------------------------------------------------------------
SELECT
Locality,
ROUND(AVG(Price_INR),2) Avg_Cost
FROM cost_of_living
GROUP BY Locality
ORDER BY Avg_Cost DESC;

-------------------------------------------------------------
-- Dashboard 2
-------------------------------------------------------------
SELECT
Category,
ROUND(AVG(Price_INR),2) Avg_Price
FROM cost_of_living
GROUP BY Category;

-------------------------------------------------------------
-- Dashboard 3
-------------------------------------------------------------
SELECT
Provider,
ROUND(AVG(Price_INR),2) Avg_Price
FROM cost_of_living
GROUP BY Provider;

-------------------------------------------------------------
-- Dashboard 4
-------------------------------------------------------------
SELECT
substr(Timestamp,1,7) Month,
ROUND(AVG(Price_INR),2) Avg_Price
FROM cost_of_living
GROUP BY Month
ORDER BY Month;

-------------------------------------------------------------
-- Dashboard 5
-------------------------------------------------------------
SELECT
Category,
SUM(Price_INR) Total
FROM cost_of_living
GROUP BY Category;

-------------------------------------------------------------
-- Dashboard 6
-------------------------------------------------------------
SELECT
Locality,
Category,
ROUND(AVG(Price_INR),2) Avg_Price
FROM cost_of_living
GROUP BY Locality,Category;

-------------------------------------------------------------
-- Dashboard 7
-------------------------------------------------------------
SELECT
Provider,
COUNT(*) Records
FROM cost_of_living
GROUP BY Provider;

-------------------------------------------------------------
-- Dashboard 8
-------------------------------------------------------------
SELECT
Locality,
COUNT(*) Records
FROM cost_of_living
GROUP BY Locality;

-------------------------------------------------------------
-- Dashboard 9
-------------------------------------------------------------
SELECT
Category,
MIN(Price_INR) Minimum,
MAX(Price_INR) Maximum
FROM cost_of_living
GROUP BY Category;

-------------------------------------------------------------
-- Dashboard 10
-------------------------------------------------------------
SELECT
Locality,
ROUND(AVG(CASE WHEN Category='rent' THEN Price_INR END),2) Rent,
ROUND(AVG(CASE WHEN Category='grocery' THEN Price_INR END),2) Grocery,
ROUND(AVG(CASE WHEN Category='delivery_app' THEN Price_INR END),2) Delivery
FROM cost_of_living
GROUP BY Locality;