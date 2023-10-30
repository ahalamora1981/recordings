from django.urls import path
from . import views


app_name = "search_playback"

urlpatterns = [
    path("", views.search_view, name="search"),
    path("import/", views.import_view, name="import"),
]