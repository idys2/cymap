from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer
from config import settings

# configure azure scheme
azure_scheme = SingleTenantAzureAuthorizationCodeBearer(
    app_client_id=settings.APP_CLIENT_ID,
    tenant_id=settings.TENANT_ID,
    scopes=settings.SCOPES,
    allow_guest_users=True
)
