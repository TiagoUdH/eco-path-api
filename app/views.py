from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import CustomUser
from .serializers import CustomUserSerializer

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

class PublicUserDetailView(APIView):
    def get(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            serializer = CustomUserSerializer(user)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response({"error": "Usuário não encontrado"}, status=404)

@csrf_exempt
@require_POST
def update_want_collect(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)  # Encontre o usuário pelo ID
        data = json.loads(request.body)
        
        # Verifique se 'want_collect' foi enviado na requisição
        if 'want_collect' in data:
            user.want_collect = data['want_collect']
            user.save()
            return JsonResponse({'success': True, 'want_collect': user.want_collect}, status=200)
        else:
            return JsonResponse({'error': 'Campo "want_collect" não fornecido'}, status=400)

    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'Usuário não encontrado'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Erro ao processar JSON'}, status=400)

