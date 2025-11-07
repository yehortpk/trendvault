import os

import googleapiclient.discovery

from celery import shared_task

from youtube.models import Region, Video


@shared_task
def fetch_trending_videos():
    api_service_name = "youtube"
    api_version = "v3"
    api_key = os.getenv("YOUTUBE_API_KEY")

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key
    )

    for region in Region.objects.all()[:5]:

        request = youtube.videos().list(
            part="snippet,statistics",
            chart="mostPopular",
            maxResults=50,
            regionCode=region.code,
        )
        response = request.execute()
        items = response.get("items", [])

        for video_data in items:
            Video.objects.update_or_create(
                id=video_data["id"],
                defaults={
                    "title": video_data["snippet"]["title"],
                    "published_at": video_data["snippet"]["publishedAt"],
                    "channel_id": video_data["snippet"]["channelId"],
                    "channel_title": video_data["snippet"]["channelTitle"],
                    "comments_count": int(video_data["statistics"].get("commentCount", 0)),
                    "views_count": int(video_data["statistics"].get("viewCount", 0)),
                    "likes_count": int(video_data["statistics"].get("likeCount", 0)),
                    "category_id": int(video_data["snippet"]["categoryId"]),
                    "region_id": region.code,
                }
            )
