from django.conf import settings
from googleapiclient.discovery import build

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
KEY = settings.YOUTUBE_API_KEY


def get_video_links_from_youtube(count):

    api_key = KEY
    channel_id = "UCDZ1HTzBVBxm_vw6tV7C3lg"

    api_service_name = "youtube"
    api_version = "v3"
    youtube = build(api_service_name, api_version, developerKey=api_key)
    request = youtube.channels().list(part="contentDetails", id=channel_id)
    response = request.execute()
    playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=count,
    )
    response2 = request.execute()
    video_links = []
    base_video_url = "https://www.youtube.com/watch?v="

    for item in response2["items"]:
        video_links.append(base_video_url + item["snippet"]["resourceId"]["videoId"])

    return video_links
