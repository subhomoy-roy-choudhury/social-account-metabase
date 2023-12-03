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
Google App Profile :- https://console.cloud.google.com/apis/credentials/oauthclient/898872788471-4knogen7v940oh8t6346smbc127lhdqb.apps.googleusercontent.com?project=social-media-metabase
Scopes:- https://developers.google.com/identity/protocols/oauth2/scopes
Reference :- https://www.oauth.com/oauth2-servers/signing-in-with-google/
"""

GOOGLE_ID_AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_ID_ACCESS_TOKEN_URL = "https://www.googleapis.com/oauth2/v4/token"


# Create your views here.
class GoogleAuthView(AuthView):
    def get(self, request):
        client_id = settings.GOOGLE_CLIENT_ID
        client = WebApplicationClient(client_id)
        request.session["state"] = secrets.token_urlsafe(16)
        url = client.prepare_request_uri(
            GOOGLE_ID_AUTHORIZATION_URL,
            redirect_uri=f"{settings.BASE_URL}/auth/google/complete/",
            state=request.session["state"],
            allow_signup="false",
            scope=[
                "openid",
                "email",
                "profile",
                "https://www.googleapis.com/auth/blogger",
                "https://www.googleapis.com/auth/drive.metadata.readonly",
            ],
        )
        return HttpResponseRedirect(url)


class GoogleAuthCompleteView(AuthView):
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

        client_id = settings.GOOGLE_CLIENT_ID
        client_secret = settings.GOOGLE_CLIENT_SECRET

        client = WebApplicationClient(client_id)
        params = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": f"{settings.BASE_URL}/auth/google/complete/",
            "client_id": client_id,
            "client_secret": client_secret,
        }
        response = requests.post(GOOGLE_ID_ACCESS_TOKEN_URL, data=params, verify=False)
        client.parse_request_body_response(response.text)
        if response.status_code == 200:
            access_token = client.token["access_token"]
            print("Access token:", access_token)
        else:
            print("Error:", response.status_code, response.text)
            return redirect(reverse("authentication:all_auth_page", kwargs={}))

        # Create Token Entry in DB
        obj, created = Token.objects.update_or_create(
            type="Google",
            # token=access_token,
            defaults={"token": access_token},
        )
        return HttpResponseRedirect(
            reverse_with_query(
                "authentication:all_auth_page",
                query_params={"check_google_token": True, "google_token": access_token},
            )
        )
