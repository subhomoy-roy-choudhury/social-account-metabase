from django.http import HttpResponse
from django.views import View

class AuthView(View):
    def __init__(self):
        pass

    def get(self, request, *args, **kwargs):
        return HttpResponse("<h1>Auth View Not Implemented</h1>")
    
    def put(self, request, *args, **kwargs):
        return HttpResponse("<h1>Auth View Not Implemented</h1>")
    
    def post(self, request, *args, **kwargs):
        return HttpResponse("<h1>Auth View Not Implemented</h1>")
    
    def delete(self, request, *args, **kwargs):
        return HttpResponse("<h1>Auth View Not Implemented</h1>")
    
    def patch(self, request, *args, **kwargs):
        return HttpResponse("<h1>Auth View Not Implemented</h1>")
    
    def head(self, request, *args, **kwargs):
        return HttpResponse("<h1>Auth View Not Implemented</h1>")
    
    def options(self, request, *args, **kwargs):
        return HttpResponse("<h1>Auth View Not Implemented</h1>")
    
    def trace(self, request, *args, **kwargs):
        return HttpResponse("<h1>Auth View Not Implemented</h1>")
