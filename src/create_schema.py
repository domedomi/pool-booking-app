from src.db import get_engine
from src.models import Base
e = get_engine()
Base.metadata.create_all(e)
print("SCHEMA_OK")
