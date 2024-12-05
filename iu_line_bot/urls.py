from django.urls import path
from . import views

app_name = "iu_line_bot"
urlpatterns = [
    path("", views.line_bot_receive, name="iu_line_bot"),
    path("ig_api_webhook", views.ig_api_webhook, name="ig_api_webhook"),
    path("privacy_policy", views.privacy_policy, name="privacy_policy"),
]
