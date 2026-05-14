from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .forms import RegisterForm


def register_user(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully registered.")
            return redirect("user-login")
        messages.error(request, "Error message.")
    return render(request, "usermodule/register.html", {"form": form})


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successfully.")
            next_url = request.GET.get("next") or request.POST.get("next")
            return redirect(next_url or "lab11-index")
        messages.error(request, "Error message.")
    return render(request, "usermodule/login.html", {"form": form})


def logout_user(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("user-login")
