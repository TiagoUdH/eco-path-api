from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import JsonResponse
from .models import CustomUser, CollectionRequest
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer, CollectionRequestSerializer

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

from rest_framework import generics
from rest_framework.exceptions import NotFound

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

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

class UserCollectionRequestListView(generics.ListAPIView):
    serializer_class = CollectionRequestSerializer

    def get_queryset(self):
        # Obtém o ID do usuário da URL
        user_id = self.kwargs['user_id']
        
        # Tenta buscar o usuário pelo ID
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise NotFound(detail="Usuário não encontrado.")

        # Filtra as solicitações de coleta feitas pelo usuário
        return CollectionRequest.objects.filter(requester=user)

class CollectionRequestCreateView(generics.CreateAPIView):
    queryset = CollectionRequest.objects.all()
    serializer_class = CollectionRequestSerializer

    def perform_create(self, serializer):
        # A criação será feita diretamente com o serializador
        serializer.save()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
# views.py
from rest_framework import generics
from rest_framework.response import Response
from .models import CollectionRequest
from rest_framework import status

class UnattendedCollectionRequestView(generics.GenericAPIView):
    
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')

        unattended_requests = CollectionRequest.objects.filter(
            requester_id=user_id,
            collection_time__isnull=True
        )

        if unattended_requests.exists():
            return Response(
                {"message": "Existem solicitações de coleta não atendidas."},
                status=status.HTTP_200_OK
            )
        
        return Response(
            {"message": "Não há solicitações de coleta não atendidas."},
            status=status.HTTP_200_OK
        )

class UnattendedRequestsView(APIView):
    def get(self, request, *args, **kwargs):
        # Consultar todas as solicitações de coleta que ainda não foram atendidas
        unattended_requests = CollectionRequest.objects.filter(collection_time__isnull=True)
        
        # Preparar os dados a serem retornados
        result = []
        for request in unattended_requests:
            requester = request.requester  # Acessando o usuário solicitante
            result.append({
                "id": request.id,
                "requester": requester.id,
                "solicitation_time": request.solicitation_time,
                "address": requester.address,
                "neighborhood": requester.address.split(',')[1] if ',' in requester.address else "Não disponível",  # Tentando pegar o bairro da rua, caso a rua tenha sido informada de maneira simples
            })
        
        return Response(result, status=status.HTTP_200_OK)

class MarkCollectionAsCompletedView(APIView):
    def patch(self, request, pk):
        try:
            collection_request = CollectionRequest.objects.get(pk=pk)
        except CollectionRequest.DoesNotExist:
            return Response({'detail': 'Solicitação de coleta não encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        # Se o 'driver' for passado no corpo da requisição, o incluímos
        driver = request.data.get('driver', None)

        # Atualiza o status da solicitação para "completed" e o driver se fornecido
        serializer = CollectionRequestSerializer(collection_request, data={'status': 'completed', 'driver': driver}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)