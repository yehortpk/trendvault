
from django.urls import path

from youtube.video.views import VideoDetailView

urlpatterns = [
    path("<str:id>", VideoDetailView.as_view(), name="video-detail"),
]
