from django.urls import path
from . import views

app_name = "debug_page"
urlpatterns = [
    path("", views.show, name="show"),
]
