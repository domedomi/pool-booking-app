from sqlalchemy import select, func
from .db import get_session
from .models import ResourceType, Station, Reservation
with get_session() as s:
    print("resource_type rows:", s.scalar(select(func.count()).select_from(ResourceType)))
    print("station rows:", s.scalar(select(func.count()).select_from(Station)))
    print("reservation rows:", s.scalar(select(func.count()).select_from(Reservation)))
