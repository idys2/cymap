from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router
from api.auth import azure_scheme
from config import settings
from database.session import sessionmanager

@asynccontextmanager
async def lifespan(app: FastAPI):

    # load OpenID config on startup.
    await azure_scheme.openid_config.load_config()

    # create tables
    async with sessionmanager.connect() as conn:
        await sessionmanager.create_all(conn)

    yield

    # clean up database connection on shutdown
    if sessionmanager._engine is not None:
        async with sessionmanager.connect() as conn:
            await sessionmanager.drop_all(sessionmanager._engine)
        await sessionmanager.close()

app = FastAPI(
    lifespan=lifespan,
    title=settings.project_name,
    
    # configure OAuth2 settings
    swagger_ui_oauth2_redirect_url='/oauth2-redirect',
    swagger_ui_init_oauth={
        'usePkceWithAuthorizationCodeGrant': True,
        'clientId': settings.OPENAPI_CLIENT_ID,
        'scopes': settings.SCOPE_NAME,
    },
)

# check for CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


# test the auth
@app.get("/", dependencies=[Security(azure_scheme)])
async def test_authentication():
    return {"message": "You are authenticated"}


app.include_router(router, prefix='/api', tags=['metrics'])

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, host="0.0.0.0", port=8000)