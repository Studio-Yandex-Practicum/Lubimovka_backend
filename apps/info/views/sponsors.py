from rest_framework.viewsets import ReadOnlyModelViewSet

# from apps.info.models import FestivalTeam, Partner, Sponsor, Volunteer


class PartnersViewSet(ReadOnlyModelViewSet):
    # queryset = Partner.objects.all()
    # serializer_class = TagSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = None
