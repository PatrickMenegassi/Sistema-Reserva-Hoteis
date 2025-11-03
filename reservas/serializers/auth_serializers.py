from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Informações extras no token
        token['user_type'] = user.user_type
        token['email'] = user.email
        token['first_name'] = user.first_name
        
        return token