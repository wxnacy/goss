
from wush.web.response import ResponseHandler
from ..constants import (
    MODULE_WWW,
    REQUEST_OAUTH_ACCESS_TOKEN
)

@ResponseHandler.register(MODULE_WWW, REQUEST_OAUTH_ACCESS_TOKEN)
def hr_oauth_access_token(response):
    pass
