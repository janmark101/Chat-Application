from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import status


class UserTests(APITestCase):
    def setUp(self):
        self.client = self.client_class()

    def test_Registration(self):
        data = {"username" : "Test","password": "123","email" : 'test@op2.pl'}
        response = self.client.post('/api-login/register/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        
    def test_Login(self):
        User.objects.create_user(username='test',password='123',email='test@op.pl')
        data = {'username':'test','password':'123'}
        response = self.client.post('/api-login/login/',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_Update(self):
        user = User.objects.create_user(username='test',password='123',email='test@op.pl')
        token = Token.objects.create(user=user)
        client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}')
        data = {'username':'testv2'}
        response = client.patch(f'/api-login/update/{user.id}',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testv2')
    
    def test_logout(self):
        user = User.objects.create_user(username='test',password='123',email='test@op.pl')
        token = Token.objects.create(user=user)
        client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = client.post('/api-login/logout/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_get_users(self):
        user = User.objects.create_user(username='test',password='123',email='test@op.pl')
        token = Token.objects.create(user=user)
        client = self.client_class(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = client.get('/api-login/Users/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)