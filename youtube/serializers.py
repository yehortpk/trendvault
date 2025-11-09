from rest_framework import serializers

from youtube.models import Region, Video, VideoStatsSnapshot


class VideoSnapshotStatSerializer(serializers.ModelSerializer):
    regions = serializers.SerializerMethodField()

    class Meta:
        model = VideoStatsSnapshot
        fields = [
            "timestamp",
            "comments_count",
            "views_count",
            "likes_count",
            "regions"
        ]

    def get_regions(self, obj):
        # Get all snapshots for this video at the same timestamp
        snapshots = VideoStatsSnapshot.objects.filter(
            video=obj.video,
            timestamp=obj.timestamp
        ).values_list('region__code', flat=True)
        return list(snapshots)


class VideoSerializer(serializers.ModelSerializer):
    stats_snapshots = serializers.SerializerMethodField()

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
            "stats_snapshots",
        ]

    def get_stats_snapshots(self, obj):
        # Get one snapshot per timestamp
        distinct_timestamps = obj.stats_snapshots.order_by('timestamp').distinct('timestamp')
        return VideoSnapshotStatSerializer(distinct_timestamps, many=True).data


class SimpleVideoSerializer(serializers.ModelSerializer):
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


class RegionVideoSnapshotStatSerializer(serializers.ModelSerializer):
    video = SimpleVideoSerializer(read_only=True)

    class Meta:
        model = VideoStatsSnapshot
        fields = [
            "video",
            "comments_count",
            "views_count",
            "likes_count",
        ]


class RegionSerializer(serializers.ModelSerializer):
    stats_snapshots = RegionVideoSnapshotStatSerializer(many=True)

    class Meta:
        model = Region
        fields = [
            "code",
            "title",
            "thumb_path",
            "stats_snapshots"
        ]
