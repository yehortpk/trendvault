from django.db.models import Prefetch
from rest_framework.generics import RetrieveAPIView

from youtube.models import Region, Video, VideoStatsSnapshot
from youtube.serializers import RegionSerializer, VideoSerializer
from youtube.validators import validate_timestamp_range


class VideoDetailView(RetrieveAPIView):
    """
    API view to retrieve details of a specific video by its ID.
    """
    queryset = Video.objects.prefetch_related("stats_snapshots").all()
    serializer_class = VideoSerializer
    lookup_field = 'id'


class RegionDetailView(RetrieveAPIView):
    """
    API view to retrieve details of a specific region trending videos by its code, and time range.
    """
    serializer_class = RegionSerializer
    lookup_field = 'code'

    def get_queryset(self):
        code = self.kwargs.get("code")
        start_at = self.request.GET.get("start_at")
        finish_at = self.request.GET.get("finish_at")

        # Validate timestamp parameters
        start_datetime, finish_datetime = validate_timestamp_range(start_at, finish_at)

        return Region.objects.filter(code=code).prefetch_related(
            Prefetch(
                "stats_snapshots",
                queryset=self._filter_qs(code, start_datetime, finish_datetime)
            )
        )

    def _filter_qs(self, code, start_datetime=None, finish_datetime=None):
        base_qs = VideoStatsSnapshot.objects.filter(region__code=code)

        if start_datetime and finish_datetime:
            base_qs = base_qs.filter(
                timestamp__gte=start_datetime,
                timestamp__lte=finish_datetime
            )

        latest_timestamp = base_qs.order_by('-timestamp').values('timestamp').first()

        if not latest_timestamp:
            return VideoStatsSnapshot.objects.none()

        # Get all snapshots from the latest timestamp
        queryset = base_qs.filter(timestamp=latest_timestamp['timestamp'])

        return queryset
