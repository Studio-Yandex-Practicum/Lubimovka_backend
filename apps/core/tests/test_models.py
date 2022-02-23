import pytest

from apps.core.models import Setting

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def different_types_setting():
    Setting.objects.create(
        field_type="IMAGE",
        group="GENERAL",
        settings_key="test_image_setting",
        image="test/path/to/image",
        description="Тестовая настройка типа image",
    )
    Setting.objects.create(
        field_type="BOOLEAN",
        group="GENERAL",
        settings_key="test_boolean_setting",
        boolean=True,
        description="Тестовая настройка типа boolean",
    )
    Setting.objects.create(
        field_type="TEXT",
        group="GENERAL",
        settings_key="test_text_setting",
        text="Текст настройки типа текст",
        description="Тестовая настройка типа text",
    )
    Setting.objects.create(
        field_type="URL",
        group="GENERAL",
        settings_key="test_url_setting",
        url="https://some_test_url.ru/test",
        description="Тестовая настройка типа url",
    )
    Setting.objects.create(
        field_type="EMAIL",
        group="GENERAL",
        settings_key="test_email_setting",
        email="nk@lubimovka.ru",
        description="Тестовая настройка типа email",
    )
    return (
        "test_image_setting",
        "test_boolean_setting",
        "test_boolean_setting",
        "test_text_setting",
        "test_url_setting",
        "test_email_setting",
    )


@pytest.mark.xfail(raises=AssertionError)
def test_setting_get_settings_dict_assert_when_incompatible_value_passed(different_types_setting):
    """Pass string to the method and check whether assertion error is raised."""
    Setting.get_settings_dict("test_image_setting")


@pytest.mark.xfail(raises=AssertionError)
def test_setting_get_settings_dict_assert_non_existed_setting_key():
    """Pass non existed setting key and check whether assertion error is raised."""
    settings_keys = ["some_non_existed_setting_key"]
    Setting.get_settings_dict(settings_keys)


def test_setting_get_settings_dict_return_expected_result(different_types_setting):
    """Evaluate `get_setting_dict` method and compare result with expected."""
    expected_result = {
        "test_image_setting": Setting.objects.get(settings_key="test_image_setting").image,
        "test_boolean_setting": Setting.objects.get(settings_key="test_boolean_setting").boolean,
        "test_text_setting": Setting.objects.get(settings_key="test_text_setting").text,
        "test_url_setting": Setting.objects.get(settings_key="test_url_setting").url,
        "test_email_setting": Setting.objects.get(settings_key="test_email_setting").email,
    }

    settings_dict_result = Setting.get_settings_dict(different_types_setting)
    assert settings_dict_result == expected_result
