from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(template_name='profiles/login.html',
                                     redirect_authenticated_user=True,),
         name='login'),
    path('registration/', Registration.as_view(), name='registration'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('<slug:slug>/', ProfileInformation.as_view(), name='info'),

]
