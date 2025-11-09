from rest_framework.generics import RetrieveAPIView

from api.serializers import VideoSerializer
from youtube.models import Video


class VideoDetailView(RetrieveAPIView):
    """
    API view to retrieve details of a specific video by its ID.
    """
    queryset = Video.objects.prefetch_related("stats_snapshots").all()
    serializer_class = VideoSerializer
    lookup_field = 'id'
