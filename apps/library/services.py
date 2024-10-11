from pathlib import Path

from django.conf import settings


def _hidden_path(media_path: Path) -> Path:
    """Вычисление пути к скрытому хранилищу."""
    return settings.HIDDEN_MEDIA_ROOT / media_path.relative_to(settings.MEDIA_ROOT)


def restore_play_file(play):
    """Вернуть файл из скрытого хранилища в общее."""
    if not play or not play.url_download:
        return
    regular_play_file = Path(play.url_download.path)
    hidden_play_file = _hidden_path(regular_play_file)
    if hidden_play_file.is_file():
        hidden_play_file.replace(regular_play_file)


def hide_play_file(play):
    """Переместить файл из общего хранилища в скрытое."""
    if not play or not play.url_download:
        return
    regular_play_file = Path(play.url_download.path)
    hidden_play_file = _hidden_path(regular_play_file)
    if regular_play_file.is_file():
        regular_play_file.replace(hidden_play_file)
