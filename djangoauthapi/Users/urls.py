from django.urls import path
from .views import UserRegisterView,UserLoginView,UserProfileView,ChangePassView,PasswordResetEmailView,PasswordRestView
urlpatterns = [
    path('register/', UserRegisterView.as_view(),name='register' ),
    path('login/', UserLoginView.as_view(),name='login' ),
    path('profile/', UserProfileView.as_view(),name='profile' ),
    path('changepassword/', ChangePassView.as_view(),name='change-password' ),
    path('resetpasswordemail/', PasswordResetEmailView.as_view(),name='reset-password-email' ),
    path('resetpassword/<uid>/<token>/', PasswordRestView.as_view(),name='reset-password' ),
]
