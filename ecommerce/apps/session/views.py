from django.shortcuts import render
from .session import Session


def basket_home(request):
    session = Session(request)

    context = {
        'session': session
    }
    return render(request, "session/basket_home.html", context)
