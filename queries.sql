-- Q1: Overview of the dataset
SELECT COUNT(*) AS restaurants,
       ROUND(AVG(rating), 2) AS avg_rating,
       ROUND(AVG(cost), 0) AS avg_cost,
       SUM(votes) AS total_votes
FROM restaurants;

-- Q2: Does higher price mean higher rating?
SELECT price_bucket,
       COUNT(*) AS restaurants,
       ROUND(AVG(rating), 2) AS avg_rating,
       ROUND(AVG(votes), 0) AS avg_votes
FROM restaurants
GROUP BY price_bucket
ORDER BY MIN(cost);

-- Q3: Which areas are most crowded?
SELECT location,
       COUNT(*) AS restaurants,
       ROUND(AVG(cost), 0) AS avg_cost,
       ROUND(AVG(rating), 2) AS avg_rating
FROM restaurants
GROUP BY location
ORDER BY restaurants DESC
LIMIT 10;

-- Q4: Do online ordering and table booking change ratings?
SELECT online_order, book_table,
       COUNT(*) AS restaurants,
       ROUND(AVG(rating), 2) AS avg_rating,
       ROUND(AVG(cost), 0) AS avg_cost
FROM restaurants
GROUP BY online_order, book_table
ORDER BY online_order, book_table;

-- Q5: Most common cuisines
SELECT cuisine, COUNT(*) AS restaurants
FROM restaurant_cuisines
GROUP BY cuisine
ORDER BY restaurants DESC
LIMIT 10;

-- Q6: Best rated cuisines (at least 50 restaurants)
SELECT cuisine,
       COUNT(*) AS restaurants,
       ROUND(AVG(rating), 2) AS avg_rating
FROM restaurant_cuisines
GROUP BY cuisine
HAVING COUNT(*) >= 50
ORDER BY avg_rating DESC
LIMIT 10;

-- Q7: Market gaps - well rated areas with fewer restaurants
SELECT location,
       COUNT(*) AS restaurants,
       ROUND(AVG(rating), 2) AS avg_rating
FROM restaurants
GROUP BY location
HAVING COUNT(*) BETWEEN 20 AND 100
ORDER BY avg_rating DESC
LIMIT 10;

-- Q8: Success rate by price bucket
SELECT price_bucket,
       COUNT(*) AS restaurants,
       ROUND(100.0 * SUM(CASE WHEN successful = 1 THEN 1 ELSE 0 END) / COUNT(*), 1) AS success_pct
FROM restaurants
GROUP BY price_bucket
ORDER BY MIN(cost);

-- Q9: Which chains have the most listings?
SELECT name,
       COUNT(*) AS listings,
       ROUND(AVG(rating), 2) AS avg_rating
FROM restaurants
GROUP BY name
ORDER BY listings DESC
LIMIT 10;

-- Q10: Top 3 rated restaurants in each area (window function)
SELECT * FROM (
    SELECT name, location, rating, votes,
           RANK() OVER (PARTITION BY location ORDER BY rating DESC, votes DESC) AS rnk
    FROM restaurants
    WHERE votes > 100
) t
WHERE rnk <= 3
ORDER BY location, rnk
LIMIT 30;
