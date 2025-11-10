from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.db import models

from trendvault import settings


def static_storage():
    return FileSystemStorage(location=str(settings.STATIC_BASE_DIR))


class Region(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    title = models.CharField(max_length=100)
    thumb_path = models.ImageField(storage=static_storage, upload_to='regions/flags', null=True)

    def __str__(self):
        return f"{self.title} ({self.code})"


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Video(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=200)
    published_at = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    channel_id = models.CharField(max_length=50)
    channel_title = models.CharField(max_length=200)
    thumb_url = models.URLField()

    def __str__(self):
        return self.title


class VideoStatsSnapshot(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, db_index=True, related_name="stats_snapshots")
    timestamp = models.DateTimeField(db_index=True)
    comments_count = models.IntegerField()
    views_count = models.IntegerField()
    likes_count = models.IntegerField()
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, related_name="stats_snapshots")

    class Meta:
        ordering = ["-timestamp"]
        # Separate index for video and timestamp for faster statistics range queries
        indexes = [
            models.Index(fields=["video", "timestamp"]),
        ]

    def __str__(self):
        return f"Stats for {self.video.title} at {self.timestamp}"

    @staticmethod
    def convert_pseudo_timestamp_to_timezone(pseudo_timestamp: str) -> datetime:
        """
        Convert a pseudo timestamp string in format 'ddmmyy:hh' to a datetime object

        Args:
            pseudo_timestamp (str): Timestamp string in format 'ddmmyy:hh'
                                  Example: '091123:14' for Nov 9, 2023 14:00

        Returns:
            datetime.datetime: Converted timezone-aware datetime object

        Raises:
            ValueError: If the pseudo_timestamp format is invalid
        """
        try:
            date_part, hour = pseudo_timestamp.split(':')
            day = int(date_part[:2])
            month = int(date_part[2:4])
            year = int('20' + date_part[4:6])  # Assuming years 2000-2099
            hour = int(hour)

            # Create datetime with zeroed minutes/seconds
            result = datetime(
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=0,
                second=0,
                microsecond=0
            )

            return result

        except (ValueError, IndexError) as e:
            raise ValueError(
                f"Invalid timestamp format. Expected 'ddmmyy:hh', got '{pseudo_timestamp}'"
            ) from e
