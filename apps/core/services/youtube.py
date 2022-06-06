import json
import urllib

from django.conf import settings


def get_video_in_channel():
    api_key = settings.YOUTUBE_API_KEY

    channel_id = "UCDZ1HTzBVBxm_vw6tV7C3lg"

    base_video_url = "https://www.youtube.com/watch?v="
    base_search_url = "https://www.googleapis.com/youtube/v3/search?"

    url = base_search_url + "key={}&channelId={}&part=snippet,id&order=date&maxResults=30".format(api_key, channel_id)
    video_links = []

    input = urllib.request.urlopen(url)
    response = json.load(input)

    for i in response["items"]:
        if i["id"]["kind"] == "youtube#video":
            video_links.append(base_video_url + i["id"]["videoId"])

    return video_links
