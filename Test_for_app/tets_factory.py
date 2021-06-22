from ..flask_pet_project import create_app


# Testing correct work of the Flask
def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
