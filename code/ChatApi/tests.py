from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import status
from .models import Conversation,Participant

class ConversationViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',password='123',email='test@op.pl')
        self.token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    
    def test_get_conversation(self):
        response = self.client.get('/api-chat/conversations')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_conversation(self):
        data = {"conversation_name":"Test Conversation","user_id_boss" : self.user.id}
        response = self.client.post('/api-chat/conversations',data,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
class ConversationObjectTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',password='123',email='test@op.pl')
        self.token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.conv = Conversation.objects.create(conversation_name="Test Conversation",user_id_boss=self.user)
        
    def test_get_conversation_pk(self):
        response = self.client.get(f'/api-chat/conversations/{self.conv.pk}')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['conversation_name'], 'Test Conversation')
        
    def test_get_noexist_object(self):
        response = self.client.get(f'/api-chat/conversations/404')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_delete_objects(self):
        response = self.client.delete(f'/api-chat/conversations/{self.conv.pk}')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertFalse(Conversation.objects.filter(pk=self.conv.pk).exists())

    def test_delete_noexist_object(self):
        response = self.client.delete(f'/api-chat/conversations/404')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_patch_object(self):
        edited_conv = {"conversation_name" : "Test Conversation (patch)"}
        response = self.client.patch(f'/api-chat/conversations/{self.conv.pk}',edited_conv,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.conv.refresh_from_db()
        self.assertEqual(self.conv.conversation_name,'Test Conversation (patch)')
        
class ParticipantTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',password='123',email='test@op.pl')
        self.token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    
    def test_get_participants(self):
        response = self.client.get('/api-chat/participants')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_participant(self):
        conv = Conversation.objects.create(conversation_name="Test Conversation",user_id_boss=self.user)
        data = {"conversation_id": conv.id,"user_id":self.user.id}
        response = self.client.post('/api-chat/participants',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        
class ParticipantForUserTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',password='123',email='test@op.pl')
        self.token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    
    def test_get_participants(self):
        response = self.client.get('/api-chat/participantionUser')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

class ParticipantForConversationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',password='123',email='test@op.pl')
        self.token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.conv = Conversation.objects.create(conversation_name="Test Conversation",user_id_boss=self.user)
        self.participation = Participant.objects.create(conversation_id=self.conv,user_id=self.user)
    
    def test_get_participants(self):
        response = self.client.get(f'/api-chat/conversationParticipants/{self.conv.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete_participant(self):
        data = {"user_id" : self.user.id}
        response = self.client.delete(f'/api-chat/conversationParticipants/{self.conv.id}',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
    

class MessageTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',password='123',email='test@op.pl')
        self.token = Token.objects.create(user=self.user)
        self.client = self.client_class(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.conv = Conversation.objects.create(conversation_name="Test Conversation",user_id_boss=self.user)
        self.participation = Participant.objects.create(conversation_id=self.conv,user_id=self.user)
        
    def test_get_message(self):
        response = self.client.get(f'/api-chat/messagesForConversation/{self.conv.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_message(self):
        data = {"conversation_id": self.conv.id,"user_id":self.user.id,"text":"test message"}
        response = self.client.post(f'/api-chat/messagesForConversation/{self.conv.id}',data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)