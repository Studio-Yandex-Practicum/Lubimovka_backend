SUCCESS_MESSAGE_FOR_AFISHA_EVENTS_FOR_200_REGULAR = {
    "count": 123,
    "next": "http://api.example.org/accounts/?page=4",
    "previous": "http://api.example.org/accounts/?page=2",
    "title": "string",
    "description": "string",
    "results": [
        {
            "id": 0,
            "type": "PERFORMANCE",
            "event_body": "string",
            "date_time": "2022-01-15T22:33:39.049Z",
            "paid": True,
            "pinned_on_main": False,
            "url": "string",
            "place": "string",
        },
        {
            "id": 1,
            "type": "READING",
            "event_body": "string",
            "date_time": "2022-01-15T22:33:39.049Z",
            "paid": False,
            "pinned_on_main": True,
            "url": "string",
            "place": "string",
        },
        {
            "id": 0,
            "type": "MASTERCLASS",
            "event_body": "string",
            "date_time": "2022-01-15T22:33:39.049Z",
            "paid": True,
            "pinned_on_main": True,
            "url": "string",
            "place": "string",
        },
    ],
}

SUCCESS_MESSAGE_FOR_AFISHA_EVENTS_FOR_200_FESTIVAL = {
    "count": 123,
    "next": "http://api.example.org/accounts/?page=4",
    "previous": "http://api.example.org/accounts/?page=2",
    "title": "string",
    "description": "string",
    "info_registration": "string",
    "asterisk_text": "string",
    "results": [
        {
            "id": 0,
            "type": "PERFORMANCE",
            "event_body": "string",
            "date_time": "2022-01-15T22:33:39.049Z",
            "paid": True,
            "pinned_on_main": False,
            "url": "string",
            "place": "string",
        },
        {
            "id": 1,
            "type": "READING",
            "event_body": "string",
            "date_time": "2022-01-15T22:33:39.049Z",
            "paid": False,
            "pinned_on_main": True,
            "url": "string",
            "place": "string",
        },
        {
            "id": 0,
            "type": "MASTERCLASS",
            "event_body": "string",
            "date_time": "2022-01-15T22:33:39.049Z",
            "paid": True,
            "pinned_on_main": True,
            "url": "string",
            "place": "string",
        },
    ],
}


AFISHA_EVENTS_SCHEMA_DESCRIPTION = """
    If the site is in festival mode, blocks are added in response:

    "info_registration" - the text under the description of the poster about registration for the festival event,
    "asterisk_text" - the text under the asterisk near the title.

    Please select Festival setup or Regular setup in examples.
    """
