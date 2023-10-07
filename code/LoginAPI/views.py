from django.shortcuts import render
from rest_framework.authtoken.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate, logout
from rest_framework import status, generics
from . serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class LoginView(APIView):
    permission_classes = ()
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({'error': 'Please provide both username and password.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if not user:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,'id':user.id})


class RegisterView(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer
    
    
class UpdateUser(generics.UpdateAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_user(self):
        user_pk = self.kwarg.get('id')
        user = User.objects.get(pk=user_pk)
        return user
    
    
class LogoutView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self, request):
        auth_token = request.META.get('HTTP_AUTHORIZATION')
        if auth_token : 
            token_key = auth_token.split(' ')[1]
            try :
                token = Token.objects.get(key=token_key)
                token.delete()
                logout(request)
                return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)
            except Token.DoesNotExists:
                pass
        return Response({'error' : 'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
    
    
class UsersList(generics.ListAPIView): # musze przeslac token w nagłowku zeby miec dostep do tej funkcji ('Authorization:Token d96d3fbd5e0b0dd4cdf681aee8c133f0d6b61e24')
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()