from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegisterForm

# Create your views here.
def user_login(request):
    forms = UserLoginForm()
    if request.method == "POST":
        forms = UserLoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data["username"]
            password = forms.cleaned_data["password"]

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Invalid User or Password")
                return redirect("login")

    context = {
        "forms": forms
    }
    return render(request, "accounts/login.html", context)

def user_logout(request):
    logout(request)
    return redirect("login")


def user_register(request):
    forms = UserRegisterForm()
    if request.method == "POST":
        forms = UserRegisterForm(request.POST)
        if forms.is_valid():
            forms.save()
            messages.success(request, "Registration completed successfully. Please login.")
            return redirect("login")

    context = {
        "forms": forms
    }
    return render(request, "accounts/register.html", context)


@login_required
def user_profile(request):
    return render(request, "accounts/profile.html")


@login_required
def user_updates(request):
    return render(request, "accounts/updates.html")


@login_required
def user_payments(request):
    return render(request, "accounts/payments.html")

