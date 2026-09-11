from synapsecord_bot.services import ApplicationScope


class FakeSession:
    def __init__(self):
        self.closed = False

    def close(self) -> None:
        self.closed = True


class FakeSessionFactory:
    def __init__(self):
        self.sessions: list[FakeSession] = []

    def __call__(self, *args, **kwargs):
        session = FakeSession()
        self.sessions.append(session)
        return session


def test_session_created_lazily() -> None:
    factory = FakeSessionFactory()

    ApplicationScope(session_factory=factory)

    assert factory.sessions == []

def test_session_reused_within_scope() -> None:
    factory = FakeSessionFactory()
    scope = ApplicationScope(session_factory=factory)

    first = scope.session
    second = scope.session

    assert first is second
    assert len(factory.sessions) == 1

def test_sessions_are_not_shared_between_scopes() -> None:
    factory = FakeSessionFactory()

    first_scope = ApplicationScope(session_factory=factory)
    second_scope = ApplicationScope(session_factory=factory)

    first_session = first_scope.session
    second_session = second_scope.session

    assert first_session is not second_session
    assert len(factory.sessions) == 2

def test_scope_closes_session() -> None:
    factory = FakeSessionFactory()
    scope = ApplicationScope(session_factory=factory)

    session = scope.session
    scope.close()

    assert session.closed

def test_context_manager_closes_session() -> None:
    factory = FakeSessionFactory()

    with ApplicationScope(factory) as scope:  # type: ignore[arg-type]
        session = scope.session

    assert session.closed