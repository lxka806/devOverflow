from .models import Questions


def save_question(data, creator):
    return Questions.objects.create(
        title=data["title"],
        context=data["context"],
        creator=creator,
    )