from datetime import datetime
from typing import Optional

from django.db.models import Prefetch
from rest_framework.generics import ListAPIView, RetrieveAPIView

from youtube.models import Region, VideoStatsSnapshot
from youtube.region.serializers import (RegionDetailSerializer,
                                        RegionListSerializer)


class RegionListView(ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionListSerializer


class RegionDetailView(RetrieveAPIView):
    """
    API view to retrieve details of a specific region trending videos by its code, and time range.
    """
    serializer_class = RegionDetailSerializer
    lookup_field = 'code'

    def get_queryset(self):
        code = self.kwargs.get("code")
        start_at = self.request.GET.get("start_at")
        finish_at = self.request.GET.get("finish_at")

        start_datetime, finish_datetime = None, None
        if start_at and finish_at:
            start_datetime = VideoStatsSnapshot.convert_pseudo_timestamp_to_timezone(start_at)
            finish_datetime = VideoStatsSnapshot.convert_pseudo_timestamp_to_timezone(finish_at)

        return Region.objects.filter(code=code).prefetch_related(
            Prefetch(
                "stats_snapshots",
                queryset=self._filter_qs(code, start_datetime, finish_datetime)
            )
        )

    def _filter_qs(self, code, start_datetime: Optional[datetime] = None,
                   finish_datetime: Optional[datetime] = None):
        base_qs = VideoStatsSnapshot.objects.filter(region__code=code)

        if start_datetime and finish_datetime:
            base_qs = base_qs.filter(
                timestamp__gte=start_datetime,
                timestamp__lte=finish_datetime
            )

        else:
            latest_timestamp = base_qs.order_by('-timestamp').values('timestamp').first()

            if not latest_timestamp:
                return VideoStatsSnapshot.objects.none()

            # Get all snapshots from the latest timestamp
            base_qs = base_qs.filter(timestamp=latest_timestamp['timestamp'])

        return base_qs
