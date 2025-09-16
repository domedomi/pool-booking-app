from __future__ import annotations
from datetime import date
from typing import Optional

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from .db import get_session
from .models import Reservation, ReservationLine, Timeslot

def _ensure_day(session, cal_date: date) -> None:
    session.execute(text("INSERT IGNORE INTO calendar_day(cal_date) VALUES (:d)"), {"d": cal_date})

def create_reservation(customer_ref: str, status: str = "HOLD") -> int:
    with get_session() as s:
        r = Reservation(customer_ref=customer_ref, status=status)
        s.add(r)
        s.commit()
        return r.reservation_id

def add_station_line(reservation_id: int, cal_date: date, timeslot: str, station_id: int, qty: Optional[int] = None) -> int:
    with get_session() as s:
        _ensure_day(s, cal_date)
        line = ReservationLine(
            reservation_id=reservation_id,
            cal_date=cal_date,
            timeslot=Timeslot[timeslot],
            station_id=station_id,
            qty=qty,
        )
        s.add(line)
        try:
            s.commit()
        except IntegrityError:
            s.rollback()
            raise
        return line.reservation_line_id

def add_resource_line(reservation_id: int, cal_date: date, timeslot: str, resource_type_id: int, qty: Optional[int] = None) -> int:
    with get_session() as s:
        _ensure_day(s, cal_date)
        line = ReservationLine(
            reservation_id=reservation_id,
            cal_date=cal_date,
            timeslot=Timeslot[timeslot],
            resource_type_id=resource_type_id,
            qty=qty,
        )
        s.add(line)
        try:
            s.commit()
        except IntegrityError:
            s.rollback()
            raise
        return line.reservation_line_id

from .models import ResStatus

def set_reservation_status(reservation_id: int, status: str) -> None:
    """status ∈ {'HOLD','CONFIRMED','CANCELLED'}"""
    with get_session() as s:
        r = s.get(Reservation, reservation_id)
        if not r:
            raise ValueError(f"reservation {reservation_id} not found")
        r.status = ResStatus[status]
        s.commit()

def delete_line(reservation_line_id: int) -> None:
    with get_session() as s:
        l = s.get(ReservationLine, reservation_line_id)
        if not l:
            return
        s.delete(l)
        s.commit()

def delete_reservation(reservation_id: int) -> None:
    with get_session() as s:
        r = s.get(Reservation, reservation_id)
        if not r:
            return
        s.delete(r)  # cascata su lines
        s.commit()
