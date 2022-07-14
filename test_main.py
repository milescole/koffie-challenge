from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_lookup_success():
    response = client.post(
        "/lookup/", 
        json={"vin": "1XPWD40X1ED215307"}
        )
    assert response.status_code == 200
    assert response.json() == {
        "vin": "1XPWD40X1ED215307",
        "make": "PETERBILT",
        "model": "388",
        "model_year": "2014",
        "body_class": "Truck-Tractor",
        "cached": True
        }
   
    
def test_lookup_validation_length():
    response = client.post(
        "/lookup/", 
        json={"vin": "1XPWD40X1ED21530"}
        )
    assert response.status_code == 422
    assert response.json() == {
        "message": [
            "vin: Invalid VIN: Must be exactly 17 characters"
        ],
        "data": None
        }
   
    
def test_lookup_validation_alphanumeric():
    response = client.post(
        "/lookup/", 
        json={"vin": "1XPWD40X1ED21530!"}
        )
    assert response.status_code == 422
    assert response.json() == {
        "message": [
            "vin: Invalid VIN: Must contain all alphanumeric characters"
        ],
        "data": None
        }
 
    
def test_delete_success():
    response = client.delete(
        "/remove/", 
        json={"vin": "1XPWD40X1ED215307"}
        )
    assert response.status_code == 200
    assert response.json() == {
        "vin": "1XPWD40X1ED215307",
        "deleted": True
        }
    
    
def test_delete_error():
    response = client.delete(
        "/remove/", 
        json={"vin": "1XPWD40X3ED215307"}
        )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "VIN 1XPWD40X3ED215307 does not exist"
        }