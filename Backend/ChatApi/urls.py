
from django.urls import path
from .views import ConversationView,ConversationObject,ParticipantsView,ParticipantionObjectsForUser,ParticipantsForConversation,MessagesView

urlpatterns = [
    path('conversations',ConversationView.as_view()),
    path('conversations/<int:pk>',ConversationObject.as_view()),
    path('participants',ParticipantsView.as_view()),
    path('participantionUser',ParticipantionObjectsForUser.as_view()),
    path('conversationParticipants/<int:pk>',ParticipantsForConversation.as_view()),
    path('messagesForConversation/<int:pk>',MessagesView.as_view())
]