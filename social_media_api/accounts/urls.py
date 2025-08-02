from django.urls import path
from .views import register, user_login, CustomAuthToken, follow_user, unfollow_user

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('profile/', user_login, name='profile'),
    path('token/', CustomAuthToken.as_view(), name='token'),
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow_user'),
    
]