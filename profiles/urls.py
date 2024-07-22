from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='profiles/login.html',
                                     redirect_authenticated_user=True),
         name='login'),
    path('registration/', views.Registration.as_view(), name='registration'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('<slug:slug>/', views.ProfileInformation.as_view(), name='info'),

]
