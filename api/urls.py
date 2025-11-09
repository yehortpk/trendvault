from django.urls import path

from api.views import VideoDetailView

urlpatterns = [
    path('<str:id>/', VideoDetailView.as_view(), name='video-detail'),
]
