/*
=============================================================
Bangalore Cost of Living Analysis
04 - Cost of Living Index

Author : Bhuvan S M
=============================================================
*/

-------------------------------------------------------------
-- 1. Cost of Living Index (Weighted Score)
-------------------------------------------------------------
SELECT
    Locality,

    ROUND(
        AVG(CASE WHEN Category='rent' THEN Price_INR END)*0.40 +
        AVG(CASE WHEN Category='grocery' THEN Price_INR END)*0.20 +
        AVG(CASE WHEN Category='delivery_app' THEN Price_INR END)*0.10 +
        AVG(CASE WHEN Category='auto_fare' THEN Price_INR END)*0.10 +
        AVG(CASE WHEN Category='internet' THEN Price_INR END)*0.10 +
        AVG(CASE WHEN Category='electricity' THEN Price_INR END)*0.05 +
        AVG(CASE WHEN Category='gym' THEN Price_INR END)*0.05
    ,2) AS Cost_Index

FROM cost_of_living
GROUP BY Locality
ORDER BY Cost_Index DESC;

-------------------------------------------------------------
-- 2. Top 10 Most Expensive Localities
-------------------------------------------------------------
SELECT
    Locality,

    ROUND(
        AVG(CASE WHEN Category='rent' THEN Price_INR END)*0.40 +
        AVG(CASE WHEN Category='grocery' THEN Price_INR END)*0.20 +
        AVG(CASE WHEN Category='delivery_app' THEN Price_INR END)*0.10 +
        AVG(CASE WHEN Category='auto_fare' THEN Price_INR END)*0.10 +
        AVG(CASE WHEN Category='internet' THEN Price_INR END)*0.10 +
        AVG(CASE WHEN Category='electricity' THEN Price_INR END)*0.05 +
        AVG(CASE WHEN Category='gym' THEN Price_INR END)*0.05
    ,2) AS Cost_Index

FROM cost_of_living
GROUP BY Locality
ORDER BY Cost_Index DESC
LIMIT 10;

-------------------------------------------------------------
-- 3. Top 10 Most Affordable Localities
-------------------------------------------------------------
SELECT
    Locality,

    ROUND(
        AVG(CASE WHEN Category='rent' THEN Price_INR END)*0.40 +
        AVG(CASE WHEN Category='grocery' THEN Price_INR END)*0.20 +
        AVG(CASE WHEN Category='delivery_app' THEN Price_INR END)*0.10 +
        AVG(CASE WHEN Category='auto_fare' THEN Price_INR END)*0.10 +
        AVG(CASE WHEN Category='internet' THEN Price_INR END)*0.10 +
        AVG(CASE WHEN Category='electricity' THEN Price_INR END)*0.05 +
        AVG(CASE WHEN Category='gym' THEN Price_INR END)*0.05
    ,2) AS Cost_Index

FROM cost_of_living
GROUP BY Locality
ORDER BY Cost_Index ASC
LIMIT 10;

-------------------------------------------------------------
-- 4. Cost Components per Locality
-------------------------------------------------------------
SELECT
    Locality,

    ROUND(AVG(CASE WHEN Category='rent' THEN Price_INR END),2) AS Rent,

    ROUND(AVG(CASE WHEN Category='grocery' THEN Price_INR END),2) AS Grocery,

    ROUND(AVG(CASE WHEN Category='delivery_app' THEN Price_INR END),2) AS Delivery,

    ROUND(AVG(CASE WHEN Category='auto_fare' THEN Price_INR END),2) AS Auto_Fare,

    ROUND(AVG(CASE WHEN Category='internet' THEN Price_INR END),2) AS Internet,

    ROUND(AVG(CASE WHEN Category='electricity' THEN Price_INR END),2) AS Electricity,

    ROUND(AVG(CASE WHEN Category='gym' THEN Price_INR END),2) AS Gym

FROM cost_of_living
GROUP BY Locality
ORDER BY Rent DESC;

-------------------------------------------------------------
-- 5. Rank Localities by Cost Index
-------------------------------------------------------------
WITH locality_cost AS
(
SELECT

Locality,

ROUND(
AVG(CASE WHEN Category='rent' THEN Price_INR END)*0.40 +
AVG(CASE WHEN Category='grocery' THEN Price_INR END)*0.20 +
AVG(CASE WHEN Category='delivery_app' THEN Price_INR END)*0.10 +
AVG(CASE WHEN Category='auto_fare' THEN Price_INR END)*0.10 +
AVG(CASE WHEN Category='internet' THEN Price_INR END)*0.10 +
AVG(CASE WHEN Category='electricity' THEN Price_INR END)*0.05 +
AVG(CASE WHEN Category='gym' THEN Price_INR END)*0.05
,2) AS Cost_Index

FROM cost_of_living

GROUP BY Locality
)

SELECT
RANK() OVER(ORDER BY Cost_Index DESC) AS Ranking,
Locality,
Cost_Index

FROM locality_cost;