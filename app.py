from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from starlette.config import Config

from utils import VerifyToken

from pydantic import BaseModel
from typing import List

import httpx


config = Config('.env')

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def retrieve_token(authorization, issuer):
    headers = {
        'accept': 'application/json',
        'authorization': authorization,
        'content-type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': config.get('OKTA_CLIENT_ID'),
        'client_secret': config.get('OKTA_CLIENT_SECRET'),
        'audience': config.get('OKTA_API_AUDIENCE')
    }
    url = issuer + '/oauth/token'

    response = httpx.post(url, headers=headers, data=data)

    if response.status_code == httpx.codes.OK:
        return response.json()
    else:
        raise HTTPException(status_code=400, detail=response.text)

def validate_token(token: str = Depends(oauth2_scheme)):
    """
    If token correctly validated then verify() should return Issuer (iss).
    """
    if VerifyToken(token=token).verify()['iss']:
        return True
    else:
        return False

class Item(BaseModel):
    id: int
    name: str


@app.get("/")
def read_root():
    return {"test endpoint response"}

@app.post("/token")
def login(request: Request):
    return retrieve_token(
        request.headers['authorization'],
        config.get('OKTA_ISSUER')
    )

@app.get('/items', response_model=List[Item])
def read_items(valid: bool = Depends(validate_token)):
    return [
        Item.parse_obj({'id': 1, 'name': 'test_value_01'}),
        Item.parse_obj({'id': 2, 'name': 'test_value_02'}),
        Item.parse_obj({'id': 3, 'name': 'test_value_03'})

    ]

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)