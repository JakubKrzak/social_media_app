
from fastapi import status, HTTPException
from jwt import decode
import pytest  
from app import schemas, oauth2
from app.models import User
from .database import client, session

@pytest.fixture
def test_user(client):
    user_data = {"email": "email@gmail.com",
                 "password": "password123"}
    
    res = client.post("/users/", json=user_data)
    new_user = res.json()
    new_user['password'] = user_data['password']
    print(new_user)
    return new_user

def test_login_user(client, test_user):
    user_data = {"username": test_user["email"],
                 "password": test_user['password']}
    
    res = client.post("/login", data=user_data)
    assert res.status_code == 200
    token = schemas.Token(**res.json())
    assert token.token_type == 'bearer'
    
    decoded_token = oauth2.decode_acces_token(token.access_token)
    print(decoded_token)
    assert decoded_token.email == test_user['email']
    assert decoded_token.id == test_user['id']



    

    
    







