from src.app import app
from dash import Dash

def test_app_instance():
    assert isinstance(app, Dash)
    assert app.title is not None
