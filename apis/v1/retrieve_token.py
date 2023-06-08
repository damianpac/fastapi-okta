from fastapi import HTTPException
from starlette.config import Config
import httpx

config = Config('.env')

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
    url = issuer + 'oauth/token'

    response = httpx.post(url, headers=headers, data=data)

    if response.status_code == httpx.codes.OK:
        return response.json()
    else:
        raise HTTPException(status_code=400, detail=response.text)