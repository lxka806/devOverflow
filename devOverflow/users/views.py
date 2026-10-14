from django.shortcuts import render, redirect, get_object_or_404

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

    if req.method == "POST":
        avatar = req.FILES.get("avatar")

        if avatar:
            user.avatar = avatar
            user.save()

    context = {
        "user": user,
        "current_user": user,
        "posts": user.posts.all(),
    }

    return render(req, "user_profile.html", context)


def logout(req):
    logout_user(req)
    return redirect("login_user")



def edit_profile(req):
    user = get_curent_user()

    if user is None:
        return redirect("login_user")

    if req.method == "POST":
        name = req.POST.get("name", "").strip()
        avatar = req.FILES.get("avatar")
        bio = req.POST.get("bio", "").strip()

        if not name:
            return render(req, "edit_profile.html", {
                "user": user,
                "error": "Name is required."
            })

        user.name = name
        user.bio = bio

        if avatar:
            user.avatar = avatar

        user.save()

        return redirect("profile")

    return render(req, "edit_profile.html", {
        "user": user
    })



def user_info(req, id):
    user = get_object_or_404(Users, id=id)
    current_user = get_curent_user()

    return render(
        req,
        "users_details.html",
        {
            "user": user,
            "current_user": current_user,
            "posts": user.posts.all(),
        },
    )
