from django.urls import path

from youtube.views import RegionDetailView, VideoDetailView

urlpatterns = [
    path("video/<str:id>/", VideoDetailView.as_view(), name="video-detail"),
    path("region/<str:code>", RegionDetailView.as_view(), name="region-detail")
]
