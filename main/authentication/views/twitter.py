import requests
import secrets
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from oauthlib.oauth2 import WebApplicationClient

from base.helpers import reverse_with_query
from authentication.models import Token
from .base import AuthView

'''
Twiitter Develoepr Document :- https://developer.twitter.com/en/docs/authentication/oauth-2-0/user-access-token
'''


class TwitterAuthView(AuthView):
    def get(self, request):
        authorization_url = "https://twitter.com/i/oauth2/authorize"
        client_id = settings.TWITTER_CLIENT_ID
        client = WebApplicationClient(client_id)
        request.session["state"] = secrets.token_urlsafe(16)
        url = client.prepare_request_uri(
            authorization_url,
            redirect_uri=f"{settings.BASE_URL}/auth/twitter/complete/",
            state=request.session["state"],
            scope=["tweet.read", "users.read", "tweet.write", "offline.access"],
            **{"code_challenge": "challenge", "code_challenge_method": "plain"},
        )
        return HttpResponseRedirect(url)


class TwitterCompleteView(AuthView):
    def get(self, request):
        data = request.GET
        code = data["code"]
        state = data["state"]

        if state != self.request.session["state"]:
            messages.add_message(
                self.request, messages.ERROR, "State information mismatch!"
            )
            return HttpResponseRedirect(reverse("authorisation:dashboard"))
        else:
            del self.request.session["state"]

        token_url = "https://api.twitter.com/2/oauth2/token"
        client_id = settings.TWITTER_CLIENT_ID
        client_secret = settings.TWITTER_CLIENT_SECRET

        client = WebApplicationClient(client_id)
        params = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": f"{settings.BASE_URL}/auth/twitter/complete/",
            "client_id": client_id,
            "client_secret": client_secret,
            "code_verifier": "challenge",
        }
        response = requests.post(
            token_url,
            data=params,
            verify=False,
        )
        client.parse_request_body_response(response.text)
        if response.status_code == 200:
            access_token = client.token["access_token"]
            print("Access token:", access_token)
        else:
            print("Error:", response.status_code, response.text)
            return redirect(reverse("authentication:all_auth_page", kwargs={}))

        # Create Token Entry in DB
        obj, created = Token.objects.update_or_create(
            type="Twitter",
            defaults={"token": access_token},
        )
        return HttpResponseRedirect(
            reverse_with_query(
                "authentication:all_auth_page",
                query_params={"check_linkedin_token": True, "token": access_token},
            )
        )
