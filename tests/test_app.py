import pytest
from unittest.mock import MagicMock
from app import user_auth
from db import session
from models import User
from utils import hash_password

@pytest.fixture(scope="function", autouse=True)
def setup_db():
    session.begin()
    session.query(User).delete()
    session.commit()
    yield
    session.rollback()

@pytest.fixture
def st_mock(mocker):
    st = mocker.patch('app.st')
    # Mocking session_state as an object with dynamic attributes
    st.session_state = MagicMock()
    return st

def test_user_auth_login_success(st_mock):
    username = "testuser"
    password = "password"
    hashed_password = hash_password(password)
    user = User(username=username, password=hashed_password)
    session.add(user)
    session.commit()

    st_mock.text_input.side_effect = [username, password]
    st_mock.button.side_effect = [True, False]

    # Set up session_state mock attributes
    st_mock.session_state.logged_in = False
    st_mock.session_state.username = ""

    user_auth()

    # Check if the session state has been updated correctly
    assert st_mock.session_state.logged_in is True
    assert st_mock.session_state.username == username

def test_user_auth_login_failure(st_mock):
    st_mock.text_input.side_effect = ["wronguser", "wrongpassword"]
    st_mock.button.side_effect = [True, False]
    st_mock.error = MagicMock()

    # Set up session_state mock attributes
    st_mock.session_state.logged_in = False
    st_mock.session_state.username = ""

    user_auth()

    assert st_mock.error.called
    assert st_mock.session_state.logged_in is False

def test_user_auth_register(st_mock):
    username = "newuser"
    password = "newpassword"
    hashed_password = hash_password(password)

    st_mock.text_input.side_effect = [username, password]
    st_mock.button.side_effect = [False, True]
    st_mock.success = MagicMock()

    # Set up session_state mock attributes
    st_mock.session_state.logged_in = False
    st_mock.session_state.username = ""

    user_auth()

    assert st_mock.success.called
    user = session.query(User).filter_by(username=username).first()
    assert user is not None
    assert user.username == username
