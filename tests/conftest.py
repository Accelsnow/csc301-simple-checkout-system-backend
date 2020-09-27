import pytest


@pytest.fixture(autouse=True)
def db_():
    """
    Use the flask database
    """
    from app import db

    db.create_all()

    yield db

    db.drop_all()
