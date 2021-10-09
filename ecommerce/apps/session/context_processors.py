from .session import Session


def session(request):
    return {'session': Session(request)}
