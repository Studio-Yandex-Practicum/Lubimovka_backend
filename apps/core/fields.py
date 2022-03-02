from rest_framework import serializers


class CharacterSeparatedSerializerField(serializers.ListField):
    """Character separated ListField.

    A field that separates a string with a given separator into a native list
    and reverts a list into a string separated with a given separator.

    Parameters:
    1. `separator`: wait for separator character. The default `,`
    2. All other arguments that suitable for `serializers.ListField`
    """

    def __init__(self, *args, **kwargs):
        self.separator = kwargs.pop("separator", ",")
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        data = data.split(self.separator)
        return super().to_internal_value(data)

    def get_value(self, dictionary):
        """Return the value for this field that should be validated and transformed to a native value.

        The *incoming* primitive data is a string. `serializers.Field` method is suitable for it.
        """
        return serializers.Field.get_value(self, dictionary)

    def to_representation(self, data):
        data = super().to_representation(data)
        return self.separator.join(data)
