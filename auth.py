import streamlit as st
import sqlite3
from hashlib import sha256

def get_connection():
    return sqlite3.connect("umrah.db")

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def login_form():
    #st.session_state.show_register = False
    st.subheader("Login")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT id, password_hash, role_id, name FROM users WHERE email=?", (email,))
        user = c.fetchone()
        conn.close()
        if user and user[1] == hash_password(password):
            st.session_state.logged_in = True
            st.session_state.user_id = user[0]
            st.session_state.role_id = user[2]
            st.session_state.user_name = user[3]
        else:
            st.error("Invalid login credentials.")

def registration_form():
    st.subheader("Register New Account")

    name = st.text_input("Full Name", key="reg_name")
    passport = st.text_input("Passport Number", key="reg_passport")
    nationality = st.text_input("Nationality", key="reg_nat")
    email = st.text_input("Email", key="reg_email")
    phone = st.text_input("Phone", key="reg_phone")
    password = st.text_input("Password", type="password", key="reg_password")
    if st.button("Register"):
        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO users 
                         (name, passport_number, nationality, email, phone, password_hash, role_id) 
                         VALUES (?, ?, ?, ?, ?, ?, ?)''',
                      (name, passport, nationality, email, phone, hash_password(password), 2))
            conn.commit()
            st.success("Registration successful. You can now log in.")
            st.session_state.show_register = False
        except sqlite3.IntegrityError:
            st.error("Email or passport number already exists.")
        finally:
            conn.close()

def logout():
    st.session_state.clear()

def is_admin():
    return st.session_state.get("role_id") == 1

def get_user_info():
    return {
        "user_id": st.session_state.get("user_id"),
        "role_id": st.session_state.get("role_id"),
        "name": st.session_state.get("user_name")
    }
