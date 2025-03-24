import logging
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
from utils.config import DATABASE_URL

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define database models
Base = declarative_base()

class DataModel(Base):
    __tablename__ = 'data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    field1 = Column(String, index=True)
    field2 = Column(Float, index=True)
    field3 = Column(DateTime, index=True)
    # Add other fields as necessary

# Create database engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def bulk_insert_data(data):
    """
    Perform bulk insert of data into the database.

    :param data: List of dictionaries containing the data to be inserted.
    """
    session = SessionLocal()
    try:
        session.bulk_insert_mappings(DataModel, data)
        session.commit()
        logger.info(f"Successfully inserted {len(data)} records into the database.")
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to insert data: {e}")
    finally:
        session.close()

# Example usage
if __name__ == "__main__":
    init_db()

    # Sample data
    data = [
        {'field1': 'value1', 'field2': 1.23, 'field3': '2025-03-24 13:38:16'},
        {'field1': 'value2', 'field2': 4.56, 'field3': '2025-03-24 13:38:17'},
        # Add more records as needed
    ]

    # Perform bulk insert
    bulk_insert_data(data)