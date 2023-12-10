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


def check_google_token():
    token_obj = None
    try:
        token_obj = Token.objects.get(type="Google")
    except ObjectDoesNotExist:
        return False, "Google token not found."

    # Google's token info endpoint
    token_info_url = "https://www.googleapis.com/oauth2/v1/tokeninfo"

    # Send a GET request with the access token
    response = requests.get(token_info_url, params={"access_token": token_obj.token})

    # Parse the response
    if response.status_code == 200:
        token_info = response.json()
        if "expires_in" in token_info:
            return (
                token_obj.token,
                f"Token is valid. Expires in {token_info['expires_in']} seconds.",
            )
        else:
            return False, "Token information could not be retrieved."
    else:
        print("Token is invalid or expired.")

def check_twitter_token():
    token_obj = None
    try:
        token_obj = Token.objects.get(type="Twitter")
    except ObjectDoesNotExist:
        return False, "Twitter token not found."

    if token_obj:
        url = "https://api.twitter.com/2/users/me"
        headers = {"Authorization": "Bearer {}".format(token_obj.token)}

        response = requests.get(url, headers=headers, verify=False)

        return 200 <= response.status_code < 300 and token_obj.token, response.text

    return False, "Invalid Twitter Access Token"
