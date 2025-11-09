from django.core.files.storage import FileSystemStorage
from django.db import models

from trendvault import settings


static_storage = FileSystemStorage(location=str(settings.STATIC_BASE_DIR))


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
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)

    channel_id = models.CharField(max_length=50)
    channel_title = models.CharField(max_length=200)
    thumb_url = models.URLField()

    def __str__(self):
        return self.title


class VideoStatsSnapshot(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, db_index=True)
    timestamp = models.DateTimeField(db_index=True)
    comments_count = models.IntegerField()
    views_count = models.IntegerField()
    likes_count = models.IntegerField()

    class Meta:
        ordering = ["-timestamp"]
        # Separate index for video and timestamp for faster statistics range queries
        indexes = [
            models.Index(fields=["video", "timestamp"]),
        ]

    def __str__(self):
        return f"Stats for {self.video.title} at {self.timestamp}"
