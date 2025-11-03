import jwt
from django.conf import settings
from .models.user import Usuario

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            # Não faz nada para o Admin - usa autenticação padrão do Django
            response = self.get_response(request)
            return response
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        print(f"Header: {auth_header}")
        
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            
            try:
                #  Lógica DIRETA sem método separado
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user = Usuario.objects.get(id=payload['user_id'])
                request.user = user
                print(f" Usuário autenticado: {user.email}")
            except jwt.ExpiredSignatureError:
                request.user = None
                print(" Token expirado")
            except jwt.InvalidTokenError:
                request.user = None
                print(" Token inválido")
            except Usuario.DoesNotExist:
                request.user = None
                print(" Usuário não existe")
            except Exception as e:
                request.user = None
                print(f" Erro: {e}")
        else:
            request.user = None
            print(" Nenhum token Bearer")

        response = self.get_response(request)
        return response
    
class DisableCSRFMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #  Desabilita CSRF para todas as rotas /api/
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        
        response = self.get_response(request)
        return response
