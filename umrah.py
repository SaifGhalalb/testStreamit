
import streamlit as st
from auth import login_form, registration_form, logout, is_admin, get_user_info
from db_utils import *
from datetime import date
import os

# Streamlit config
st.set_page_config(page_title="Umrah Travel Agency", page_icon="🕋", layout="wide")

# Sidebar
st.sidebar.title("Umrah Portal")
if not st.session_state.get("logged_in"):
    login_form()
    st.sidebar.markdown("Don't have an account?")
    if st.sidebar.button("Register"):
        st.session_state.show_register = True
else:
    user_info = get_user_info()
    st.sidebar.write(f"Logged in as: {user_info['name']}")
    if st.sidebar.button("Logout"):
        logout()

if st.session_state.get("show_register"):
    registration_form()
    st.stop()

# Navigation
menu = st.sidebar.radio("Navigate", ["🏠 Home", "📦 Packages", "📝 Book", "📋 Dashboard", "🆘 Support"] + (["⚙️ Admin"] if is_admin() else []))

# Home
if menu == "🏠 Home":
    st.title("🕋 Welcome to the Umrah Travel Agency Portal")
    st.markdown("""
    Plan your spiritual journey with ease. Book reliable, curated Umrah packages and get live updates on your booking.
    """)
    st.image("https://images.unsplash.com/photo-1585409164169-43e1db9ed48e?auto=format&fit=crop&w=1350&q=80", use_column_width=True)

# Packages
elif menu == "📦 Packages":
    st.header("Available Umrah Packages")
    packages = get_all_packages()
    st.dataframe(packages)

# Book
elif menu == "📝 Book":
    if not st.session_state.get("logged_in"):
        st.warning("Login required to book.")
        st.stop()

    st.header("Book an Umrah Package")
    packages = get_all_packages()
    package_map = dict(zip(packages['name'], packages['id']))
    selected = st.selectbox("Choose a package", list(package_map.keys()))

    travel_date = st.date_input("Travel Date", min_value=date.today())
    payment_method = st.selectbox("Payment Method", ["Credit Card", "Bank Transfer", "Cash"])
    documents = st.file_uploader("Upload Documents (PDF/Image)", accept_multiple_files=True)

    if st.button("Confirm Booking"):
        booking_id = create_booking(st.session_state.user_id, package_map[selected], travel_date, payment_method)

        os.makedirs("upload", exist_ok=True)
        for doc in documents:
            path = f"upload/{booking_id}_{doc.name}"
            with open(path, "wb") as f:
                f.write(doc.read())
            save_booking_file(booking_id, path)

        log_activity(st.session_state.user_id, f"Created booking {booking_id}")
        st.success("Booking submitted successfully.")

# Dashboard
elif menu == "📋 Dashboard":
    if not st.session_state.get("logged_in"):
        st.warning("Login required.")
        st.stop()

    st.header("My Dashboard")
    bookings = get_user_bookings(st.session_state.user_id)
    st.subheader("My Bookings")
    st.dataframe(bookings)

    st.subheader("Support History")
    support = get_user_support(st.session_state.user_id)
    st.dataframe(support)

# Support
elif menu == "🆘 Support":
    if not st.session_state.get("logged_in"):
        st.warning("Login required.")
        st.stop()

    st.header("Submit a Support Request")
    issue = st.text_area("Describe your issue")
    if st.button("Submit Request"):
        create_support_request(st.session_state.user_id, issue)
        log_activity(st.session_state.user_id, "Submitted support request")
        st.success("Support request submitted.")

# Admin Panel
elif menu == "⚙️ Admin":
    st.title("Admin Panel")

    tab1, tab2, tab3 = st.tabs(["Manage Packages", "Bookings", "Support"])

    with tab1:
        st.subheader("All Packages")
        packages = get_all_packages()
        st.dataframe(packages)

        st.subheader("Add Package")
        with st.form("new_package"):
            name = st.text_input("Name")
            price = st.number_input("Price", min_value=100.0)
            hotel = st.text_input("Hotel")
            duration = st.number_input("Duration (days)", min_value=1)
            transport = st.text_input("Transport")
            submitted = st.form_submit_button("Add")
            if submitted:
                add_package(name, price, hotel, duration, transport)
                st.success("Package added.")

    with tab2:
        st.subheader("Manage Bookings")
        bookings = get_all_bookings()
        for _, row in bookings.iterrows():
            st.markdown(f"### Booking #{row['id']}: {row['package_name']} for {row['user_name']}")
            st.write(f"Status: {row['status']}, Travel Date: {row['travel_date']}, Payment: {row['payment_method']}")
            new_status = st.selectbox(f"Update Status for #{row['id']}", ["Pending", "Confirmed", "Cancelled"], index=["Pending", "Confirmed", "Cancelled"].index(row['status']), key=f"status_{row['id']}")
            if st.button(f"Save #{row['id']}"):
                update_booking_status(row['id'], new_status)
                log_activity(st.session_state.user_id, f"Updated booking {row['id']} to {new_status}")
                st.success(f"Booking {row['id']} updated.")

    with tab3:
        st.subheader("Support Tickets")
        tickets = get_all_support()
        for _, t in tickets.iterrows():
            st.markdown(f"#### Ticket #{t['id']} - From User {t['user_id']}")
            st.write(f"Issue: {t['issue']}")
            st.write(f"Status: {t['status']}")
            new_status = st.selectbox(f"Set Status #{t['id']}", ["Pending", "Resolved"], index=["Pending", "Resolved"].index(t['status']), key=f"support_{t['id']}")
            if st.button(f"Update Ticket #{t['id']}"):
                update_support_status(t['id'], new_status)
                st.success("Status updated.")

st.markdown("---")
st.markdown("© 2025 Umrah Travel Agency | All Rights Reserved")
