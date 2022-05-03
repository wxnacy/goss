
from wush.web.response import ResponseHandler, ResponseClient
from wush.config.function import load_super_function
from goss.config import (
    save_github_access_token
)
from ..constants import (
    MODULE_WWW,
    REQUEST_OAUTH_ACCESS_TOKEN
)

super_function = load_super_function()

@ResponseHandler.register(MODULE_WWW, REQUEST_OAUTH_ACCESS_TOKEN)
def hr_oauth_access_token(response: ResponseClient):
    try:
        data = response.json()
        client_id = response.request_builder.params.get("client_id")
        access_token = data.get("access_token")
        save_github_access_token(client_id, access_token)
    except:
        import traceback
        traceback.print_exc()
        traceback.print_stack()

    super_function.handler_response(response)
