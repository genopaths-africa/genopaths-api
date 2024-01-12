import pytest
from genopaths import app as genopaths_app
#from genopaths import create_app

@pytest.fixture
def app():
#    app = create_app()

    yield genopaths_app

@pytest.fixture
def client(app):
    return app.test_client()