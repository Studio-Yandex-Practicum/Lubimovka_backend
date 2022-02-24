import pytest

from apps.core.models import Setting

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def different_types_setting():
    test_image_setting = Setting.objects.create(
        field_type="IMAGE",
        group="GENERAL",
        settings_key="test_image_setting",
        image="test/path/to/image",
        description="Тестовая настройка типа image",
    )
    test_boolean_setting = Setting.objects.create(
        field_type="BOOLEAN",
        group="GENERAL",
        settings_key="test_boolean_setting",
        boolean=True,
        description="Тестовая настройка типа boolean",
    )
    test_text_setting = Setting.objects.create(
        field_type="TEXT",
        group="GENERAL",
        settings_key="test_text_setting",
        text="Текст настройки типа текст",
        description="Тестовая настройка типа text",
    )
    test_url_setting = Setting.objects.create(
        field_type="URL",
        group="GENERAL",
        settings_key="test_url_setting",
        url="https://some_test_url.ru/test",
        description="Тестовая настройка типа url",
    )
    test_email_setting = Setting.objects.create(
        field_type="EMAIL",
        group="GENERAL",
        settings_key="test_email_setting",
        email="nk@lubimovka.ru",
        description="Тестовая настройка типа email",
    )
    return (
        test_image_setting.settings_key,
        test_boolean_setting.settings_key,
        test_text_setting.settings_key,
        test_url_setting.settings_key,
        test_email_setting.settings_key,
    )


@pytest.mark.parametrize(
    "settings_key, settings_attribute",
    (
        ("test_image_setting", "image"),
        ("test_boolean_setting", "boolean"),
        ("test_text_setting", "text"),
        ("test_url_setting", "url"),
        ("test_email_setting", "email"),
    ),
)
def test_setting_classmethod_get_setting_existed_key(settings_key, settings_attribute, different_types_setting):
    """Check that `get_setting` classmethod returns the expected result."""
    setting = Setting.objects.get(settings_key=settings_key)
    expected_result = getattr(setting, settings_attribute)

    get_setting_result = Setting.get_setting(settings_key)

    assert get_setting_result == expected_result, "Метод вернул неожидаемое значение"


@pytest.mark.xfail(raises=AssertionError)
def test_setting_classmethod_get_setting_assert_non_existed_key(different_types_setting):
    """Check that `get_setting` classmethod asserts if non existed settings_key passed."""
    non_existed_key = "some_non_existed_setting_key"
    Setting.get_setting(non_existed_key)


@pytest.mark.xfail(raises=AssertionError)
def test_setting_get_settings_assert_when_incompatible_value_passed(different_types_setting):
    """Pass string to the method and check whether assertion error is raised."""
    Setting.get_settings("test_image_setting")


@pytest.mark.xfail(raises=AssertionError)
def test_setting_get_settings_assert_when_empty_value_passed(different_types_setting):
    """Pass empty tuple or list to `get_settings` classmethod and check whether assertion error is raised."""
    Setting.get_settings(tuple())
    Setting.get_settings(list())


@pytest.mark.xfail(raises=AssertionError)
def test_setting_classmethod_get_settings_assert_non_existed_setting_key():
    """Pass non existed setting key and check whether assertion error is raised."""
    non_existed_key = ["some_non_existed_setting_key"]
    Setting.get_settings(non_existed_key)


def test_setting_classmethod_get_settings_return_expected_result(different_types_setting):
    """Evaluate `get_settings` (plural ;) ) method and compare result with expected."""
    expected_result = {
        "test_image_setting": Setting.get_setting("test_image_setting"),
        "test_boolean_setting": Setting.get_setting("test_boolean_setting"),
        "test_text_setting": Setting.get_setting("test_text_setting"),
        "test_url_setting": Setting.get_setting("test_url_setting"),
        "test_email_setting": Setting.get_setting("test_email_setting"),
    }

    settings_dict_result = Setting.get_settings(different_types_setting)
    assert settings_dict_result == expected_result
