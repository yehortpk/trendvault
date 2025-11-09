from django.urls import include, path

urlpatterns = [
    path("youtube/", include("youtube.urls")),
]
