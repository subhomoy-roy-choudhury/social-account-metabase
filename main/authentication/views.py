from django.shortcuts import render, redirect
import requests
from django.conf import settings
from authentication.models import Token

# Create your views here.

def dashboard(request):
    token_obj = Token.objects.get(type="Linkedin")
    check_linkedin_token = False
    if token_obj:
        url = "https://api.linkedin.com/v2/userinfo"
        payload = {}
        headers = {
            'Authorization': f'Bearer {token_obj.token}',
        }

        response = requests.request("GET", url, headers=headers, data=payload, verify=False)

        check_linkedin_token = True if response.status_code == 200 else False
            
    return render(request, "all_auth.html", {"check_linkedin_token": check_linkedin_token})

def auth(request, backend):
    linkedin_auth_url = f"https://www.linkedin.com/oauth/v2/authorization?client_id={settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY}&redirect_uri=http://localhost:8000/auth/complete/&state=2dPoUgtehfo74gT2Jrs5rgMSHal7DDex&response_type=code&scope=email+profile+openid+w_member_social"
    return redirect(linkedin_auth_url)

def complete(request):
    auth_code = request.GET.get("code")
    url = 'https://www.linkedin.com/oauth/v2/accessToken'
    params = {
        'grant_type': 'authorization_code',
        'code': auth_code,
            'redirect_uri': 'http://localhost:8000/auth/complete/',
            'client_id': settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY,
            'client_secret': settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET
        }
    response = requests.post(url, data=params, verify=False)

    if response.status_code == 200:
            access_token = response.json()['access_token']
            print('Access token:', access_token)
    else:
        print('Error:', response.status_code, response.text)
    # Create Token Entry in DB
    Token.objects.create(type="Linkedin", token=access_token)
    return render(request, "all_auth.html", {"token": access_token})
        