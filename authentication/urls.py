from django.urls import path
from .views import dashboard, auth, complete

app_name = "authentication"

urlpatterns = [
    path("login/<str:backend>/", auth, name="begin"),
    path("complete/", complete, name="complete"),
    path("all/", dashboard, name="all_auth_page"),
]