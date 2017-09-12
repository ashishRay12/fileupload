import json
from falcon.util.uri import parse_query_string
from falcon import HTTPBadRequest
from mongoengine import DoesNotExist
from ..models import AuthInfo


class AuthMiddleware(object):

    def process_resource(self, req, resp, resource, params):

        form = dict()
        if req.method == "GET":
            form = parse_query_string(req.query_string)
            params["form"] = form
        else:
            if 'json' in req.get_header('content-type', None):
                form = json.load(req.stream)
                params['form'] = dict(form)

    def process_request(self, req, resp):
        restricted_apis = ["/upload", "/query"]
        if req.path in restricted_apis:
            try:
                user_id = req.get_header("user_id", required=True)
                token = req.get_header("token", required=True)
                auth_data = AuthInfo.objects.get(user_id=user_id)
                if token != auth_data.token:
                    raise HTTPBadRequest
            except (HTTPBadRequest, DoesNotExist) as e:
                raise HTTPBadRequest(title="token", description="invalid token")
