from django.shortcuts import render
import requests
from authentication.models import Token

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