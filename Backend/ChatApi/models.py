from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Conversation(models.Model):
    conversation_name = models.CharField(max_length=100)
    date_created = models.DateField(auto_now_add=True)
    user_id_boss =  models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.conversation_name
    
class Participant(models.Model):
    conversation_id = models.ForeignKey(Conversation,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    joined_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return str(self.conversation_id) + " participant : " + str(self.user_id)
    
    
class Message(models.Model):
    conversation_id = models.ForeignKey(Conversation,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    date_send = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return str(self.conversation_id) + " message from " + str(self.user_id)