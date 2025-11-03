import hashlib
import secrets
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from ..models.user import Usuario

class AuthSystem:
    @staticmethod
    def hash_password(password):
        """Cria hash seguro da senha"""
        salt = secrets.token_hex(16)
        return hashlib.sha256((password + salt).encode()).hexdigest() + ':' + salt
    
    @staticmethod
    def verify_password(password, hashed):
        """Verifica se a senha está correta"""
        try:
            hashed_pw, salt = hashed.split(':')
            return hashlib.sha256((password + salt).encode()).hexdigest() == hashed_pw
        except:
            return False
    
    @staticmethod
    def create_jwt_token(user):
        """Cria token JWT personalizado"""
        payload = {
            'user_id': user.id,
            'email': user.email,
            'user_type': user.user_type,
            'nome': user.nome,
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    
    @staticmethod
    def verify_jwt_token(token):
        """Verifica token JWT"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return payload
        except:
            return None
    
    @staticmethod
    def authenticate_user(email, password):
        """Autentica usuário por email e senha"""
        try:
            user = Usuario.objects.get(email=email, ativo=True)
            if AuthSystem.verify_password(password, user.senha):
                return user
        except Usuario.DoesNotExist:
            return None
        return None