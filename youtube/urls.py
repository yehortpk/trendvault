from django.urls import path

from youtube.views import VideoDetailView

urlpatterns = [
    path('video/<str:id>/', VideoDetailView.as_view(), name='video-detail'),
]
