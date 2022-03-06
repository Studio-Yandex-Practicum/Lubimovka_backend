import datetime
import os

import git
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.info.serializers import VersionSerializer


class VersionAPIView(APIView):
    @extend_schema(request=None, responses=VersionSerializer)
    def get(self, request):
        """Get data containing tag, last_commit, commit_date, and environment."""
        repo = git.Repo(os.getcwd())
        master = repo.head.reference
        commit_date = datetime.datetime.fromtimestamp(master.commit.committed_date)
        last_tag = repo.tags[-1]
        tag = str(last_tag) if master.commit == last_tag.commit else None
        data = {
            "last_commit": str(master.commit)[:7],
            "commit_date": commit_date.strftime("%Y-%m-%d %H:%M:%S"),
            "tag": tag,
            "environment": str(master).split("/")[0],
        }
        serializer = VersionSerializer(data)
        return Response(serializer.data)
