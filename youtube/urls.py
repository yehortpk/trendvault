from django.urls import include, path

urlpatterns = [
    path("video/", include("youtube.video.urls")),
    path("region/", include("youtube.region.urls")),
]
