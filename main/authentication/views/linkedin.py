import requests
import secrets
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import urlencode
from django.http import HttpResponseRedirect
from django.contrib import messages
from oauthlib.oauth2 import WebApplicationClient

from base.helpers import reverse_with_query
from authentication.models import Token
from .base import AuthView

"""
Linkedin App Profile :- https://www.linkedin.com/developers/apps/213597097/settings
"""


# Create your views here.
class LinkedinAuthView(AuthView):
    def get(self, request):
        authorization_url = "https://www.linkedin.com/oauth/v2/authorization"
        client_id = settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY
        client = WebApplicationClient(client_id)
        request.session["state"] = secrets.token_urlsafe(16)
        url = client.prepare_request_uri(
            authorization_url,
            redirect_uri=f"{settings.BASE_URL}/auth/linkedin/complete/",
            state=request.session["state"],
            scope=["email", "profile", "openid", "w_member_social"],
            # **{"response_type": "code"}
        )
        return HttpResponseRedirect(url)


class LinkedinCompleteView(AuthView):
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

        token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        client_id = settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY
        client_secret = settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET

        client = WebApplicationClient(client_id)
        params = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": f"{settings.BASE_URL}/auth/linkedin/complete/",
            "client_id": client_id,
            "client_secret": client_secret,
        }
        response = requests.post(token_url, data=params, verify=False)
        client.parse_request_body_response(response.text)
        if response.status_code == 200:
            access_token = client.token['access_token']
            print("Access token:", access_token)
        else :
            print("Error:", response.status_code, response.text)
            return redirect(reverse("authentication:all_auth_page", kwargs={}))

        # Create Token Entry in DB
        obj, created = Token.objects.update_or_create(
            type="Linkedin",
            # token=access_token,
            defaults={"token": access_token},
        )
        return HttpResponseRedirect(
            reverse_with_query(
                "authentication:all_auth_page",
                query_params={"check_linkedin_token": True, "token": access_token},
            )
        )
