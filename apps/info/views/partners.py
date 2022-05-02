from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.fields import CharacterSeparatedSerializerField
from apps.info import selectors
from apps.info.models import Partner


class PartnerListAPIView(APIView):
    class PartnerListFilterSerializer(serializers.Serializer):
        in_footer_partner = serializers.BooleanField(
            required=False,
            help_text="Партнер отображается в футере",
        )
        types = CharacterSeparatedSerializerField(
            child=serializers.ChoiceField(choices=Partner.PartnerType.choices),
            required=False,
            help_text="Тип партнера. Можно указать несколько значений разделенных запятой",
        )

    class PartnerListOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Partner
            fields = (
                "id",
                "name",
                "type",
                "url",
                "image",
                "in_footer_partner",
            )

    @extend_schema(
        parameters=[PartnerListFilterSerializer],
        responses=PartnerListOutputSerializer(many=True),
    )
    def get(self, request):
        filter_serializer = self.PartnerListFilterSerializer(data=request.query_params, partial=True)
        filter_serializer.is_valid(raise_exception=True)
        response_data = selectors.partner_list(filters=filter_serializer.data)
        context = {"request": request}
        serializer = self.PartnerListOutputSerializer(response_data, context=context, many=True)
        return Response(serializer.data)
