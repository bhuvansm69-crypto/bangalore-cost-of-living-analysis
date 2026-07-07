/*
=============================================================
Bangalore Cost of Living Analysis
08 - Time Series Analysis

Author : Bhuvan S M
=============================================================
*/

-------------------------------------------------------------
-- 1. Monthly Average Cost
-------------------------------------------------------------
SELECT
    substr(Timestamp,1,7) AS Month,
    ROUND(AVG(Price_INR),2) AS Average_Price
FROM cost_of_living
GROUP BY Month
ORDER BY Month;

-------------------------------------------------------------
-- 2. Monthly Total Spending
-------------------------------------------------------------
SELECT
    substr(Timestamp,1,7) AS Month,
    ROUND(SUM(Price_INR),2) AS Total_Spending
FROM cost_of_living
GROUP BY Month
ORDER BY Month;

-------------------------------------------------------------
-- 3. Monthly Rent Trend
-------------------------------------------------------------
SELECT
    substr(Timestamp,1,7) AS Month,
    ROUND(AVG(Price_INR),2) AS Average_Rent
FROM cost_of_living
WHERE Category='rent'
GROUP BY Month
ORDER BY Month;

-------------------------------------------------------------
-- 4. Monthly Grocery Trend
-------------------------------------------------------------
SELECT
    substr(Timestamp,1,7) AS Month,
    ROUND(AVG(Price_INR),2) AS Average_Grocery
FROM cost_of_living
WHERE Category='grocery'
GROUP BY Month
ORDER BY Month;

-------------------------------------------------------------
-- 5. Monthly Delivery Trend
-------------------------------------------------------------
SELECT
    substr(Timestamp,1,7) AS Month,
    ROUND(AVG(Price_INR),2) AS Average_Delivery
FROM cost_of_living
WHERE Category='delivery_app'
GROUP BY Month
ORDER BY Month;

-------------------------------------------------------------
-- 6. Monthly Auto Fare Trend
-------------------------------------------------------------
SELECT
    substr(Timestamp,1,7) AS Month,
    ROUND(AVG(Price_INR),2) AS Average_Auto_Fare
FROM cost_of_living
WHERE Category='auto_fare'
GROUP BY Month
ORDER BY Month;

-------------------------------------------------------------
-- 7. Monthly Fuel Trend
-------------------------------------------------------------
SELECT
    substr(Timestamp,1,7) AS Month,
    ROUND(AVG(Price_INR),2) AS Average_Fuel
FROM cost_of_living
WHERE Category='fuel'
GROUP BY Month
ORDER BY Month;

-------------------------------------------------------------
-- 8. Monthly Electricity Bills
-------------------------------------------------------------
SELECT
    substr(Timestamp,1,7) AS Month,
    ROUND(AVG(Price_INR),2) AS Average_Bill
FROM cost_of_living
WHERE Category='electricity'
GROUP BY Month
ORDER BY Month;

-------------------------------------------------------------
-- 9. Monthly Internet Charges
-------------------------------------------------------------
SELECT
    substr(Timestamp,1,7) AS Month,
    ROUND(AVG(Price_INR),2) AS Average_Internet
FROM cost_of_living
WHERE Category='internet'
GROUP BY Month
ORDER BY Month;

-------------------------------------------------------------
-- 10. Monthly Gym Fees
-------------------------------------------------------------
SELECT
    substr(Timestamp,1,7) AS Month,
    ROUND(AVG(Price_INR),2) AS Average_Gym
FROM cost_of_living
WHERE Category='gym'
GROUP BY Month
ORDER BY Month;

-------------------------------------------------------------
-- 11. Monthly Metro Fare
-------------------------------------------------------------
SELECT
    substr(Timestamp,1,7) AS Month,
    ROUND(AVG(Price_INR),2) AS Average_Metro
FROM cost_of_living
WHERE Category='metro'
GROUP BY Month
ORDER BY Month;

-------------------------------------------------------------
-- 12. Monthly BMTC Fare
-------------------------------------------------------------
SELECT
    substr(Timestamp,1,7) AS Month,
    ROUND(AVG(Price_INR),2) AS Average_BMTC
FROM cost_of_living
WHERE Category='bmtc'
GROUP BY Month
ORDER BY Month;

-------------------------------------------------------------
-- 13. Yearly Average Cost
-------------------------------------------------------------
SELECT
    substr(Timestamp,1,4) AS Year,
    ROUND(AVG(Price_INR),2) AS Average_Cost
FROM cost_of_living
GROUP BY Year
ORDER BY Year;

-------------------------------------------------------------
-- 14. Yearly Spending
-------------------------------------------------------------
SELECT
    substr(Timestamp,1,4) AS Year,
    ROUND(SUM(Price_INR),2) AS Total_Spending
FROM cost_of_living
GROUP BY Year
ORDER BY Year;

-------------------------------------------------------------
-- 15. Records per Month
-------------------------------------------------------------
SELECT
    substr(Timestamp,1,7) AS Month,
    COUNT(*) AS Total_Records
FROM cost_of_living
GROUP BY Month
ORDER BY Month;