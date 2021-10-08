

class Session:
    """
    Class allow us communicate using django session framework (cookies)
    """

    def __init__(self, request):
        self.session = request.session
        current_session = self.session.get("session")
        if "session" not in self.session:
            current_session = self.session["session"] = {}
        self.current_session = current_session
