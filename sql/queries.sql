-- 1. Total number of trips
SELECT COUNT(*) AS total_trips
FROM uber_trips;

-- 2. Trips per month
SELECT month, COUNT(*) AS trips
FROM uber_trips
GROUP BY month
ORDER BY month;

-- 3. Trips per weekday
SELECT weekday, COUNT(*) AS trips
FROM uber_trips
GROUP BY weekday
ORDER BY trips DESC;

-- 4. Peak hour analysis
SELECT hour, COUNT(*) AS trips
FROM uber_trips
GROUP BY hour
ORDER BY trips DESC;

-- 5. Active vehicles per day
SELECT date, COUNT(DISTINCT vehicle_id) AS active_vehicles
FROM uber_trips
GROUP BY date
ORDER BY date;