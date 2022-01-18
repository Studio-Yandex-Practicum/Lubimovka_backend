MAIN_SCHEMA_DESCRIPTION = """
    If the site is in festival mode, blocks are added in response:

    Afisha blocks:
    "info_registration" - the text under the description of the poster about registration for the festival event,
    "asterisk_text" - the text under the asterisk near the title.

    Please select Festival setup or Regular setup in examples.
    """

MAIN_SCHEMA_SUCCESS_MESSAGE_FESTIVAL = {
    "first_screen": {"title": "string", "url_title": "string", "url": "string"},
    "blog": {
        "title": "string",
        "items": [
            {
                "id": 0,
                "pub_date": "2022-01-16T14:39:25.453Z",
                "title": "string",
                "description": "string",
                "author_url": "string",
                "author_url_title": "string",
                "image": "string",
            }
        ],
    },
    "news": {
        "title": "string",
        "items": [
            {
                "id": 0,
                "title": "string",
                "description": "string",
                "image": "string",
                "pub_date": "2022-01-16T14:39:25.453Z",
            }
        ],
    },
    "afisha": {
        "title": "string",
        "description": "string",
        "info_registration": "string",
        "asterisk_text": "string",
        "items": [
            {
                "id": 0,
                "type": "PERFORMANCE",
                "event_body": "string",
                "date_time": "2022-01-16T14:39:25.453Z",
                "paid": True,
                "url": "string",
                "place": "string",
            }
        ],
    },
    "banners": {
        "items": [
            {
                "id": 0,
                "title": "string",
                "description": "string",
                "url": "string",
                "image": "string",
                "button": "TICKETS",
            }
        ]
    },
    "short_list": {
        "title": "string",
        "items": [
            {
                "id": 0,
                "name": "string",
                "authors": [{"name": "string", "id": 0}],
                "city": "string",
                "year": 2022,
                "url_download": "string",
                "url_reading": "string",
            }
        ],
    },
    "places": {
        "items": [
            {
                "id": 0,
                "name": "string",
                "description": "string",
                "city": "string",
                "address": "string",
                "map_link": "string",
            }
        ]
    },
    "video_archive": {"url": "string", "photo": "string"},
}

MAIN_SCHEMA_SUCCESS_MESSAGE_REGULAR = {
    "first_screen": {"title": "string", "url_title": "string", "url": "string"},
    "blog": {
        "title": "string",
        "items": [
            {
                "id": 0,
                "pub_date": "2022-01-16T14:39:25.453Z",
                "title": "string",
                "description": "string",
                "author_url": "string",
                "author_url_title": "string",
                "image": "string",
            }
        ],
    },
    "news": {
        "title": "string",
        "items": [
            {
                "id": 0,
                "title": "string",
                "description": "string",
                "image": "string",
                "pub_date": "2022-01-16T14:39:25.453Z",
            }
        ],
    },
    "afisha": {
        "title": "string",
        "description": "string",
        "items": [
            {
                "id": 0,
                "type": "PERFORMANCE",
                "event_body": "string",
                "date_time": "2022-01-16T14:39:25.453Z",
                "paid": True,
                "url": "string",
                "place": "string",
            }
        ],
    },
    "banners": {
        "items": [
            {
                "id": 0,
                "title": "string",
                "description": "string",
                "url": "string",
                "image": "string",
                "button": "TICKETS",
            }
        ]
    },
    "short_list": {
        "title": "string",
        "items": [
            {
                "id": 0,
                "name": "string",
                "authors": [{"name": "string", "id": 0}],
                "city": "string",
                "year": 2022,
                "url_download": "string",
                "url_reading": "string",
            }
        ],
    },
    "places": {
        "items": [
            {
                "id": 0,
                "name": "string",
                "description": "string",
                "city": "string",
                "address": "string",
                "map_link": "string",
            }
        ]
    },
    "video_archive": {"url": "string", "photo": "string"},
}
