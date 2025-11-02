from impl import AUTH_TRY_LIMIT


class TooManyAuthTriesException(Exception):
    pass


class Authentificator:
    def __init__(self):
        self._users: dict[str, str] = {}
        self._auth_tries: dict[str, int] = {}

    def register(self, username, password):
        if username not in self._users:
            self._users[username] = password
            self._auth_tries[username] = 1

    def authenticate(self, username, password) -> bool:
        if not (username in self._users and self._users[username] == password):
            if self._auth_tries[username] >= AUTH_TRY_LIMIT:
                raise TooManyAuthTriesException("Too many auth tries")

            self._auth_tries[username] += 1
            return False

        self._auth_tries[username] = 1
        return True
