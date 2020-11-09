from rest_framework.views import APIView
from rest_framework.reverse import reverse as api_reverse
from rest_framework.response import Response


class APIHomeView(APIView):
    def get(self, request):
        data = {
            "convert json to csv": {
                "convert_json_to_csv": api_reverse("converter:api_create", request=request),
            },
        }
        return Response(data)
