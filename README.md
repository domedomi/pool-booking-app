<<<<<<< HEAD
# Gestionale-Piscina
=======
# Pool Booking App

## Setup
1. Avvia MySQL su Docker esposto su 3307.
2. Crea `.env` copiando `.env.example`.
3. `python -m pip install -r requirements.txt`
4. `python -m src.sanity` per verifica connessione.

## Schema
- Import iniziale: `docker cp schema.sql ...` e `mysql < schema.sql`.
- Oppure (solo tabelle ORM, senza trigger): `python -m src.create_schema`.

## CRUD
- API in `src/repo.py`:
  - `create_reservation`, `add_station_line`, `add_resource_line`
  - `set_reservation_status`, `delete_line`, `delete_reservation`

## Query
- SQL e descrizioni: `docs/queries.sql`
- Wrapper Python: `src/queries.py`

## Note
- Dialetto MySQL usato per colonne `UNSIGNED`.
- Trigger su `reservation_line` fanno rispettare XOR tra `station_id` e `resource_type_id`.
>>>>>>> 81e119d (init: SQLAlchemy CRUD app + schema + queries)
