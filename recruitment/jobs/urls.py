from django.urls import re_path as url
from jobs import views

urlpatterns = [
    url(r"^joblist/", views.joblist, name="joblist")
]