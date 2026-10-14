from .utils import get_curent_user


def current_user(request):
    return {"current_user": get_curent_user()}
