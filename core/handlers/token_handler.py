from core.handlers.verify_token import VerifyToken
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def validate_token(token: str = Depends(oauth2_scheme)):
    """
    If token correctly validated then verify() should return Issuer (iss).
    """
    if VerifyToken(token=token).verify()['iss']:
        return True
    else:
        return False