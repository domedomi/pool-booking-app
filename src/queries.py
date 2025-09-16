from datetime import date
from typing import Iterable, Tuple
from sqlalchemy import text
from .db import get_session

def lines_by_day(d_from: date, d_to: date) -> Iterable[Tuple]:
    sql = text("""
        SELECT rl.cal_date,
               rl.timeslot,
               r.reservation_id,
               r.customer_ref,
               rl.station_id,
               rl.resource_type_id,
               rl.qty
        FROM reservation_line rl
        JOIN reservation r ON r.reservation_id = rl.reservation_id
        WHERE rl.cal_date BETWEEN :d1 AND :d2
        ORDER BY rl.cal_date, rl.timeslot, rl.reservation_id, rl.reservation_line_id
    """)
    with get_session() as s:
        return list(s.execute(sql, {"d1": d_from, "d2": d_to}).fetchall())

def counts_by_resource_type(d_from: date, d_to: date) -> Iterable[Tuple]:
    sql = text("""
        SELECT rl.cal_date, rl.timeslot, rl.resource_type_id,
               COUNT(*) AS line_count, COALESCE(SUM(rl.qty),0) AS qty_sum
        FROM reservation_line rl
        WHERE rl.resource_type_id IS NOT NULL
          AND rl.cal_date BETWEEN :d1 AND :d2
        GROUP BY rl.cal_date, rl.timeslot, rl.resource_type_id
        ORDER BY rl.cal_date, rl.timeslot, rl.resource_type_id
    """)
    with get_session() as s:
        return list(s.execute(sql, {"d1": d_from, "d2": d_to}).fetchall())

def counts_by_station(d_from: date, d_to: date) -> Iterable[Tuple]:
    sql = text("""
        SELECT rl.cal_date, rl.timeslot, rl.station_id,
               COUNT(*) AS line_count, COALESCE(SUM(rl.qty),0) AS qty_sum
        FROM reservation_line rl
        WHERE rl.station_id IS NOT NULL
          AND rl.cal_date BETWEEN :d1 AND :d2
        GROUP BY rl.cal_date, rl.timeslot, rl.station_id
        ORDER BY rl.cal_date, rl.timeslot, rl.station_id
    """)
    with get_session() as s:
        return list(s.execute(sql, {"d1": d_from, "d2": d_to}).fetchall())
