from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from app.forms import LoginForm, RegistrationForm


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account is ready.")

            return redirect("home")

    else:
        form = RegistrationForm()

    return render(
        request,
        "authentication/register.html",
        {"form": form},
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password,
            )

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}.")

                return redirect("home")

            form.add_error(
                None,
                "Invalid username or password.",
            )

    else:
        form = LoginForm()

    return render(
        request,
        "authentication/login.html",
        {"form": form},
    )


def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "You have been logged out.")

    return redirect("home")
