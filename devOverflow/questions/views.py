from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Count, Q

from users.utils import get_curent_user


from .form import QuestionForm, add_comment
from .models import Questions, Comments
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
    search_query = request.GET.get("q", "").strip()
    sort_order = request.GET.get("sort", "latest")
    questions = Questions.objects.select_related("creator").annotate(
        comments_count=Count("comments")
    )
    if search_query:
        questions = questions.filter(
            Q(title__icontains=search_query) | Q(context__icontains=search_query)
        )
    if sort_order == "most_discussed":
        questions = questions.order_by("-comments_count", "-created_at")
    else:
        sort_order = "latest"
        questions = questions.order_by("-created_at")

    context = {
        "all_posts": questions,
        "active_questions": Questions.objects.annotate(
            comments_count=Count("comments")
        ).order_by("-comments_count", "-created_at")[:4],
        "question_count": Questions.objects.count(),
        "result_count": questions.count(),
        "comment_count": Comments.objects.count(),
        "search_query": search_query,
        "sort_order": sort_order,
        "current_user": get_curent_user(),
    }
    return render(request, "all_posts.html", context)

def question_detail(req, id):
    question = get_object_or_404(Questions, id=id)
    current_user = get_curent_user()
    form = add_comment()

    if req.method == "POST":
        if current_user is None:
            return redirect("login_user")

        form = add_comment(req.POST)

        if form.is_valid():
            Comments.objects.create(
                author=current_user,
                question=question,
                context=form.cleaned_data["context"]
            )
            return redirect("question_detail", id=question.id)

    comments = Comments.objects.filter(
        question=question
    ).select_related("author").order_by("-created_at")

    return render(req, "question_detail.html", {
        "question": question,
        "current_user": current_user,
        "form": form,
        "comments": comments
    })