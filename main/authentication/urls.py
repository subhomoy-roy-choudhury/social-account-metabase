from django.urls import path
from authentication.views.dashboard import Dashboard, dashboard
from authentication.views.github import GithubAuthView, GithubAuthCompleteView
from authentication.views.linkedin import LinkedinAuthView, LinkedinCompleteView
from authentication.views.google import GoogleAuthView, GoogleAuthCompleteView

app_name = "authentication"

urlpatterns = [
    # Linkedin
    path("linkedin/login/", LinkedinAuthView.as_view(), name="linkedin_begin"),
    path(
        "linkedin/complete/", LinkedinCompleteView.as_view(), name="linkedin_complete"
    ),
    # Github
    path("github/login/", GithubAuthView.as_view(), name="github_begin"),
    path("github/complete/", GithubAuthCompleteView.as_view(), name="github_complete"),
    # Google
    path("google/login/", GoogleAuthView.as_view(), name="google_begin"),
    path("google/complete/", GoogleAuthCompleteView.as_view(), name="google_complete"),
    # Dashboard
    path("all/", dashboard, name="all_auth_page"),
]
