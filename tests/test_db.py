import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, init_db
from models import User, Property, Booking, Review
from datetime import date  # 追加

# テスト用のSQLiteデータベースを使用
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope='function')
def session():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_user_creation(session):
    # テストユーザーを作成
    user = User(username="testuser", password="hashed_password")
    session.add(user)
    session.commit()

    # データベースからユーザーを取得
    retrieved_user = session.query(User).filter_by(username="testuser").first()
    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"

def test_property_creation(session):
    # ユーザーを作成
    user = User(username="propertyowner", password="hashed_password")
    session.add(user)
    session.commit()

    # プロパティを作成
    property = Property(name="Test Property", price=100.0, location="Tokyo", owner_id=user.id)
    session.add(property)
    session.commit()

    # データベースからプロパティを取得
    retrieved_property = session.query(Property).filter_by(name="Test Property").first()
    assert retrieved_property is not None
    assert retrieved_property.name == "Test Property"
    assert retrieved_property.owner.username == "propertyowner"

def test_booking_creation(session):
    # ユーザーとプロパティを作成
    user = User(username="testuser", password="hashed_password")
    property = Property(name="Test Property", price=100.0, location="Tokyo")
    session.add(user)
    session.add(property)
    session.commit()

    # ブッキングを作成
    booking = Booking(user_id=user.id, property_id=property.id, date=date(2024, 12, 1))  # 修正
    session.add(booking)
    session.commit()

    # データベースからブッキングを取得
    retrieved_booking = session.query(Booking).filter_by(user_id=user.id).first()
    assert retrieved_booking is not None
    assert retrieved_booking.property.name == "Test Property"
    assert retrieved_booking.user.username == "testuser"

def test_review_creation(session):
    # ユーザーとプロパティを作成
    user = User(username="testuser", password="hashed_password")
    property = Property(name="Test Property", price=100.0, location="Tokyo")
    session.add(user)
    session.add(property)
    session.commit()

    # レビューを作成
    review = Review(user_id=user.id, property_id=property.id, review_text="Great place!", date=date(2024, 12, 2))  # 修正
    session.add(review)
    session.commit()

    # データベースからレビューを取得
    retrieved_review = session.query(Review).filter_by(user_id=user.id).first()
    assert retrieved_review is not None
    assert retrieved_review.review_text == "Great place!"
    assert retrieved_review.property.name == "Test Property"
