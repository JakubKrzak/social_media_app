from fastapi import status, HTTPException
from fastapi.exceptions import PydanticV1NotSupportedError
from jwt import decode
import pytest  
from app import schemas, oauth2
from app.models import User

def test_login_user(client, test_user):
    response = client.post("/login/", data={"username": test_user['email'],
                                            "password": test_user['password']})
    assert response.status_code == 200
    token = schemas.Token(**response.json())
    assert token.token_type == 'bearer'
    decoded_token = oauth2.decode_access_token(token.access_token)
    assert decoded_token.email == test_user['email']
    assert decoded_token.id == test_user['id']

def test_incorrect_login(client, test_user):
    user_data = {"username": test_user['email'],
                 "password": "password_incorrect"}
    response = client.post("/login/", data=user_data)
    assert response.status_code == 403
    

    
    







