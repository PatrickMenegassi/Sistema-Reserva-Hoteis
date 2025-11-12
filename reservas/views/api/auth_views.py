from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from ...models.user import Usuario
from ...utils.auth_utils import AuthSystem
from ...serializers.user_serializers import UserRegistrationSerializer, UserLoginSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Registra novo usuário"""
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user_data = serializer.validated_data
        
        # Verifica se email já existe
        if Usuario.objects.filter(email=user_data['email']).exists():
            return Response(
                {'error': 'Email já cadastrado'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cria usuário
        user = Usuario.objects.create(
            email=user_data['email'],
            senha=AuthSystem.hash_password(user_data['senha']),
            nome=user_data['nome'],
            telefone=user_data.get('telefone', ''),
            cpf=user_data.get('cpf', ''),
            data_nascimento=user_data.get('data_nascimento'),
            endereco=user_data.get('endereco', ''),
            username=user_data['nome'],
            user_type='customer'  # Sempre cria como cliente
        )
        
        # Gera token
        token = AuthSystem.create_jwt_token(user)
        
        return Response({
            'message': 'Usuário criado com sucesso',
            'token': token,
            'user': {
                'id': user.id,
                'email': user.email,
                'nome': user.nome,
                'user_type': user.user_type
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login de usuário"""
    serializer = UserLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['senha']
        
        user = AuthSystem.authenticate_user(email, password)
        
        if user:
            token = AuthSystem.create_jwt_token(user)
            
            return Response({
                'message': 'Login realizado com sucesso',
                'token': token,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'nome': user.nome,
                    'user_type': user.user_type
                }
            })
        
        return Response(
            {'error': 'Email ou senha incorretos'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout(request):
    """Logout (apenas invalida token no frontend)"""
    return Response({'message': 'Logout realizado com sucesso'})