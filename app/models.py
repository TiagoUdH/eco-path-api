from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

class CustomUser(AbstractUser):
    class Meta:
        db_table = 'users'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    driver = models.BooleanField(verbose_name="Motorista?", default=False)

    address = models.CharField(max_length=255, verbose_name="Endereço", null=True)
    neighborhood = models.CharField(max_length=255, verbose_name="Bairro", null=True)
    
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(120)],
        verbose_name="Idade",
        null=True
    )
    
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Número inválido.")],
        verbose_name="Telefone",
        null=True
    )

    def __str__(self):
        return self.username

class CollectionRequest(models.Model):
    requester = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        limit_choices_to={'driver': False}, 
        verbose_name="Solicitante",
        related_name='collection_requests_made'
    )
    driver = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        limit_choices_to={'driver': True}, 
        verbose_name="Motorista",
        related_name='collection_requests_assigned'
    )

    solicitation_time = models.DateTimeField(auto_now_add=timezone.now, verbose_name="Hora da Solicitação")
    collection_time = models.DateTimeField(null=True, verbose_name="Hora da Coleta", blank=True)
    status = models.CharField(
        max_length=50, 
        choices=[('in_progress', 'Em Andamento'), ('completed', 'Concluída')],
        default='in_progress',
        verbose_name="Status da Solicitação"
    )

    def __str__(self):
        return f"Solicitação de Coleta - {self.get_status_display()}"

    class Meta:
        db_table = 'collection_requests'
        verbose_name = 'Solicitação de Coleta'
        verbose_name_plural = 'Solicitações de Coleta'
