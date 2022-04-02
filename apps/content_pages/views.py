from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.urls import reverse
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

POPUP_SUFFIX = "?_popup=1"


@extend_schema(
    responses={
        200: {"example": {"url": "string"}},
    }
)
class GetContentTypeLink(APIView):
    """Return URL link to add or change based on `model_id` and `object_id`."""

    permission_classes = [IsAdminUser]

    class QueryParamsSerializer(serializers.Serializer):
        model_id = serializers.IntegerField()
        object_id = serializers.IntegerField(required=False)
        link_type = serializers.ChoiceField(choices=("add", "change"))

    def get(self, request):
        query_params_serializer = self.QueryParamsSerializer(data=request.query_params)
        query_params_serializer.is_valid(raise_exception=True)
        data = query_params_serializer.validated_data

        link_type = data.get("link_type")
        model_id = data.get("model_id")
        object_id = data.get("object_id")

        reverse_args = (object_id,) if link_type == "change" and object_id else None
        content_model = get_object_or_404(ContentType, id=model_id)

        url = reverse(f"admin:{content_model.app_label}_{content_model.model}_{link_type}", args=reverse_args)
        url += POPUP_SUFFIX
        data = {"url": url}
        return Response(data=data, status=status.HTTP_200_OK)
