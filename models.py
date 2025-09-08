from sqlalchemy import Column, Integer, String
from database import Base


class Apartments(Base):
    __tablename__ = "apartments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)   # e.g., building age in years
