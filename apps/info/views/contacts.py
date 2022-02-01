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
        privacy_policy_link = Setting.get_setting("url_to_privacy_policy")
        data = {"email": email, "privacy_policy_link": privacy_policy_link}
        serializer = ContactsSerializer(data)
        return Response(serializer.data)
