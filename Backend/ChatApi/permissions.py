from . models import Conversation, Participant
from rest_framework import permissions
from rest_framework.authtoken.models import Token



#permisje dla admina konwersacji do usuwania jej i zmieniania nazwy
class ConversationPermissions(permissions.BasePermission):
    def user(self,request):
        auth_token = request.META.get('HTTP_AUTHORIZATION')
        token_key = auth_token.split(' ')[1]
        token = Token.objects.get(key=token_key)
        return token.user
    
    def has_object_permission(self,request,view,pk_conversation):
        if request.method in ['DELETE','PATCH']:  # sprawdzenie czy dany uzytkownik jest adminem konwersacji, jesli tak to moze edytowac ja usunac i usuwac z niej uzytkownikow
            user_id = self.user(request)
            
            conversation_object = Conversation.objects.get(pk=pk_conversation)

            return user_id == conversation_object.user_id_boss

        elif request.method in ['GET','POST']: # sprawdzenie czy uzytkownik jest w danej konwersacji zeby mogl zobaczyc innych uczestnikow (zeby nie bylo ze osoba nie bedaca w konwersacji moze przegladc jej uzytkownikow)
            user_id = self.user(request)
            try:
                participationobject = Participant.objects.get(conversation_id=pk_conversation,user_id=user_id)
                return True
            except Participant.DoesNotExist:
                return False    
        


            
        