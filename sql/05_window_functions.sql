/*
=============================================================
Bangalore Cost of Living Analysis
05 - Window Functions

Author : Bhuvan S M
=============================================================
*/

-------------------------------------------------------------
-- 1. Rank Localities by Average Cost
-------------------------------------------------------------

SELECT
    Locality,
    ROUND(AVG(Price_INR),2) AS Avg_Cost,
    RANK() OVER(ORDER BY AVG(Price_INR) DESC) AS Cost_Rank
FROM cost_of_living
GROUP BY Locality;

-------------------------------------------------------------
-- 2. Dense Rank Localities
-------------------------------------------------------------

SELECT
    Locality,
    ROUND(AVG(Price_INR),2) AS Avg_Cost,
    DENSE_RANK() OVER(ORDER BY AVG(Price_INR) DESC) AS Dense_Rank
FROM cost_of_living
GROUP BY Locality;

-------------------------------------------------------------
-- 3. Row Number
-------------------------------------------------------------

SELECT
    Locality,
    ROUND(AVG(Price_INR),2) Avg_Cost,
    ROW_NUMBER() OVER(ORDER BY AVG(Price_INR) DESC) Row_Num
FROM cost_of_living
GROUP BY Locality;

-------------------------------------------------------------
-- 4. Rank Providers
-------------------------------------------------------------

SELECT
    Provider,
    ROUND(AVG(Price_INR),2) Avg_Price,
    RANK() OVER(ORDER BY AVG(Price_INR) DESC) Provider_Rank
FROM cost_of_living
GROUP BY Provider;

-------------------------------------------------------------
-- 5. Top 3 Localities Per Category
-------------------------------------------------------------

WITH Ranked AS
(
SELECT
Category,
Locality,
ROUND(AVG(Price_INR),2) Avg_Price,
ROW_NUMBER() OVER(
PARTITION BY Category
ORDER BY AVG(Price_INR) DESC
) rn
FROM cost_of_living
GROUP BY Category,Locality
)

SELECT *
FROM Ranked
WHERE rn<=3;

-------------------------------------------------------------
-- 6. Bottom 3 Localities Per Category
-------------------------------------------------------------

WITH Ranked AS
(
SELECT
Category,
Locality,
ROUND(AVG(Price_INR),2) Avg_Price,
ROW_NUMBER() OVER(
PARTITION BY Category
ORDER BY AVG(Price_INR)
) rn
FROM cost_of_living
GROUP BY Category,Locality
)

SELECT *
FROM Ranked
WHERE rn<=3;

-------------------------------------------------------------
-- 7. Quartiles
-------------------------------------------------------------

SELECT
Locality,
ROUND(AVG(Price_INR),2) Avg_Cost,
NTILE(4) OVER(ORDER BY AVG(Price_INR)) Quartile
FROM cost_of_living
GROUP BY Locality;

-------------------------------------------------------------
-- 8. Running Total
-------------------------------------------------------------

WITH Monthly AS
(
SELECT
substr(Timestamp,1,7) Month,
SUM(Price_INR) Total
FROM cost_of_living
GROUP BY Month
)

SELECT
Month,
Total,
SUM(Total) OVER(ORDER BY Month) Running_Total
FROM Monthly;

-------------------------------------------------------------
-- 9. Moving Average
-------------------------------------------------------------

WITH Monthly AS
(
SELECT
substr(Timestamp,1,7) Month,
AVG(Price_INR) Avg_Price
FROM cost_of_living
GROUP BY Month
)

SELECT
Month,
ROUND(Avg_Price,2),
ROUND(
AVG(Avg_Price) OVER(
ORDER BY Month
ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
),2) Moving_Average
FROM Monthly;

-------------------------------------------------------------
-- 10. Previous Month Cost
-------------------------------------------------------------

WITH Monthly AS
(
SELECT
substr(Timestamp,1,7) Month,
AVG(Price_INR) Avg_Price
FROM cost_of_living
GROUP BY Month
)

SELECT
Month,
ROUND(Avg_Price,2),
ROUND(LAG(Avg_Price) OVER(ORDER BY Month),2) Previous_Month
FROM Monthly;

-------------------------------------------------------------
-- 11. Next Month Cost
-------------------------------------------------------------

WITH Monthly AS
(
SELECT
substr(Timestamp,1,7) Month,
AVG(Price_INR) Avg_Price
FROM cost_of_living
GROUP BY Month
)

SELECT
Month,
ROUND(Avg_Price,2),
ROUND(LEAD(Avg_Price) OVER(ORDER BY Month),2) Next_Month
FROM Monthly;

-------------------------------------------------------------
-- 12. Monthly Change
-------------------------------------------------------------

WITH Monthly AS
(
SELECT
substr(Timestamp,1,7) Month,
AVG(Price_INR) Avg_Price
FROM cost_of_living
GROUP BY Month
)

SELECT
Month,
ROUND(Avg_Price,2),
ROUND(
Avg_Price-
LAG(Avg_Price) OVER(ORDER BY Month)
,2) Change
FROM Monthly;