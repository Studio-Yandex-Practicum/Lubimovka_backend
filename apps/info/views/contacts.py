from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import Setting
from apps.info.serializers import ContactsSerializer


class ContactsAPIView(APIView):
    def get(self, request):
        """Get an email for questions and link for document.

        with a privacy policy on contacts page.
        """
        email = Setting.get_setting("email_send_to")
        link = Setting.get_setting("url_to_privacy_policy")
        data = {"email": email, "link": link}
        serializer = ContactsSerializer(data)
        return Response(serializer.data)
