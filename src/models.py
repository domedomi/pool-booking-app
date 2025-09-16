from __future__ import annotations
from typing import List, Optional
from enum import Enum as PyEnum
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, String, Boolean, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import BIGINT as MyBIGINT, INTEGER as MyINTEGER

class Base(DeclarativeBase):
    pass

class Timeslot(PyEnum):
    AM = "AM"
    PM = "PM"
    FULL = "FULL"

class ResStatus(PyEnum):
    HOLD = "HOLD"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"

class ResourceType(Base):
    __tablename__ = "resource_type"
    resource_type_id: Mapped[int] = mapped_column(MyBIGINT(unsigned=True), primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_quantifiable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    needs_map: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    cap_default_am: Mapped[Optional[int]] = mapped_column(MyINTEGER(unsigned=True), nullable=True)
    cap_default_pm: Mapped[Optional[int]] = mapped_column(MyINTEGER(unsigned=True), nullable=True)
    cap_default_full: Mapped[Optional[int]] = mapped_column(MyINTEGER(unsigned=True), nullable=True)

    stations: Mapped[List["Station"]] = relationship(back_populates="resource_type", lazy="selectin")
    lines: Mapped[List["ReservationLine"]] = relationship(back_populates="resource_type", lazy="selectin")

class Station(Base):
    __tablename__ = "station"
    station_id: Mapped[int] = mapped_column(MyBIGINT(unsigned=True), primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    resource_type_id: Mapped[int] = mapped_column(
        MyBIGINT(unsigned=True),
        ForeignKey("resource_type.resource_type_id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    resource_type: Mapped["ResourceType"] = relationship(back_populates="stations", lazy="joined")
    lines: Mapped[List["ReservationLine"]] = relationship(back_populates="station", lazy="selectin")

class CalendarDay(Base):
    __tablename__ = "calendar_day"
    cal_date: Mapped[date] = mapped_column(Date, primary_key=True)

class Reservation(Base):
    __tablename__ = "reservation"
    reservation_id: Mapped[int] = mapped_column(MyBIGINT(unsigned=True), primary_key=True, autoincrement=True)
    customer_ref: Mapped[Optional[str]] = mapped_column(String(100))
    status: Mapped[ResStatus] = mapped_column(Enum(ResStatus), nullable=False, default=ResStatus.HOLD)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP")
    )

    lines: Mapped[List["ReservationLine"]] = relationship(
        back_populates="reservation",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin",
    )

class ReservationLine(Base):
    __tablename__ = "reservation_line"
    __table_args__ = (
        UniqueConstraint("reservation_id","cal_date","timeslot","station_id", name="uq_rl_station"),
        UniqueConstraint("reservation_id","cal_date","timeslot","resource_type_id", name="uq_rl_resource"),
    )

    reservation_line_id: Mapped[int] = mapped_column(MyBIGINT(unsigned=True), primary_key=True, autoincrement=True)
    reservation_id: Mapped[int] = mapped_column(
        MyBIGINT(unsigned=True),
        ForeignKey("reservation.reservation_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    cal_date: Mapped[date] = mapped_column(Date, nullable=False)
    timeslot: Mapped[Timeslot] = mapped_column(Enum(Timeslot), nullable=False)
    station_id: Mapped[Optional[int]] = mapped_column(
        MyBIGINT(unsigned=True),
        ForeignKey("station.station_id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=True,
    )
    resource_type_id: Mapped[Optional[int]] = mapped_column(
        MyBIGINT(unsigned=True),
        ForeignKey("resource_type.resource_type_id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=True,
    )
    qty: Mapped[Optional[int]] = mapped_column(MyINTEGER(unsigned=True), nullable=True)

    reservation: Mapped["Reservation"] = relationship(back_populates="lines", lazy="joined")
    station: Mapped[Optional["Station"]] = relationship(back_populates="lines", lazy="joined")
    resource_type: Mapped[Optional["ResourceType"]] = relationship(back_populates="lines", lazy="joined")
