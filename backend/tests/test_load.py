import pytest
from unittest.mock import patch
from load.postgres_loader import bulk_insert_data
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.database import Base, DataModel

DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope='module')
def db_engine():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture(scope='module')
def db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.close()

@patch('load.postgres_loader.SessionLocal')
def test_bulk_insert_data(mock_session_local, db_session):
    sample_data = [
        {'field1': 'value1', 'field2': 1.23, 'field3': '2025-03-24 13:38:16'},
        {'field1': 'value2', 'field2': 4.56, 'field3': '2025-03-24 13:38:17'}
    ]

    mock_session_local.return_value = db_session
    bulk_insert_data(sample_data)

    results = db_session.query(DataModel).all()
    assert len(results) == len(sample_data)