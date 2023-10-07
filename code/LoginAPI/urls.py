
from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('update/<int:id>', views.UpdateUser.as_view()),
    path('Users/', views.UsersList.as_view())
]