from rest_framework import serializers

from youtube.models import Region, Video, VideoStatsSnapshot


class Region_VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            "id",
            "title",
            "published_at",
            "category",
            "channel_id",
            "channel_title",
            "thumb_url",
        ]


class Region_StatsSnapshotSerializer(serializers.ModelSerializer):
    video = Region_VideoSerializer(read_only=True)

    class Meta:
        model = VideoStatsSnapshot
        fields = [
            "video",
            "comments_count",
            "views_count",
            "likes_count",
        ]


class RegionDetailSerializer(serializers.ModelSerializer):
    stats_snapshots = Region_StatsSnapshotSerializer(many=True)
    stats_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Region
        fields = [
            "code",
            "title",
            "thumb_path",
            "stats_snapshots",
            "stats_count"
        ]

    def get_stats_count(self, obj) -> int:
        return obj.stats_snapshots.count()


class RegionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = [
            "code",
            "title",
            "thumb_path",
        ]
