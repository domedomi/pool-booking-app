from sqlalchemy import text
from .db import engine

with engine.connect() as conn:
    v, es = conn.execute(text("SELECT VERSION(), @@event_scheduler")).one()
    print("MySQL:", v, "event_scheduler:", es)
    conn.execute(text("USE pool_booking"))
    tables = conn.execute(text("SHOW TABLES")).all()
    print("Tabelle:", [t[0] for t in tables])
