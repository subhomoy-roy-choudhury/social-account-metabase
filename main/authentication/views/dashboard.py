from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
import requests
from django.conf import settings
from authentication.models import Token
from urllib.parse import urlencode

from authentication.models import AuthServiceConfiguration


def reverse_with_query(viewname, query_params=None, **kwargs):
    url = reverse(viewname, **kwargs)
    if query_params:
        url = f"{url}?{urlencode(query_params)}"
    return url

def dashboard(request):
    check_linkedin_token = False
    token_obj = None 
    try :
        token_obj = Token.objects.get(type="Linkedin")
    except Exception as e:
        print(e)
    if token_obj:
        url = "https://api.linkedin.com/v2/userinfo"
        payload = {}
        headers = {
            'Authorization': f'Bearer {token_obj.token}',
        }

        response = requests.request("GET", url, headers=headers, data=payload, verify=False)

        check_linkedin_token = True if response.status_code == 200 else False
            
    return render(request, "all_auth.html", {"check_linkedin_token": check_linkedin_token})

class Dashboard(View):
    def get(self, request):
        service_list = AuthServiceConfiguration.objects.values("name", "id")
        return render(request, "all_auth_v1.html", {"service_list": service_list})

class AuthConfigurationView(View):
    def get(self, request):
        pass
    
    def update(self, request):
        pass