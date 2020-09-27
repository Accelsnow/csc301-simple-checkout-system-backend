import pytest


@pytest.fixture()
def client():
    """
    Use Flask app
    """
    from app import app
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


@pytest.fixture()
def db_():
    """
    Use the flask database
    """
    from app import db

    db.create_all()

    yield db

    db.drop_all()
