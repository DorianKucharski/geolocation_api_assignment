from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from rest_framework_simplejwt.tokens import AccessToken, SlidingToken, RefreshToken, Token

def home(request):
    return render(request, "home.html", {})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            u = User.objects.get(username=username)
            token = AccessToken.for_user(u)
            refresh_token = RefreshToken.for_user(u)
            login(request, user)
            # return redirect('/')
            html = f'<html><body>API Token: {token}</br>Refresh Token: {refresh_token}</body></html>'
            return HttpResponse(html)

    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
