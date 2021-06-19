from flask_pet_project import create_app

# (цю ф-цію можна видалити, бо вона тестує сам фласк)
def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
