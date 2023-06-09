# fastapi-okta
 
This is an example of FastAPI api endpoint protection using Okta. 

## Prerequisites

- Python 3.10
- Okta account

For local development the .env file is of the following structure is required in root directory:

```
OKTA_CLIENT_ID= __client_id__
OKTA_CLIENT_SECRET= __client_secret__
OKTA_API_AUDIENCE=  __audience__
OKTA_ISSUER= __issuer__
OKTA_DOMAIN= __domain__
```

To gather these Okta-related constants you need to have access to Okta account and to create a new API configuration. (Example: https://developer.okta.com/blog/2020/12/17/build-and-secure-an-api-in-python-with-fastapi#setting-up-a-new-application-in-okta)

This API exposes three endpoints:

|Path          |Endpoint description                                        |
|--------------|------------------------------------------------------------|
|- /           |:   GET/ Root unprotected                                   |
|- /token      |:  POST/ To authorize                                       |
|- /items      |: GET/ Protected endpoint that requires token authorization |

To run server:
```
uvicorn main:app --reload --port 8080
```