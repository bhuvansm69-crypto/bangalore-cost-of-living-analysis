/*
=============================================================
Bangalore Cost of Living Analysis
06 - SQL Views

Author : Bhuvan S M
=============================================================
*/

-------------------------------------------------------------
-- View 1 : Average Cost by Locality
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS vw_locality_average AS
SELECT
    Locality,
    ROUND(AVG(Price_INR),2) AS Average_Cost
FROM cost_of_living
GROUP BY Locality;

-------------------------------------------------------------
-- View 2 : Average Rent
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS vw_rent_summary AS
SELECT
    Locality,
    ROUND(AVG(Price_INR),2) AS Average_Rent
FROM cost_of_living
WHERE Category='rent'
GROUP BY Locality;

-------------------------------------------------------------
-- View 3 : Grocery Summary
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS vw_grocery_summary AS
SELECT
    Locality,
    ROUND(AVG(Price_INR),2) AS Average_Grocery
FROM cost_of_living
WHERE Category='grocery'
GROUP BY Locality;

-------------------------------------------------------------
-- View 4 : Delivery Summary
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS vw_delivery_summary AS
SELECT
    Provider,
    ROUND(AVG(Price_INR),2) AS Average_Delivery_Cost
FROM cost_of_living
WHERE Category='delivery_app'
GROUP BY Provider;

-------------------------------------------------------------
-- View 5 : Auto Fare Summary
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS vw_auto_summary AS
SELECT
    Provider,
    ROUND(AVG(Price_INR),2) AS Average_Fare
FROM cost_of_living
WHERE Category='auto_fare'
GROUP BY Provider;

-------------------------------------------------------------
-- View 6 : Internet Summary
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS vw_internet_summary AS
SELECT
    Provider,
    ROUND(AVG(Price_INR),2) AS Average_Internet
FROM cost_of_living
WHERE Category='internet'
GROUP BY Provider;

-------------------------------------------------------------
-- View 7 : Gym Summary
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS vw_gym_summary AS
SELECT
    Provider,
    ROUND(AVG(Price_INR),2) AS Average_Gym_Fee
FROM cost_of_living
WHERE Category='gym'
GROUP BY Provider;

-------------------------------------------------------------
-- View 8 : Monthly Summary
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS vw_monthly_summary AS
SELECT
    substr(Timestamp,1,7) AS Month,
    ROUND(AVG(Price_INR),2) AS Average_Price,
    SUM(Price_INR) AS Total_Cost
FROM cost_of_living
GROUP BY Month;

-------------------------------------------------------------
-- View 9 : Provider Summary
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS vw_provider_summary AS
SELECT
    Provider,
    COUNT(*) AS Total_Records,
    ROUND(AVG(Price_INR),2) AS Average_Price,
    MIN(Price_INR) AS Minimum_Price,
    MAX(Price_INR) AS Maximum_Price
FROM cost_of_living
GROUP BY Provider;

-------------------------------------------------------------
-- View 10 : Category Summary
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS vw_category_summary AS
SELECT
    Category,
    COUNT(*) AS Total_Records,
    ROUND(AVG(Price_INR),2) AS Average_Price
FROM cost_of_living
GROUP BY Category;

-------------------------------------------------------------
-- View 11 : Cost Index
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS vw_cost_index AS

SELECT

Locality,

ROUND(
AVG(CASE WHEN Category='rent' THEN Price_INR END)*0.40+
AVG(CASE WHEN Category='grocery' THEN Price_INR END)*0.20+
AVG(CASE WHEN Category='delivery_app' THEN Price_INR END)*0.10+
AVG(CASE WHEN Category='auto_fare' THEN Price_INR END)*0.10+
AVG(CASE WHEN Category='internet' THEN Price_INR END)*0.10+
AVG(CASE WHEN Category='electricity' THEN Price_INR END)*0.05+
AVG(CASE WHEN Category='gym' THEN Price_INR END)*0.05
,2) AS Cost_Index

FROM cost_of_living

GROUP BY Locality;

-------------------------------------------------------------
-- View 12 : Locality Dashboard
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS vw_dashboard AS

SELECT

Locality,

COUNT(*) AS Records,

ROUND(AVG(Price_INR),2) Avg_Price,

SUM(Price_INR) Total_Cost,

MIN(Price_INR) Minimum,

MAX(Price_INR) Maximum

FROM cost_of_living

GROUP BY Locality;

-------------------------------------------------------------
-- Test Views
-------------------------------------------------------------

SELECT * FROM vw_cost_index LIMIT 10;

SELECT * FROM vw_dashboard LIMIT 10;

SELECT * FROM vw_provider_summary LIMIT 10;

SELECT * FROM vw_category_summary;