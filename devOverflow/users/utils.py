from django.db import transaction

from .models import Users


def register_user(req):
    new_user = Users(
        name=req.get('name'),
        email=req.get('email'),
        password=req.get('password'),
        bio='',
    )
    new_user.save()


def login_user(req):
    found_user = Users.objects.filter(
        email=req.get("email"),
        password=req.get("password"),
    ).first()

    if found_user is None:
        raise Users.DoesNotExist

    with transaction.atomic():
        Users.objects.update(is_curentUser=False)
        found_user.is_curentUser = True
        found_user.save(update_fields=["is_curentUser"])


def get_curent_user():
    return Users.objects.filter(is_curentUser=True).first()


def logout_user():
    Users.objects.update(is_curentUser=False)
