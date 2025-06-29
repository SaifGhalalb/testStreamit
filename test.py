import streamlit as st
import pandas as pd
from datetime import date

# Streamlit App configuration
st.set_page_config(
    page_title="Umrah Travel Agency",
    page_icon="🕋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS Styling for modern UI
st.markdown("""
<style>
    .main {
        background-color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #f5f5f5;
    }
    h1, h2, h3 {
        color: #333;
    }
    button {
        background-color: #007BFF !important;
        color: white !important;
        border-radius: 8px !important;
    }
    button:hover {
        background-color: #0056b3 !important;
    }
</style>
""", unsafe_allow_html=True)

# Dummy data for packages
packages = pd.DataFrame({
    'Package Name': ['Economy', 'Deluxe', 'Premium'],
    'Price (USD)': [1200, 2000, 3500],
    'Hotel': ['3-Star', '4-Star', '5-Star'],
    'Duration (days)': [7, 10, 14],
    'Transport': ['Bus', 'Private Car', 'Luxury Car'],
})

# Sidebar navigation
menu = st.sidebar.radio('Menu', [
    '🏠 Home',
    '📦 Packages',
    '📝 Book Package',
    '📖 My Bookings',
    '👤 User Profile',
    '⚙️ Admin Panel',
    '📞 Support'
])

# Home Page
if menu == '🏠 Home':
    st.title('🕋 Umrah Travel Agency')
    st.write("Welcome to your trusted partner for your spiritual journey.")
    st.image("https://images.unsplash.com/photo-1585409164169-43e1db9ed48e?auto=format&fit=crop&w=1350&q=80",
             caption="Experience tranquility and spirituality with us.", use_container_width=True)

# Packages Page
elif menu == '📦 Packages':
    st.title('📦 Available Umrah Packages')
    st.dataframe(packages, use_container_width=True)

# Book Package Page
elif menu == '📝 Book Package':
    st.title('📝 Book Your Umrah Package')
    package_selected = st.selectbox('Select Package', packages['Package Name'])
    traveler_name = st.text_input('Full Name')
    passport_number = st.text_input('Passport Number')
    nationality = st.text_input('Nationality')
    email = st.text_input('Email')
    phone = st.text_input('Phone Number')
    travel_date = st.date_input('Travel Date', min_value=date.today())

    docs_uploaded = st.file_uploader('Upload Required Documents', accept_multiple_files=True)

    payment_method = st.selectbox('Payment Method', ['Credit Card', 'Debit Card', 'Bank Transfer'])

    if st.button('Confirm Booking'):
        if traveler_name and passport_number and email:
            st.success(f'Booking confirmed for {traveler_name}! You chose the {package_selected} package on {travel_date}.')
        else:
            st.error('Please fill in all required fields.')

# My Bookings Page
elif menu == '📖 My Bookings':
    st.title('📖 My Bookings')
    st.info('Bookings will be displayed here after database integration.')

# User Profile Page
elif menu == '👤 User Profile':
    st.title('👤 User Profile')
    with st.form('update_profile'):
        name = st.text_input('Name')
        passport = st.text_input('Passport Number')
        nationality = st.text_input('Nationality')
        phone = st.text_input('Phone Number')
        email = st.text_input('Email')
        submitted = st.form_submit_button('Update Profile')
        if submitted:
            st.success('Profile updated successfully!')

# Admin Panel Page
elif menu == '⚙️ Admin Panel':
    st.title('⚙️ Admin Panel')
    admin_menu = st.selectbox('Admin Options', ['Manage Packages', 'View Reports', 'User Management'])

    if admin_menu == 'Manage Packages':
        st.subheader('Manage Packages')
        st.info('Package management functionalities go here.')

    elif admin_menu == 'View Reports':
        st.subheader('Reports & Analytics')
        st.info('Booking analytics and reports will be displayed here.')

    elif admin_menu == 'User Management':
        st.subheader('User Management')
        st.info('User account management functionalities go here.')

# Support Page
elif menu == '📞 Support':
    st.title('📞 Customer Support')
    with st.form('support_form'):
        issue = st.text_area('Describe your issue', height=150)
        submitted = st.form_submit_button('Submit Issue')
        if submitted:
            st.success('Your issue has been submitted. Our support team will contact you shortly.')

# Footer
st.markdown('---')
st.markdown('© 2025 Umrah Travel Agency | All Rights Reserved', unsafe_allow_html=True)
