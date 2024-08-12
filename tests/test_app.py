import pytest
from unittest.mock import MagicMock
from app import user_auth, search_properties, main
from db import session
from models import User, Property, Booking
from utils import hash_password, check_password
from datetime import date

# DBの初期化
@pytest.fixture(scope="function", autouse=True)
def setup_db():
    session.begin()
    session.query(User).delete()  # ユーザーを削除してテストの干渉を防ぐ
    session.query(Property).delete()  # プロパティを削除
    session.query(Booking).delete()  # 予約を削除
    session.commit()
    yield
    session.rollback()

# Streamlitのモック
@pytest.fixture
def st_mock(mocker):
    st = mocker.patch('app.st')
    return st

# user_authのテスト
def test_user_auth_login_success(st_mock):
    username = "testuser"
    password = "password"
    hashed_password = hash_password(password)
    user = User(username=username, password=hashed_password)
    session.add(user)
    session.commit()

    st_mock.text_input.side_effect = [username, password]
    st_mock.button.side_effect = [True, False]
    st_mock.write = MagicMock()
    st_mock.error = MagicMock()

    user_auth()

    st_mock.write.assert_called_with(f"Welcome, {username}!")
    assert st_mock.session_state.logged_in is True
    assert st_mock.session_state.username == username



def test_user_auth_login_failure(st_mock):
    st_mock.text_input.side_effect = ["wronguser", "wrongpassword"]
    st_mock.button.side_effect = [True, False]

    user_auth()

    assert st_mock.error.called

def test_user_auth_register(st_mock):
    username = "newuser"
    password = "newpassword"

    st_mock.text_input.side_effect = [username, password]
    st_mock.button.side_effect = [False, True]

    user_auth()

    assert st_mock.success.called
    user = session.query(User).filter_by(username=username).first()
    assert user is not None
    assert user.username == username

# search_propertiesのテスト
def test_search_properties_no_results(st_mock):
    st_mock.selectbox.return_value = "Tokyo"
    st_mock.date_input.return_value = date.today()
    st_mock.slider.return_value = (50, 300)
    st_mock.button.return_value = False

    search_properties()

    assert st_mock.write.called_with("Found 0 properties")

def test_search_properties_with_results(st_mock):
    username = "owner"
    password = "password"
    hashed_password = hash_password(password)
    owner = User(username=username, password=hashed_password)
    property = Property(name="Test Property", price=150.0, location="Tokyo", owner_id=owner.id, availability=True)
    session.add(owner)
    session.add(property)
    session.commit()

    st_mock.selectbox.return_value = "Tokyo"
    st_mock.date_input.return_value = date.today()
    st_mock.slider.return_value = (50, 300)
    st_mock.button.return_value = False

    search_properties()

    assert st_mock.write.called_with("Found 1 properties")
    assert st_mock.write.called_with("Name: Test Property, Price: 150.0, Available: True")

# main関数のテスト
def test_main_home(st_mock):
    st_mock.sidebar.selectbox.return_value = "Home"

    main()

    assert st_mock.title.called_with("Airbnb Clone")
    assert st_mock.write.called_with("Welcome to Airbnb Clone!")

def test_main_search_properties(st_mock):
    st_mock.sidebar.selectbox.return_value = "Search Properties"

    main()

    assert st_mock.selectbox.called

def test_main_add_property_logged_in(st_mock):
    st_mock.sidebar.selectbox.return_value = "Add Property"
    st_mock.session_state.logged_in = True
    st_mock.text_input.side_effect = ["Property Name", "Location"]
    st_mock.number_input.return_value = 100
    st_mock.button.return_value = True

    main()

    assert st_mock.success.called

def test_main_add_property_not_logged_in(st_mock):
    st_mock.sidebar.selectbox.return_value = "Add Property"
    st_mock.session_state.logged_in = False

    main()

    assert st_mock.error.called_with("You need to login first")

def test_main_login_register(st_mock):
    st_mock.sidebar.selectbox.return_value = "Login/Register"

    main()

    assert st_mock.text_input.called
