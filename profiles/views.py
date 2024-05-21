from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DetailView

from .forms import ProfileRegister
from .models import Profile


class Registration(CreateView):
    model = Profile
    form_class = ProfileRegister
    success_url = reverse_lazy('products')
    template_name = 'profiles/registration.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('products')
        return super().get(request, *args, **kwargs)


class CustomLogoutView(View):

    def get(self, request):
        if self.request.user.is_authenticated:
            logout(request)
            return redirect('products')


class ProfileInformation(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/profile_information.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Profile, slug=self.kwargs['slug'])
        return obj
