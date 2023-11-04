
import requests
import secrets
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from oauthlib.oauth2 import WebApplicationClient

from base.helpers import reverse_with_query
from authentication.models import Token
from .base import AuthView

"""
Github App Profile :- https://github.com/settings/applications/2370090
Reference :- https://github.com/mchesler613/django_adventures/blob/main/oauth2_web_application_integration_with_github_and_oauthlib.md
"""


# Create your views here.
class GithubAuthView(AuthView):
    def get(self, request):
        authorization_url = "https://github.com/login/oauth/authorize"
        client_id = settings.GITHUB_CLIENT_ID
        client = WebApplicationClient(client_id)
        request.session["state"] = secrets.token_urlsafe(16)
        url = client.prepare_request_uri(
            authorization_url,
            redirect_uri=f"{settings.BASE_URL}/auth/github/complete/",
            state=request.session["state"],
            allow_signup="false",
        )
        return HttpResponseRedirect(url)


class GithubAuthCompleteView(AuthView):
    def get(self, request):
        data = request.GET
        code = data["code"]
        state = data["state"]

        if state != self.request.session["state"]:
            messages.add_message(
                self.request, messages.ERROR, "State information mismatch!"
            )
            return HttpResponseRedirect(reverse("github:welcome"))
        else:
            del self.request.session["state"]

        token_url = "https://github.com/login/oauth/access_token"
        client_id = settings.GITHUB_CLIENT_ID
        client_secret = settings.GITHUB_CLIENT_SECRET

        client = WebApplicationClient(client_id)
        data = client.prepare_request_body(
            code=code,
            redirect_uri=f"{settings.BASE_URL}/auth/github/complete/",
            client_id=client_id,
            client_secret=client_secret,
        )
        response = requests.post(token_url, data=data)
        client.parse_request_body_response(response.text)
        if response.status_code == 200:
            access_token = client.token['access_token']
            print("Access token:", access_token)
        else :
            print("Error:", response.status_code, response.text)
            return redirect(reverse("authentication:all_auth_page", kwargs={}))
        
        # Create Token Entry in DB
        obj, created = Token.objects.update_or_create(
            type="Github",
            # token=access_token,
            defaults={"token": access_token},
        )
        return HttpResponseRedirect(
            reverse_with_query(
                "authentication:all_auth_page",
                query_params={"check_github_token": True, "github_token": access_token},
            )
        )
        


