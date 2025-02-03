from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

class CustomUser(AbstractUser):
    class Meta:
        db_table = 'users'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    driver = models.BooleanField(verbose_name="Motorista?", default=False)
    want_collect = models.BooleanField(verbose_name="Quer coleta?", default=False)

    address = models.CharField(max_length=255, verbose_name="Endereço", null=True)
    
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