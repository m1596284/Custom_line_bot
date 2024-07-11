from django.urls import path
from . import views

app_name = "iu_line_bot"
urlpatterns = [
    path("", views.line_bot_receive, name="iu_line_bot"),
]
