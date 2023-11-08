from django.urls import path
from authentication.views import linkedin, dashboard
from authentication.views.github import GithubAuthView, GithubAuthCompleteView
from authentication.views.linkedin import LinkedinAuthView, LinkedinCompleteView

app_name = "authentication"

urlpatterns = [
    # Linkedin
    path("linkedin/login/", LinkedinAuthView.as_view(), name="linkedin_begin"),
    path("linkedin/complete/", LinkedinCompleteView.as_view(), name="linkedin_complete"),

    # Github
    path("github/login/", GithubAuthView.as_view(), name="github_begin"),
    path("github/complete/", GithubAuthCompleteView.as_view(), name="github_complete"),

    # Dashboard
    path("all/", dashboard, name="all_auth_page"),
]