import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.db.db import engine
from app.db.models import Base

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Tables created successfully.")
