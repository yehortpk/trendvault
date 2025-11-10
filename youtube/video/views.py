from rest_framework.generics import RetrieveAPIView

from youtube.models import Video
from youtube.video.serializers import VideoDetailSerializer


class VideoDetailView(RetrieveAPIView):
    """
    API view to retrieve details of a specific video by its ID.
    """
    queryset = Video.objects.prefetch_related("stats_snapshots").all()
    serializer_class = VideoDetailSerializer
    lookup_field = 'id'
