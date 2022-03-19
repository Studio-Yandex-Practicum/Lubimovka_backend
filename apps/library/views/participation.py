import logging

import yadisk
from drf_spectacular.utils import extend_schema
from googleapiclient.errors import HttpError
from rest_framework import mixins, viewsets

from apps.library.permissions import SettingsPlayReceptionPermission
from apps.library.schema.schema_extension import (
    ERROR_MESSAGES_FOR_PARTICIPATION_FOR_400,
    ERROR_MESSAGES_FOR_PARTICIPATION_FOR_403,
)
from apps.library.serializers.participation import ParticipationSerializer
from apps.library.services.spreadsheets import GoogleSpreadsheets
from apps.library.utilities import yandex_disk_export
from config.logging import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

gs = GoogleSpreadsheets()
y = yadisk.YaDisk(token="AQAAAAAoiXEIAAfBYfQtH0Dmg05Zpw0i8B-_1_Y")


@extend_schema(
    responses={
        201: ParticipationSerializer,
        400: ERROR_MESSAGES_FOR_PARTICIPATION_FOR_400,
        403: ERROR_MESSAGES_FOR_PARTICIPATION_FOR_403,
    }
)
class ParticipationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [SettingsPlayReceptionPermission]
    serializer_class = ParticipationSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        domain = self.request.build_absolute_uri()

        yandex_disk_export(y, instance)
        # cwd = str(os.getcwd())
        # name = str(instance.file).split("/")[-1]
        # name = name.replace("\\", '_').replace("/", '_')
        # try:
        #     y.mkdir(f"/{str(instance.year)}")
        # except yadisk.exceptions.PathExistsError:
        #     pass
        # to_dir = f"/{str(instance.year)}/{name}"
        # from_dir = cwd.replace("\\", '/') + "/media/" + str(instance.file)
        # try:
        #     y.upload(from_dir, to_dir)
        # except yadisk.exceptions.PathExistsError:
        #     pass
        # print(y.exists(f"/{str(instance.year)}"))
        # print(y.copy(f"/{str(instance.year)}"))

        try:
            export_success = gs.export(instance=instance, domain=domain)
            if export_success:
                instance.exported_to_google = True
                instance.save()
        except (ValueError, HttpError) as error:
            logger.critical(error, exc_info=True)
