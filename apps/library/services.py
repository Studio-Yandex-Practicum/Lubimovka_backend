from pathlib import Path

from django.conf import settings


def _hidden_path(play) -> Path:
    """Вычисление пути к скрытому хранилищу."""
    return settings.HIDDEN_MEDIA_ROOT / Path(play.url_download.path).relative_to(settings.MEDIA_ROOT)


def restore_play_file(play):
    """Вернуть файл из скрытого хранилища в общее."""
    if not play.url_download:
        return
    regular_play_file = Path(play.url_download.path)
    hidden_play_file = _hidden_path(play)
    if hidden_play_file.is_file():
        hidden_play_file.replace(regular_play_file)


def hide_play_file(play):
    """Переместить файл из общего хранилища в скрытое."""
    if not play.url_download:
        return
    regular_play_file = Path(play.url_download.path)
    hidden_play_file = _hidden_path(play)
    if regular_play_file.is_file():
        regular_play_file.replace(hidden_play_file)
