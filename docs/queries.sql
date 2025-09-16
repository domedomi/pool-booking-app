-- 1) Linee per giorno
SELECT rl.cal_date, rl.timeslot, r.reservation_id, r.customer_ref,
       rl.station_id, rl.resource_type_id, rl.qty
FROM reservation_line rl
JOIN reservation r ON r.reservation_id = rl.reservation_id
WHERE rl.cal_date BETWEEN :d1 AND :d2
ORDER BY rl.cal_date, rl.timeslot, rl.reservation_id, rl.reservation_line_id;

-- 2) Conteggi per resource_type
SELECT rl.cal_date, rl.timeslot, rl.resource_type_id,
       COUNT(*) AS line_count, COALESCE(SUM(rl.qty),0) AS qty_sum
FROM reservation_line rl
WHERE rl.resource_type_id IS NOT NULL
  AND rl.cal_date BETWEEN :d1 AND :d2
GROUP BY rl.cal_date, rl.timeslot, rl.resource_type_id
ORDER BY rl.cal_date, rl.timeslot, rl.resource_type_id;

-- 3) Conteggi per station
SELECT rl.cal_date, rl.timeslot, rl.station_id,
       COUNT(*) AS line_count, COALESCE(SUM(rl.qty),0) AS qty_sum
FROM reservation_line rl
WHERE rl.station_id IS NOT NULL
  AND rl.cal_date BETWEEN :d1 AND :d2
GROUP BY rl.cal_date, rl.timeslot, rl.station_id
ORDER BY rl.cal_date, rl.timeslot, rl.station_id;
