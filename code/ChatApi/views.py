from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from . models import Conversation,Message,Participant
from .serializers import ConversationSerializer, ParticipantsSerializer, MessagesSerializer
from django.http import Http404
from ChatApi.permissions import ConversationPermissions
from rest_framework.authtoken.models import Token



class ConversationView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request):
        objects = Conversation.objects.all()
        serializer = ConversationSerializer(objects,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ConversationSerializer(data=request.data)
        if serializer.is_valid():
            conv = serializer.save()
            Participant.objects.create(conversation_id=conv,user_id=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ConversationObject(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[ConversationPermissions,permissions.IsAuthenticated]
    
    def get_obj(self,pk):
        try : 
            return Conversation.objects.get(pk=pk)
        except Conversation.DoesNotExist:
            raise Http404
        
    def get(self,request,pk):
        obj = self.get_obj(pk)
        serializer = ConversationSerializer(obj,many=False)
        conversation_participants = Participant.objects.filter(conversation_id=pk).count()
        data = serializer.data
        data['participants'] = conversation_participants
        return Response(data)
    
    def delete(self,request,pk):
        object = self.get_obj(pk)
        self.check_object_permissions(self.request,pk)
        object.delete()
        return Response({"Message" : "Conversation succesfully deleted!"}, status=status.HTTP_204_NO_CONTENT)
    
    def patch(self,request,pk):
        obj = self.get_obj(pk)
        serializer = ConversationSerializer(obj,data=request.data,partial=True)
        self.check_object_permissions(self.request,pk)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ParticipantsView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self,request):
        obj = Participant.objects.all()
        serializer = ParticipantsSerializer(obj,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ParticipantsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ParticipantionObjectsForUser(APIView):   # api zwracajace konwersacje, w ktorych zalogowany uzytkownik bierze udzial 
    authentication_classes=[TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self,request):
        auth_token = request.META.get('HTTP_AUTHORIZATION')
        token_key = auth_token.split(' ')[1]
        token = Token.objects.get(key=token_key)
        
        obj = Participant.objects.filter(user_id=token.user)
        serializer = ParticipantsSerializer(obj,many=True)
        return Response(serializer.data)
    
    
class ParticipantsForConversation(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[ConversationPermissions,permissions.IsAuthenticated]
    
    def get(self,request,pk):
        participants = Participant.objects.filter(conversation_id=pk)
        self.check_object_permissions(self.request,pk)
        serializer = ParticipantsSerializer(participants,many=True)       
        return Response(serializer.data)
    
    def delete(self,request,pk):
        user_id = request.data.get('user_id')
        obj = Participant.objects.get(conversation_id=pk,user_id=user_id)
        self.check_object_permissions(self.request,pk)  
        obj.delete()
        return Response({"Message" : "Participant succesfully deleted!"}, status=status.HTTP_204_NO_CONTENT)

    
    
class MessagesView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[ConversationPermissions,permissions.IsAuthenticated]
    
    def get(self,request,pk):
        messages = Message.objects.filter(conversation_id=pk)
        self.check_object_permissions(self.request,pk)
        serializer = MessagesSerializer(messages,many=True)
        return Response(serializer.data)
    
    def post(self,request,pk):
        serializer = MessagesSerializer(data=request.data)
        self.check_object_permissions(self.request,pk)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)
   
    