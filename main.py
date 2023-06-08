from fastapi import FastAPI, Depends, Request
from starlette.config import Config

from core.schemas.items import Item
from core.handlers.token_handler import validate_token
from apis.v1.retrieve_token import retrieve_token

from typing import List


config = Config('.env')

app = FastAPI()

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