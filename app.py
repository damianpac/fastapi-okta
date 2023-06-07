from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from starlette.config import Config
import httpx


config = Config('.env')

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def retrieve_token(authorization, issuer, scope='items'):
    headers = {
        'accept': 'application/json',
        'authorization': authorization,
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'scope': scope
    }
    url = issuer + '/v1/token'

    response = httpx.post(url, headers=headers, data=data)

    if response.status_code == httpx.codes.OK:
        return response.json()
    else:
        raise HTTPException(status_code=400, detail=response.text)

@app.get("/")
def read_root():
    return {"test endpoint response"}


def login(request: Request):
    return retrieve_token(
        request.headers['authorization'],
        config['OKTA_ISSUER'],
        'items'
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)