from django.shortcuts import render, redirect

from .utils import register_user, login_user, get_curent_user, logout_user
from .form import registerForm, loginForm
from .models import Users


def register(req):
    if req.method == "POST":
        email = req.POST.get("email")

        used_email = Users.objects.filter(email=email).exists()

        if used_email:
            return render(req, "register_user.html", {
                "context": registerForm(req.POST),
                "error": "This email is already registered"
            })

        register_user(req.POST)
        return redirect("login_user")

    context = {
        "context": registerForm()
    }

    return render(req, "register_user.html", context)


def login(req):
    login_form = loginForm(req.POST or None)

    if req.method == "POST":
        try:
            login_user(req.POST)
            return redirect("profile")
        except Users.DoesNotExist:
            return render(req, "login_user.html", {
                "login_form": login_form,
                "error": "Invalid email or password"
            })

    return render(req, "login_user.html", {
        "login_form": login_form
    })


def profile(req):
    user = get_curent_user()

    if user is None:
        return redirect("login_user")

    context = {
        "user": user,
        "current_user": user,
    }

    return render(req, "user_profile.html", context)


def logout(req):
    logout_user(req)
    return redirect("login_user")