
from django.urls import path

from youtube.region.views import RegionDetailView, RegionListView

urlpatterns = [
    path("", RegionListView.as_view(), name="region-list"),
    path("<str:code>", RegionDetailView.as_view(), name="region-detail")
]
