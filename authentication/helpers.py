import requests
from django.core.exceptions import ObjectDoesNotExist
from authentication.models import Token


def check_linkedin_token():
    token_obj = None
    try:
        token_obj = Token.objects.get(type="Linkedin")
    except ObjectDoesNotExist:
        return False, "LinkedIn token not found."

    if token_obj:
        url = "https://api.linkedin.com/v2/userinfo"
        headers = {
            "Authorization": f"Bearer {token_obj.token}",
        }

        response = requests.get(url, headers=headers, verify=False)

        return 200 <= response.status_code < 300 and token_obj.token, response.text

    return False, "Invalid Linkdin Access Token"


def check_github_token():
    token_obj = None
    try:
        token_obj = Token.objects.get(type="Github")
    except ObjectDoesNotExist:
        return False, "Github token not found."

    if token_obj:
        url = "https://api.github.com/user"
        headers = {"Authorization": "token {}".format(token_obj.token)}

        response = requests.get(url, headers=headers, verify=False)

        return 200 <= response.status_code < 300 and token_obj.token, response.text

    return False, "Invalid Github Access Token"
