# **TrendVault**

**TrendVault** is a modular Django-based analytics platform designed to collect, store, and analyze trending content statistics from external platforms.
Currently, it focuses on **YouTube trending videos**.

## **Project Overview**

TrendVault is a project structured around independent apps, beginning with the `youtube` app.
The system periodically collects and stores trending video data across multiple regions and categories using the **YouTube Data API v3**.

It provides:

* Persistent database models for **regions**, **categories**, **videos**, and **video statistics snapshots**.
* Scheduled Celery tasks that periodically fetch updated metrics (views, likes, comments).
* API endpoints (via Django REST Framework) for accessing and aggregating this data.
* Extensible modular design to integrate additional trend sources in the future.


## **Core Components**

### **1. Django Application**

* Currently one app: `youtube/`

  * **Models:**

    * `Region`: stores country metadata (code, title, flag path).
    * `Category`: stores video categories fetched from YouTube.
    * `Video`: represents a YouTube video with relevant metadata.
    * `VideoStatsSnapshot`: time-series model storing hourly snapshots of each video’s statistics.
  * Migrations include automatic population of **regions** and **categories** from YouTube API endpoints.

### **2. Celery Integration**

* Celery is configured in `celery.py`, auto-discovering tasks from installed apps.
* Used for **scheduled hourly jobs** fetching updated statistics.
* Supports both:

  * Automated cron-like execution.
  * Manual task triggering for ad-hoc data refreshes.
* Tasks log activity through the Celery worker process.


### **3. YouTube API Integration**

* Uses `googleapiclient.discovery.build` with API key authentication.
* Fetches:

  * **Regions**: via `youtube.i18nRegions().list(part="snippet")`.
  * **Categories**: via `youtube.videoCategories().list(part="snippet")`.
  * **Trending videos**: via `youtube.videos().list(chart="mostPopular", part="statistics", regionCode=...)`.
* Each request’s results are persisted via Django ORM.
* Country flags are downloaded once and stored in `static/regions/flags/`.


### **4. Database**
* Indexed fields:

  * `Region.code`
  * `VideoStatsSnapshot.video`
  * `VideoStatsSnapshot.timestamp`
* Estimated data footprint: ~6–7 GB/year for 5,400 tracked videos with hourly snapshots (Youtube App).


## **Local Setup**

### **1. Set environment Variables**
*Can be set in .env file at the same level as docker compose.yml, or you can specify the location in the command below

| Variable                 | Description                                       |
| ------------------------ | ------------------------------------------------- |
| `YOUTUBE_API_KEY`        | Your YouTube Data API v3 key                      |
| `CELERY_BROKER_URL`      | Celery Message broker (e.g., `redis://localhost:6379`) |
| `SECRET_KEY`             | Django secret key                                 |
| `DB_USER`                | Database username                                 |
| `DB_PASSWORD`            | Database password                                 |
| `DB_NAME`                | Database name                                     |

### **2. Run docker compose**
```bash
docker-compose [--env-file location] up
```
## **License**

This project is open for educational and research purposes.
All data is retrieved via the **YouTube Data API**, and usage is subject to [YouTube’s Terms of Service](https://developers.google.com/youtube/terms/api-services-terms-of-service).
