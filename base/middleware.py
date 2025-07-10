from django.utils.deprecation import MiddlewareMixin

class CustomCorsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"
        response["Access-Control-Allow-Headers"] = "Origin, Content-Type, Accept, Authorization"
        response["Access-Control-Allow-Credentials"] = "true"
        return response
