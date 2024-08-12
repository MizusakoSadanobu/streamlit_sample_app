import streamlit as st
from db import session, init_db
from models import User, Property, Booking, Review
from utils import hash_password, check_password
from datetime import date

# DB初期化
init_db()

# ユーザー登録/ログイン
def user_auth():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        st.write(f"Welcome, {st.session_state.username}!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
    else:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = session.query(User).filter_by(username=username).first()
            if user and check_password(user.password, password):
                st.session_state.logged_in = True
                st.session_state.username = username
            else:
                st.error("Invalid credentials")

        if st.button("Register"):
            hashed_password = hash_password(password)
            new_user = User(username=username, password=hashed_password)
            session.add(new_user)
            session.commit()
            st.success("User registered successfully")

# 宿の検索
def search_properties():
    location = st.selectbox("Location", session.query(Property.location).distinct().all())
    date_input = st.date_input("Date", min_value=date.today())
    price_range = st.slider("Price Range", 0, 500, (50, 300))
    
    results = session.query(Property).filter(Property.location == location, Property.price.between(*price_range)).all()
    st.write(f"Found {len(results)} properties")
    for prop in results:
        st.write(f"Name: {prop.name}, Price: {prop.price}, Available: {prop.availability}")
        if st.button(f"Book {prop.name}"):
            if st.session_state.logged_in:
                new_booking = Booking(user_id=session_state.username, property_id=prop.id, date=date_input)
                prop.availability = False
                session.add(new_booking)
                session.commit()
                st.success("Booking confirmed")
            else:
                st.error("You need to login first")

# メインページ
def main():
    st.title("Airbnb Clone")
    menu = ["Home", "Search Properties", "Add Property", "Login/Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.write("Welcome to Airbnb Clone!")
    elif choice == "Search Properties":
        search_properties()
    elif choice == "Add Property":
        if st.session_state.logged_in:
            name = st.text_input("Property Name")
            price = st.number_input("Price")
            location = st.text_input("Location")
            if st.button("Add"):
                new_property = Property(name=name, price=price, location=location, owner_id=session_state.username)
                session.add(new_property)
                session.commit()
                st.success("Property added successfully")
        else:
            st.error("You need to login first")
    elif choice == "Login/Register":
        user_auth()

if __name__ == "__main__":
    main()
