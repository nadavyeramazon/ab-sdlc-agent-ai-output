from app.routes.root import read_root

def test_read_root():
    response = read_root()
    assert response == {'Hello': 'World'}