from django.shortcuts import redirect, render

from users.utils import get_curent_user

from .form import QuestionForm, add_comment
from .models import Questions
from .utils import save_question


def create_question(request):
    current_user = get_curent_user()
    if current_user is None:
        return redirect("login_user")

    form = QuestionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        save_question(form.cleaned_data, current_user)
        return redirect("main_page")

    return render(request, "create_question.html", {"form": form})


def all_posts(request):
    context = {
        "all_posts": Questions.objects.select_related("creator").order_by("-created_at"),
        "current_user": get_curent_user(),
    }
    return render(request, "all_posts.html", context)
