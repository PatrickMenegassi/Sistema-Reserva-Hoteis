from rest_framework import serializers
from ..models.user import Usuario

class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    senha = serializers.CharField(min_length=6, write_only=True)
    confirmar_senha = serializers.CharField(write_only=True)
    nome = serializers.CharField(max_length=100)
    telefone = serializers.CharField(max_length=11, required=False)
    cpf = serializers.CharField(max_length=11, required=False)
    data_nascimento = serializers.DateField(required=False)
    endereco = serializers.CharField(required=False)
    
    def validate(self, data):
        if data['senha'] != data['confirmar_senha']:
            raise serializers.ValidationError("Senhas não coincidem")
        return data

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    senha = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'email', 'nome', 'telefone', 'user_type', 'data_criacao']
        read_only_fields = ['id', 'user_type', 'data_criacao']