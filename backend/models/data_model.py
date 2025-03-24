from sqlalchemy import Column, Integer, String
from .database import Base

class DataModel(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True, index=True)
    field1 = Column(String, index=True)
    field2 = Column(String, index=True)
    # Add other fields as necessary