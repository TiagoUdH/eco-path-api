from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import CustomUserSerializer

class PublicUserDetailView(APIView):
    def get(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            serializer = CustomUserSerializer(user)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response({"error": "Usuário não encontrado"}, status=404)
