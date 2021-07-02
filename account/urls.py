from django.urls import path

from products.views import Favoritess
from .views import *


urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('activation/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('reset_password/', ResetPassword.as_view()),
    path('reset_password_complete/', ResetPasswordCompleteView.as_view()),
    path('change_password/', ChangePassword.as_view()),
    path('favorite/', Favoritess.as_view()),
    path('profile/', Profile.as_view())
]