from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        db_table = 'reservas_user'  # Nome personalizado para a tabela
    
    USER_TYPES = (
        ('customer', 'Cliente'),
        ('staff', 'Funcionário'),
        ('admin', 'Administrador'),
    )
    
    # Campos de identificação
    email = models.EmailField(
        unique=True,
        verbose_name='E-mail'
    )
    
    # Campos pessoais
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome completo'
    )
    
    telefone = models.CharField(
        max_length=11,
        verbose_name='Telefone'
    )

    senha = models.CharField(max_length=255, verbose_name='Senha')

    cpf = models.CharField(
        max_length=11,
        unique=True,
        null=True,
        blank=True,
        verbose_name='CPF'
    )

    data_nascimento = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data de nascimento'
    )

    endereco = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        verbose_name='Endereço'
    )

    # Campos do sistema
    user_type = models.CharField(
        max_length=20, 
        choices=USER_TYPES, 
        default='customer',
        verbose_name='Tipo de usuário'
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name='Ativo'
    )
    
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de criação'
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name='Data de atualização'
    )

    def __str__(self):
        return f"{self.nome} ({self.email})"
    
    def get_full_name(self):
        return self.nome
    
    @property
    def is_active(self):
        """Compatibilidade com Django auth"""
        return self.ativo  # Use seu campo 'ativo' ou sempre True